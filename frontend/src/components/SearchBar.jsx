import { useState } from 'react'

const DEMO_TICKERS = ['AAPL', 'NVDA', 'MSFT', 'TSLA', 'GOOGL', 'AMZN']

export default function SearchBar({ onAnalyze, loading }) {
  const [ticker, setTicker] = useState('')
  const [horizon, setHorizon] = useState('short-term')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!ticker.trim() || loading) return
    onAnalyze(ticker.trim(), horizon)
  }

  const handleDemo = (t) => {
    setTicker(t)
    onAnalyze(t, horizon)
  }

  return (
    <div className="card p-6 space-y-5">
      {/* Title */}
      <div className="text-center space-y-1">
        <h1 className="text-3xl sm:text-4xl font-mono font-bold gradient-text">
          AI Stock Advisor
        </h1>
        <p className="text-slate-400 text-sm">
          Multi-agent analysis powered by OpenAI • Real-time data from Yahoo Finance
        </p>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500 text-sm font-mono">
            $
          </span>
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
            placeholder="AAPL, NVDA, MSFT..."
            maxLength={10}
            className="w-full bg-[#1a1a2e] border border-white/10 rounded-xl px-4 py-3 pl-8 text-white placeholder-slate-600 font-mono text-sm focus:outline-none focus:border-[#7c3aed]/60 transition-colors"
          />
        </div>

        <select
          value={horizon}
          onChange={(e) => setHorizon(e.target.value)}
          className="bg-[#1a1a2e] border border-white/10 rounded-xl px-4 py-3 text-white text-sm focus:outline-none focus:border-[#7c3aed]/60 transition-colors cursor-pointer"
        >
          <option value="short-term">Short-term (6 months)</option>
          <option value="long-term">Long-term (5 years)</option>
        </select>

        <button
          type="submit"
          disabled={!ticker.trim() || loading}
          className="px-6 py-3 rounded-xl font-semibold text-sm text-white transition-all disabled:opacity-40 disabled:cursor-not-allowed"
          style={{
            background: loading
              ? 'rgba(124,58,237,0.5)'
              : 'linear-gradient(135deg, #7c3aed, #00d4aa)',
          }}
        >
          {loading ? (
            <span className="flex items-center gap-2">
              <svg className="animate-spin-slow w-4 h-4" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
              </svg>
              Loading...
            </span>
          ) : (
            'Analyze →'
          )}
        </button>
      </form>

      {/* Quick picks */}
      <div className="flex flex-wrap gap-2 items-center">
        <span className="text-slate-600 text-xs">Quick pick:</span>
        {DEMO_TICKERS.map((t) => (
          <button
            key={t}
            onClick={() => handleDemo(t)}
            disabled={loading}
            className="px-3 py-1 rounded-lg text-xs font-mono border border-white/8 text-slate-400 hover:border-[#00d4aa]/40 hover:text-[#00d4aa] transition-colors disabled:opacity-40"
          >
            {t}
          </button>
        ))}
      </div>

      {/* Info pills */}
      <div className="flex flex-wrap gap-3 justify-center pt-1">
        {[
          ['🤖', '2 AI Agents'],
          ['📊', 'Real-time Data'],
          ['⚡', '~30-60s Analysis'],
        ].map(([icon, label]) => (
          <span
            key={label}
            className="flex items-center gap-1.5 text-xs text-slate-500 bg-white/3 px-3 py-1.5 rounded-full border border-white/5"
          >
            <span>{icon}</span>
            <span>{label}</span>
          </span>
        ))}
      </div>
    </div>
  )
}
