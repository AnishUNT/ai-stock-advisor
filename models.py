# models.py
"""Pydantic models for structured output from AI agents."""

from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class RecommendationAction(str, Enum):
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"


class ConfidenceLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class RiskAssessment(BaseModel):
    """Risk assessment for a stock."""
    score: float = Field(..., ge=1, le=10, description="Risk score from 1 (low) to 10 (high)")
    level: str = Field(..., description="Risk level: Low, Medium, or High")
    factors: List[str] = Field(default_factory=list, description="Key risk factors identified")


class NewsItem(BaseModel):
    """A news article about the stock."""
    title: str = Field(..., description="News headline")
    link: str = Field(..., description="URL to the full article")
    publisher: str = Field(..., description="News publisher/source")
    published: str = Field(..., description="Publication date")


class StockAnalysis(BaseModel):
    """Structured output from stock data analysis."""
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    sector: str = Field(..., description="Industry sector")
    current_price: float = Field(..., description="Current stock price in USD")
    price_change_percent: float = Field(..., description="Price change over analysis period")
    trend: str = Field(..., description="Current trend: bullish or bearish")
    volatility: float = Field(..., description="Daily volatility percentage")
    risk: RiskAssessment = Field(..., description="Risk assessment")
    key_insights: List[str] = Field(..., description="Key insights from technical analysis")


class InvestmentRecommendation(BaseModel):
    """Structured investment recommendation output."""
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    action: RecommendationAction = Field(..., description="Recommended action: BUY, HOLD, or SELL")
    confidence: ConfidenceLevel = Field(..., description="Confidence level in the recommendation")
    confidence_score: int = Field(..., ge=0, le=100, description="Confidence percentage 0-100")
    time_horizon: str = Field(..., description="Investment time horizon analyzed")
    
    # Analysis summary
    price_analysis: str = Field(..., description="Summary of price performance and trends")
    news_sentiment: str = Field(..., description="Summary of recent news sentiment")
    
    # Rationale
    rationale: str = Field(..., description="Detailed reasoning for the recommendation")
    bull_case: List[str] = Field(..., description="Reasons the stock could outperform")
    bear_case: List[str] = Field(..., description="Risks and reasons the stock could underperform")
    
    # Risk info
    risk_score: float = Field(..., ge=1, le=10, description="Risk score from 1-10")
    risk_level: str = Field(..., description="Risk level: Low, Medium, or High")
    
    # News references
    news_items: List[NewsItem] = Field(default_factory=list, description="Recent news articles referenced")
    
    # Disclaimer
    disclaimer: str = Field(
        default="This is AI-generated analysis for educational purposes only. Not financial advice. "
                "Past performance does not guarantee future results. Always consult a qualified "
                "financial advisor before making investment decisions.",
        description="Legal disclaimer"
    )


class DemoResult(BaseModel):
    """Complete result for demo display."""
    recommendation: InvestmentRecommendation
    analysis_timestamp: str
    data_sources: List[str] = Field(
        default=["Yahoo Finance (price data)", "Yahoo Finance (news)"],
        description="Data sources used"
    )
