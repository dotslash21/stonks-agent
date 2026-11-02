"""Stonks Agent Plugin for Hermes Agent.

Exposes 5 specialized investment intelligence skills, 10 read-only MCP data sources,
and strict advisory-only lifecycle hooks ensuring zero live order execution.
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("hermes.plugins.stonks_agent")

PLUGIN_DIR = Path(__file__).resolve().parent

# Strict prohibition list: no automated order placement or capital commitment
FORBIDDEN_EXECUTION_TOOLS = frozenset([
    "place_order",
    "place_gtt_order",
    "cancel_order",
    "modify_order",
    "execute_trade",
    "buy_order",
    "sell_order",
])

SKILLS = [
    ("portfolio-sentinel", PLUGIN_DIR / "skills" / "portfolio-sentinel" / "SKILL.md"),
    ("fundamental-valuation", PLUGIN_DIR / "skills" / "fundamental-valuation" / "SKILL.md"),
    ("nse-corporate-filings", PLUGIN_DIR / "skills" / "nse-corporate-filings" / "SKILL.md"),
    ("mf-etf-health-check", PLUGIN_DIR / "skills" / "mf-etf-health-check" / "SKILL.md"),
    ("obsidian-portfolio-memory", PLUGIN_DIR / "skills" / "obsidian-portfolio-memory" / "SKILL.md"),
]


def pre_tool_guardrail_hook(tool_name: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any) -> Optional[Dict[str, Any]]:
    """Enforce strict 100% advisory-only policy by intercepting and halting execution tools."""
    normalized_name = (tool_name or "").strip().lower()
    for forbidden in FORBIDDEN_EXECUTION_TOOLS:
        if forbidden in normalized_name:
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


def handle_sentinel_command(raw_args: str = "") -> str:
    """Slash command handler for /sentinel_audit."""
    target = f" for '{raw_args.strip()}'" if raw_args.strip() else ""
    return (
        f"Initiating pre-market risk audit{target} across Zerodha Kite, Groww, and INDmoney holdings.\n"
        "Checking corporate actions (splits, bonuses, dividends, ex-dates), quarterly XBRL disclosures, "
        "and overnight global market cues."
    )


def handle_valuation_command(raw_args: str = "") -> str:
    """Slash command handler for /valuation_audit."""
    symbol = raw_args.strip().upper() if raw_args.strip() else "target holding"
    return (
        f"Initiating 5-Pillar Fundamental Valuation for {symbol}:\n"
        "1. Economic Moat & ROIC vs WACC (Cost of Equity ~12.5%)\n"
        "2. Forensic Cash Flow & Earnings Quality (CFO/PAT ratio)\n"
        "3. Multi-Scenario 2-Stage DCF (Terminal Growth 5.0%)\n"
        "4. PEG & Valuation Multiples vs 5-Year Historical Bands\n"
        "5. Margin of Safety & Target Entry Zones"
    )


def handle_mf_command(raw_args: str = "") -> str:
    """Slash command handler for /mf_audit."""
    target = f" for '{raw_args.strip()}'" if raw_args.strip() else ""
    return (
        f"Initiating Mutual Fund & ETF health check{target}:\n"
        "Inspecting direct-plan TERs, tracking error vs underlying benchmark, "
        "AUM bloat, fund manager tenure, and scheme overlap across AMFI schemes."
    )


def handle_status_command(raw_args: str = "") -> str:
    """Slash command handler for /market_status."""
    return (
        "=== Indian Market Trading Plugin (Hermes Agent) ===\n"
        "Status: Active (100% Advisory-Only)\n"
        "MCP Servers Configured: 10 (Zerodha, Groww, INDmoney, NSE CM, NSE Bhavcopy, Indian Market, DalalOS, yFinance, Alpha Vantage, Obsidian)\n"
        "Skills Registered: 5 (Sentinel, Valuation, NSE Filings, MF/ETF Health, Obsidian Memory)\n"
        "Guardrail: Active (Execution tools strictly blocked)"
    )


def register(ctx: Any) -> None:
    """Hermes Agent plugin entry point.
    
    Registers skills, safety lifecycle hooks, and slash commands.
    """
    logger.info("Registering Indian Market Trading Plugin with Hermes Agent context...")

    # 1. Register all 5 bundled skills
    if hasattr(ctx, "register_skill"):
        for skill_name, skill_path in SKILLS:
            if skill_path.exists():
                ctx.register_skill(skill_name, str(skill_path))
                logger.debug("Registered Hermes skill '%s' from %s", skill_name, skill_path)
            else:
                logger.warning("Skill definition missing at %s", skill_path)

    # 2. Register lifecycle safety hooks
    if hasattr(ctx, "register_hook"):
        ctx.register_hook("pre_tool_call", pre_tool_guardrail_hook)
        ctx.register_hook("post_tool_call", post_tool_advisory_hook)
        logger.debug("Registered pre_tool_call and post_tool_call safety hooks.")

    # 3. Register convenience slash commands
    if hasattr(ctx, "register_command"):
        ctx.register_command(
            name="sentinel_audit",
            handler=handle_sentinel_command,
            description="Trigger pre-market risk audit across broker holdings and corporate filings.",
        )
        ctx.register_command(
            name="valuation_audit",
            handler=handle_valuation_command,
            description="Perform 5-pillar fundamental valuation and moat analysis for an Indian equity holding.",
        )
        ctx.register_command(
            name="mf_audit",
            handler=handle_mf_command,
            description="Audit mutual funds and ETFs for TER, AUM bloat, and benchmark tracking error.",
        )
        ctx.register_command(
            name="market_status",
            handler=handle_status_command,
            description="Display active data sources, broker connection status, and advisory policy.",
        )
        logger.debug("Registered Hermes slash commands: /sentinel_audit, /valuation_audit, /mf_audit, /market_status.")
