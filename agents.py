# agents.py
"""Two-agent stock analysis pipeline using the OpenAI API directly."""

from openai import OpenAI
from dotenv import load_dotenv
import os

from stock_tools import summarize_stock_trend, fetch_stock_news, format_news_for_context
from models import InvestmentRecommendation

load_dotenv()

_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")


def run_analyst(ticker: str, horizon: str) -> str:
    """Agent 1: Analyze stock data and return a trend summary."""
    stock_summary = summarize_stock_trend(ticker, horizon)
    news_text = format_news_for_context(fetch_stock_news(ticker))

    response = _client.chat.completions.create(
        model=_MODEL,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Senior Stock Data Analyst with 15 years of experience at top "
                    "investment firms. You specialize in technical analysis and identifying key "
                    "price movements. Always cite specific data points and never make claims "
                    "without evidence."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Analyze {ticker} for a {horizon} investment strategy.\n\n"
                    f"Stock data:\n{stock_summary}\n\n"
                    f"{news_text}\n\n"
                    "Provide a comprehensive analysis covering:\n"
                    "1. Price performance with specific percentages\n"
                    "2. Technical indicators (volatility, trend, moving averages)\n"
                    "3. Risk factors\n"
                    "4. News sentiment summary with source citations\n"
                    "5. Overall market sentiment"
                ),
            },
        ],
    )
    return response.choices[0].message.content


def run_advisor(ticker: str, horizon: str, analysis: str) -> InvestmentRecommendation:
    """Agent 2: Generate a structured investment recommendation."""
    response = _client.beta.chat.completions.parse(
        model=_MODEL,
        temperature=0.1,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a fiduciary investment advisor with CFA certification and 20 years "
                    "of experience. You always provide balanced bull and bear perspectives and "
                    "never give advice without acknowledging uncertainty and risks."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Based on the analysis below, create a detailed investment recommendation "
                    f"for {ticker} as a {horizon} investment.\n\n"
                    f"Analysis:\n{analysis}\n\n"
                    "Requirements:\n"
                    "- Clear BUY, HOLD, or SELL recommendation\n"
                    "- Confidence level (HIGH/MEDIUM/LOW) with percentage score\n"
                    "- Specific bull case reasons\n"
                    "- Specific bear case risks\n"
                    "- Reference actual news articles from the analysis\n"
                    "- Appropriate risk warnings\n\n"
                    "Time horizon guidance:\n"
                    "- Short-term (6 months): focus on momentum, news, technical patterns\n"
                    "- Long-term (5 years): focus on fundamentals, sector trends, company position"
                ),
            },
        ],
        response_format=InvestmentRecommendation,
    )
    return response.choices[0].message.parsed
