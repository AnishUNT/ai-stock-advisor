import { useState, useCallback } from 'react'
import Header from './components/Header'
import SearchBar from './components/SearchBar'
import StockDashboard from './components/StockDashboard'
import ErrorBanner from './components/ErrorBanner'

const API_BASE = 'http://localhost:8000'

export default function App() {
  const [loading, setLoading] = useState(false)
  const [loadingAI, setLoadingAI] = useState(false)
  const [stockData, setStockData] = useState(null)
  const [recommendation, setRecommendation] = useState(null)
  const [error, setError] = useState(null)
  const [currentTicker, setCurrentTicker] = useState(null)

  const handleAnalyze = useCallback(async (ticker, horizon) => {
    const t = ticker.toUpperCase().trim()
    setLoading(true)
    setError(null)
    setStockData(null)
    setRecommendation(null)
    setCurrentTicker(t)

    try {
      // Step 1: Validate ticker
      const vRes = await fetch(`${API_BASE}/api/validate/${t}`)
      const vData = await vRes.json()
      if (!vData.valid) {
        setError(`"${t}" is not a valid ticker symbol. Try AAPL, NVDA, MSFT, etc.`)
        setLoading(false)
        return
      }

      // Step 2: Fetch stock data + chart (fast)
      const sRes = await fetch(`${API_BASE}/api/stock/${t}?horizon=${horizon}`)
      if (!sRes.ok) {
        const err = await sRes.json()
        throw new Error(err.detail || 'Failed to fetch stock data')
      }
      const data = await sRes.json()
      setStockData(data)
      setLoading(false)

      // Step 3: Run AI analysis (slow — 30-60s)
      setLoadingAI(true)
      const aRes = await fetch(`${API_BASE}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: t, time_horizon: horizon }),
      })
      if (!aRes.ok) {
        const err = await aRes.json()
        throw new Error(err.detail || 'AI analysis failed')
      }
      const rec = await aRes.json()
      setRecommendation(rec)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
      setLoadingAI(false)
    }
  }, [])

  return (
    <div className="min-h-screen" style={{ background: '#0a0a12' }}>
      <Header />
      <main className="max-w-6xl mx-auto px-4 py-8 space-y-6">
        <SearchBar onAnalyze={handleAnalyze} loading={loading} />
        {error && <ErrorBanner message={error} onDismiss={() => setError(null)} />}
        {(loading || stockData) && (
          <StockDashboard
            ticker={currentTicker}
            stockData={stockData}
            recommendation={recommendation}
            loading={loading}
            loadingAI={loadingAI}
          />
        )}
      </main>
      <footer className="text-center py-8 text-slate-600 text-sm">
        Built with OpenAI &amp; React • Data from Yahoo Finance •{' '}
        <span className="text-yellow-600">For educational purposes only. Not financial advice.</span>
      </footer>
    </div>
  )
}
