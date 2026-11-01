# Indian Market Portfolio Sentinel & Trading Plugin Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a modular, distributable AI Agent Plugin for Antigravity, Claude Desktop, and OpenClaw that monitors Indian equities, ETFs, and direct mutual funds held across Zerodha Kite, Groww, and INDmoney for negative market events, provides advisory valuation/risk audits, and journals memory in Obsidian.

**Architecture:** The plugin leverages official exchange MCP servers (`nse-cm-market`, `nse-bhavcopy`), specialized mutual fund/flow endpoints (`indian-market-mcp`), forensic regulatory analysis (`DalalOS`), and resilient fallbacks (`yfinance-mcp`, `Alpha Vantage`), interacting with read-only broker MCPs under strict authentication gating and persisting investment memory in Obsidian.

**Tech Stack:** Model Context Protocol (MCP) servers (JSON-RPC 2.0 over stdio and Streamable HTTP), Antigravity Plugin manifest (`plugin.json`), Markdown agent personas and skills with YAML frontmatter, Obsidian Local REST API (`obsidian-mcp-server`), Python 3 verification test suite.

**Spec:** [`docs/superpowers/specs/2026-11-01-indian-market-trading-plugin-design.md`](file:///c:/Users/aruna/development/agentic-trading-setup/docs/superpowers/specs/2026-11-01-indian-market-trading-plugin-design.md)

---

## Global Constraints

- **Strictly Advisory Recommendations**: All recommendations are strictly advisory. No live order placement tools (`place_order`, `place_gtt_order`) may be bound to agents or defined in skills.
- **Delivery Assets Only**: Scope is strictly cash delivery equities, ETFs, and direct mutual funds. Strictly NO Futures & Options (F&O) and NO intraday day trading/scalping.
- **Strict Broker Authentication Gate**: If any required broker (Kite, Groww, INDmoney) session is missing or expired, the agent must halt and actively trigger re-authentication prompts rather than silently ignoring the broker or using fallback mock data.
- **Corporate Action Price-Adjustment Check**: Agents and skills must cross-reference corporate actions (splits, bonuses, demergers) on ex-dates before flagging nominal price plunges (>20%) as catastrophic breakdowns.
- **Multi-Tiered Data Routing with Graceful Fallbacks**: Official NSE feeds (`nse-cm-market`, `nse-bhavcopy`) serve as primary ground truth, falling back gracefully to `indian-market-mcp` and `yfinance-mcp` on timeout or failure.
- **Token-Optimized Output**: Prefer server-side computed indicators and compact markdown/CSV tables over raw, multi-thousand-token OHLCV JSON dumps.
- **Persistent Obsidian Journaling**: Theses, MF audits, and risk alert logs are persisted to the user's Obsidian vault via `obsidian-mcp-server`.

---

## Review Focus

1. **Broker Session Expiration**: When Kite session token expires at 06:00 IST, the agent halts with an interactive auth guide; verified by checking `rules/AGENTS.md` and `agents/portfolio_manager.md`.
2. **Corporate Action Nominal Plunge**: When a stock splits 2:1 or issues a 1:1 bonus, the sentinel checks `get_corporate_actions` before generating a price crash alert; verified by rule assertions in `skills/indian-portfolio-sentinel/SKILL.md`.
3. **Execution Tool Prohibition**: Under no circumstances may an agent persona or skill define or bind an execution tool (`place_order`, `place_gtt_order`); verified by automated regex scanning in `tests/test_plugin_verification.py`.
4. **Primary Market Data Fallback**: When `nse-cm-market` or `nse-bhavcopy` times out, the market intel agent routes seamlessly to `indian-market-mcp` or `yfinance-mcp`; verified by fallback matrix in `agents/market_intel.md`.
5. **Context Window Token Exhaustion**: Skills must mandate server-side indicators or compact table serialization rather than raw JSON time-series; verified by instructions in `skills/indian-portfolio-sentinel/SKILL.md`.

---

## File Structure

```
agentic-trading-setup/
├── plugin.json                              # Antigravity plugin manifest
├── mcp_config.json                          # Unified MCP server registry (10 servers)
├── README.md                                # Comprehensive user & harness setup guide
├── rules/
│   └── AGENTS.md                            # Universal guardrails (Advisory, auth gates, corporate actions, No F&O)
├── agents/
│   ├── portfolio_sentinel.md                # Adverse event radar (corporate action aware)
│   ├── fundamental_analyst.md               # 5-Pillar valuation, moat analyst & XBRL audit
│   ├── market_intel.md                      # Multi-tiered market data orchestrator
│   └── portfolio_manager.md                 # Multi-broker consolidator & auth orchestrator
├── skills/
│   ├── indian-portfolio-sentinel/
│   │   └── SKILL.md                         # Risk matrix, corporate action adjustment & severity rules
│   ├── indian-fundamental-valuation/
│   │   └── SKILL.md                         # 5-Pillar valuation, DCF & DalalOS XBRL audits
│   ├── nse-corporate-filings/
│   │   └── SKILL.md                         # SEBI LODR Reg 30 disclosures & insider trading audits
│   ├── mf-etf-health-check/
│   │   └── SKILL.md                         # AMFI scheme analytics, tracking error & expense ratio audits
│   └── obsidian-portfolio-memory/
│       └── SKILL.md                         # Obsidian vault note & thesis journaling
├── templates/
│   └── obsidian/
│       ├── stock-thesis-template.md         # Template for fundamental stock theses
│       ├── mf-etf-review-template.md        # Template for mutual fund / ETF health reviews
│       └── risk-alert-journal-template.md   # Template for adverse event incident logs
├── harnesses/
│   ├── claude_desktop_config.json           # Claude Desktop configuration snippet
│   └── openclaw_config.json                 # OpenClaw configuration snippet
├── examples/
│   └── mock_portfolio.json                  # Sample portfolio for explicit simulated runs
└── tests/
    └── test_plugin_verification.py          # Automated verification suite for plugin integrity & guardrails
```

---

## Implementation Tasks

### Task 1: Automated Verification Test Suite (TDD Foundation)

**Files:**
- Create: `tests/test_plugin_verification.py`

**Interfaces:**
- Consumes: JSON manifests (`plugin.json`, `mcp_config.json`), agent personas (`agents/*.md`), skill definitions (`skills/*/SKILL.md`), rules (`rules/AGENTS.md`), and templates (`templates/obsidian/*.md`).
- Produces: Test runner script that returns exit code 0 when all schemas, guardrails, corporate action rules, auth gates, and link paths pass.

- [ ] **Step 1: Write the failing verification test suite in `tests/test_plugin_verification.py`**
  Write tests covering:
  - `test_plugin_manifest_validity()`: Checks `plugin.json` exists, valid JSON, contains `name`, `version`, `description`, `author`, and at least 3 `suggestedPrompts`.
  - `test_mcp_config_validity()`: Checks `mcp_config.json` exists, valid JSON, contains all 10 MCP servers (`zerodha-kite`, `groww`, `indmoney`, `nse-cm-market`, `nse-bhavcopy`, `indian-market-mcp`, `dalalos`, `yfinance-mcp`, `alpha-vantage`, `obsidian`).
  - `test_no_execution_tools_prohibition()`: Scans all `.md` and `.json` files in `agents/`, `skills/`, and `rules/` for forbidden execution tools (`place_order`, `place_gtt_order`, `cancel_order`) to ensure 0 matches.
  - `test_corporate_action_rule_enforcement()`: Asserts that `agents/portfolio_sentinel.md` and `skills/indian-portfolio-sentinel/SKILL.md` contain corporate action checks (`get_corporate_actions` or split/bonus check).
  - `test_broker_auth_gate_enforcement()`: Asserts that `rules/AGENTS.md` and `agents/portfolio_manager.md` explicitly enforce halting on unauthenticated brokers.
  - `test_all_skills_and_agents_exist()`: Asserts that all 5 skills and 4 agents exist with valid YAML frontmatter.
  - `test_mock_portfolio_schema()`: Asserts `examples/mock_portfolio.json` exists and parses cleanly.

- [ ] **Step 2: Run verification test to verify it fails initially**
  Run: `python tests/test_plugin_verification.py`
  Expected: FAIL with `AssertionError: plugin.json does not exist` or similar missing file error.

- [ ] **Step 3: Commit initial test harness**
  ```bash
  git add tests/test_plugin_verification.py
  git commit -m "test: add automated plugin verification test suite"
  ```

---

### Task 2: Plugin Manifest & Master MCP Registry

**Files:**
- Create: `plugin.json`
- Create: `mcp_config.json`

**Interfaces:**
- Consumes: Specifications from Section 6 and Section 7 of design doc.
- Produces: Antigravity plugin manifest and unified 10-server MCP configuration.

- [ ] **Step 1: Implement `plugin.json`**
  Define plugin metadata for Antigravity & OpenClaw:
  - `name`: `"indian-market-trading-plugin"`
  - `version`: `"1.0.0"`
  - `description`: `"Proactive AI Agent Plugin for Indian equities, ETFs, and direct mutual funds across Zerodha Kite, Groww, and INDmoney with official NSE data and Obsidian memory."`
  - `author`: `"Antigravity Ecosystem"`
  - `suggestedPrompts`:
    1. `"Run a comprehensive pre-market risk audit across my Zerodha Kite and Groww portfolios for any adverse events, corporate filings, or technical breakdowns."`
    2. `"Perform a 5-pillar fundamental valuation and moat analysis on my top 3 equity holdings, verifying balance sheets against BSE-XBRL filings."`
    3. `"Audit my mutual funds on INDmoney and Groww for manager departures, AUM bloat, and expense ratio changes, and journal findings in Obsidian."`

- [ ] **Step 2: Implement `mcp_config.json`**
  Register all 10 MCP servers with exact configurations:
  - `zerodha-kite`: `npx -y mcp-remote https://mcp.kite.trade/mcp`
  - `groww`: `npx -y mcp-remote@0.1.18 https://mcp.groww.in/mcp 52155`
  - `indmoney`: `https://mcp.indmoney.com/mcp`
  - `nse-cm-market`: `npx -y mcp-remote https://mcp.nseindia.in/cmmkt/mcp`
  - `nse-bhavcopy`: `npx -y mcp-remote https://mcp.nseindia.in/bhavcopy/cm/mcp`
  - `indian-market-mcp`: `uvx indian-market-mcp`
  - `dalalos`: `https://mcp.dalalos.in/mcp`
  - `yfinance-mcp`: `uvx yfmcp`
  - `alpha-vantage`: `https://mcp.alphavantage.co/mcp`
  - `obsidian`: `npx -y obsidian-mcp-server@3.7.2` (with user's `OBSIDIAN_API_KEY`)

- [ ] **Step 3: Run verification test on manifest & MCP config**
  Run: `python -c "import tests.test_plugin_verification as t; t.test_plugin_manifest_validity(); t.test_mcp_config_validity(); print('PASS')"`
  Expected: PASS

- [ ] **Step 4: Commit**
  ```bash
  git add plugin.json mcp_config.json
  git commit -m "feat: add plugin manifest and unified 10-server MCP config"
  ```

---

### Task 3: Universal Operating Rules & Safety Guardrails

**Files:**
- Create: `rules/AGENTS.md`

**Interfaces:**
- Consumes: Anti-goals and constraints from design doc.
- Produces: Top-level rule file read by all agents in Antigravity and other harnesses.

- [ ] **Step 1: Implement `rules/AGENTS.md`**
  Enforce the four cardinal laws:
  1. **Strictly Advisory**: All trade signals, stop-loss levels, and rebalancing recommendations are strictly advisory markdown outputs. Live order placement (`place_order`, `place_gtt_order`) is prohibited.
  2. **Mandatory Broker Authentication Gating**: If any designated broker (Zerodha Kite, Groww, INDmoney) session is missing or expired, the agent must immediately pause and emit an authentication request card. Never fall back to mock data or silently skip an unauthenticated broker.
  3. **Cash Delivery Equities, ETFs & Direct MFs Only**: Strictly NO Futures & Options (F&O) and NO intraday scalping.
  4. **Corporate Action Price Verification**: Never interpret nominal price drops as market crashes without checking corporate action registries (`get_corporate_actions` or DalalOS) on the ex-date.
  5. **Token Optimization**: Use server-side calculated indicators (`moving_average`, Alpha Vantage) and compact markdown/CSV tables rather than uncompressed JSON candlestick dumps.

- [ ] **Step 2: Run verification test on rules**
  Run: `python -c "import tests.test_plugin_verification as t; t.test_no_execution_tools_prohibition(); t.test_broker_auth_gate_enforcement(); print('PASS')"`
  Expected: PASS

- [ ] **Step 3: Commit**
  ```bash
  git add rules/AGENTS.md
  git commit -m "feat: add universal agent rules and safety guardrails"
  ```

---

### Task 4: Core Skills Packaging & Domain Intelligence Salvage

**Files:**
- Create: `skills/indian-portfolio-sentinel/SKILL.md`
- Create: `skills/indian-fundamental-valuation/SKILL.md`
- Create: `skills/nse-corporate-filings/SKILL.md`
- Create: `skills/mf-etf-health-check/SKILL.md`

**Interfaces:**
- Consumes: Salvaged domain knowledge from `config/risk_rules.json`, `src/analyzers/five_pillar_valuation.py`, and `src/connectors/nse_filings_connector.py`.
- Produces: Clean, standard SKILL.md packages with YAML frontmatter, execution workflows, and fallback logic.

- [ ] **Step 1: Implement `skills/indian-portfolio-sentinel/SKILL.md`**
  - Frontmatter: `name: indian-portfolio-sentinel`, `description: "Monitors Indian equity and ETF holdings for negative market events, corporate filings, and trend breakdowns."`
  - Salvage: Risk categories (Critical, High, Medium, Low), threshold triggers (e.g., Promoter pledge > 25%, 200 EMA breakdown, RSI 14 < 30).
  - Add: **Corporate Action Adjustment Rule** — explicit instruction to check `get_corporate_actions` before triggering price crash alerts.
  - Add: Primary (NSE Live CM / Bhavcopy) -> Fallback (`indian-market-mcp` -> `yfinance-mcp`) routing table.

- [ ] **Step 2: Implement `skills/indian-fundamental-valuation/SKILL.md`**
  - Frontmatter: `name: indian-fundamental-valuation`, `description: "Performs 5-pillar fundamental valuation, moat durability analysis, and DCF intrinsic value calculation for Indian equities."`
  - Salvage: 5 pillars (RoCE > 15%, Moat durability, Clean governance & pledge < 10%, Debt safety D/E < 1.0, DCF margin of safety > 20%).
  - Add: DalalOS BSE-XBRL integration for verified balance sheet line-items, capex commitments, and order books.

- [ ] **Step 3: Implement `skills/nse-corporate-filings/SKILL.md`**
  - Frontmatter: `name: nse-corporate-filings`, `description: "Monitors SEBI LODR Regulation 30 corporate announcements, board meeting outcomes, and insider trading disclosures."`
  - Salvage: Key announcement types (auditor resignation, forensic audit, promoter pledge, litigation, earnings miss).
  - Add: Verification via official NSE feeds and DalalOS XBRL disclosures.

- [ ] **Step 4: Implement `skills/mf-etf-health-check/SKILL.md`**
  - Frontmatter: `name: mf-etf-health-check`, `description: "Monitors direct mutual fund schemes and ETFs for star manager departures, AUM bloat, expense ratio creep, and tracking errors."`
  - Add: AMFI scheme lookup across 47,000+ schemes via `indian-market-mcp`, rolling returns, Sharpe, Sortino, SIP XIRR.
  - Add: `yfinance-mcp` fund look-through (`yfinance_get_fund_data`) for ETF sector weights and Morningstar style boxes.

- [ ] **Step 5: Run verification test on skills**
  Run: `python -c "import tests.test_plugin_verification as t; t.test_all_skills_and_agents_exist(); print('PASS')"`
  Expected: Passes skill check tests.

- [ ] **Step 6: Commit**
  ```bash
  git add skills/
  git commit -m "feat: package core investment analysis skills with corporate action checks and multi-tier routing"
  ```

---

### Task 5: Obsidian Portfolio Memory Skill & Note Templates

**Files:**
- Create: `skills/obsidian-portfolio-memory/SKILL.md`
- Create: `templates/obsidian/stock-thesis-template.md`
- Create: `templates/obsidian/mf-etf-review-template.md`
- Create: `templates/obsidian/risk-alert-journal-template.md`

**Interfaces:**
- Consumes: `obsidian-mcp-server` tools (`create_note`, `update_note`, `get_notes`, `search_notes`) and vault structure.
- Produces: Memory management skill and ready-to-use markdown note templates for the user's Obsidian vault.

- [ ] **Step 1: Implement `skills/obsidian-portfolio-memory/SKILL.md`**
  - Frontmatter: `name: obsidian-portfolio-memory`, `description: "Manages persistent investment memory, stock theses, mutual fund audits, and risk alert logs in Obsidian vault via obsidian-mcp-server."`
  - Define folder conventions: `Investing/Theses/`, `Investing/Funds/`, `Investing/Alerts/`.
  - Provide tool call examples for reading prior theses before judging a stock and appending new alert entries.

- [ ] **Step 2: Implement `templates/obsidian/stock-thesis-template.md`**
  - Frontmatter properties: `symbol`, `company_name`, `entry_date`, `avg_buy_price`, `thesis_summary`, `moat_type`, `target_exit_price`, `stop_loss_level`.
  - Sections: Business Model & Moat, 5-Pillar Scorecard, Key Growth Catalysts, Invalidation Criteria (What would make me sell?).

- [ ] **Step 3: Implement `templates/obsidian/mf-etf-review-template.md`**
  - Frontmatter properties: `scheme_code`, `scheme_name`, `amc`, `category`, `nav`, `expense_ratio`, `fund_manager`, `review_date`.
  - Sections: 3yr/5yr Rolling Returns vs Benchmark, Sharpe & Sortino ratios, Portfolio Overlap & Concentration, Red Flags & Advisory Status.

- [ ] **Step 4: Implement `templates/obsidian/risk-alert-journal-template.md`**
  - Frontmatter properties: `incident_id`, `date`, `symbol`, `severity`, `status`.
  - Sections: Event Summary, Triggering MCP Source, Corporate Action Verification Status, Portfolio Impact, Advisory Recommended Action.

- [ ] **Step 5: Verify templates and memory skill**
  Run: `python tests/test_plugin_verification.py`
  Expected: Passes template existence and syntax checks.

- [ ] **Step 6: Commit**
  ```bash
  git add skills/obsidian-portfolio-memory/ templates/obsidian/
  git commit -m "feat: add Obsidian portfolio memory skill and note templates"
  ```

---

### Task 6: Specialized Agent Personas & Orchestration

**Files:**
- Create: `agents/portfolio_sentinel.md`
- Create: `agents/fundamental_analyst.md`
- Create: `agents/market_intel.md`
- Create: `agents/portfolio_manager.md`

**Interfaces:**
- Consumes: Skills in `skills/`, rules in `rules/AGENTS.md`, and MCP connections from `mcp_config.json`.
- Produces: 4 production agent personas ready for Antigravity, Claude, and OpenClaw.

- [ ] **Step 1: Implement `agents/portfolio_sentinel.md`**
  - Role: Adverse event early-warning radar.
  - Instructions: Pull user holdings via `portfolio_manager`, scan NSE Live CM / Bhavcopy for price/volume anomalies, check SEBI LODR announcements. Strictly verify corporate actions on ex-dates to eliminate false crash alarms. Produce advisory risk alert cards.

- [ ] **Step 2: Implement `agents/fundamental_analyst.md`**
  - Role: 5-Pillar Buffett/Duan valuation & moat analyst.
  - Instructions: Evaluate RoCE, moat durability, clean governance (pledge < 10%), debt safety, and DCF intrinsic value. Cross-examine reported balance sheets against DalalOS BSE-XBRL filings. Read/write theses in Obsidian.

- [ ] **Step 3: Implement `agents/market_intel.md`**
  - Role: Multi-tiered market data orchestrator.
  - Instructions: Manage official NSE feeds (`nse-cm-market`, `nse-bhavcopy`), route MF/ETF queries to `indian-market-mcp`, query DalalOS for deep XBRL governance audits, and seamlessly fall back to `yfinance-mcp` or `Alpha Vantage` if primary endpoints are unreachable.

- [ ] **Step 4: Implement `agents/portfolio_manager.md`**
  - Role: Multi-broker asset consolidator and authentication orchestrator.
  - Instructions: Ingest holdings across Zerodha Kite, Groww, and INDmoney. Enforce strict authentication: if a broker session is invalid, halt and prompt the user to log in. Aggregate total net worth, asset allocation (Equity / ETF / MF), and dispatch tasks to specialized agents.

- [ ] **Step 5: Run verification test on agents**
  Run: `python tests/test_plugin_verification.py`
  Expected: Passes agent existence and persona guardrail checks.

- [ ] **Step 6: Commit**
  ```bash
  git add agents/
  git commit -m "feat: implement specialized agent personas with multi-tier routing and corporate action safeguards"
  ```

---

### Task 7: Multi-Harness Integration Manifests & Mock Data Relocation

**Files:**
- Create: `harnesses/claude_desktop_config.json`
- Create: `harnesses/openclaw_config.json`
- Create: `examples/mock_portfolio.json` (relocate from `data/mock_portfolio.json`)

**Interfaces:**
- Consumes: `mcp_config.json` server definitions.
- Produces: Ready-to-copy configuration files for Claude Desktop and OpenClaw, plus clean test portfolio for offline simulations.

- [ ] **Step 1: Implement `harnesses/claude_desktop_config.json`**
  - Format standard `claude_desktop_config.json` snippet with all 10 MCP servers so Claude Desktop users can drop it directly into their `claude_desktop_config.json`.

- [ ] **Step 2: Implement `harnesses/openclaw_config.json`**
  - Format OpenClaw plugin/agent configuration mapping agents and MCP servers.

- [ ] **Step 3: Relocate test portfolio to `examples/mock_portfolio.json`**
  - Move `data/mock_portfolio.json` into `examples/mock_portfolio.json` and ensure it reflects multi-broker holdings (Kite, Groww, INDmoney) across cash equities, ETFs, and direct mutual funds for simulation testing.

- [ ] **Step 4: Run verification test**
  Run: `python tests/test_plugin_verification.py`
  Expected: Passes mock portfolio and harness config checks.

- [ ] **Step 5: Commit**
  ```bash
  git add harnesses/ examples/
  git commit -m "feat: add multi-harness configurations and relocate mock portfolio to examples"
  ```

---

### Task 8: Codebase Clean-Up (Deprecation of Standalone Runner)

**Files:**
- Delete: `src/` directory
- Delete: `workflows/` directory
- Delete: `pyproject.toml`
- Delete: `data/` directory (now preserved in `examples/`)
- Delete: `reports/` directory (temporary test runs from previous iteration)
- Delete: `config/` directory (salvaged into skills)

**Interfaces:**
- Consumes: Workspace directories.
- Produces: Clean, pure AI Agent Plugin repository without standalone Python execution clutter.

- [ ] **Step 1: Remove obsolete standalone application artifacts**
  Safely delete `src/`, `workflows/`, `pyproject.toml`, `data/`, `config/`, and `reports/`.

- [ ] **Step 2: Verify git status is clean of legacy runtime code**
  Run: `git status`
  Expected: Only clean plugin files, `tests/`, `docs/`, `agents/`, `skills/`, `templates/`, `harnesses/`, and `examples/` remain.

- [ ] **Step 3: Commit**
  ```bash
  git add -A
  git commit -m "refactor: remove legacy standalone Python runtime artifacts and finalize plugin structure"
  ```

---

### Task 9: Documentation & Full Verification Suite Pass

**Files:**
- Create/Overwrite: `README.md`
- Verify: `tests/test_plugin_verification.py`

**Interfaces:**
- Consumes: Complete plugin files.
- Produces: End-to-end user guide and passing test suite.

- [ ] **Step 1: Write comprehensive `README.md`**
  Document:
  - Architecture overview and multi-tier market data hierarchy.
  - Setup instructions for Antigravity, Claude Desktop, and OpenClaw.
  - MCP configuration and authentication guide (Zerodha Kite, Groww, INDmoney, Obsidian API key).
  - Corporate action adjustment rules and advisory-only guardrails.
  - Example user prompts for portfolio audits, 5-pillar valuation, and mutual fund health checks.

- [ ] **Step 2: Run the full verification suite**
  Run: `python tests/test_plugin_verification.py`
  Expected: All checks PASS with exit code 0.

- [ ] **Step 3: Commit**
  ```bash
  git add README.md tests/test_plugin_verification.py
  git commit -m "docs: finalize user guide and complete plugin verification"
  ```

---

## Plan Self-Review Checklist

- [x] **Spec coverage**: Covers all requirements from design document: multi-broker ingestion with strict auth, 4-tier market data routing with fallbacks, corporate action price checks, token optimization, advisory-only guardrails, Obsidian memory, multi-harness manifests, and legacy code salvage.
- [x] **Step scan**: Every step specifies clear files, exact actions, expected outputs, and git commit commands.
- [x] **Type consistency**: Exact MCP server identifiers (`zerodha-kite`, `groww`, `indmoney`, `nse-cm-market`, `nse-bhavcopy`, `indian-market-mcp`, `dalalos`, `yfinance-mcp`, `alpha-vantage`, `obsidian`) are consistent across `mcp_config.json`, skills, agents, harnesses, and test suites.
- [x] **Review Focus**: Addressed broker session expiration, corporate action nominal plunge, execution tool prohibition, primary data fallback routing, and token optimization.
- [x] **Proportion**: Balanced task decomposition giving exact specifications without redundant transcripts.
