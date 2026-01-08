# main.py
"""Main entry point for the Stock Advisor CrewAI workflow."""

from crewai import Crew, Process
from tasks import analyze_stock_task, advise_investment_task
from agents import stock_data_analyst, investment_advisor

# Create the crew with sequential process
crew = Crew(
    agents=[stock_data_analyst, investment_advisor],
    tasks=[analyze_stock_task, advise_investment_task],
    process=Process.sequential,
    verbose=True
)


def run_analysis(ticker: str, time_horizon: str) -> dict:
    """
    Run the full stock analysis pipeline.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        time_horizon: Either 'short-term' or 'long-term'
    
    Returns:
        The structured recommendation from the crew
    """
    result = crew.kickoff(inputs={
        "ticker": ticker.upper(),
        "time_horizon": time_horizon
    })
    return result


if __name__ == "__main__":
    # Demo mode - run with example tickers
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
