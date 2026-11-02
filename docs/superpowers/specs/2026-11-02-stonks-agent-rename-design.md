# Design: Rename Plugin to `stonks-agent` and Generalize Skill Names

## Intent and Why
Align the repository identity with the project directory name `stonks-agent`, simplify skill naming conventions by dropping geographical prefixes (`indian-fundamental-valuation` -> `fundamental-valuation`, `indian-portfolio-sentinel` -> `portfolio-sentinel`), and update all configurations, docs, manifests, and tests consistently.

## Goals
- Rename plugin ID/name from `indian-market-trading-plugin` to `stonks-agent` in `plugin.json`, `plugin.yaml`, and `harnesses/openclaw_config.json`.
- Rename skill directories and skill frontmatter:
  - `skills/indian-fundamental-valuation` -> `skills/fundamental-valuation`
  - `skills/indian-portfolio-sentinel` -> `skills/portfolio-sentinel`
- Rename spec and plan documents in `docs/superpowers/`:
  - `docs/superpowers/specs/2026-11-01-indian-market-trading-plugin-design.md` -> `docs/superpowers/specs/2026-11-01-stonks-agent-design.md`
  - `docs/superpowers/plans/2026-11-01-indian-market-trading-plugin-plan.md` -> `docs/superpowers/plans/2026-11-01-stonks-agent-plan.md`
- Update all references across `agents/*.md`, `skills/**/SKILL.md`, `README.md`, `harnesses/*`, and `tests/*.py`.
- Ensure all automated unit tests (`tests/test_plugin_verification.py`, `tests/test_hermes_plugin.py`) pass cleanly.

## Non-Goals & Anti-Goals
- Do not alter underlying MCP server IDs (e.g. `indian-market-mcp`) or domain market data logic (NSE/BSE/AMFI).
- Do not introduce breaking syntax errors in YAML or JSON configs.

## Selected Approach
Option A: Direct rename of plugin identifiers, skill folder names, skill manifest declarations, spec/plan filenames, and all associated repository references, followed by test suite verification.
