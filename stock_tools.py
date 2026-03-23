# stock_tools.py
"""Stock data tools for fetching price history and news."""

import yfinance as yf
import pandas as pd
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta
def is_valid_ticker(ticker: str) -> bool:
    """Validate if a ticker symbol exists and has data."""
    try:
        stock = yf.Ticker(ticker.upper().strip())
        info = stock.info
        # Check for valid stock - must have market cap or regular market price
        return info and (info.get('marketCap') or info.get('regularMarketPrice'))
    except Exception:
        return False


def get_stock_info(ticker: str) -> Optional[Dict[str, Any]]:
    """Get basic stock information."""
    try:
        stock = yf.Ticker(ticker.upper().strip())
        info = stock.info
        return {
            "name": info.get("shortName", ticker.upper()),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "market_cap": info.get("marketCap", 0),
            "current_price": info.get("regularMarketPrice", info.get("currentPrice", 0)),
            "previous_close": info.get("regularMarketPreviousClose", 0),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh", 0),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow", 0),
            "pe_ratio": info.get("trailingPE", None),
            "dividend_yield": info.get("dividendYield", None),
            "beta": info.get("beta", None),
        }
    except Exception as e:
        return None


def get_stock_history(ticker: str, horizon: str) -> Optional[pd.DataFrame]:
    """
    Fetch stock price history based on investment horizon.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL')
        horizon: Either 'short-term' (6mo) or 'long-term' (5y)
    
    Returns:
        DataFrame with OHLCV data or None if error
    """
    try:
        stock = yf.Ticker(ticker.upper().strip())
        period = "6mo" if horizon == "short-term" else "5y"
        df = stock.history(period=period)
        
        if df.empty:
            return None
        return df
    except Exception as e:
        return None


def calculate_technical_indicators(df: pd.DataFrame) -> Dict[str, Any]:
    """Calculate key technical indicators from price data."""
    if df is None or df.empty:
        return {}
    
    close = df['Close']
    
    # Price changes
    start_price = close.iloc[0]
    end_price = close.iloc[-1]
    percent_change = ((end_price - start_price) / start_price) * 100
    
    # Volatility (standard deviation of daily returns)
    daily_returns = close.pct_change().dropna()
    volatility = daily_returns.std() * 100  # as percentage
    
    # Simple moving averages
    sma_20 = close.rolling(window=20).mean().iloc[-1] if len(close) >= 20 else None
    sma_50 = close.rolling(window=50).mean().iloc[-1] if len(close) >= 50 else None
    
    # Max drawdown
    cumulative_max = close.cummax()
    drawdown = (close - cumulative_max) / cumulative_max
    max_drawdown = drawdown.min() * 100
    
    # Trend direction
    if sma_20 and sma_50:
        trend = "bullish" if sma_20 > sma_50 else "bearish"
    else:
        trend = "bullish" if percent_change > 0 else "bearish"
    
    return {
        "start_price": round(start_price, 2),
        "end_price": round(end_price, 2),
        "percent_change": round(percent_change, 2),
        "volatility": round(volatility, 2),
        "max_drawdown": round(max_drawdown, 2),
        "sma_20": round(sma_20, 2) if sma_20 else None,
        "sma_50": round(sma_50, 2) if sma_50 else None,
        "trend": trend,
        "high": round(close.max(), 2),
        "low": round(close.min(), 2),
    }


def calculate_risk_score(indicators: Dict[str, Any], info: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate a risk score (1-10) based on volatility, beta, and drawdown.
    Higher score = higher risk.
    """
    score = 5.0  # Start neutral
    factors = []
    
    # Volatility factor (daily volatility > 3% is high)
    volatility = indicators.get("volatility", 2)
    if volatility > 4:
        score += 2
        factors.append(f"High volatility ({volatility:.1f}%)")
    elif volatility > 2.5:
        score += 1
        factors.append(f"Moderate volatility ({volatility:.1f}%)")
    elif volatility < 1.5:
        score -= 1
        factors.append(f"Low volatility ({volatility:.1f}%)")
    
    # Max drawdown factor
    max_drawdown = abs(indicators.get("max_drawdown", 0))
    if max_drawdown > 30:
        score += 2
        factors.append(f"Significant max drawdown ({max_drawdown:.1f}%)")
    elif max_drawdown > 15:
        score += 1
        factors.append(f"Moderate max drawdown ({max_drawdown:.1f}%)")
    
    # Beta factor (if available)
    beta = info.get("beta") if info else None
    if beta:
        if beta > 1.5:
            score += 1.5
            factors.append(f"High beta ({beta:.2f})")
        elif beta < 0.8:
            score -= 1
            factors.append(f"Low beta ({beta:.2f})")
    
    # Clamp score between 1-10
    score = max(1, min(10, score))
    
    return {
        "score": round(score, 1),
        "level": "High" if score >= 7 else "Medium" if score >= 4 else "Low",
        "factors": factors
    }


def summarize_stock_trend(ticker: str, horizon: str) -> str:
    """Generate a comprehensive trend summary for the stock."""
    try:
        df = get_stock_history(ticker, horizon)
        info = get_stock_info(ticker)
        
        if df is None or df.empty:
            return f"No historical data available for {ticker}."
        
        indicators = calculate_technical_indicators(df)
        period = "6 months" if horizon == "short-term" else "5 years"
        
        summary = f"""
Stock: {info.get('name', ticker.upper()) if info else ticker.upper()}
Sector: {info.get('sector', 'Unknown') if info else 'Unknown'}
Analysis Period: {period}

Price Performance:
- Start: ${indicators['start_price']} → End: ${indicators['end_price']}
- Change: {indicators['percent_change']:+.2f}%
- Period High: ${indicators['high']} | Low: ${indicators['low']}

Technical Indicators:
- Trend: {indicators['trend'].upper()}
- Daily Volatility: {indicators['volatility']:.2f}%
- Max Drawdown: {indicators['max_drawdown']:.2f}%
{f"- SMA 20: ${indicators['sma_20']}" if indicators['sma_20'] else ""}
{f"- SMA 50: ${indicators['sma_50']}" if indicators['sma_50'] else ""}

Current Price: ${info.get('current_price', 'N/A') if info else 'N/A'}
P/E Ratio: {info.get('pe_ratio', 'N/A') if info else 'N/A'}
Beta: {info.get('beta', 'N/A') if info else 'N/A'}
""".strip()
        
        return summary
    except Exception as e:
        return f"Error analyzing stock trend: {e}"


def fetch_stock_news(ticker: str) -> List[Dict[str, str]]:
    """
    Fetch recent news for a stock using yfinance.
    Returns list of news items with title, link, and publisher.
    """
    try:
        stock = yf.Ticker(ticker.upper().strip())
        news = stock.news
        
        if not news:
            return []
        
        # Extract relevant news items (limit to 5 most recent)
        news_items = []
        for item in news[:5]:
            news_items.append({
                "title": item.get("title", "No title"),
                "link": item.get("link", ""),
                "publisher": item.get("publisher", "Unknown"),
                "published": datetime.fromtimestamp(
                    item.get("providerPublishTime", 0)
                ).strftime("%Y-%m-%d %H:%M") if item.get("providerPublishTime") else "Unknown"
            })
        
        return news_items
    except Exception as e:
        return []


def format_news_for_context(news_items: List[Dict[str, str]]) -> str:
    """Format news items into a string for LLM context."""
    if not news_items:
        return "No recent news available for this stock."
    
    formatted = "Recent News:\n"
    for i, item in enumerate(news_items, 1):
        formatted += f"\n{i}. {item['title']}\n"
        formatted += f"   Source: {item['publisher']} | Date: {item['published']}\n"
        formatted += f"   Link: {item['link']}\n"
    
    return formatted


