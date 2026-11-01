---
name: indian-fundamental-valuation
description: 5-Pillar Fundamental & Valuation analysis model for Indian stocks (NSE/BSE), adapting Buffett-style moat, FCF, DCF, PEG, and margin-of-safety principles.
---

# Indian Fundamental Valuation Skill

## Purpose
Executes a rigorous 5-pillar fundamental analysis on any Indian listed stock (NSE/BSE) to establish whether a company qualifies as a durable long-term compounder, determine intrinsic value via DCF, and compute optimal accumulation price zones.

## The 5 Pillars

```mermaid
flowchart TD
    A["Stock Ticker (NSE/BSE)"] --> B["1. Moat & Quality (ROE > 15%, ROCE > 18%, Low Debt)"]
    A --> C["2. Free Cash Flow (CFO/PAT > 0.8, Positive FCF Yield)"]
    A --> D["3. PEG & Growth (3-5 Yr CAGR > 15%, PEG < 1.5)"]
    A --> E["4. DCF Valuation (India WACC 11-13%, Terminal 5-6%)"]
    A --> F["5. Margin of Safety & Entry (52w range, 5-Yr Median P/E)"]
    B --> G["Synthesis & Final Recommendation"]
    C --> G
    D --> G
    E --> G
    F --> G
```

## Step-by-Step Procedure

1. **Step 1: Retrieve Financial Statements & Ratios**
   - Query `indian-market-mcp:get_financial_ratios` (ROE, ROCE, P/E, P/B, Debt-to-Equity).
   - Query `indian-market-mcp:get_cash_flow` (Cash from Operations, Capital Expenditure, Free Cash Flow).
   - Query `indian-market-mcp:get_historical_data` (Past 3-5 years price and P/E history).

2. **Step 2: Score Business Moat & Capital Efficiency**
   - Verify 3-year average ROE >= 15% and ROCE >= 18%.
   - Check Net Debt / Equity <= 0.5 (or Tier 1 CRAR >= 15% for BFSI).
   - Evaluate working capital days and cash conversion cycle.

3. **Step 3: Free Cash Flow Quality Check**
   - Calculate `CFO / PAT`. If < 0.8 consistently, flag potential revenue recognition issues or aggressive accounting.
   - Calculate Free Cash Flow = `Operating Cash Flow - CapEx`.

4. **Step 4: DCF & PEG Valuation Modeling**
   - Apply Indian Discount Rate ($WACC = 11.5\% - 12.5\%$).
   - Apply Terminal Growth Rate ($g = 5.0\% - 5.5\%$).
   - Compute DCF intrinsic per share value.
   - Compare with current market price to derive Margin of Safety percentage.

5. **Step 5: Output Research Memo**
   - Generate formatted investment memo with clear accumulation range and stop-loss/invalidation thesis.
