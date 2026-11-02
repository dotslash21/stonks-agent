"""Unit and integration tests for the Indian Market Trading Hermes Agent Plugin."""

import importlib.util
from pathlib import Path
import re
import sys
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_SKILLS = [
    "portfolio-sentinel",
    "fundamental-valuation",
    "nse-corporate-filings",
    "mf-etf-health-check",
    "obsidian-portfolio-memory",
]

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

FORBIDDEN_TOOLS = [
    "place_order",
    "place_gtt_order",
    "cancel_order",
    "modify_order",
    "execute_trade",
    "buy_order",
    "sell_order",
]

ALLOWED_TOOLS = [
    "get_holdings",
    "get_positions",
    "get_margins",
    "get_quote",
    "get_market_breadth",
    "get_bhavcopy",
    "get_corporate_actions",
    "search_xbrl_filings",
    "get_scheme_details",
    "create_obsidian_note",
]


class MockHermesContext:
    """Mock Hermes Agent registration context for verification."""

    def __init__(self):
        self.skills = {}
        self.hooks = {}
        self.commands = {}
        self.tools = {}

    def register_skill(self, name: str, path: str):
        self.skills[name] = path

    def register_hook(self, event_name: str, handler):
        self.hooks[event_name] = handler

    def register_command(self, name: str, handler, description: str = ""):
        self.commands[name] = {"handler": handler, "description": description}

    def register_tool(self, name: str, **kwargs):
        self.tools[name] = kwargs


def parse_simple_yaml_dict(text: str) -> dict:
    """Minimal zero-dependency YAML dictionary/list parser for test assertions."""
    lines = text.splitlines()
    data = {}
    current_key = None
    current_list = None

    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Check for list item under current_key
        if line.startswith("  - ") or line.startswith("    - "):
            item = stripped[2:].strip().strip("'\"")
            if current_list is not None and not item.startswith("name:"):
                current_list.append(item)
            continue

        # Only lines with zero leading whitespace can define top-level keys
        if not line.startswith(" ") and not line.startswith("\t") and ":" in stripped:
            k, v = stripped.split(":", 1)
            k = k.strip()
            v = v.strip().strip("'\"")

            if not v or v == "[]":
                current_key = k
                if v == "[]":
                    data[k] = []
                    current_list = None
                else:
                    current_list = []
                    data[k] = current_list
            else:
                data[k] = v
                current_key = None
                current_list = None

    return data


class TestHermesPlugin(unittest.TestCase):
    """Test suite verifying Hermes Agent plugin specification conformance."""

    def setUp(self):
        self.plugin_yaml_path = REPO_ROOT / "plugin.yaml"
        self.init_py_path = REPO_ROOT / "__init__.py"
        self.hermes_config_path = REPO_ROOT / "harnesses" / "hermes_config.yaml"

    def test_plugin_yaml_exists_and_conforms(self):
        """Verify plugin.yaml exists, has required metadata, and references valid skill files."""
        self.assertTrue(self.plugin_yaml_path.exists(), "plugin.yaml must exist at repo root")
        content = self.plugin_yaml_path.read_text(encoding="utf-8")

        parsed = parse_simple_yaml_dict(content)
        self.assertEqual(parsed.get("name"), "stonks-agent")
        self.assertEqual(parsed.get("version"), "1.0.0")
        self.assertIn("advisory-only", parsed.get("description", "").lower())
        self.assertIn("Antigravity Ecosystem", parsed.get("author", ""))

        # Check provides_hooks
        hooks = parsed.get("provides_hooks", [])
        self.assertIn("pre_tool_call", hooks)
        self.assertIn("post_tool_call", hooks)

        # Check provides_tools is empty (advisory-only guarantee)
        tools = parsed.get("provides_tools", [])
        self.assertEqual(len(tools), 0, "provides_tools must be empty (0 execution tools allowed)")

        # Verify skills referenced in YAML exist on disk
        skills = parsed.get("skills", [])
        self.assertEqual(len(skills), 5, f"Expected 5 skills declared in plugin.yaml, found {len(skills)}")
        for skill_rel in skills:
            skill_file = REPO_ROOT / skill_rel
            self.assertTrue(skill_file.exists(), f"Skill file does not exist: {skill_file}")

    def test_init_py_registration(self):
        """Verify __init__.py exports register(ctx) and populates skills, hooks, and commands."""
        self.assertTrue(self.init_py_path.exists(), "__init__.py must exist at repo root")

        spec = importlib.util.spec_from_file_location("hermes_plugin", str(self.init_py_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.assertTrue(hasattr(module, "register"), "__init__.py must define register(ctx)")
        self.assertTrue(callable(module.register), "register must be a callable function")

        mock_ctx = MockHermesContext()
        module.register(mock_ctx)

        # 1. Check all 5 skills registered
        for skill in REQUIRED_SKILLS:
            self.assertIn(skill, mock_ctx.skills, f"Skill '{skill}' was not registered")
            path = Path(mock_ctx.skills[skill])
            self.assertTrue(path.exists(), f"Registered path for '{skill}' does not exist: {path}")

        # 2. Check hooks registered
        self.assertIn("pre_tool_call", mock_ctx.hooks, "pre_tool_call hook not registered")
        self.assertIn("post_tool_call", mock_ctx.hooks, "post_tool_call hook not registered")

        # 3. Check slash commands registered
        expected_commands = ["sentinel_audit", "valuation_audit", "mf_audit", "market_status"]
        for cmd in expected_commands:
            self.assertIn(cmd, mock_ctx.commands, f"Command '/{cmd}' was not registered")

        # 4. Check zero execution tools registered
        self.assertEqual(len(mock_ctx.tools), 0, "No tools should be directly registered (0 execution tools)")

    def test_guardrail_hook_blocks_forbidden_tools(self):
        """Verify pre_tool_call hook blocks all forbidden trade execution tools."""
        spec = importlib.util.spec_from_file_location("hermes_plugin", str(self.init_py_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        guardrail = module.pre_tool_guardrail_hook

        # Every forbidden execution tool must be blocked
        for forbidden in FORBIDDEN_TOOLS:
            result = guardrail(forbidden, {"symbol": "INFY", "quantity": 10})
            self.assertIsInstance(result, dict, f"Expected dict result for forbidden tool '{forbidden}'")
            self.assertEqual(result.get("action"), "block", f"Tool '{forbidden}' must be blocked")
            self.assertIn("strictly forbidden", result.get("message", "").lower())

        # Variation with prefixes/suffixes (e.g., kite_place_order)
        for variant in ["kite_place_order", "groww_cancel_order", "execute_trade_now"]:
            result = guardrail(variant, {})
            self.assertIsInstance(result, dict)
            self.assertEqual(result.get("action"), "block")

        # Read-only allowed tools must NOT be blocked
        for allowed in ALLOWED_TOOLS:
            result = guardrail(allowed, {"symbol": "RELIANCE"})
            self.assertIsNone(result, f"Allowed tool '{allowed}' was unexpectedly blocked: {result}")

    def test_slash_command_handlers(self):
        """Verify registered slash commands return non-empty informative guidance."""
        spec = importlib.util.spec_from_file_location("hermes_plugin", str(self.init_py_path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        mock_ctx = MockHermesContext()
        module.register(mock_ctx)

        sentinel_out = mock_ctx.commands["sentinel_audit"]["handler"]("TCS")
        self.assertIn("pre-market risk audit", sentinel_out.lower())
        self.assertIn("tcs", sentinel_out.lower())

        valuation_out = mock_ctx.commands["valuation_audit"]["handler"]("HDFCBANK")
        self.assertIn("5-pillar fundamental valuation", valuation_out.lower())
        self.assertIn("hdfcbank", valuation_out.lower())

        mf_out = mock_ctx.commands["mf_audit"]["handler"]("Parag Parikh Flexi Cap")
        self.assertIn("mutual fund", mf_out.lower())

        status_out = mock_ctx.commands["market_status"]["handler"]("")
        self.assertIn("100% advisory-only", status_out.lower())

    def test_hermes_config_yaml_validity(self):
        """Verify harnesses/hermes_config.yaml defines all 10 required MCP servers."""
        self.assertTrue(self.hermes_config_path.exists(), "hermes_config.yaml must exist")
        content = self.hermes_config_path.read_text(encoding="utf-8")

        self.assertIn("mcp_servers:", content)

        for server in REQUIRED_MCP_SERVERS:
            self.assertTrue(
                re.search(rf"^\s+{re.escape(server)}:\s*$", content, re.MULTILINE),
                f"hermes_config.yaml missing server definition for '{server}'",
            )


if __name__ == "__main__":
    unittest.main()
