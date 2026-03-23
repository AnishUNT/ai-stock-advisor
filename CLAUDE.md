# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp env.example .env  # then add OPENAI_API_KEY to .env
```

Required environment variable: `OPENAI_API_KEY`. Optional: `OPENAI_MODEL` (defaults to `gpt-4o`).

## Running the App

```bash
# Web UI (primary interface)
streamlit run app.py

# CLI (for quick testing)
python main.py AAPL short-term
python main.py NVDA long-term
```

## Architecture

This is a CrewAI multi-agent application that analyzes stocks and generates investment recommendations.

**Data flow:**

1. User provides a ticker + time horizon (`short-term` or `long-term`)
2. `stock_tools.py` fetches price history via yfinance and calculates technical indicators (SMA20, SMA50, volatility, beta, drawdown)
3. **Agent 1** (`Stock Data Analyst` in `agents.py`) calls the `analyze_stock_data()` and `get_stock_news()` tools, then produces a trend summary
4. **Agent 2** (`Investment Advisor`) receives Agent 1's output as context and returns a structured `InvestmentRecommendation` Pydantic model with `BUY/HOLD/SELL`, confidence, risk score, bull/bear cases, and news items
5. `app.py` displays the result with Plotly charts, a risk gauge, and a downloadable Markdown report

**Key files:**
- `main.py` — `run_analysis(ticker, horizon)` orchestrates the CrewAI `Crew` with sequential process
- `agents.py` — defines the two `Agent` objects using `ChatOpenAI` (temperature=0.1)
- `tasks.py` — defines the two `Task` objects; Task 2 takes Task 1 as `context`
- `stock_tools.py` — all data fetching and math; tools are decorated with `@tool` for CrewAI
- `models.py` — Pydantic schemas (`InvestmentRecommendation`, `RiskAssessment`, `NewsItem`)
- `app.py` — Streamlit UI; calls `stock_tools` functions directly for charts, then calls `run_analysis` for the AI recommendation

**Structured output:** The Investment Advisor agent uses `output_pydantic=InvestmentRecommendation` so CrewAI enforces schema compliance from the LLM response.

**Time horizon mapping:** `short-term` fetches 6 months of history; `long-term` fetches 5 years.

## No test infrastructure

There are no tests, linters, or formatters configured. The project has no CI/CD pipeline.
