---
name: mf-etf-health-check
description: Mutual Fund and ETF portfolio health analyzer, tracking manager changes, expense ratios, category performance, tracking error, and stock overlap.
---

# Mutual Fund & ETF Health Check Skill

## Purpose
Monitors the user's non-direct-equity holdings (Mutual Funds and ETFs held in Groww, Zerodha Coin / Kite, and INDmoney) to detect degradation in fund management quality, hidden risk concentration, and tracking errors.

## What it Monitors

### 1. Mutual Funds (Held via Groww / INDmoney / Zerodha Coin)
- **Fund Manager Turnover**: Alert if the lead fund manager departs or is replaced.
- **AUM Bloat in Mid & Small Cap Funds**: Rapid AUM growth that forces fund managers into large-cap cash parking or illiquidity.
- **Rolling Returns vs Category Benchmark**: Underperforming the category median over trailing 1-year and 3-year periods.
- **Expense Ratio Creep**: Incremental hikes in Direct Plan Total Expense Ratio (TER).
- **Portfolio Overlap**: Measuring overlap across funds (e.g., overlapping flexicap and large & midcap holdings) to avoid duplicate risk.

### 2. ETFs (NIFTYBEES, GOLDBEES, JUNIORBEES, BANKBEES, etc.)
- **Tracking Error & Difference**: Difference between ETF NAV return and underlying index return over 12 months.
- **Liquidity & Impact Cost**: Bid-ask spread on NSE/BSE to ensure clean exit capability.
- **Premium/Discount to iNAV**: Whether ETF is trading at significant divergence to real-time indicative NAV.

## Standard Output Format
```markdown
### 📈 MF / ETF Health Assessment
- **Scheme Name**: [Scheme Name]
- **Category**: [Flexicap / Smallcap / Index ETF / Gold ETF]
- **Broker Account**: [Groww / Zerodha / INDmoney]
- **Fund Manager**: [Current Name] (Tenure: [X] years)
- **1-Yr Alpha vs Category**: [+/-X%]
- **Expense Ratio (TER)**: [X%]
- **Overlap with other held funds**: [X%] (Key common stocks: [Stock A, Stock B])
- **Health Rating**: [EXCELLENT | WATCHLIST | UNDERPERFORMING]
- **Action**: [Continue SIP | Pause SIP | Switch Scheme]
```
