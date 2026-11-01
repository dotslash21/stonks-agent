"""
Workflow: 5-Pillar Fundamental Review
Runs in-depth fundamental, moat, FCF, DCF, and margin-of-safety evaluation
on any Indian listed stock (NSE/BSE).
"""
import os
import sys

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.analyzers.five_pillar_valuation import FivePillarValuationEngine


def review_stock(symbol: str):
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    engine = FivePillarValuationEngine()
    res = engine.analyze(symbol)

    print("\n" + "=" * 80)
    print(f"[VALUATION] 5-PILLAR FUNDAMENTAL REVIEW: {res.company_name} ({res.symbol})")
    print("=" * 80)
    print(f"Current Price: Rs. {res.current_price:,.2f} | Moat Quality Score: {res.moat_score}/10")
    print(f"P/E Ratio: {res.pe_ratio:.1f}x (5-Yr Median P/E: {res.five_year_median_pe:.1f}x) | PEG Ratio: {res.peg_ratio:.2f}")
    print(f"Cash Flow Health: CFO/PAT Ratio = {res.cfo_pat_ratio:.2f} | TTM FCF: Rs. {res.fcf_crores:,.0f} Cr")
    print(f"DCF Intrinsic Value: Rs. {res.dcf_intrinsic_value:,.2f} | Margin of Safety: {res.margin_of_safety_pct:+.1f}%")
    print(f"Accumulation Zone: {res.accumulation_zone}")
    print(f"Verdict: {res.verdict}")
    print("-" * 80)
    print(f"Thesis Summary:\n{res.thesis_summary}")
    print("=" * 80 + "\n")


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "HDFCBANK"
    review_stock(target)


if __name__ == "__main__":
    main()
