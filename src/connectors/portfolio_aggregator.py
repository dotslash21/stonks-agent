"""
Unified Portfolio Aggregator for Zerodha Kite, Groww, and INDmoney
"""
import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from src.models.portfolio import Holding, UnifiedPortfolio, AssetType, Broker


class PortfolioAggregator:
    """
    Normalizes multi-broker portfolios from Zerodha Kite, Groww, and INDmoney
    into a unified portfolio schema.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "config",
            "brokers_config.json"
        )

    def load_from_json(self, file_path: str) -> UnifiedPortfolio:
        """Loads a portfolio from a pre-configured or exported JSON file."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Portfolio file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        holdings = []
        for item in data.get("holdings", []):
            holding = Holding(
                symbol=item["symbol"],
                isin=item.get("isin", ""),
                name=item.get("name", item["symbol"]),
                asset_type=AssetType(item.get("asset_type", "EQUITY")),
                broker=Broker(item.get("broker", "MANUAL")),
                quantity=float(item.get("quantity", 0)),
                average_price=float(item.get("average_price", 0)),
                current_price=float(item.get("current_price", item.get("average_price", 0))),
                sector=item.get("sector", "General"),
                market_cap_category=item.get("market_cap_category", "Large Cap")
            )
            holdings.append(holding)

        portfolio = UnifiedPortfolio(
            holdings=holdings,
            cash_balance=float(data.get("cash_balance", 0.0)),
            last_updated=datetime.now()
        )
        portfolio.calculate_weights()
        return portfolio

    def get_sample_indian_portfolio(self) -> UnifiedPortfolio:
        """
        Creates a realistic Indian portfolio across Zerodha Kite, Groww, and INDmoney
        incorporating Direct Stocks, ETFs, and Mutual Funds.
        """
        holdings = [
            # 1. Zerodha Kite: Core Direct Stocks & ETFs
            Holding(
                symbol="HDFCBANK",
                isin="INE040A01034",
                name="HDFC Bank Limited",
                asset_type=AssetType.EQUITY,
                broker=Broker.ZERODHA,
                quantity=120,
                average_price=1520.00,
                current_price=1745.50,
                sector="Banking & Financials",
                market_cap_category="Large Cap"
            ),
            Holding(
                symbol="RELIANCE",
                isin="INE002A01018",
                name="Reliance Industries Limited",
                asset_type=AssetType.EQUITY,
                broker=Broker.ZERODHA,
                quantity=80,
                average_price=2750.00,
                current_price=2910.00,
                sector="Energy & Conglomerate",
                market_cap_category="Large Cap"
            ),
            Holding(
                symbol="TATAMOTORS",
                isin="INE155A01022",
                name="Tata Motors Limited",
                asset_type=AssetType.EQUITY,
                broker=Broker.ZERODHA,
                quantity=150,
                average_price=880.00,
                current_price=925.00,
                sector="Automotive",
                market_cap_category="Large Cap"
            ),
            Holding(
                symbol="NIFTYBEES",
                isin="INF204KB14I2",
                name="Nippon India Nifty 50 ETF",
                asset_type=AssetType.ETF,
                broker=Broker.ZERODHA,
                quantity=1000,
                average_price=235.00,
                current_price=262.50,
                sector="Index ETF",
                market_cap_category="Large Cap"
            ),
            Holding(
                symbol="GOLDBEES",
                isin="INF204KB17I5",
                name="Nippon India Gold ETF",
                asset_type=AssetType.ETF,
                broker=Broker.ZERODHA,
                quantity=800,
                average_price=58.00,
                current_price=69.50,
                sector="Commodities / Gold",
                market_cap_category="ETF"
            ),

            # 2. Groww: Direct Mutual Funds
            Holding(
                symbol="PARAG_PARIKH_FLEXI_CAP",
                isin="INF879O01027",
                name="Parag Parikh Flexi Cap Fund Direct-Growth",
                asset_type=AssetType.MUTUAL_FUND,
                broker=Broker.GROWW,
                quantity=3500.5,
                average_price=68.50,
                current_price=82.20,
                sector="Diversified Equity",
                market_cap_category="Multi Cap"
            ),
            Holding(
                symbol="NIPPON_INDIA_SMALL_CAP",
                isin="INF204K01W08",
                name="Nippon India Small Cap Fund Direct-Growth",
                asset_type=AssetType.MUTUAL_FUND,
                broker=Broker.GROWW,
                quantity=1800.0,
                average_price=125.00,
                current_price=162.40,
                sector="Small Cap Equity",
                market_cap_category="Small Cap"
            ),

            # 3. INDmoney: Direct Equities & US Tech Tracking
            Holding(
                symbol="INFY",
                isin="INE009A01021",
                name="Infosys Limited",
                asset_type=AssetType.EQUITY,
                broker=Broker.INDMONEY,
                quantity=110,
                average_price=1460.00,
                current_price=1780.00,
                sector="Information Technology",
                market_cap_category="Large Cap"
            ),
            Holding(
                symbol="KAYNES",
                isin="INE918Z01012",
                name="Kaynes Technology India Limited",
                asset_type=AssetType.EQUITY,
                broker=Broker.INDMONEY,
                quantity=40,
                average_price=3950.00,
                current_price=4850.00,
                sector="Electronics Manufacturing (EMS)",
                market_cap_category="Mid Cap"
            )
        ]

        portfolio = UnifiedPortfolio(
            holdings=holdings,
            cash_balance=150000.00,  # Available cash buffer across accounts
            last_updated=datetime.now()
        )
        portfolio.calculate_weights()
        return portfolio
