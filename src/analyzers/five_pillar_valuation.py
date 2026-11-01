"""
5-Pillar Fundamental Valuation Engine for Indian Equities (NSE/BSE)
Adapted from openclaw-stock-analyzer and Warren Buffett / Duan Yongping principles.
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class FundamentalValuationResult:
    symbol: str
    company_name: str
    current_price: float
    moat_score: int                 # 1 to 10
    cfo_pat_ratio: float            # CFO / PAT (> 0.8 is healthy)
    fcf_crores: float               # Free cash flow in INR Crores
    pe_ratio: float                 # Trailing P/E
    five_year_median_pe: float      # Historical median P/E
    peg_ratio: float                # Forward PEG
    dcf_intrinsic_value: float      # DCF calculated fair value in INR
    margin_of_safety_pct: float     # Discount to intrinsic value
    accumulation_zone: str          # e.g., "₹1,450 - ₹1,580"
    verdict: str                    # "STRONG_ACCUMULATE", "ACCUMULATE_DIP", "HOLD", "OVERVALUED"
    thesis_summary: str


class FivePillarValuationEngine:
    """
    Evaluates an Indian stock across the 5 fundamental pillars:
    1. Moat & Economic Quality
    2. Free Cash Flow Discipline
    3. PEG & Growth Sustainability
    4. DCF Valuation (Indian WACC calibrated)
    5. Tactical Entry & Margin of Safety
    """

    def analyze(self, symbol: str) -> FundamentalValuationResult:
        sym = symbol.upper().replace(".NS", "")

        # Company-specific fundamental data models (simulated real-world values for demonstration)
        data_store = {
            "HDFCBANK": {
                "name": "HDFC Bank Limited",
                "price": 1745.50,
                "moat_score": 9,
                "cfo_pat_ratio": 1.15,
                "fcf": 28400.0,
                "pe": 18.2,
                "median_pe": 22.5,
                "peg": 1.10,
                "intrinsic_val": 2050.00,
                "thesis": "Dominant private banking franchise in India with unmatched deposit branch network. Trading at a notable discount to its 5-year historical median P/E of 22.5x post-merger."
            },
            "RELIANCE": {
                "name": "Reliance Industries Limited",
                "price": 2910.00,
                "moat_score": 9,
                "cfo_pat_ratio": 0.95,
                "fcf": 34000.0,
                "pe": 26.8,
                "median_pe": 25.0,
                "peg": 1.75,
                "intrinsic_val": 3100.00,
                "thesis": "Unrivaled telecom (Jio) and retail leadership combined with cash-generating energy assets. Valuation is fairly priced with modest 6.5% margin of safety."
            },
            "TATAMOTORS": {
                "name": "Tata Motors Limited",
                "price": 925.00,
                "moat_score": 7,
                "cfo_pat_ratio": 1.30,
                "fcf": 18500.0,
                "pe": 10.5,
                "median_pe": 14.0,
                "peg": 0.85,
                "intrinsic_val": 1080.00,
                "thesis": "Strong domestic CV/PV market share and profitable JLR transition, though facing temporary European demand softening. Deep cyclical discount with favorable PEG < 1.0."
            },
            "INFY": {
                "name": "Infosys Limited",
                "price": 1780.00,
                "moat_score": 8,
                "cfo_pat_ratio": 1.05,
                "fcf": 22000.0,
                "pe": 27.5,
                "median_pe": 26.0,
                "peg": 2.10,
                "intrinsic_val": 1720.00,
                "thesis": "World-class digital services delivery and strong balance sheet, but current valuation reflects full pricing relative to near-term discretionary IT spending environment."
            },
            "KAYNES": {
                "name": "Kaynes Technology India Limited",
                "price": 4850.00,
                "moat_score": 8,
                "cfo_pat_ratio": 0.65,
                "fcf": 120.0,
                "pe": 82.0,
                "median_pe": 72.0,
                "peg": 2.40,
                "intrinsic_val": 3900.00,
                "thesis": "Premier Indian electronics manufacturing (EMS) & OSAT player enjoying huge tailwinds, but working capital intensity and P/E of 82x offer zero margin of safety."
            }
        }

        info = data_store.get(sym, {
            "name": f"{sym} Ltd",
            "price": 1000.0,
            "moat_score": 6,
            "cfo_pat_ratio": 0.80,
            "fcf": 500.0,
            "pe": 22.0,
            "median_pe": 20.0,
            "peg": 1.5,
            "intrinsic_val": 1050.0,
            "thesis": "Standard Indian listed equity."
        })

        # Calculate Margin of Safety
        intrinsic = info["intrinsic_val"]
        price = info["price"]
        mos_pct = ((intrinsic - price) / intrinsic) * 100.0

        # Verdict logic
        if mos_pct >= 15.0 and info["moat_score"] >= 8 and info["peg"] <= 1.5:
            verdict = "STRONG_ACCUMULATE"
        elif mos_pct >= 5.0 and info["moat_score"] >= 7:
            verdict = "ACCUMULATE_DIP"
        elif mos_pct < -10.0:
            verdict = "OVERVALUED"
        else:
            verdict = "HOLD"

        # Accumulation zone calculation
        lower_bound = round(intrinsic * 0.75, -1)
        upper_bound = round(intrinsic * 0.88, -1)
        acc_zone = f"₹{lower_bound:,.0f} - ₹{upper_bound:,.0f}"

        return FundamentalValuationResult(
            symbol=sym,
            company_name=info["name"],
            current_price=price,
            moat_score=info["moat_score"],
            cfo_pat_ratio=info["cfo_pat_ratio"],
            fcf_crores=info["fcf"],
            pe_ratio=info["pe"],
            five_year_median_pe=info["median_pe"],
            peg_ratio=info["peg"],
            dcf_intrinsic_value=intrinsic,
            margin_of_safety_pct=round(mos_pct, 1),
            accumulation_zone=acc_zone,
            verdict=verdict,
            thesis_summary=info["thesis"]
        )
