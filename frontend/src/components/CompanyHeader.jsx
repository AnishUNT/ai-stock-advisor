export default function CompanyHeader({ ticker, info, indicators }) {
  const price = info?.current_price
  const prevClose = info?.previous_close
  const dayChange = price && prevClose ? ((price - prevClose) / prevClose * 100) : null
  const positive = (indicators?.percent_change ?? 0) >= 0

  return (
    <div className="card p-5 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#7c3aed]/30 to-[#00d4aa]/30 border border-white/10 flex items-center justify-center font-mono font-bold text-sm text-[#00d4aa]">
            {ticker?.slice(0, 2)}
          </div>
          <div>
            <h2 className="font-bold text-lg text-white leading-tight">{info?.name || ticker}</h2>
            <p className="text-slate-500 text-xs">{info?.sector || 'Equity'} • {ticker}</p>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap gap-6">
        {price && (
          <div className="text-right">
            <div className="text-2xl font-mono font-bold text-white">${price.toFixed(2)}</div>
            {dayChange !== null && (
              <div className={`text-sm font-mono ${dayChange >= 0 ? 'text-[#00d4aa]' : 'text-red-400'}`}>
                {dayChange >= 0 ? '▲' : '▼'} {Math.abs(dayChange).toFixed(2)}% today
              </div>
            )}
          </div>
        )}
        {info?.pe_ratio && (
          <div className="text-right">
            <div className="text-xs text-slate-500 mb-0.5">P/E Ratio</div>
            <div className="font-mono font-semibold text-white">{info.pe_ratio.toFixed(1)}</div>
          </div>
        )}
        {info?.market_cap && (
          <div className="text-right">
            <div className="text-xs text-slate-500 mb-0.5">Market Cap</div>
            <div className="font-mono font-semibold text-white">
              {info.market_cap >= 1e12
                ? `$${(info.market_cap / 1e12).toFixed(2)}T`
                : info.market_cap >= 1e9
                ? `$${(info.market_cap / 1e9).toFixed(1)}B`
                : `$${(info.market_cap / 1e6).toFixed(0)}M`}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
