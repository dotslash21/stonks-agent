---
scheme_code: "{{scheme_code}}"
scheme_name: "{{scheme_name}}"
amc: "{{amc}}"
category: "{{category}}"
nav: 0.00
expense_ratio: 0.00
fund_manager: "{{fund_manager}}"
review_date: "{{review_date}}"
---

# Mutual Fund & ETF Health Audit: {{scheme_name}}

> **AMC**: {{amc}} | **Category**: {{category}}  
> **AMFI Scheme Code**: {{scheme_code}} | **Latest NAV**: ₹{{nav}}  
> **Direct Plan TER**: {{expense_ratio}}% | **Fund Manager**: {{fund_manager}}  
> **Audit Date**: {{review_date}}

---

## 1. Performance vs Category & Benchmark (Rolling Returns, Alpha, Beta)

| Time Horizon | Scheme Return | Category Average | Benchmark TRI Return | Excess Return (Alpha) | Tracking Error (ETFs) |
|---|---|---|---|---|---|
| **1-Year Trailing** | {{ret_1y}}% | {{cat_1y}}% | {{bench_1y}}% | {{alpha_1y}}% | {{te_1y}}% |
| **3-Year Rolling** | {{ret_3y}}% | {{cat_3y}}% | {{bench_3y}}% | {{alpha_3y}}% | {{te_3y}}% |
| **5-Year Rolling** | {{ret_5y}}% | {{cat_5y}}% | {{bench_5y}}% | {{alpha_5y}}% | {{te_5y}}% |

- **Benchmark Total Return Index (TRI)**: {{benchmark_index_name}}
- **Beta vs Category**: {{beta_value}} (Sensitivity relative to market benchmark movements)
- **Consistency Score**: {{consistency_score}} / 100 (% of 3-year rolling periods outperforming benchmark)

---

## 2. Risk-Adjusted Metrics (Sharpe, Sortino, Downside Capture)

| Metric | Scheme Value | Category Median | Interpretation |
|---|---|---|---|
| **Standard Deviation ($\sigma$)** | {{std_dev}}% | {{cat_std_dev}}% | Total volatility of scheme returns. |
| **Sharpe Ratio** | {{sharpe_ratio}} | {{cat_sharpe}} | Excess return per unit of total risk above 91-day T-Bill ($R_f \approx 6.5\%$). |
| **Sortino Ratio** | {{sortino_ratio}} | {{cat_sortino}} | Excess return per unit of bad (downside) volatility. |
| **Downside Capture Ratio** | {{downside_capture}}% | $< 85\%$ | Percentage of benchmark market decline absorbed during corrections. |
| **Upside Capture Ratio** | {{upside_capture}}% | $> 100\%$ | Percentage of benchmark market rally captured during bull phases. |

---

## 3. Portfolio Concentration & Top 10 Holdings

| # | Holding / Security | Sector | Weight (%) | Moat / Assessment |
|:---:|---|---|---|---|
| 1 | {{holding_1}} | {{sector_1}} | {{weight_1}}% | Tier-1 Core Compounder |
| 2 | {{holding_2}} | {{sector_2}} | {{weight_2}}% | Core Compounder |
| 3 | {{holding_3}} | {{sector_3}} | {{weight_3}}% | Growth Leader |
| 4 | {{holding_4}} | {{sector_4}} | {{weight_4}}% | Value / Cyclical |
| 5 | {{holding_5}} | {{sector_5}} | {{weight_5}}% | High RoCE Niche |
| 6 | {{holding_6}} | {{sector_6}} | {{weight_6}}% | Diversified Holding |
| 7 | {{holding_7}} | {{sector_7}} | {{weight_7}}% | Growth Midcap |
| 8 | {{holding_8}} | {{sector_8}} | {{weight_8}}% | Secular Tailwind |
| 9 | {{holding_9}} | {{sector_9}} | {{weight_9}}% | Financials |
| 10 | {{holding_10}} | {{sector_10}} | {{weight_10}}% | Defensive Buffer |

- **Top 10 Concentration Ratio**: {{top10_weight}}% (Threshold: Flag if $> 55\%$ in diversified equity funds).
- **Cash & Arbitrage Buffer**: {{cash_pct}}% (Threshold: Flag if $> 12\%$ during strong market conditions).
- **Total Number of Stocks**: {{num_stocks}}

---

## 4. Expense Ratio & AUM Health Watch

- **Direct Plan Total Expense Ratio (TER)**: {{expense_ratio}}%
- **TER Trend (12 Months)**: {{ter_trend}} (Alert if crept upward by $> 15-20$ bps without AUM contraction).
- **Total AUM**: ₹{{total_aum}} Crores
- **AUM Velocity / Bloat Analysis**:
  - Small/Mid-cap fund capacity check: Flag if small-cap AUM exceeds ₹25,000 Cr causing deployment friction or involuntary large-cap migration.
  - Liquidity profile: Liquidity days required to liquidate 20% and 50% of the underlying portfolio under SEBI stress test guidelines: {{liquidation_days}} days.

---

## 5. Fund Manager Tenure & Pedigree

- **Lead Fund Manager**: {{fund_manager}}
- **Tenure with Scheme**: {{manager_tenure}} years
- **Co-Manager(s)**: {{co_managers}}
- **Investment Philosophy & Style Consistency**:
  - Style Box: [ ] Large-Cap Blend [ ] Mid-Cap Growth [ ] Multi-Cap Value [ ] Global Diversified
  - Turnover Ratio: {{turnover_ratio}}% (High turnover $> 80\%$ vs low turnover $< 25\%$)
  - Manager Continuity Check: No sudden or unplanned lead manager resignation detected.

---

## 6. Advisory Status & Recommendations

> [!NOTE]
> All recommendations below are strictly advisory qualitative research outputs. **No live order placement tools** or automated transactions are triggered.

- **Overall Fund Health Rating**: `[ EXCELLENT | HEALTHY | WATCHLIST | REBALANCE_CANDIDATE ]`
- **Current Allocation Recommendation**:
  - [ ] **Continue SIP**: Fund exhibits healthy alpha, stable expense ratio, and disciplined style execution.
  - [ ] **Pause SIP / Hold Existing Units**: Fund experiencing temporary manager transition or elevated cash drag; monitor next 2 quarters.
  - [ ] **Switch / Reallocate**: Persistent rolling underperformance vs benchmark TRI over 4 consecutive quarters or unaddressed AUM bloat.
- **Actionable Investor Steps**:
  1. Maintain scheduled direct SIP installments.
  2. Review cross-fund portfolio overlap against complementary portfolio holdings.
