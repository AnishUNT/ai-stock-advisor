# 📈 AI Stock Advisor

> Multi-agent AI system for stock analysis and investment recommendations powered by CrewAI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-purple.svg)](https://github.com/joaomdmoura/crewAI)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)

---

## 🎯 What It Does

Input a stock ticker and investment horizon → Get AI-powered analysis with:
- **Real price data** from Yahoo Finance
- **Technical indicators** (volatility, trends, moving averages)
- **Risk assessment** with quantified score
- **News sentiment** from recent articles
- **Investment recommendation** (BUY/HOLD/SELL) with confidence level

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT UI                              │
│   [Ticker Input] [Horizon Select] [Analyze Button]              │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       CREWAI ORCHESTRATOR                        │
│                                                                  │
│  ┌─────────────────────┐      ┌─────────────────────────────┐  │
│  │  STOCK DATA ANALYST │      │    INVESTMENT ADVISOR        │  │
│  │  ─────────────────  │      │    ─────────────────────     │  │
│  │  • Fetches prices   │ ───▶ │  • Analyzes data             │  │
│  │  • Calculates       │      │  • Generates recommendation  │  │
│  │    indicators       │      │  • Assigns confidence        │  │
│  │  • Gathers news     │      │  • Lists bull/bear cases     │  │
│  └─────────────────────┘      └─────────────────────────────┘  │
│           │                                                      │
│           ▼                                                      │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      TOOLS                               │    │
│  │  • analyze_stock_data() - Price history & technicals    │    │
│  │  • get_stock_news()     - Recent news articles          │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA SOURCES                                │
│  • Yahoo Finance (yfinance) - Real-time prices & news           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STRUCTURED OUTPUT                              │
│  {                                                               │
│    "action": "BUY/HOLD/SELL",                                   │
│    "confidence": "HIGH/MEDIUM/LOW",                             │
│    "confidence_score": 0-100,                                   │
│    "risk_score": 1-10,                                          │
│    "rationale": "...",                                          │
│    "bull_case": [...],                                          │
│    "bear_case": [...],                                          │
│    "news_items": [...]                                          │
│  }                                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (< 5 minutes)

### 1. Clone & Navigate
```bash
git clone <your-repo-url>
cd stockadvisor
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
# Copy the example env file
copy env.example .env    # Windows
cp env.example .env      # macOS/Linux

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here
```

### 5. Run the App
```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## 🎮 Demo Mode

For reliable demos, use these pre-validated tickers:
- **AAPL** - Apple Inc. (large cap, stable)
- **NVDA** - NVIDIA Corp. (high growth, tech)

Click the demo buttons in the sidebar or enter manually.

---

## 📁 Project Structure

```
stockadvisor/
├── app.py              # Streamlit UI
├── main.py             # CrewAI crew setup
├── agents.py           # Agent definitions
├── tasks.py            # Task definitions
├── stock_tools.py      # Data fetching tools
├── models.py           # Pydantic output models
├── requirements.txt    # Dependencies
├── env.example         # Environment template
└── README.md           # This file
```

---

## 🔧 Configuration

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | - | Your OpenAI API key |
| `OPENAI_MODEL` | No | `gpt-4o` | Model to use (gpt-4o, gpt-4-turbo, gpt-3.5-turbo) |

---

## 📊 Features

### ✅ Implemented
- [x] Multi-agent workflow (Analyst + Advisor)
- [x] Real price data from Yahoo Finance
- [x] Technical indicators (SMA, volatility, drawdown)
- [x] Risk scoring (1-10 scale)
- [x] News fetching with source links
- [x] Structured JSON output (Pydantic)
- [x] Interactive Plotly charts
- [x] Confidence ratings
- [x] Bull/Bear case analysis
- [x] Downloadable reports
- [x] Invalid ticker handling
- [x] Legal disclaimers

### ⚠️ Limitations
- News is limited to Yahoo Finance's feed
- Analysis takes 30-60 seconds (LLM processing)
- Historical data limited by Yahoo Finance
- Not suitable for real trading decisions

---

## 🛡️ Guardrails & Safety

1. **Ticker Validation**: Verifies ticker exists before analysis
2. **Missing Data Handling**: Graceful fallbacks for API failures
3. **Confidence Levels**: All recommendations include uncertainty
4. **Legal Disclaimer**: Prominent "not financial advice" warnings
5. **Risk Scoring**: Quantified risk with explanatory factors

---

## 🧪 Running CLI Demo

```bash
# Analyze AAPL short-term
python main.py AAPL short-term

# Analyze NVDA long-term
python main.py NVDA long-term
```

---

## 📝 License

MIT License - For educational purposes only.

---

## ⚠️ Disclaimer

**This application is for educational and demonstration purposes only.**

- Not financial advice
- Past performance does not guarantee future results
- Always consult a qualified financial advisor
- Do not make investment decisions based on this tool

---

## 🤝 Credits

- [CrewAI](https://github.com/joaomdmoura/crewAI) - Multi-agent framework
- [LangChain](https://langchain.com/) - LLM integration
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance API
- [Streamlit](https://streamlit.io/) - Web UI framework
- [Plotly](https://plotly.com/) - Interactive charts
