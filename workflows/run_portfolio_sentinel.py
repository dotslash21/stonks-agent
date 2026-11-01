"""
Workflow: Indian Portfolio Sentinel
Loads the unified portfolio, executes multi-source adverse event diagnostics,
prints the summary, and writes an executive markdown briefing report.
"""
import os
import sys

# Ensure root directory is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from src.connectors.portfolio_aggregator import PortfolioAggregator
from src.analyzers.adverse_event_analyzer import AdverseEventAnalyzer
from src.alerts.notifier import AlertNotifier


def main():
    print("\nInitializing Indian Portfolio Sentinel Workflow...")
    aggregator = PortfolioAggregator()

    # Load portfolio from data/mock_portfolio.json if present, else fallback to generated sample
    data_file = os.path.join(root_dir, "data", "mock_portfolio.json")
    if os.path.exists(data_file):
        portfolio = aggregator.load_from_json(data_file)
    else:
        portfolio = aggregator.get_sample_indian_portfolio()

    print(f"Loaded portfolio: {len(portfolio.holdings)} assets across Kite, Groww, and INDmoney.")

    # Run adverse event analyzer
    analyzer = AdverseEventAnalyzer()
    print("Scanning technical levels, NSE/BSE filings, and news sentiment...")
    events = analyzer.analyze_portfolio(portfolio)

    # Print terminal output
    AlertNotifier.print_terminal_summary(portfolio, events)

    # Generate Markdown Report
    report_md = AlertNotifier.generate_markdown_report(portfolio, events)
    output_dir = os.path.join(root_dir, "reports")
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, "sentinel_adverse_briefing.md")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_md)

    print(f"📄 Full executive briefing report generated: {report_path}\n")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    main()
