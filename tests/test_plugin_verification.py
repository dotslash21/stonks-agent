"""Automated verification test suite for Indian Market Trading Plugin.

Acts as the TDD verification foundation for the entire plugin:
- Manifest & MCP configuration schemas
- Strict guardrails (zero live execution tools)
- Corporate action verification rules
- Mandatory broker authentication gating
- Agent personas and skill packages with YAML frontmatter
- Mock portfolio and multi-harness manifests
"""

import json
from pathlib import Path
import re
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_MCP_SERVERS = [
    "zerodha-kite",
    "groww",
    "indmoney",
    "nse-cm-market",
    "nse-bhavcopy",
    "indian-market-mcp",
    "dalalos",
    "yfinance-mcp",
    "alpha-vantage",
    "obsidian",
]

FORBIDDEN_EXECUTION_TOOLS = [
    "place_order",
    "place_gtt_order",
    "cancel_order",
]

PROHIBITION_KEYWORDS = [
    "prohibit",
    "forbidden",
    "anti-goal",
    "strictly no",
    "no live",
    "not allowed",
    "disallow",
    "never",
    "do not",
    "no order",
    "without placing order",
    "without live order",
    "without live execution",
]

REQUIRED_SKILLS = [
    "indian-portfolio-sentinel",
    "indian-fundamental-valuation",
    "nse-corporate-filings",
    "mf-etf-health-check",
    "obsidian-portfolio-memory",
]

REQUIRED_AGENTS = [
    "portfolio_sentinel.md",
    "fundamental_analyst.md",
    "market_intel.md",
    "portfolio_manager.md",
]

REQUIRED_OBSIDIAN_TEMPLATES = [
    "stock-thesis-template.md",
    "mf-etf-review-template.md",
    "risk-alert-journal-template.md",
]

REQUIRED_HARNESS_CONFIGS = [
    "claude_desktop_config.json",
    "openclaw_config.json",
]


def extract_yaml_frontmatter(file_path: Path) -> dict:
    """Extract and parse YAML frontmatter from a markdown file."""
    if not file_path.exists():
        raise AssertionError(f"Target markdown file does not exist: {file_path}")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        content = f.read()

    stripped = content.lstrip()
    if not stripped.startswith("---"):
        raise AssertionError(f"{file_path} is missing opening YAML frontmatter '---'")

    parts = stripped.split("---", 2)
    if len(parts) < 3:
        raise AssertionError(f"{file_path} has unclosed YAML frontmatter (missing closing '---')")

    frontmatter_text = parts[1]
    data = {}
    for line in frontmatter_text.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue
        if ":" in line_str:
            k, v = line_str.split(":", 1)
            data[k.strip()] = v.strip().strip("'\"")
    return data


def test_plugin_manifest_validity():
    """Verify plugin.json exists, has valid JSON, and contains all required metadata."""
    manifest_path = REPO_ROOT / "plugin.json"
    assert manifest_path.exists(), f"plugin.json does not exist at {manifest_path}"

    with open(manifest_path, "r", encoding="utf-8") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError as err:
            raise AssertionError(f"plugin.json is not valid JSON: {err}") from err

    assert isinstance(manifest, dict), "plugin.json must contain a JSON object"

    required_fields = ["name", "version", "description", "author", "suggestedPrompts"]
    for field in required_fields:
        assert field in manifest, f"plugin.json missing required field '{field}'"
        assert manifest[field], f"plugin.json field '{field}' must not be empty"

    prompts = manifest["suggestedPrompts"]
    assert isinstance(prompts, list), "suggestedPrompts must be a list"
    assert len(prompts) >= 3, (
        f"suggestedPrompts must contain at least 3 prompts, found {len(prompts)}"
    )
    for i, prompt in enumerate(prompts):
        assert isinstance(prompt, str) and prompt.strip(), (
            f"suggestedPrompt[{i}] must be a non-empty string"
        )


def test_mcp_config_validity():
    """Verify mcp_config.json exists, has valid JSON, and contains all 10 MCP servers."""
    mcp_path = REPO_ROOT / "mcp_config.json"
    assert mcp_path.exists(), f"mcp_config.json does not exist at {mcp_path}"

    with open(mcp_path, "r", encoding="utf-8") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError as err:
            raise AssertionError(f"mcp_config.json is not valid JSON: {err}") from err

    assert isinstance(config, dict), "mcp_config.json must contain a JSON object"

    if "mcpServers" in config and isinstance(config["mcpServers"], dict):
        servers = config["mcpServers"]
    else:
        servers = config

    missing_servers = [s for s in REQUIRED_MCP_SERVERS if s not in servers]
    assert not missing_servers, (
        f"mcp_config.json is missing required MCP servers: {missing_servers}"
    )


def test_no_execution_tools_prohibition():
    """Verify 0 live execution tools (place_order, place_gtt_order, cancel_order) are bound."""
    scanned_dirs = [
        REPO_ROOT / "agents",
        REPO_ROOT / "skills",
        REPO_ROOT / "rules",
    ]

    violations = []

    for target_dir in scanned_dirs:
        if not target_dir.exists():
            continue
        for file_path in target_dir.rglob("*"):
            if file_path.suffix.lower() not in [".md", ".json"]:
                continue
            try:
                with open(file_path, "r", encoding="utf-8-sig", errors="ignore") as f:
                    for line_num, line in enumerate(f, start=1):
                        line_lower = line.lower()
                        # If the line explicitly states prohibition, it is a guardrail rule, not a tool binding
                        if any(kw in line_lower for kw in PROHIBITION_KEYWORDS):
                            continue
                        for tool in FORBIDDEN_EXECUTION_TOOLS:
                            if re.search(rf"\b{re.escape(tool)}\b", line_lower):
                                violations.append(
                                    f"{file_path.relative_to(REPO_ROOT)}:{line_num} "
                                    f"references forbidden tool '{tool}': {line.strip()}"
                                )
            except Exception as err:
                violations.append(f"Failed to scan {file_path}: {err}")

    assert not violations, (
        f"Forbidden execution tools detected ({len(violations)} violations):\n"
        + "\n".join(f"  - {v}" for v in violations)
    )


def test_corporate_action_rule_enforcement():
    """Verify corporate action verification checks exist in sentinel agent and skill."""
    sentinel_agent = REPO_ROOT / "agents" / "portfolio_sentinel.md"
    sentinel_skill = REPO_ROOT / "skills" / "indian-portfolio-sentinel" / "SKILL.md"

    assert sentinel_agent.exists(), f"Sentinel agent missing: {sentinel_agent}"
    assert sentinel_skill.exists(), f"Sentinel skill missing: {sentinel_skill}"

    for target_path in [sentinel_agent, sentinel_skill]:
        with open(target_path, "r", encoding="utf-8-sig") as f:
            content = f.read().lower()

        has_corporate_actions = (
            "get_corporate_actions" in content
            or (
                "corporate action" in content
                and any(term in content for term in ["split", "bonus", "demerger", "ex-date"])
            )
        )
        assert has_corporate_actions, (
            f"{target_path.relative_to(REPO_ROOT)} must contain explicit corporate action checks "
            "(e.g., 'get_corporate_actions' or split/bonus verification)."
        )


def test_broker_auth_gate_enforcement():
    """Verify rules/AGENTS.md and portfolio_manager.md enforce halting on unauthenticated brokers."""
    rules_file = REPO_ROOT / "rules" / "AGENTS.md"
    manager_agent = REPO_ROOT / "agents" / "portfolio_manager.md"

    assert rules_file.exists(), f"Rules file missing: {rules_file}"
    assert manager_agent.exists(), f"Portfolio manager agent missing: {manager_agent}"

    for target_path in [rules_file, manager_agent]:
        with open(target_path, "r", encoding="utf-8-sig") as f:
            content = f.read().lower()

        has_auth_gate = (
            ("auth" in content or "session" in content)
            and any(kw in content for kw in ["halt", "pause", "stop", "prompt"])
            and any(broker in content for broker in ["kite", "groww", "indmoney", "broker"])
        )
        assert has_auth_gate, (
            f"{target_path.relative_to(REPO_ROOT)} must explicitly enforce halting on "
            "unauthenticated or expired broker sessions."
        )


def test_skills_exist(required_skills=None):
    """Verify required skills exist with valid YAML frontmatter."""
    skills_to_check = required_skills or REQUIRED_SKILLS
    missing_skills = []
    for skill_name in skills_to_check:
        skill_path = REPO_ROOT / "skills" / skill_name / "SKILL.md"
        if not skill_path.exists():
            missing_skills.append(str(skill_path.relative_to(REPO_ROOT)))
            continue
        frontmatter = extract_yaml_frontmatter(skill_path)
        assert "name" in frontmatter and frontmatter["name"], (
            f"Skill {skill_path.relative_to(REPO_ROOT)} frontmatter missing non-empty 'name'"
        )
        assert "description" in frontmatter and frontmatter["description"], (
            f"Skill {skill_path.relative_to(REPO_ROOT)} frontmatter missing non-empty 'description'"
        )

    assert not missing_skills, f"Missing required skills: {missing_skills}"


def test_agents_exist(required_agents=None):
    """Verify required agents exist with valid YAML frontmatter."""
    agents_to_check = required_agents or REQUIRED_AGENTS
    missing_agents = []
    for agent_file in agents_to_check:
        agent_path = REPO_ROOT / "agents" / agent_file
        if not agent_path.exists():
            missing_agents.append(str(agent_path.relative_to(REPO_ROOT)))
            continue
        frontmatter = extract_yaml_frontmatter(agent_path)
        assert "name" in frontmatter and frontmatter["name"], (
            f"Agent {agent_path.relative_to(REPO_ROOT)} frontmatter missing non-empty 'name'"
        )
        has_description_or_role = bool(
            frontmatter.get("description") or frontmatter.get("role")
        )
        assert has_description_or_role, (
            f"Agent {agent_path.relative_to(REPO_ROOT)} frontmatter missing 'description' or 'role'"
        )

    assert not missing_agents, f"Missing required agents: {missing_agents}"


def test_all_skills_and_agents_exist():
    """Verify all 5 skills and 4 agents exist with valid YAML frontmatter."""
    test_skills_exist()
    test_agents_exist()


def test_mock_portfolio_schema():
    """Verify examples/mock_portfolio.json exists and parses cleanly."""
    mock_path = REPO_ROOT / "examples" / "mock_portfolio.json"
    assert mock_path.exists(), f"examples/mock_portfolio.json does not exist at {mock_path}"

    with open(mock_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as err:
            raise AssertionError(f"examples/mock_portfolio.json is invalid JSON: {err}") from err

    assert isinstance(data, dict), "Mock portfolio must be a JSON object"
    assert "holdings" in data and isinstance(data["holdings"], list), (
        "Mock portfolio must contain a 'holdings' list"
    )
    assert len(data["holdings"]) > 0, "Mock portfolio holdings list must not be empty"

    for idx, holding in enumerate(data["holdings"]):
        assert isinstance(holding, dict), f"Holding #{idx} must be a JSON object"
        assert "symbol" in holding and holding["symbol"], f"Holding #{idx} missing symbol"


def test_obsidian_templates_exist():
    """Verify all Obsidian note templates exist and are non-empty."""
    template_dir = REPO_ROOT / "templates" / "obsidian"
    assert template_dir.exists(), f"Template directory missing: {template_dir}"

    for template_name in REQUIRED_OBSIDIAN_TEMPLATES:
        template_path = template_dir / template_name
        assert template_path.exists(), f"Obsidian template missing: {template_path}"
        assert template_path.stat().st_size > 0, f"Template file is empty: {template_path}"


def test_harness_configs_validity():
    """Verify claude_desktop_config.json and openclaw_config.json exist and are valid JSON."""
    harness_dir = REPO_ROOT / "harnesses"
    assert harness_dir.exists(), f"Harness directory missing: {harness_dir}"

    for config_name in REQUIRED_HARNESS_CONFIGS:
        config_path = harness_dir / config_name
        assert config_path.exists(), f"Harness config missing: {config_path}"
        with open(config_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as err:
                raise AssertionError(f"{config_name} is invalid JSON: {err}") from err
        assert isinstance(data, dict), f"{config_name} must contain a JSON object"


class TestPluginVerification(unittest.TestCase):
    """Unittest wrapper exposing all verification functions for test runners."""

    def test_plugin_manifest_validity(self):
        test_plugin_manifest_validity()

    def test_mcp_config_validity(self):
        test_mcp_config_validity()

    def test_no_execution_tools_prohibition(self):
        test_no_execution_tools_prohibition()

    def test_corporate_action_rule_enforcement(self):
        test_corporate_action_rule_enforcement()

    def test_broker_auth_gate_enforcement(self):
        test_broker_auth_gate_enforcement()

    def test_all_skills_and_agents_exist(self):
        test_all_skills_and_agents_exist()

    def test_mock_portfolio_schema(self):
        test_mock_portfolio_schema()

    def test_obsidian_templates_exist(self):
        test_obsidian_templates_exist()

    def test_harness_configs_validity(self):
        test_harness_configs_validity()


def main():
    """Execute all verification tests and return exit code 0 on success, 1 on failure."""
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPluginVerification)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
