function MetricCard({ label, value, sub, valueColor }) {
  return (
    <div className="card card-hover p-4">
      <div className="text-xs text-slate-500 mb-1">{label}</div>
      <div className={`text-xl font-mono font-bold ${valueColor || 'text-white'}`}>{value}</div>
      {sub && <div className="text-xs text-slate-600 mt-0.5">{sub}</div>}
    </div>
  )
}

export default function MetricsGrid({ indicators, risk }) {
  const change = indicators?.percent_change ?? 0
  const positive = change >= 0

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
      <MetricCard
        label="Period Change"
        value={`${positive ? '+' : ''}${change.toFixed(2)}%`}
        valueColor={positive ? 'text-[#00d4aa]' : 'text-red-400'}
        sub={positive ? '▲ Gained' : '▼ Lost'}
      />
      <MetricCard
        label="Trend"
        value={indicators?.trend?.toUpperCase() || '—'}
        valueColor={indicators?.trend === 'bullish' ? 'text-[#00d4aa]' : 'text-red-400'}
        sub="Based on SMAs"
      />
      <MetricCard
        label="Volatility"
        value={`${indicators?.volatility?.toFixed(2) || '—'}%`}
        sub="Daily avg"
      />
      <MetricCard
        label="Max Drawdown"
        value={`${indicators?.max_drawdown?.toFixed(2) || '—'}%`}
        valueColor="text-yellow-400"
        sub="From peak"
      />
    </div>
  )
}
