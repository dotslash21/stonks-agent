---
incident_id: "{{incident_id}}"
date: "{{date}}"
symbol: "{{symbol}}"
severity: "{{severity}}"
status: "{{status}}"
---

# Risk Incident Journal: {{symbol}} ({{date}})

> **Incident ID**: {{incident_id}} | **Date Logged**: {{date}}  
> **Security Symbol**: {{symbol}} | **Assigned Severity**: `{{severity}}` (CRITICAL / HIGH / MEDIUM / LOW)  
> **Resolution Status**: `{{status}}` (OPEN / INVESTIGATING / VERIFIED_FALSE_POSITIVE / RESOLVED)

---

## 1. Incident Overview & Summary
- **Anomaly Description**: Concisely describe the anomalous market price movement, corporate filing alert, or credit event detected.
- **Immediate Detection Trigger**: Nominal price movement (e.g., -24.5% intraday drop), circuit limit breach, statutory auditor resignation filing, or sudden credit downgrade.
- **Initial Sentinel Action**: Portfolio Sentinel initiated immediate surveillance check and halted false-positive alarm triggers pending corporate action verification.

---

## 2. Triggering MCP Source & Metric (NSE Bhavcopy / Live CM / DalalOS / AMFI)

| Dimension | Primary Observation | Supporting Tool / MCP Source | Verification Details |
|---|---|---|---|
| **Market Price / OHLCV** | Close: ₹{{current_price}} ({{pct_change}}%) | `nse-cm-market` / `nse-bhavcopy` | Verified against official exchange trade book. |
| **Volume & Delivery** | Volume: {{volume}} ({{vol_multiple}}x 20DMA) | `nse-bhavcopy:get_historical_bhavcopy` | High-volume distribution vs low-liquidity slippage. |
| **Regulatory / Filings** | Announcement: {{filing_title}} | `dalalos:get_regulatory_filings` | BSE/NSE LODR Regulation 30 disclosure feed. |
| **Corporate Actions** | Ex-Date Check: {{corporate_action_type}} | `indian-market-mcp:get_corporate_actions` | Official ex-date split, bonus, or demerger registry. |
| **Technical Breakdowns** | Level: Below 200 EMA (₹{{ema_200}}) | `alpha-vantage` / `indian-market-mcp` | Daily close breakdown below primary trend support. |

---

## 3. Corporate Action Verification Status (Ex-date split/bonus verified?)
> [!IMPORTANT]
> **Mandatory Corporate Action Verification Protocol**:
> All nominal price drops exceeding 20% must be validated against official corporate action records before treating the move as an adverse capital loss.

- **Corporate Action Query Executed**: `indian-market-mcp:get_corporate_actions` / `dalalos:get_corporate_actions`
- **Ex-Date Matching**:
  - [ ] **Confirmed Corporate Action**: Today is within $\pm 2$ trading sessions of the announced ex-date for:
    - Type: `[ STOCK_SPLIT | BONUS_ISSUE | DEMERGER | RIGHTS_ISSUE | SPECIAL_DIVIDEND ]`
    - Announced Ratio: `{{ca_ratio}}` (e.g., 10:1 split, 1:1 bonus)
    - Theoretical Adjusted Price: ₹{{adjusted_ref_price}}
    - Nominal Drop Explained: **YES (False-Positive Alert Suppressed)**
  - [ ] **No Corporate Action Identified**: True adverse market shock or institutional liquidation event.

---

## 4. Portfolio Exposure & Capital at Risk

- **Portfolio Account(s)**: Zerodha Kite / Groww / INDmoney
- **Quantity Held**: {{quantity_held}} shares / units
- **Average Purchase Price**: ₹{{avg_buy_price}}
- **Current Position Value**: ₹{{current_value}}
- **Total Portfolio Weight**: {{portfolio_weight}}%
- **Unrealized P&L Impact**: ₹{{unrealized_pnl}} ({{unrealized_pnl_pct}}%)
- **Max Capital at Risk (to Stop-Loss)**: ₹{{capital_at_risk}}

---

## 5. Forensic / Fundamental Assessment

- **Forensic Check Results (via DalalOS / MCA / BSE-XBRL)**:
  - Auditor integrity: [ ] Clean [ ] Resignation / Qualified Opinion
  - Related-party transactions: [ ] Normal course [ ] Unusual surge
  - Promoter pledge status: [ ] $< 5\%$ [ ] Sudden pledge creation $> 5\%$
  - Credit rating status: [ ] Unchanged [ ] Downgraded
- **Root Cause Analysis**: Detailed narrative explaining why the price collapsed or filing occurred.
- **Thesis Invalidation Evaluation**: Does this event violate Section 4 ("Invalidation Criteria & Exit Triggers") of `Investing/Theses/{{symbol}}-thesis.md`?

---

## 6. Advisory Actionable Recommendations (Strictly manual review)
> [!NOTE]
> All suggested actions are strictly advisory research conclusions. **No live order placement tools** or automatic trade executions are authorized or executed.

- **Sentinel Advisory Status**: `[ SUPPRESS_ALERT_CORPORATE_ACTION | HOLD_AND_MONITOR | TIGHTEN_STOP_LOSS | EXIT_ON_THESIS_VIOLATION ]`
- **Recommended Action Plan**:
  1. **Immediate Step**: {{recommended_step_1}}
  2. **Contingent Trigger**: If stock fails to recover above ₹{{recovery_level}} within 3 trading sessions, manually execute risk-reduction exit.
  3. **Investor Discretion**: Log final manual decision and update thesis file in `Investing/Theses/{{symbol}}-thesis.md`.
