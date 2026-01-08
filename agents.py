# agents.py
"""CrewAI agents for stock analysis and investment advice."""

from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

from stock_tools import analyze_stock_data, get_stock_news

# Load environment variables
load_dotenv()

# Initialize LLM with appropriate settings
llm = ChatOpenAI(
    model=os.getenv("OPENAI_MODEL", "gpt-4o"),
    temperature=0.1  # Low temperature for consistent, factual outputs
)

# Stock Data Analyst Agent
stock_data_analyst = Agent(
    role="Senior Stock Data Analyst",
    goal="Analyze stock price data, technical indicators, and market trends to provide accurate, data-driven insights",
    backstory="""You are a seasoned quantitative analyst with 15 years of experience at top 
    investment firms. You specialize in technical analysis, understanding market patterns, 
    and identifying key price movements. You always cite specific data points and never 
    make claims without evidence. You understand that volatility, drawdowns, and trend 
    indicators are crucial for risk assessment.""",
    llm=llm,
    tools=[analyze_stock_data, get_stock_news],
    verbose=True,
    allow_delegation=False
)

# Investment Advisor Agent  
investment_advisor = Agent(
    role="Certified Investment Advisor",
    goal="Provide balanced, well-reasoned investment recommendations with clear confidence levels and risk warnings",
    backstory="""You are a fiduciary investment advisor with CFA certification and 20 years 
    of experience. You prioritize client protection and always provide balanced perspectives 
    including both bull and bear cases. You never give advice without acknowledging uncertainty 
    and risks. You understand that different time horizons require different analysis approaches. 
    You always remind clients that past performance doesn't guarantee future results.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)
