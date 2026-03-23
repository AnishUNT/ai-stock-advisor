# api.py
"""FastAPI backend for AI Stock Advisor."""

import sys
import os

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI(title="AI Stock Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:4173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    ticker: str
    time_horizon: str = "short-term"


def _safe_float(v):
    if v is None:
        return None
    try:
        f = float(v)
        if np.isnan(f) or np.isinf(f):
            return None
        return round(f, 4)
    except Exception:
        return None


@app.get("/api/validate/{ticker}")
def validate_ticker(ticker: str):
    from stock_tools import is_valid_ticker
    valid = is_valid_ticker(ticker.upper().strip())
    return {"valid": valid, "ticker": ticker.upper().strip()}


@app.get("/api/stock/{ticker}")
def get_stock_data(ticker: str, horizon: str = Query("short-term")):
    ticker = ticker.upper().strip()
    from stock_tools import (
        get_stock_history, get_stock_info,
        calculate_technical_indicators, calculate_risk_score, fetch_stock_news
    )

    info = get_stock_info(ticker)
    history = get_stock_history(ticker, horizon)

    if history is None or history.empty:
        raise HTTPException(status_code=404, detail=f"No price data for {ticker}")

    indicators = calculate_technical_indicators(history)
    risk = calculate_risk_score(indicators, info)
    news = fetch_stock_news(ticker)

    # Serialize history to list of OHLCV dicts for lightweight-charts
    history_data = []
    for date, row in history.iterrows():
        try:
            date_str = pd.Timestamp(date).strftime('%Y-%m-%d')
            o = _safe_float(row['Open'])
            h = _safe_float(row['High'])
            l = _safe_float(row['Low'])
            c = _safe_float(row['Close'])
            if None not in (o, h, l, c):
                history_data.append({"time": date_str, "open": o, "high": h, "low": l, "close": c})
        except Exception:
            continue

    # SMA lines
    sma20 = []
    if len(history) >= 20:
        series = history['Close'].rolling(window=20).mean()
        for date, val in series.items():
            if not pd.isna(val):
                sma20.append({"time": pd.Timestamp(date).strftime('%Y-%m-%d'), "value": round(float(val), 2)})

    sma50 = []
    if len(history) >= 50:
        series = history['Close'].rolling(window=50).mean()
        for date, val in series.items():
            if not pd.isna(val):
                sma50.append({"time": pd.Timestamp(date).strftime('%Y-%m-%d'), "value": round(float(val), 2)})

    # Clean indicators
    clean_indicators = {}
    for k, v in indicators.items():
        if isinstance(v, (np.floating, np.integer)):
            clean_indicators[k] = _safe_float(v)
        else:
            clean_indicators[k] = v

    # Clean info
    clean_info = {}
    if info:
        for k, v in info.items():
            if isinstance(v, (np.floating, np.integer)):
                clean_info[k] = _safe_float(v)
            else:
                clean_info[k] = v

    return {
        "info": clean_info,
        "history": history_data,
        "sma20": sma20,
        "sma50": sma50,
        "indicators": clean_indicators,
        "risk": risk,
        "news": news,
    }


@app.post("/api/analyze")
def analyze(body: AnalyzeRequest):
    from main import run_analysis
    try:
        result = run_analysis(body.ticker.upper().strip(), body.time_horizon)
        return result.model_dump()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
