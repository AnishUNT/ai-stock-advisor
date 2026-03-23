# main.py
"""Main entry point for the Stock Advisor workflow."""

from agents import run_analyst, run_advisor
from models import InvestmentRecommendation


def run_analysis(ticker: str, time_horizon: str) -> InvestmentRecommendation:
    """
    Run the full two-agent stock analysis pipeline.

    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        time_horizon: Either 'short-term' or 'long-term'

    Returns:
        Structured InvestmentRecommendation
    """
    analysis = run_analyst(ticker, time_horizon)
    recommendation = run_advisor(ticker, time_horizon, analysis)
    return recommendation


if __name__ == "__main__":
    import sys

    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    horizon = sys.argv[2] if len(sys.argv) > 2 else "short-term"

    print(f"\n{'='*60}")
    print(f"  AI Stock Advisor - Analyzing {ticker.upper()}")
    print(f"  Time Horizon: {horizon}")
    print(f"{'='*60}\n")

    result = run_analysis(ticker, horizon)

    print(f"\n{'='*60}")
    print("  FINAL RECOMMENDATION")
    print(f"{'='*60}\n")
    print(result)
