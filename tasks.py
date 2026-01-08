# tasks.py
"""CrewAI tasks for the stock advisor workflow."""

from crewai import Task
from agents import stock_data_analyst, investment_advisor
from models import InvestmentRecommendation

# Task 1: Analyze stock data
analyze_stock_task = Task(
    description="""
    Analyze the stock {ticker} for a {time_horizon} investment strategy.
    
    Your analysis must include:
    1. Use the analyze_stock_data tool to get price history and technical indicators
    2. Use the get_stock_news tool to fetch recent news articles
    3. Evaluate the current trend (bullish/bearish)
    4. Assess volatility and risk factors
    5. Note any significant price movements or patterns
    
    Be specific with numbers and cite actual data points. Do not hallucinate or make up data.
    """,
    expected_output="""A comprehensive analysis including:
    - Price performance summary with specific percentages
    - Technical indicator values (volatility, trend, moving averages)
    - Risk factors identified
    - Summary of relevant news with source citations
    - Overall market sentiment assessment""",
    agent=stock_data_analyst
)

# Task 2: Generate investment recommendation
advise_investment_task = Task(
    description="""
    Based on the analysis provided, create a detailed investment recommendation for {ticker} 
    as a {time_horizon} investment.
    
    You MUST:
    1. Provide a clear BUY, HOLD, or SELL recommendation
    2. Assign a confidence level (HIGH/MEDIUM/LOW) with a percentage score
    3. List specific bull case reasons (why it could go up)
    4. List specific bear case reasons (risks and downsides)
    5. Reference the actual news articles from the analysis
    6. Include appropriate risk warnings
    
    Consider the time horizon carefully:
    - Short-term (6 months): Focus on momentum, recent news, technical patterns
    - Long-term (5 years): Focus on fundamentals, sector trends, company position
    
    Always acknowledge uncertainty. Never claim guaranteed returns.
    """,
    expected_output="""A structured recommendation with all required fields filled in accurately.
    The response must be grounded in the data provided - do not make up statistics or news.""",
    agent=investment_advisor,
    output_pydantic=InvestmentRecommendation,
    context=[analyze_stock_task]  # This task depends on the analysis task
)
