---
name: indian-portfolio-sentinel
description: Early warning radar and adverse event monitor for Indian stock, ETF, and mutual fund portfolios across Zerodha Kite, Groww, and INDmoney.
---

# Indian Portfolio Sentinel Skill

## Purpose
Monitors user's held assets across Zerodha Kite, Groww, and INDmoney against live market news, NSE/BSE corporate filings, quarterly results, credit rating revisions, and technical breakdown levels. Alerts the investor to potential adverse developments before capital loss escalates.

## When to Run
- **Pre-Market (8:30 AM IST)**: Scan overnight corporate disclosures, global cues, and earnings announcements from the previous evening.
- **Mid-Market / Real-Time**: Triggered when a breaking headline, exchange notice, or severe price swing (>4% drop) hits any held ticker.
- **Post-Market (4:00 PM IST)**: Review daily corporate announcements, board meeting outcomes, and institutional bulk/block deals.

## Step-by-Step Procedure

1. **Step 1: Fetch Consolidated Portfolio**
   - Connect to `zerodha-kite`, `groww-portfolio`, and `indmoney-portfolio` MCP servers (or local cached portfolio).
   - Extract unique NSE/BSE symbols, ISINs, asset classes (Direct Stock, ETF, Mutual Fund), and position sizes.

2. **Step 2: Query Market Intelligence & Filings**
   - Call `indian-market-mcp:get_corporate_announcements` filtered for held symbols.
   - Call `nse-filings-scanner:get_board_meetings` and `get_insider_trading_disclosures`.
   - Run financial news scan (Moneycontrol, Economic Times, Livemint RSS) for adverse keyword matches:
     `["downgrade", "fraud", "auditor", "resigned", "raid", "penalty", "sebi", "missed", "default", "pledge"]`.

3. **Step 3: Evaluate Technical Guardrails**
   - Call `indian-market-mcp:get_technical_indicators` (200 EMA, 50 EMA, RSI 14, Supertrend).
   - Check if any positional holding closed below its 200 EMA with above-average volume.

4. **Step 4: Classify Adverse Events & Generate Action Plan**
   - Categorize by severity:
     - `CRITICAL`: Auditor resignation, forensic probe, promoter pledge >30%, debt default.
     - `HIGH`: CEO/CFO abrupt departure, massive earnings miss, 200 EMA breakdown.
     - `MEDIUM`: Margin compression, sector tax headwind, ASM/GSM surveillance entry.
     - `LOW`: Routine corporate action or minor broker target downgrade.
   - Emit structured warning markdown report and trigger configured alerts (Console / Telegram / Discord).
