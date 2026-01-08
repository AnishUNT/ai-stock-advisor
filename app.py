# -*- coding: utf-8 -*-
# app.py
"""Streamlit UI for the AI Stock Advisor."""

import sys
import os

# Fix Windows encoding issues
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    os.environ['PYTHONIOENCODING'] = 'utf-8'

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json

from main import crew
from stock_tools import (
    is_valid_ticker, 
    get_stock_history, 
    get_stock_info,
    calculate_technical_indicators,
    calculate_risk_score,
    fetch_stock_news,
    format_news_for_context
)
from models import InvestmentRecommendation, RecommendationAction

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Stock Advisor",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for better styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@400;500;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a3e 50%, #0d0d1a 100%);
    }
    
    .main-header {
        font-family: 'Space Mono', monospace;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00d4aa, #7c3aed, #f472b6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-family: 'DM Sans', sans-serif;
        color: #a0a0c0;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        backdrop-filter: blur(10px);
    }
    
    .recommendation-buy {
        background: linear-gradient(135deg, rgba(0, 212, 170, 0.2), rgba(0, 212, 170, 0.05));
        border: 2px solid #00d4aa;
        border-radius: 16px;
        padding: 2rem;
    }
    
    .recommendation-hold {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2), rgba(251, 191, 36, 0.05));
        border: 2px solid #fbbf24;
        border-radius: 16px;
        padding: 2rem;
    }
    
    .recommendation-sell {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.2), rgba(239, 68, 68, 0.05));
        border: 2px solid #ef4444;
        border-radius: 16px;
        padding: 2rem;
    }
    
    .risk-low { color: #00d4aa; }
    .risk-medium { color: #fbbf24; }
    .risk-high { color: #ef4444; }
    
    .disclaimer-box {
        background: rgba(251, 191, 36, 0.1);
        border-left: 4px solid #fbbf24;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        font-size: 0.85rem;
        color: #d4d4e0;
    }
    
    .news-item {
        background: rgba(255, 255, 255, 0.02);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #7c3aed, #00d4aa);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 12px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(124, 58, 237, 0.4);
    }
    
    .demo-badge {
        background: linear-gradient(90deg, #7c3aed, #f472b6);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<h1 class="main-header">📈 AI Stock Advisor</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Multi-agent AI analysis powered by CrewAI • Real-time data from Yahoo Finance</p>', unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("### 🎯 Quick Start")
    st.markdown("""
    1. Enter a stock ticker (e.g., AAPL)
    2. Select your investment horizon
    3. Click **Analyze** and wait ~30 seconds
    """)
    
    st.markdown("---")
    st.markdown("### 🚀 Demo Mode")
    st.markdown("Try these pre-validated tickers:")
    
    col1, col2 = st.columns(2)
    if col1.button("AAPL", key="demo_aapl", use_container_width=True):
        st.session_state.demo_ticker = "AAPL"
    if col2.button("NVDA", key="demo_nvda", use_container_width=True):
        st.session_state.demo_ticker = "NVDA"
    
    st.markdown("---")
    st.markdown("### ℹ️ About")
    st.markdown("""
    **Data Sources:**
    - Yahoo Finance (prices)
    - Yahoo Finance (news)
    
    **AI Models:**
    - GPT-4o via CrewAI
    - 2 specialized agents
    
    **Architecture:**
    - Stock Data Analyst
    - Investment Advisor
    """)
    
    st.markdown("---")
    st.markdown("### ⚠️ Disclaimer")
    st.warning("This is for educational purposes only. Not financial advice. Always consult a qualified advisor.")

# --- Main Input Section ---
st.markdown("---")

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    # Check for demo ticker
    default_ticker = st.session_state.get("demo_ticker", "")
    ticker = st.text_input(
        "🔎 Stock Ticker",
        value=default_ticker,
        placeholder="e.g., AAPL, NVDA, MSFT",
        help="Enter a valid stock ticker symbol"
    ).upper().strip()

with col2:
    time_horizon = st.selectbox(
        "🕒 Investment Horizon",
        options=["short-term", "long-term"],
        help="Short-term: 6 months | Long-term: 5 years"
    )

with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button("🚀 Analyze", type="primary", use_container_width=True)

# --- Analysis Section ---
if analyze_clicked and ticker:
    # Clear demo ticker
    if "demo_ticker" in st.session_state:
        del st.session_state.demo_ticker
    
    # Validate ticker
    with st.spinner("Validating ticker..."):
        if not is_valid_ticker(ticker):
            st.error(f"❌ **Invalid ticker:** '{ticker}' is not a valid stock symbol. Please try again with a real ticker (e.g., AAPL, NVDA, MSFT).")
            st.stop()
    
    # Show progress
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Fetch stock info and history
    status_text.text("📊 Fetching stock data...")
    progress_bar.progress(10)
    
    info = get_stock_info(ticker)
    history = get_stock_history(ticker, time_horizon)
    
    if history is None or history.empty:
        st.error(f"⚠️ Could not fetch price history for {ticker}. Please try again later.")
        st.stop()
    
    progress_bar.progress(25)
    
    # Step 2: Calculate indicators
    status_text.text("📈 Calculating technical indicators...")
    indicators = calculate_technical_indicators(history)
    risk = calculate_risk_score(indicators, info)
    progress_bar.progress(35)
    
    # Step 3: Fetch news
    status_text.text("📰 Fetching recent news...")
    news_items = fetch_stock_news(ticker)
    progress_bar.progress(45)
    
    # Step 4: Run AI analysis
    status_text.text("🤖 Running AI analysis (this may take 30-60 seconds)...")
    
    try:
        result = crew.kickoff(inputs={
            "ticker": ticker,
            "time_horizon": time_horizon
        })
        progress_bar.progress(90)
        
        # Extract the structured output
        try:
            if hasattr(result, 'pydantic'):
                recommendation = result.pydantic
            elif hasattr(result.tasks_output[-1], 'pydantic'):
                recommendation = result.tasks_output[-1].pydantic
            else:
                # Fallback: parse from raw output
                raw_output = result.tasks_output[-1].raw if hasattr(result.tasks_output[-1], 'raw') else str(result)
                recommendation = None
        except Exception as e:
            recommendation = None
            raw_output = str(result)
        
        progress_bar.progress(100)
        status_text.empty()
        progress_bar.empty()
        
        # --- Display Results ---
        st.markdown("---")
        st.markdown(f"## 📊 Analysis Results for {ticker}")
        
        # Company info row
        if info:
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Company", info.get("name", ticker))
            col2.metric("Current Price", f"${info.get('current_price', 'N/A')}")
            col3.metric("Sector", info.get("sector", "N/A"))
            col4.metric("P/E Ratio", f"{info.get('pe_ratio', 'N/A'):.2f}" if info.get('pe_ratio') else "N/A")
        
        # Price chart
        st.markdown("### 📈 Price History")
        
        fig = go.Figure()
        
        # Candlestick chart
        fig.add_trace(go.Candlestick(
            x=history.index,
            open=history['Open'],
            high=history['High'],
            low=history['Low'],
            close=history['Close'],
            name='Price',
            increasing_line_color='#00d4aa',
            decreasing_line_color='#ef4444'
        ))
        
        # Add SMA lines if available
        if len(history) >= 20:
            sma20 = history['Close'].rolling(window=20).mean()
            fig.add_trace(go.Scatter(
                x=history.index, y=sma20,
                name='SMA 20', line=dict(color='#7c3aed', width=1)
            ))
        
        if len(history) >= 50:
            sma50 = history['Close'].rolling(window=50).mean()
            fig.add_trace(go.Scatter(
                x=history.index, y=sma50,
                name='SMA 50', line=dict(color='#f472b6', width=1)
            ))
        
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_rangeslider_visible=False,
            height=400,
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        change_color = "normal" if indicators['percent_change'] >= 0 else "inverse"
        col1.metric(
            f"{'6-Month' if time_horizon == 'short-term' else '5-Year'} Change",
            f"{indicators['percent_change']:+.2f}%",
            delta=f"{'📈' if indicators['percent_change'] >= 0 else '📉'}"
        )
        col2.metric("Trend", indicators['trend'].upper())
        col3.metric("Volatility", f"{indicators['volatility']:.2f}%")
        col4.metric("Max Drawdown", f"{indicators['max_drawdown']:.2f}%")
        
        # Risk Score Gauge
        st.markdown("### ⚠️ Risk Assessment")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Risk gauge
            risk_color = "#00d4aa" if risk['level'] == "Low" else "#fbbf24" if risk['level'] == "Medium" else "#ef4444"
            
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk['score'],
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [1, 10], 'tickwidth': 1},
                    'bar': {'color': risk_color},
                    'bgcolor': "rgba(255,255,255,0.1)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [1, 4], 'color': 'rgba(0, 212, 170, 0.3)'},
                        {'range': [4, 7], 'color': 'rgba(251, 191, 36, 0.3)'},
                        {'range': [7, 10], 'color': 'rgba(239, 68, 68, 0.3)'}
                    ],
                },
                title={'text': f"Risk Level: {risk['level']}", 'font': {'size': 16}}
            ))
            
            fig_gauge.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                font={'color': 'white'},
                height=250,
                margin=dict(l=20, r=20, t=50, b=20)
            )
            
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with col2:
            st.markdown("**Risk Factors:**")
            for factor in risk['factors']:
                st.markdown(f"• {factor}")
            
            if not risk['factors']:
                st.markdown("• No significant risk factors identified")
        
        # AI Recommendation
        st.markdown("### 🤖 AI Investment Recommendation")
        
        if recommendation and isinstance(recommendation, InvestmentRecommendation):
            # Determine recommendation style
            if recommendation.action == RecommendationAction.BUY:
                rec_class = "recommendation-buy"
                rec_emoji = "🟢"
            elif recommendation.action == RecommendationAction.HOLD:
                rec_class = "recommendation-hold"
                rec_emoji = "🟡"
            else:
                rec_class = "recommendation-sell"
                rec_emoji = "🔴"
            
            st.markdown(f"""
            <div class="{rec_class}">
                <h2 style="margin:0; color: white;">{rec_emoji} {recommendation.action.value}</h2>
                <p style="color: #a0a0c0; margin: 0.5rem 0;">
                    Confidence: <strong>{recommendation.confidence.value}</strong> ({recommendation.confidence_score}%)
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Rationale:** {recommendation.rationale}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📈 Bull Case")
                for point in recommendation.bull_case:
                    st.markdown(f"✅ {point}")
            
            with col2:
                st.markdown("#### 📉 Bear Case")
                for point in recommendation.bear_case:
                    st.markdown(f"⚠️ {point}")
            
            # News references
            if recommendation.news_items:
                st.markdown("### 📰 Referenced News")
                for item in recommendation.news_items:
                    st.markdown(f"""
                    <div class="news-item">
                        <strong>{item.title}</strong><br>
                        <small>{item.publisher} • {item.published}</small><br>
                        <a href="{item.link}" target="_blank">Read more</a>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Disclaimer
            st.markdown(f"""
            <div class="disclaimer-box">
                ⚠️ <strong>Important:</strong> {recommendation.disclaimer}
            </div>
            """, unsafe_allow_html=True)
            
        else:
            # Fallback display for unstructured output
            st.info("📝 AI Analysis (unstructured output):")
            st.markdown(raw_output if 'raw_output' in dir() else str(result))
            
            st.markdown("""
            <div class="disclaimer-box">
                ⚠️ <strong>Important:</strong> This is AI-generated analysis for educational purposes only. 
                Not financial advice. Past performance does not guarantee future results. 
                Always consult a qualified financial advisor before making investment decisions.
            </div>
            """, unsafe_allow_html=True)
        
        # News Section (from our fetch)
        if news_items:
            with st.expander("📰 Latest News Headlines", expanded=False):
                for item in news_items:
                    st.markdown(f"""
                    **{item['title']}**  
                    *{item['publisher']}* • {item['published']}  
                    [Read full article]({item['link']})
                    
                    ---
                    """)
        
        # Download Report
        st.markdown("---")
        
        report_content = f"""# AI Stock Advisor Report
## {ticker} - {info.get('name', '') if info else ''}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Summary
- **Ticker:** {ticker}
- **Time Horizon:** {time_horizon}
- **Current Price:** ${info.get('current_price', 'N/A') if info else 'N/A'}
- **Period Change:** {indicators['percent_change']:+.2f}%
- **Risk Level:** {risk['level']} ({risk['score']}/10)

## Technical Analysis
- Trend: {indicators['trend'].upper()}
- Volatility: {indicators['volatility']:.2f}%
- Max Drawdown: {indicators['max_drawdown']:.2f}%

## AI Recommendation
{recommendation.action.value if recommendation else 'See analysis above'}

{recommendation.rationale if recommendation else ''}

## Disclaimer
This is AI-generated analysis for educational purposes only. Not financial advice. 
Past performance does not guarantee future results. Always consult a qualified 
financial advisor before making investment decisions.
"""
        
        st.download_button(
            label="📥 Download Report",
            data=report_content,
            file_name=f"{ticker}_stock_report_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown"
        )
        
    except Exception as e:
        progress_bar.empty()
        status_text.empty()
        st.error(f"❌ Analysis failed: {str(e)}")
        st.info("This might be due to API rate limits or network issues. Please try again in a moment.")

elif analyze_clicked and not ticker:
    st.warning("⚠️ Please enter a stock ticker to analyze.")

# Footer
st.markdown("---")
st.markdown("""
<p style="text-align: center; color: #666; font-size: 0.8rem;">
    Built with CrewAI, LangChain, and Streamlit • Data from Yahoo Finance<br>
    <strong>For educational purposes only. Not financial advice.</strong>
</p>
""", unsafe_allow_html=True)
