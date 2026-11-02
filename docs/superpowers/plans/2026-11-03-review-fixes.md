# Systematically Address Repository Review Gaps Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Systematically implement all architectural, configuration, guardrail, and data consistency fixes identified in the repository review (`docs/review.md`), adding SEC EDGAR and OpenBB MCP servers, fixing auth configurations, expanding the mock portfolio, instituting survivorship bias guardrails, reformatting the review report, and updating test verification.

**Architecture:** 
1. Reformat `docs/review.md` from an unformatted 25KB string into structured, clean GitHub-flavored Markdown.
2. Expand `examples/mock_portfolio.json` to include equities (with KAYNES), ETFs, Mutual Funds, and US Equities matching `README.md`.
3. Integrate `sec-edgar` and `openbb` MCP servers across all harnesses (`.mcp.json`, `mcp.json`, `mcp_config.json`, `plugin.json`, `plugin.yaml`, `harnesses/*`, `__init__.py`) and fix Alpha Vantage / DalalOS authentication headers.
4. Add mandatory Survivorship Bias guardrails and US filings workflows across `AGENTS.md`, `rules/AGENTS.md`, `CLAUDE.md`, agents, and skills.
5. Update and expand `tests/test_plugin_verification.py` to verify all additions and maintain 100% compliance.

**Tech Stack:** Python 3.10, JSON, YAML, Markdown, Model Context Protocol (MCP) v1.0.

**Spec:** `docs/review.md` and repository audit findings.

## Global Constraints
- Advisory-Only Mandate: Absolutely ZERO live order execution tools (`place_order`, `place_gtt_order`, `cancel_order`).
- Mandatory Broker Auth Gating: Never silently skip or mock authenticated broker sessions in live audits.
- Cash Delivery Equities, ETFs, Direct MFs, and INDmoney US Equities only (no F&O, intraday, margin).
- Corporate Action Price-Adjustment Safeguard must be preserved across sentinel workflows.
- All test assertions in `tests/test_plugin_verification.py` must pass.

## Review Focus
1. `mcpServers` keys in `.mcp.json`, `mcp_config.json`, and `mcp.json` must be strictly identical and include all 12 servers (`sec-edgar` and `openbb` included).
2. `examples/mock_portfolio.json` must preserve top-level `holdings` list for existing test compatibility while providing typed segments or metadata for equities, ETFs, MFs, and US stocks.
3. Survivorship bias guardrail must be explicitly present and verifiable by regex in `AGENTS.md`, `rules/AGENTS.md`, and relevant agent/skill files.
4. Alpha Vantage and DalalOS server configurations must declare proper auth headers/keys without leaking live credentials.
5. `tests/test_plugin_verification.py` must run and verify all 12 servers, templates, guardrails, and mock schemas cleanly.

---

### Task 1: Reformat `docs/review.md` into Structured Markdown

**Files:**
- Modify: `docs/review.md`

**Interfaces:**
- Produces: Clean, readable GitHub-flavored markdown with executive summary, MCP server evaluation, architectural analysis, survivorship bias analysis, and multi-tier fallback tables.

- [ ] **Step 1: Parse and format `docs/review.md`**
Read raw content of `docs/review.md` and format it with clear H1/H2/H3 headings, markdown comparison tables, bold highlights, bullet points, and code blocks.

- [ ] **Step 2: Verify `docs/review.md` formatting**
Ensure file is readable, contains no run-on walls of text, and accurately preserves all research findings and server details.

---

### Task 2: Synchronize and Enrich `examples/mock_portfolio.json`

**Files:**
- Modify: `examples/mock_portfolio.json`
- Test: `tests/test_plugin_verification.py:test_mock_portfolio_schema`

**Interfaces:**
- Consumes: Mock holdings documented in `README.md`.
- Produces: JSON structure with `holdings` array containing:
  - Indian Equities: RELIANCE, TCS, HDFCBANK, INFY, ICICIBANK, KOTAKBANK, LT, ITC, BHARTIARTL, SBIN, KAYNES.
  - Indian ETFs: NIFTYBEES, GOLDBEES, MON100.
  - Mutual Funds: PARAG_PARIKH_FLEXI_CAP (Scheme 122639), QUANT_SMALL_CAP (Scheme 120828), NIPPON_INDIA_SMALL_CAP (Scheme 118778).
  - US Equities (INDmoney): AAPL, MSFT, GOOGL, NVDA.

- [ ] **Step 1: Write enriched `examples/mock_portfolio.json`**
Structure holdings with `asset_type` (`equity`, `etf`, `mutual_fund`, `us_equity`), `symbol`, `name`, `isin` / `amfi_code`, `quantity`, `average_price`, `current_price`, and `broker` (`zerodha`, `groww`, `indmoney`).

- [ ] **Step 2: Verify JSON syntax and schema**
Ensure valid JSON, non-empty `holdings` list with all expected assets.

---

### Task 3: Add `sec-edgar` and `openbb` MCP Servers & Fix Auth across Manifests

**Files:**
- Modify: `.mcp.json`
- Modify: `mcp_config.json`
- Modify: `mcp.json`
- Modify: `plugin.json`
- Modify: `plugin.yaml`
- Modify: `harnesses/claude_desktop_config.json`
- Modify: `harnesses/openclaw_config.json`
- Modify: `harnesses/hermes_config.yaml`
- Modify: `__init__.py`

**Interfaces:**
- Consumes: MCP server configurations from review document.
- Produces: Consistent 12 MCP servers:
  1. `zerodha-kite`
  2. `groww`
  3. `indmoney`
  4. `nse-cm-market`
  5. `nse-bhavcopy`
  6. `indian-market-mcp`
  7. `dalalos`
  8. `yfinance-mcp`
  9. `alpha-vantage`
  10. `obsidian`
  11. `sec-edgar`
  12. `openbb`
- Produces: Correct auth headers for `alpha-vantage` (`apikey` param or `Authorization` header) and `dalalos` (`X-API-Key: ${DALALOS_API_KEY}`).

- [ ] **Step 1: Update `.mcp.json`, `mcp_config.json`, and `mcp.json`**
Add `sec-edgar` and `openbb`. Fix Alpha Vantage and DalalOS auth headers. Ensure strict key parity across all three files.

- [ ] **Step 2: Update `plugin.json` and `plugin.yaml`**
Register `sec-edgar` and `openbb` under server tools/capabilities.

- [ ] **Step 3: Update `harnesses/claude_desktop_config.json`, `harnesses/openclaw_config.json`, `harnesses/hermes_config.yaml`, and `__init__.py`**
Add the new servers and correct auth headers in Claude Desktop, OpenClaw, and Hermes configs.

---

### Task 4: Incorporate Survivorship Bias Guardrails & US Filing Workflows in Rules, Agents, and Skills

**Files:**
- Modify: `AGENTS.md` and `rules/AGENTS.md`
- Modify: `CLAUDE.md`
- Modify: `agents/portfolio_sentinel.md`
- Modify: `agents/fundamental_analyst.md`
- Modify: `agents/market_intel.md`
- Modify: `skills/portfolio-sentinel/SKILL.md`
- Modify: `skills/fundamental-valuation/SKILL.md`
- Modify: `skills/nse-corporate-filings/SKILL.md`

**Interfaces:**
- Produces:
  - Section 8 in `AGENTS.md` & `rules/AGENTS.md`: "Survivorship Bias & Historical Data Integrity Guardrails".
  - Multi-tier fallback table including `sec-edgar` and `openbb`.
  - US filings verification steps in `portfolio_sentinel` and `nse-corporate-filings` (now corporate filings).
  - Point-in-time constituent safeguards in `fundamental_analyst` and `market_intel`.

- [ ] **Step 1: Update `AGENTS.md` and `rules/AGENTS.md`**
Add rule Section 8 on Survivorship Bias and update the Multi-Tiered Market Data Fallback Protocol table.

- [ ] **Step 2: Update `CLAUDE.md` and `README.md`**
Update summary fallback tables and rule summaries.

- [ ] **Step 3: Update Agents (`portfolio_sentinel.md`, `fundamental_analyst.md`, `market_intel.md`)**
Bind `sec-edgar` and `openbb` to primary/fallback MCP lists. Add explicit survivorship bias guardrail instructions and US corporate filings checks.

- [ ] **Step 4: Update Skills (`skills/portfolio-sentinel/SKILL.md`, `skills/fundamental-valuation/SKILL.md`, `skills/nse-corporate-filings/SKILL.md`)**
Add instructions for handling US filings via `sec-edgar` and survivorship bias filtering in screening.

---

### Task 5: Update and Expand Automated Verification Test Suite

**Files:**
- Modify: `tests/test_plugin_verification.py`

**Interfaces:**
- Consumes: All updated configs, agents, skills, and mock portfolio.
- Produces: Test assertions for:
  - 12 required MCP servers (including `sec-edgar` and `openbb`).
  - Strict absence of live order execution tools.
  - Corporate action price adjustment checks.
  - Mandatory broker auth gate checks.
  - Survivorship bias guardrail presence across rules and agents.
  - Mock portfolio comprehensive schema (equities, ETFs, mutual funds, US equities).
  - Parity across `.mcp.json`, `mcp_config.json`, `mcp.json`, `claude_desktop_config.json`, and `openclaw_config.json`.

- [ ] **Step 1: Update `REQUIRED_MCP_SERVERS` in `tests/test_plugin_verification.py`**
Add `"sec-edgar"` and `"openbb"`.

- [ ] **Step 2: Add test `test_survivorship_bias_guardrail_enforcement`**
Verify that `AGENTS.md`, `rules/AGENTS.md`, and `fundamental_analyst.md` contain explicit survivorship bias guardrails.

- [ ] **Step 3: Add test `test_mock_portfolio_asset_diversity`**
Verify `examples/mock_portfolio.json` contains `equity`, `etf`, `mutual_fund`, and `us_equity`.

- [ ] **Step 4: Execute verification test suite and verify 100% pass**
Run test suite and confirm all tests pass.
