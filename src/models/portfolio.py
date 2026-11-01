"""
Portfolio and Risk Data Models for Indian Market Trading & Sentinel System
"""
from enum import Enum
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime


class AssetType(str, Enum):
    EQUITY = "EQUITY"
    ETF = "ETF"
    MUTUAL_FUND = "MUTUAL_FUND"
    SOVEREIGN_GOLD_BOND = "SGB"


class Broker(str, Enum):
    ZERODHA = "ZERODHA_KITE"
    GROWW = "GROWW"
    INDMONEY = "INDMONEY"
    MANUAL = "MANUAL"


class SeverityLevel(str, Enum):
    CRITICAL = "CRITICAL"   # Immediate action required (fraud, auditor resignation, >35% profit drop)
    HIGH = "HIGH"           # Significant risk (CEO exit, 200 EMA break, debt downgrade)
    MEDIUM = "MEDIUM"       # Notable headwind (margin squeeze, tariff change, 50 EMA break)
    LOW = "LOW"             # Informational / minor fluctuation
    NEUTRAL = "NEUTRAL"     # Routine announcements


@dataclass
class Holding:
    symbol: str                     # e.g., "HDFCBANK", "NIFTYBEES", "PARAG_PARIKH_FLEXICAP"
    isin: str                       # e.g., "INE040A01034"
    name: str                       # Company or Fund Name
    asset_type: AssetType           # EQUITY, ETF, MUTUAL_FUND
    broker: Broker                  # ZERODHA, GROWW, INDMONEY
    quantity: float                 # Units held
    average_price: float            # In INR (₹)
    current_price: float            # In INR (₹)
    sector: str = "General"         # e.g., "Banking", "IT", "Pharma"
    market_cap_category: str = "Large Cap"  # Large, Mid, Small Cap
    weight_pct: float = 0.0         # % of total portfolio
    currency: str = "INR"

    @property
    def invested_value(self) -> float:
        return self.quantity * self.average_price

    @property
    def current_value(self) -> float:
        return self.quantity * self.current_price

    @property
    def pnl(self) -> float:
        return self.current_value - self.invested_value

    @property
    def pnl_pct(self) -> float:
        if self.invested_value <= 0:
            return 0.0
        return (self.pnl / self.invested_value) * 100.0


@dataclass
class AdverseEvent:
    symbol: str
    headline: str
    source: str                     # e.g., "NSE Corporate Filings", "Moneycontrol", "Technical Watchdog"
    severity: SeverityLevel
    category: str                   # e.g., "Corporate Governance", "Earnings Miss", "Technical Breakdown"
    summary: str
    recommended_action: str         # "EXIT", "TRIM", "TIGHTEN_STOP_LOSS", "HOLD", "ACCUMULATE_DIP"
    timestamp: datetime = field(default_factory=datetime.now)
    url: Optional[str] = None


@dataclass
class UnifiedPortfolio:
    holdings: List[Holding] = field(default_factory=list)
    cash_balance: float = 0.0
    last_updated: datetime = field(default_factory=datetime.now)

    @property
    def total_invested(self) -> float:
        return sum(h.invested_value for h in self.holdings)

    @property
    def total_current_value(self) -> float:
        return sum(h.current_value for h in self.holdings)

    @property
    def total_net_worth(self) -> float:
        return self.total_current_value + self.cash_balance

    @property
    def total_pnl(self) -> float:
        return self.total_current_value - self.total_invested

    @property
    def total_pnl_pct(self) -> float:
        if self.total_invested <= 0:
            return 0.0
        return (self.total_pnl / self.total_invested) * 100.0

    def calculate_weights(self):
        total = self.total_current_value
        if total > 0:
            for h in self.holdings:
                h.weight_pct = round((h.current_value / total) * 100.0, 2)
