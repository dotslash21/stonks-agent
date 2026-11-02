---
name: nse-corporate-filings
description: Monitors SEBI LODR Regulation 30 corporate announcements, board meeting outcomes, and insider trading disclosures.
---

# NSE Corporate Filings Skill

## Purpose
The **NSE Corporate Filings** skill monitors, parses, and ranks regulatory corporate disclosures mandated by the Securities and Exchange Board of India (SEBI) under the **SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015 (LODR)** and the **SEBI (Prohibition of Insider Trading) Regulations, 2015 (PIT)**. It identifies material corporate developments before financial media syndication or broker commentary occurs, protecting portfolios against asymmetric information risks.

## Regulatory Scope & Key Announcements Scanned

### 1. Auditor & Governance Red Flags
- **Auditor Resignation**: Mid-term resignation of statutory auditors under SEBI Circular CIR/CFD/CMD1/114/2019, including mandated detailed reasons, audit qualifications, and lack of information disclosures.
- **Forensic Audits**: Initiation of forensic audits ordered by SEBI, the Ministry of Corporate Affairs (MCA), Serious Fraud Investigation Office (SFIO), or lenders.
- **Independent Director Dissents**: Casual vacancies or resignations of independent directors citing accounting disagreements, audit committee disputes, or governance failures.

### 2. Capital Restructuring & Corporate Actions
- **Board Meeting Notices & Outcomes**: Early scheduling and approvals of stock splits, bonus shares, rights issues, equity dilutions, preferential allotments, qualified institutional placements (QIP), and share buybacks.
- **Dividend & Record Dates**: Interim, final, and special dividend recommendations along with ex-dates and record dates.
- **Mergers & Demergers**: Scheme of arrangement filings, demerger swap ratios, and business spin-offs.

### 3. Credit Rating Actions
- **Rating Revisions**: Upgrades, downgrades, and affirmations by credit rating agencies (CRISIL, ICRA, CARE, India Ratings).
- **Watch & Outlook Alerts**: Placements on "Rating Watch with Negative Implications" or downgrades into default/speculative rating bands.

### 4. Material Events & Litigation (SEBI LODR Regulation 30)
- **Regulatory Actions & Raids**: Search and seizure operations by the Income Tax Department, Enforcement Directorate (ED), Central Bureau of Investigation (CBI), or Directorate General of GST Intelligence (DGGI).
- **Material Litigation & Claims**: Tax notices, contractual disputes, arbitration awards, or regulatory penalty orders exceeding 5% of net worth.
- **Operational Disruptions**: Factory lockouts, strikes, major fire incidents, environmental closure notices, or force majeure events.
- **Debt Service Defaults**: Defaults on commercial paper (CP), Non-Convertible Debentures (NCDs), interest coupons, or bank loan covenants.

### 5. Earnings & Performance Releases (Regulation 33)
- **Quarterly & Annual Results**: Unaudited and audited standalone and consolidated financial results, segment reports, and investor presentation disclosures.
- **Audit Qualifications**: True-and-fair view qualifications or "Emphasis of Matter" paragraphs highlighted by statutory auditors.

### 6. Insider Trading & Shareholding Disclosures (SEBI PIT & SAST)
- **Regulation 7(2) PIT Disclosures**: Market acquisitions, disposals, or pledge creations by Promoters, Directors, and Key Managerial Personnel (KMP) exceeding the regulatory reporting threshold (e.g., transaction value $> ₹10$ Lakhs).
- **Regulation 31 SAST Disclosures**: Promoter share pledge creation, invocation of pledge by lenders, or pledge revocations.

### 7. US SEC EDGAR Regulatory Disclosures (INDmoney US Equities)
- **Form 8-K**: Unscheduled material events, including executive changes (Item 5.02), asset impairments (Item 2.06), non-reliance on financial statements (Item 4.02), and bankruptcy/receivership (Item 1.03).
- **Form 10-K / 10-Q**: Audited annual and quarterly financial statements, risk factors, and legal proceedings.
- **Form 4 / Schedule 13D/G**: Officer, director, and 10% beneficial owner transaction reports for insider accumulation or liquidation.

## Cross-Examination against DalalOS BSE-XBRL & SEC EDGAR
To eliminate ambiguity from unstructured PDF press releases, the skill cross-examines unstructured filings against structured data sources:
1. **XBRL Validation**: Reconcile company-issued press release statements with machine-readable XBRL balance sheet line-items in DalalOS (`dalalos`) and SEC EDGAR (`sec-edgar`).
2. **Exchange Feed Verification**: Cross-verify promoter pledge announcements against official exchange SAST registries to detect delays or discrepancies in reported pledge percentages.
3. **Corporate Action Reconciliation**: Confirm announced dividend, split, or bonus ratios directly against clearing corporation circulars to guarantee verified ex-date pricing calculations.

## Multi-Tier Data Routing Table
To handle exchange downtime and API rate limits, regulatory queries follow an automated fallback cascade:

| Filing Type | Primary Feed | Fallback Tier 1 | Fallback Tier 2 |
|---|---|---|---|
| **Live Regulation 30 Announcements** | NSE Live CM (`nse-cm-market:get_announcements`) | DalalOS (`dalalos:get_regulatory_filings`) | `indian-market-mcp:get_corporate_announcements` |
| **BSE / NSE Structured XBRL** | DalalOS (`dalalos:get_financial_statements`) | `nse-bhavcopy` (Corporate Filings) | `indian-market-mcp:get_corporate_actions` |
| **US SEC EDGAR 8-K / 10-K / 10-Q** | `sec-edgar` (Authoritative XBRL) | `yfinance-mcp` | SEC EDGAR portal |
| **Board Meeting Schedules** | NSE Live CM (`nse-cm-market:get_board_meetings`) | DalalOS (`dalalos:get_board_meetings`) | `indian-market-mcp:get_board_meetings` |
| **Insider Trading (PIT / SAST / Form 4)** | NSE Live CM (`nse-cm-market:get_insider_trading`) | DalalOS (`dalalos:get_insider_trading`) | `sec-edgar` (for US Form 4) |
| **Credit Rating Reports** | NSE Live CM (`nse-cm-market:get_announcements`) | DalalOS (`dalalos:get_regulatory_filings`) | `indian-market-mcp:get_news` |

## Step-by-Step Execution Workflow
1. **Identify Symbols**: Ingest list of equity symbols from active portfolio or analysis target list.
2. **Fetch Disclosures**: Query primary exchange feed (`nse-cm-market`) for regulatory announcements within the specified time window (trailing 24 hours for daily sweeps, trailing 7 days for weekly audits).
3. **Execute Fallback if Necessary**: If primary feed returns empty or errors, seamlessly fall back to `dalalos` and `indian-market-mcp`.
4. **Filter & Classify**: Categorize each filing by regulatory classification: `Financial Results`, `Board Meeting`, `Credit Rating`, `Material Event / Reg 30`, `Insider Trading`.
5. **Pattern Match Critical Keywords**: Flag high-risk terms such as `"auditor resignation"`, `"forensic audit"`, `"fraud"`, `"investigation"`, `"default"`, `"penalty"`, `"pledge creation"`.
6. **XBRL Cross-Check**: For high-impact balance sheet or restructuring disclosures, verify details against DalalOS XBRL records.
7. **Generate Advisory Digest**: Output prioritized chronological disclosure table with direct regulatory links, categorized severity, and recommended investor assessment.

## Strictly Advisory Guardrails
- **Anti-Goal**: Live order placement tools (such as place_order, place_gtt_order, or cancel_order) are forbidden and strictly prohibited.
- **Advisory Only**: This skill provides regulatory intelligence and risk categorization only. No automated order placement or trade execution is performed. All actions require manual review and confirmation by the investor.
