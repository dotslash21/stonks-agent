---
name: nse-corporate-filings
description: Scans official NSE/BSE corporate filings, board meeting announcements, credit rating disclosures, and insider transactions under SEBI LODR/PIT.
---

# NSE Corporate Filings Skill

## Purpose
Directly queries official National Stock Exchange (NSE) and Bombay Stock Exchange (BSE) regulatory filing feeds to detect market-moving disclosures before media coverage or retail broker alerts occur.

## Key Disclosures Scanned
- **Board Meetings**: Earnings release schedules, dividend declarations, fund-raising (QIP, rights, ADR/GDR), stock splits.
- **Credit Rating Revisions**: Upgrades and downgrades by CRISIL, ICRA, CARE, India Ratings.
- **Auditor & Management Changes**: Resignations, casual vacancies, independent director dissents.
- **SEBI SAST & PIT Filings**: Promoter acquisitions, pledge creation/revocation, disposal of shares.
- **Material Events (Regulation 30 LODR)**: Litigation, arbitration, income tax/GST notices, fire/force majeure, factory lockouts.

## Step-by-Step Procedure
1. Retrieve portfolio ticker symbols.
2. Query exchange disclosures via `indian-market-mcp:get_corporate_announcements` or `nse-filings-scanner`.
3. Filter by category: `Financial Results`, `Board Meeting`, `Credit Rating`, `Company Updates`.
4. Run regex classifier to highlight critical terms: `"loss"`, `"downgrade"`, `"resignation"`, `"fraud"`, `"investigation"`, `"default"`.
5. Return ranked list of disclosures with direct exchange link and severity tag.
