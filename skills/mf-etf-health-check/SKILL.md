---
name: mf-etf-health-check
description: Monitors direct mutual fund schemes and ETFs for star manager departures, AUM bloat, expense ratio creep, and tracking errors.
---

# Mutual Fund & ETF Health Check Skill

## Purpose
The **Mutual Fund & ETF Health Check** skill provides institutional-grade surveillance and diagnostics for direct Mutual Fund schemes (Growth plans) and Exchange Traded Funds (ETFs) held across Zerodha Coin / Kite, Groww, and INDmoney. It monitors fund manager continuity, AUM bloat, expense ratio creep, tracking errors, style drift, cash drag, and hidden cross-fund portfolio overlap to maintain an optimal passive and semi-passive asset allocation.

## AMFI Scheme Lookup & Quantitative Analytics
The skill leverages the Association of Mutual Funds in India (AMFI) database via `indian-market-mcp` covering over 47,000+ active and historical mutual fund schemes:

### 1. Rolling Return Benchmarking
- **Trailing & Rolling Windows**: Computes 1-year, 3-year, and 5-year rolling returns from daily NAV histories.
- **Benchmark TRI Indices**: Evaluates performance against official Total Return Indices (TRI):
  - Large Cap: Nifty 50 TRI / S&P BSE Sensex TRI
  - Flexi Cap / Large & Mid Cap: Nifty 500 TRI / Nifty LargeMidcap 250 TRI
  - Mid Cap: Nifty Midcap 150 TRI
  - Small Cap: Nifty Smallcap 250 TRI

### 2. Risk-Adjusted Return Metrics
- **Sharpe Ratio**:
  $$\text{Sharpe} = \frac{R_p - R_f}{\sigma_p}$$
  Evaluates excess return per unit of total risk against the 91-day Indian Treasury Bill risk-free rate ($R_f \approx 6.5\%$).
- **Sortino Ratio**: Evaluates excess return against downside semi-deviation, penalizing only negative return volatility.
- **Beta & Standard Deviation**: Assesses scheme volatility and sensitivity relative to category benchmark indices.
- **SIP XIRR Calculation**: Computes the exact annualized internal rate of return (XIRR) across periodic SIP installment dates and portfolio cash flows.

## Fund Look-Through via `yfinance-mcp`
Using `yfinance-mcp` fund analytics (`yfinance_get_fund_data`), the skill performs granular look-through on ETFs and fund holdings:
1. **Top Holdings Concentration**: Identifies top 10 single-stock weights (flags any single stock weight $> 10\%$ in non-thematic diversified funds).
2. **Sector Weight Breakdown**: Decomposes sector exposures to prevent hidden macroeconomic concentration (e.g., combined Financial Services exposure exceeding 35%).
3. **Morningstar Style Box**: Maps underlying asset distribution across market cap (Large / Mid / Small) and investment style (Value / Blend / Growth).
4. **Cash Drag Audit**: Measures cash and cash-equivalent holdings. Flags funds holding $> 10-12\%$ cash during strong bull markets, leading to structural underperformance.

## Surveillance Thresholds & Alert Triggers
The health check flags schemes that violate the following calibrated thresholds:

| Metric / Trigger | Safe Threshold | Alert Trigger Level | Recommended Action |
|---|---|---|---|
| **ETF Tracking Error** | $\le 0.25\%$ | $> 0.50\%$ annualized | Audit ETF liquidity; consider index fund alternative |
| **Expense Ratio (TER) Creep** | Stable or falling | Increased by $> 20$ bps YoY | Check AMC justification; evaluate lower TER peers |
| **Lead Fund Manager Turnover** | Stable ($>3$ yr tenure) | Star manager departure or replacement | Place fund on 6-month observation watchlist |
| **Small-Cap AUM Bloat** | AUM $< ₹20,000$ Cr | AUM $> ₹25,000$ Cr with cash $> 12\%$ | Pause fresh SIPs; redirect to less bloated schemes |
| **ETF iNAV Divergence** | Premium/discount $\le 0.5\%$ | Divergence $> 1.0\%$ from real-time iNAV | Avoid market orders; use limit orders near iNAV |
| **Portfolio Overlap** | Overlap $< 30\%$ | Overlap $> 40\%$ between two held funds | Consolidate duplicate schemes into single best-in-class |
| **Rolling Alpha Underperformance** | Alpha $\ge 0\%$ vs TRI | Negative alpha for 4 consecutive quarters | Review fund investment process and style suitability |

## Multi-Tier Data Routing Table
To maintain continuous analytics across volatile trading sessions, data requests route through a multi-tier hierarchy:

| Fund Data Requirement | Primary Feed | Fallback Tier 1 | Fallback Tier 2 |
|---|---|---|---|
| **AMFI NAV & Scheme Database** | `indian-market-mcp:get_mutual_fund_nav` | AMFI Official Portal (`amfiindia.com`) | `yfinance-mcp:yfinance_get_quote` |
| **ETF Live Price & Market Depth** | NSE Live CM (`nse-cm-market:get_quote`) | NSE Bhavcopy (`nse-bhavcopy`) | `indian-market-mcp:get_quote` |
| **Fund Look-Through & Style Box** | `yfinance-mcp:yfinance_get_fund_data` | `indian-market-mcp:get_fund_holdings` | Fund Factsheet Disclosures |
| **Rolling Returns & Benchmarks** | `indian-market-mcp:get_historical_nav` | Calculated from historical AMFI NAVs | `yfinance-mcp:yfinance_get_historical_data` |

## Standard Output Format
The skill outputs structured markdown assessment cards:

```markdown
### 📈 Mutual Fund / ETF Health Assessment

- **Scheme Name**: Parag Parikh Flexi Cap Fund - Direct Plan - Growth
- **AMFI Scheme Code**: 122639
- **Category**: Equity - Flexi Cap Fund
- **AUM**: ₹72,400 Cr (Cash / Arbitrage Buffer: 14.2%)
- **Fund Manager**: Rajeev Thakkar (Tenure: 11+ years)
- **3-Year Rolling Alpha vs Nifty 500 TRI**: +3.8%
- **Direct Plan TER**: 0.63% (TER change trailing 12m: 0 bps)
- **Sharpe Ratio**: 1.42 | **Sortino Ratio**: 2.15
- **Style Box**: Large-Cap Blend with Global Diversification
- **Portfolio Overlap**: 24% overlap with Mirae Asset Large & Midcap Fund
- **Health Rating**: EXCELLENT
- **Advisory Recommendation**: Continue existing SIP; cash buffer is a disciplined risk mitigation in elevated market conditions.
```

## Strictly Advisory Guardrails
- **Anti-Goal**: Live order placement tools (such as place_order, place_gtt_order, or cancel_order) are forbidden and strictly prohibited.
- **Advisory Only**: All outputs are research assessments, fund diagnostics, and rebalancing recommendations. No automated order placement occurs; all investment execution decisions remain solely with the human investor.
