# CLAUDE.md — Stonks Agent Plugin Instructions

## Project Overview
**stonks-agent** is an institutional-grade, multi-agent intelligence plugin designed for Indian capital market investors (NSE/BSE cash delivery equities, ETFs, and AMFI direct mutual funds across Zerodha Kite, Groww, and INDmoney).

## 🛡️ Critical Safety Mandate (100% Advisory-Only)
- **Zero Live Execution**: Live automated order placement, modification, or cancellation (`place_order`, `place_gtt`, `cancel_order`, etc.) is strictly forbidden.
- **Human-in-the-Loop**: All outputs are formatted as structured advisory cards for the investor to manually inspect and execute in their broker portal.
- **Zero F&O / Zero Day Trading**: Strictly delivery equities and direct mutual funds only. No derivatives, intraday leverage, or scalping.
- **Mandatory Corporate Action Verification**: Always verify corporate actions (splits, bonuses, demergers) via `get_corporate_actions` before raising price plunge or stop-loss alerts.

## MCP Configuration (.mcp.json)
This repository defines 10 MCP servers in `.mcp.json` automatically loaded by Claude Code:
1. `zerodha-kite`: User holdings, positions, margins (read-only).
2. `groww`: Direct equity & MF portfolio holdings.
3. `indmoney`: Consolidated Indian stocks, US stocks, and CAMS/KFintech MFs.
4. `nse-cm-market`: Official NSE live capital market quotes and market breadth.
5. `nse-bhavcopy`: Official NSE 5-year historical EOD prices and delivery volumes.
6. `indian-market-mcp`: 47,000+ AMFI schemes, NAV, SIP XIRR, and FII/DII institutional flows.
7. `dalalos`: Forensic BSE-XBRL filings, capex disclosures, and shareholding pledge audits.
8. `yfinance-mcp`: Universal unauthenticated fallback quotes (`.NS`/`.BO`) and WebP charts.
9. `alpha-vantage`: Server-side technical indicators (RSI, MACD, Bollinger Bands).
10. `obsidian`: Local investment research memory via Obsidian Local REST API.

## Available Skills
- `skills/portfolio-sentinel/SKILL.md`: Early warning risk radar, corporate actions, and SEBI LODR disclosures.
- `skills/fundamental-valuation/SKILL.md`: 5-Pillar Buffett/Duan fundamental valuation and 2-stage DCF model.
- `skills/nse-corporate-filings/SKILL.md`: SEBI LODR Reg 30 disclosures, insider trades, and forensic XBRL audits.
- `skills/mf-etf-health-check/SKILL.md`: AMFI scheme analytics, tracking error, TER creep, and AUM bloat audits.
- `skills/obsidian-portfolio-memory/SKILL.md`: Investment theses, risk alerts, and review notes in Obsidian.

## Operating Guidelines & Testing
- Read `AGENTS.md` for full universal rules and multi-tier data routing fallback hierarchy.
- Run tests: `.venv\Scripts\python -m unittest discover tests` (or `python -m unittest discover tests`).
- Ensure all environment variables (`ZERODHA_ACCESS_TOKEN`, `GROWW_AUTH_TOKEN`, `INDMONEY_API_TOKEN`, `ALPHA_VANTAGE_API_KEY`, `OBSIDIAN_API_KEY`, `OBSIDIAN_VAULT_PATH`) are set before running authenticated audits.
