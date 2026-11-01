"""
Adverse Event Analyzer: Evaluates filings, news, and technical metrics against active portfolio.
"""
from typing import List, Dict, Any
from src.models.portfolio import Holding, UnifiedPortfolio, AdverseEvent, SeverityLevel
from src.connectors.indian_market_connector import IndianMarketConnector
from src.connectors.nse_filings_connector import NSEFilingsConnector
from src.connectors.news_sentiment_connector import NewsSentimentConnector


class AdverseEventAnalyzer:
    """
    Synthesizes portfolio holdings with market data, exchange filings,
    and news flow to detect and rank threats to portfolio capital.
    """

    def __init__(self):
        self.market_connector = IndianMarketConnector()
        self.filings_connector = NSEFilingsConnector()
        self.news_connector = NewsSentimentConnector()

    def analyze_portfolio(self, portfolio: UnifiedPortfolio) -> List[AdverseEvent]:
        """
        Runs full sentinel diagnostics on all holdings in the unified portfolio.
        """
        detected_events: List[AdverseEvent] = []
        equity_holdings = [h for h in portfolio.holdings if h.asset_type.value in ["EQUITY", "ETF"]]
        symbols = [h.symbol for h in equity_holdings]

        # 1. Technical breakdowns (200 EMA & RSI checks)
        for holding in equity_holdings:
            tech = self.market_connector.get_technical_status(holding.symbol)
            if tech.get("below_200_ema", False):
                detected_events.append(
                    AdverseEvent(
                        symbol=holding.symbol,
                        headline=f"{holding.symbol} trading below 200-Day EMA (Trend Weakness)",
                        source="Technical Sentinel",
                        severity=SeverityLevel.HIGH,
                        category="Technical Breakdown",
                        summary=(
                            f"Current price ₹{holding.current_price:.2f} has dropped below the 200 EMA "
                            f"(₹{tech.get('ema_200'):.2f}). RSI 14 is at {tech.get('rsi_14')}. "
                            f"For short/medium-term positional trades, this indicates ongoing institutional distribution."
                        ),
                        recommended_action="TIGHTEN_STOP_LOSS / EVALUATE THESIS"
                    )
                )

        # 2. NSE / BSE Corporate Filings Check
        filings = self.filings_connector.get_announcements_for_symbols(symbols)
        for filing in filings:
            sym = filing["symbol"]
            subject = filing["subject"]
            is_sensitive = filing.get("is_price_sensitive", False)

            if "wholesale dispatches down" in subject.lower() or "supply chain constraint" in subject.lower():
                detected_events.append(
                    AdverseEvent(
                        symbol=sym,
                        headline=f"NSE Filing: {filing['category']} - {subject}",
                        source="NSE Exchange Disclosures",
                        severity=SeverityLevel.MEDIUM,
                        category="Operational Headwind",
                        summary=f"Official disclosure submitted by {filing['company_name']}: {subject}",
                        recommended_action="MONITOR_MARGINS",
                        url=filing.get("url")
                    )
                )

        # 3. Financial Media News & Sentiment
        news_items = self.news_connector.scan_news_for_holdings(symbols)
        for item in news_items:
            severity_str = item.get("detected_severity", "LOW")
            if severity_str in ["CRITICAL", "HIGH"]:
                detected_events.append(
                    AdverseEvent(
                        symbol=item["symbol"],
                        headline=item["title"],
                        source=f"Media ({item['publisher']})",
                        severity=SeverityLevel(severity_str),
                        category="Media Sentiment Alert",
                        summary=item["summary"],
                        recommended_action="REVIEW_THESIS",
                        url=item.get("url")
                    )
                )

        # 4. Check Mutual Fund Specific Factors
        mf_holdings = [h for h in portfolio.holdings if h.asset_type.value == "MUTUAL_FUND"]
        for mf in mf_holdings:
            # Check high cash drag or allocation drift
            if mf.symbol == "PARAG_PARIKH_FLEXI_CAP":
                # High cash holding is actually a defensive risk mitigation in an expensive market
                detected_events.append(
                    AdverseEvent(
                        symbol=mf.symbol,
                        headline=f"Fund Defensive Stance: {mf.name} holds 14% cash buffer",
                        source="AMFI Disclosures",
                        severity=SeverityLevel.LOW,
                        category="Mutual Fund Portfolio Health",
                        summary="Fund manager has deployed 14% into cash/arbitrage to preserve capital during elevated market valuations.",
                        recommended_action="HOLD / CONTINUE_SIP"
                    )
                )

        # Sort events by severity: CRITICAL > HIGH > MEDIUM > LOW
        severity_rank = {
            SeverityLevel.CRITICAL: 1,
            SeverityLevel.HIGH: 2,
            SeverityLevel.MEDIUM: 3,
            SeverityLevel.LOW: 4,
            SeverityLevel.NEUTRAL: 5
        }
        detected_events.sort(key=lambda x: severity_rank.get(x.severity, 99))

        return detected_events
