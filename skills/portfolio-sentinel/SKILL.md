---
name: portfolio-sentinel
description: Monitors equity and ETF holdings for negative market events, corporate filings, and trend breakdowns.
---

# Indian Portfolio Sentinel Skill

## Purpose
The **Indian Portfolio Sentinel** skill provides automated early warning surveillance and adverse event monitoring across Indian equities, ETFs, and mutual funds held in Zerodha Kite, Groww, and INDmoney. It continuously tracks holdings against live market feeds, official exchange filings under SEBI LODR/PIT, credit rating actions, and technical breakdown levels to protect investor capital before adverse developments escalate.

## Multi-Tier Data Routing Table
To ensure reliable operation during market hours and off-market scans, data queries follow a deterministic routing hierarchy:

| Data Requirement | Primary Feed | Fallback Tier 1 | Fallback Tier 2 |
|---|---|---|---|
| **Live / EOD Quotes & OHLCV** | NSE Live CM (`nse-cm-market`) / NSE Bhavcopy (`nse-bhavcopy`) | `indian-market-mcp:get_quote` | `yfinance-mcp:yfinance_get_historical_data` (`.NS` / `.BO`) |
| **Technical Indicators (EMA, RSI)** | `indian-market-mcp:get_technical_indicators` | Calculated from `nse-bhavcopy` history | Calculated from `yfinance-mcp:yfinance_get_historical_data` |
| **Corporate Disclosures (Indian LODR Reg 30)** | NSE Live CM (`nse-cm-market:get_announcements`) | `dalalos:get_regulatory_filings` | `indian-market-mcp:get_corporate_announcements` |
| **Corporate Disclosures (US 8-K / 10-K / 10-Q)** | `sec-edgar` (Authoritative XBRL filings) | `yfinance-mcp:yfinance_get_news` | SEC EDGAR portal |
| **Corporate Actions (Split, Bonus, Div)** | `indian-market-mcp:get_corporate_actions` | `dalalos:get_corporate_actions` | `yfinance-mcp:yfinance_get_historical_data` (actions lookback) |
| **Financial Media & News Flow** | `indian-market-mcp:get_news` | `yfinance-mcp:yfinance_get_news` | — |

## Corporate Action Adjustment Rule
> [!IMPORTANT]
> **Mandatory Corporate Action Verification Protocol**:
> Before flagging any nominal price plunge (>20% drop or sharp gap-down) as a critical technical breakdown, stop-loss violation, or adverse panic event, the sentinel MUST verify corporate action registries (`get_corporate_actions` or DalalOS XBRL / exchange announcements) for stock splits, bonus share distributions, rights issues, and demergers on the ex-date.
>
> 1. **Check Ex-Date Timing**: Query `get_corporate_actions` via `indian-market-mcp` or `dalalos` for the target symbol. Confirm whether the current session is on or within 2 trading sessions of the announced ex-date.
> 2. **Calculate Adjusted Price & Ratio**:
>    - **Stock Split** (e.g., 10:1 split): Adjusted benchmark price = $\text{Pre-Split Price} / 10$; expected holdings multiplier $= 10\times$.
>    - **Bonus Issue** (e.g., 1:1 bonus): Adjusted benchmark price = $\text{Pre-Bonus Price} / 2$; expected holdings multiplier $= 2\times$.
>    - **Demerger / Spin-off**: Check cost of acquisition apportionment ratio and track spun-off entity pending separate listing.
> 3. **Suppress False-Positive Alarms**: If the nominal price drop matches the announced corporate action ratio on the ex-date, classify the movement as an **Expected Corporate Action Adjustment**. Update the portfolio's adjusted purchase price and share count, and suppress all adverse panic alerts.

## Risk Classification & Threshold Triggers
Holding events are ranked across four severity tiers salvaged from `config/risk_rules.json` and `src/analyzers/adverse_event_analyzer.py`:

### 1. Critical Severity (Immediate Alert & Capital Preservation Review)
- **Auditor Resignation**: Statutory auditor resigns before term completion without satisfactory explanation.
- **Forensic Audit**: Forensic investigation ordered by SEBI, the Ministry of Corporate Affairs (MCA), or lenders.
- **Credit Rating Downgrade**: Credit rating downgraded by 2 or more notches, or reduced into speculative/default grade (CRISIL, ICRA, CARE, India Ratings).
- **High Promoter Pledge**: Promoter share pledging exceeding 25% of total promoter holding (or sudden pledge creation > 5%).
- **Earnings Plunge**: Quarterly net profit decline > 35% YoY without prior management guidance or cyclical industry explanation.
- **Debt Default**: Default or delayed servicing of commercial paper (CP), bond/NCD coupon, or bank loan covenants.
- **Sentinel Action**: Trigger immediate high-priority alert; prompt user for capital preservation and thesis review.

### 2. High Severity (Alert & Thesis Review)
- **KMP Resignation**: Abrupt departure or termination of CEO, Managing Director, or Chief Financial Officer.
- **Material Litigation / Tax Demand**: Disputed tax demand, fine, or legal claim exceeding 5% of net worth.
- **SEBI Surveillance**: Stock included in Additional Surveillance Measure (ASM) or Graded Surveillance Measure (GSM) frameworks.
- **200 EMA Breakdown**: Positional holding daily closing price breaks below the 200-day Exponential Moving Average (EMA) with $>2\times$ 20-day average volume, indicating institutional distribution.
- **Momentum Breakdown**: RSI (14) dropping below 30 under heavy selling volume.
- **Star Fund Manager Exit**: Departure of lead mutual fund manager with $>3$-year successful track record.
- **MF AUM Bloat / Cash Drag**: Mutual fund category AUM ballooning causing involuntary cash/arbitrage parking $> 12\%$.
- **Sentinel Action**: Request investor thesis review; advise tightening trailing stop-loss (standard 8% threshold).

### 3. Medium Severity (Weekly Memo & Allocation Pause)
- **Margin Contraction**: Quarterly EBITDA margin compression $> 200$ bps driven by raw material inflation or pricing weakness.
- **Policy Headwinds**: Sudden regulatory interventions (windfall taxes, export duties, anti-dumping duty repeals, tariff adjustments).
- **Promoter Stake Dilution**: Open-market promoter stake sales $> 2\%$ without clear succession or debt repayment rationale.
- **Short-Term Trend Breakdown**: Daily close below 50-day EMA for short-term swing holdings.
- **TER Creep**: Mutual fund direct plan Total Expense Ratio (TER) increased by $> 15-20$ bps without asset base justification.
- **Sentinel Action**: Log to weekly portfolio memo; recommend holding existing units while pausing fresh SIPs or additions.

### 4. Low Severity (Informational Monitor)
- **Broker Target Adjustments**: Minor target price revisions without downgrade in rating.
- **Routine Corporate Updates**: Non-material contract completions, commercial lease updates, participation in investor conferences.
- **Defensive Cash Buffer**: Mutual fund manager temporarily allocating 10-15% in cash/arbitrage to navigate frothy broad market valuations.
- **Sentinel Action**: Record in audit log; no active investor intervention required.

## Technical Guardrails
- **Positional Holdings**:
  - Primary Trend Support: 200 EMA.
  - Intermediate Trend Momentum: 50 EMA.
  - Trailing Stop-Loss: 8.0% from swing high.
  - RSI Overbought Warning: RSI (14) $\ge 78$.
  - RSI Oversold Support: RSI (14) $\le 32$.
- **Long-Term Compounders**:
  - Trend Gauge: 200 EMA.
  - Dip Accumulation Zone: 15.0% below 52-week high.
  - Deep Value Accumulation Zone: 25.0% below 52-week high.

## Execution Workflow
1. **Fetch Holdings**: Retrieve unified portfolio symbols, quantities, and asset classes from active broker sessions or local cache.
2. **Scan Corporate Actions**: Run `get_corporate_actions` for all symbols experiencing nominal price drops $>20\%$ to verify split, bonus, or demerger ex-dates.
3. **Query Market Data**: Execute multi-tier routing (NSE CM / Bhavcopy $\rightarrow$ `indian-market-mcp` $\rightarrow$ `yfinance-mcp`) to obtain latest quotes and technical indicators (200 EMA, 50 EMA, RSI 14).
4. **Scan Filings & News**: Ingest regulatory disclosures under SEBI LODR Regulation 30 and adverse news headlines.
5. **Score & Rank**: Classify all detected events into Critical, High, Medium, or Low severity.
6. **Deliver Advisory Report**: Publish structured markdown summary highlighting verified risks, corporate action notes, and recommended portfolio adjustments.

## Strictly Advisory Guardrails
- **Anti-Goal**: Live order placement tools (such as place_order, place_gtt_order, or cancel_order) are forbidden and strictly prohibited.
- **Advisory Only**: All outputs are research observations and early warning alerts. No automated trade execution is permitted; all investment decisions remain solely with the human investor.
