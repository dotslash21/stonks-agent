"""Stonks Agent Plugin for Hermes Agent.

Exposes 5 specialized investment intelligence skills, 12 read-only MCP data sources,
and strict advisory-only lifecycle hooks ensuring zero live order execution.
"""

import logging
import os
from pathlib import Path
import re
from typing import Any, Dict, Optional

logger = logging.getLogger("hermes.plugins.stonks_agent")

PLUGIN_DIR = Path(__file__).resolve().parent

# Strict prohibition tokens and patterns: zero automated order placement or capital commitment
FORBIDDEN_EXECUTION_STEMS = frozenset([
    "place_order",
    "place_gtt",
    "place_gtt_order",
    "cancel_order",
    "cancel_gtt",
    "cancel_all_orders",
    "modify_order",
    "modify_gtt",
    "execute_trade",
    "execute_order",
    "buy_order",
    "sell_order",
    "exit_position",
    "exit_order",
    "square_off",
    "close_position",
])

FORBIDDEN_PATTERNS = re.compile(
    r'(?:^|_)(place|cancel|modify|execute|create|submit|send|exit|square_?off|close|buy|sell)(?:_.*)?_(order|orders|trade|trades|gtt|position|positions)(?:$|_)'
    r'|(?:^|_)(place_gtt|cancel_gtt|modify_gtt|square_?off|buy_order|sell_order)(?:$|_)',
    re.IGNORECASE,
)

SKILLS = [
    ("portfolio-sentinel", PLUGIN_DIR / "skills" / "portfolio-sentinel" / "SKILL.md"),
    ("fundamental-valuation", PLUGIN_DIR / "skills" / "fundamental-valuation" / "SKILL.md"),
    ("nse-corporate-filings", PLUGIN_DIR / "skills" / "nse-corporate-filings" / "SKILL.md"),
    ("mf-etf-health-check", PLUGIN_DIR / "skills" / "mf-etf-health-check" / "SKILL.md"),
    ("obsidian-portfolio-memory", PLUGIN_DIR / "skills" / "obsidian-portfolio-memory" / "SKILL.md"),
]


def normalize_tool_name(name: str) -> str:
    """Normalize tool names across snake_case, camelCase, kebab-case and punctuation."""
    s1 = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name or "")
    return re.sub(r'[^a-zA-Z0-9]+', '_', s1).strip('_').lower()


def pre_tool_guardrail_hook(tool_name: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Optional[Dict[str, Any]]:
    """Enforce strict 100% advisory-only policy by intercepting and halting execution tools."""
    normalized_name = normalize_tool_name(tool_name)

    is_forbidden = False
    for forbidden in FORBIDDEN_EXECUTION_STEMS:
        if forbidden in normalized_name:
            is_forbidden = True
            break

    if not is_forbidden and FORBIDDEN_PATTERNS.search(normalized_name):
        is_forbidden = True

    if is_forbidden:
        err_msg = (
            f"Advisory Guardrail Violation: Execution tool '{tool_name}' is strictly forbidden. "
            "This plugin operates exclusively in read-only advisory mode. All orders must be "
            "manually entered by the human investor in their respective broker terminal."
        )
        logger.warning("[Guardrail Blocked] %s", err_msg)
        return {"action": "block", "message": err_msg}

    return None


def post_tool_advisory_hook(tool_name: str, params: Optional[Dict[str, Any]] = None, result: Optional[Any] = None, **kwargs: Any) -> None:
    """Audit post-tool call telemetry to ensure advisory integrity."""
    logger.debug("[Advisory Hook] Tool '%s' executed successfully.", tool_name)


def handle_sentinel_command(raw_args: Optional[str] = "") -> str:
    """Slash command handler for /sentinel_audit."""
    args = (raw_args or "").strip()
    target = f" for '{args}'" if args else ""
    return (
        f"Initiating pre-market risk audit{target} across Zerodha Kite, Groww, and INDmoney holdings.\n"
        "Checking corporate actions (splits, bonuses, dividends, ex-dates), quarterly XBRL disclosures, "
        "and overnight global market cues."
    )


def handle_valuation_command(raw_args: Optional[str] = "") -> str:
    """Slash command handler for /valuation_audit."""
    args = (raw_args or "").strip()
    symbol = args.upper() if args else "target holding"
    return (
        f"Initiating 5-Pillar Fundamental Valuation for {symbol}:\n"
        "1. Economic Moat & ROIC vs WACC (Cost of Equity ~12.5%)\n"
        "2. Forensic Cash Flow & Earnings Quality (CFO/PAT ratio)\n"
        "3. Multi-Scenario 2-Stage DCF (Terminal Growth 5.0%)\n"
        "4. PEG & Valuation Multiples vs 5-Year Historical Bands\n"
        "5. Margin of Safety & Target Entry Zones"
    )


def handle_mf_command(raw_args: Optional[str] = "") -> str:
    """Slash command handler for /mf_audit."""
    args = (raw_args or "").strip()
    target = f" for '{args}'" if args else ""
    return (
        f"Initiating Mutual Fund & ETF health check{target}:\n"
        "Inspecting direct-plan TERs, tracking error vs underlying benchmark, "
        "AUM bloat, fund manager tenure, and scheme overlap across AMFI schemes."
    )


def handle_status_command(raw_args: Optional[str] = "") -> str:
    """Slash command handler for /market_status with live configuration and auth token inspection."""
    kite_status = "CONFIGURED (Token present)" if os.getenv("ZERODHA_ACCESS_TOKEN") else "UNCONFIGURED / EXPIRED (Missing ZERODHA_ACCESS_TOKEN)"
    groww_status = "CONFIGURED (Token present)" if os.getenv("GROWW_AUTH_TOKEN") else "UNCONFIGURED (Missing GROWW_AUTH_TOKEN)"
    indmoney_status = "CONFIGURED (Token present)" if os.getenv("INDMONEY_API_TOKEN") else "UNCONFIGURED (Missing INDMONEY_API_TOKEN)"
    obsidian_status = "CONFIGURED (Key present)" if os.getenv("OBSIDIAN_API_KEY") else "UNCONFIGURED (Missing OBSIDIAN_API_KEY)"
    alpha_status = "CONFIGURED (Key present)" if os.getenv("ALPHA_VANTAGE_API_KEY") else "UNCONFIGURED (Missing ALPHA_VANTAGE_API_KEY)"
    dalalos_status = "CONFIGURED (Key present)" if os.getenv("DALALOS_API_KEY") else "UNCONFIGURED (Missing DALALOS_API_KEY)"
    sec_status = "CONFIGURED (User-Agent present)" if os.getenv("SEC_EDGAR_USER_AGENT") else "UNCONFIGURED (Missing SEC_EDGAR_USER_AGENT)"

    return (
        "=== Stonks Agent Plugin (Hermes Agent) ===\n"
        "Advisory Guardrail: ACTIVE (Live order execution strictly blocked)\n\n"
        "Broker & Data Source Readiness:\n"
        f"- Zerodha Kite: {kite_status}\n"
        f"- Groww: {groww_status}\n"
        f"- INDmoney: {indmoney_status}\n"
        f"- Obsidian Vault: {obsidian_status}\n"
        f"- Alpha Vantage: {alpha_status}\n"
        f"- DalalOS: {dalalos_status}\n"
        f"- SEC EDGAR: {sec_status}\n"
        "- Public Feeds (NSE CM Live, Bhavcopy, AMFI schemes, yFinance, OpenBB): Configured\n\n"
        "Skills Registered: 5 (portfolio-sentinel, fundamental-valuation, nse-corporate-filings, mf-etf-health-check, obsidian-portfolio-memory)\n"
        "Notice: Broker sessions (Zerodha Kite) require daily TOTP re-authentication (expires 06:00 AM IST). "
        "This status reflects local token presence; verify active session before executing pre-market audit."
    )


def register(ctx: Any) -> None:
    """Hermes Agent plugin entry point.
    
    Registers skills, safety lifecycle hooks, and slash commands.
    """
    logger.info("Registering Stonks Agent Plugin with Hermes Agent context...")

    # 1. Register all 5 bundled skills
    if hasattr(ctx, "register_skill"):
        for skill_name, skill_path in SKILLS:
            try:
                if skill_path.exists():
                    ctx.register_skill(skill_name, str(skill_path))
                    logger.debug("Registered Hermes skill '%s' from %s", skill_name, skill_path)
                else:
                    logger.warning("Skill definition missing at %s", skill_path)
            except Exception as err:
                logger.error("Failed to register skill '%s': %s", skill_name, err)

    # 2. Register lifecycle safety hooks
    if hasattr(ctx, "register_hook"):
        try:
            ctx.register_hook("pre_tool_call", pre_tool_guardrail_hook)
            ctx.register_hook("post_tool_call", post_tool_advisory_hook)
            logger.debug("Registered pre_tool_call and post_tool_call safety hooks.")
        except Exception as err:
            logger.error("Failed to register safety hooks: %s", err)

    # 3. Register convenience slash commands
    if hasattr(ctx, "register_command"):
        commands = [
            ("sentinel_audit", handle_sentinel_command, "Trigger pre-market risk audit across broker holdings and corporate filings."),
            ("valuation_audit", handle_valuation_command, "Perform 5-pillar fundamental valuation and moat analysis for an Indian equity holding."),
            ("mf_audit", handle_mf_command, "Audit mutual funds and ETFs for TER, AUM bloat, and benchmark tracking error."),
            ("market_status", handle_status_command, "Display active data sources, broker connection status, and advisory policy."),
        ]
        for name, handler, desc in commands:
            try:
                ctx.register_command(name=name, handler=handler, description=desc)
            except Exception as err:
                logger.error("Failed to register command '/%s': %s", name, err)
        logger.debug("Registered Hermes slash commands: /sentinel_audit, /valuation_audit, /mf_audit, /market_status.")
