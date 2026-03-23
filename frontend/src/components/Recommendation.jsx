import Skeleton from './Skeleton'

const ACTION_STYLES = {
  BUY: {
    bg: 'bg-[#00d4aa]/10',
    border: 'border-[#00d4aa]/40',
    text: 'text-[#00d4aa]',
    badge: 'bg-[#00d4aa]/20 text-[#00d4aa]',
    icon: '🟢',
  },
  HOLD: {
    bg: 'bg-yellow-400/10',
    border: 'border-yellow-400/40',
    text: 'text-yellow-400',
    badge: 'bg-yellow-400/20 text-yellow-400',
    icon: '🟡',
  },
  SELL: {
    bg: 'bg-red-500/10',
    border: 'border-red-500/40',
    text: 'text-red-400',
    badge: 'bg-red-500/20 text-red-400',
    icon: '🔴',
  },
}

export default function Recommendation({ recommendation, loading }) {
  if (loading) {
    return (
      <div className="card p-5 space-y-4">
        <h2 className="font-semibold text-slate-200">AI Recommendation</h2>
        <div className="flex flex-col items-center justify-center py-8 space-y-3 text-slate-500">
          <svg className="animate-spin-slow w-8 h-8 text-[#7c3aed]" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
          <p className="text-sm">Running AI analysis...</p>
          <p className="text-xs text-slate-600">This takes 30-60 seconds</p>
        </div>
        <Skeleton className="h-4 rounded" />
        <Skeleton className="h-4 rounded w-4/5" />
        <Skeleton className="h-4 rounded w-3/5" />
      </div>
    )
  }

  if (!recommendation) {
    return (
      <div className="card p-5 flex flex-col items-center justify-center py-12 text-slate-600 space-y-2">
        <span className="text-3xl">🤖</span>
        <p className="text-sm">AI recommendation will appear here</p>
      </div>
    )
  }

  const style = ACTION_STYLES[recommendation.action] || ACTION_STYLES.HOLD

  return (
    <div className="card p-5 space-y-4">
      <h2 className="font-semibold text-slate-200">AI Recommendation</h2>

      {/* Action badge */}
      <div className={`rounded-xl p-4 border ${style.bg} ${style.border} flex items-center justify-between`}>
        <div className="flex items-center gap-3">
          <span className="text-2xl">{style.icon}</span>
          <div>
            <div className={`text-2xl font-mono font-bold ${style.text}`}>{recommendation.action}</div>
            <div className="text-xs text-slate-500">{recommendation.company_name}</div>
          </div>
        </div>
        <div className="text-right">
          <div className={`text-sm font-semibold px-2 py-1 rounded-lg ${style.badge}`}>
            {recommendation.confidence} confidence
          </div>
          <div className="text-xs text-slate-500 mt-1">{recommendation.confidence_score}%</div>
        </div>
      </div>

      {/* Rationale */}
      <p className="text-sm text-slate-300 leading-relaxed">{recommendation.rationale}</p>

      {/* Bull/Bear */}
      <div className="grid grid-cols-1 gap-3">
        {recommendation.bull_case?.length > 0 && (
          <div className="space-y-1.5">
            <div className="text-xs font-semibold text-[#00d4aa] uppercase tracking-wider">Bull Case</div>
            {recommendation.bull_case.map((point, i) => (
              <div key={i} className="flex items-start gap-2 text-xs text-slate-400">
                <span className="text-[#00d4aa] mt-0.5 shrink-0">✓</span>
                {point}
              </div>
            ))}
          </div>
        )}
        {recommendation.bear_case?.length > 0 && (
          <div className="space-y-1.5">
            <div className="text-xs font-semibold text-yellow-500 uppercase tracking-wider">Bear Case</div>
            {recommendation.bear_case.map((point, i) => (
              <div key={i} className="flex items-start gap-2 text-xs text-slate-400">
                <span className="text-yellow-500 mt-0.5 shrink-0">⚠</span>
                {point}
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Disclaimer */}
      <div className="text-xs text-slate-600 border-t border-white/5 pt-3 leading-relaxed">
        ⚠ {recommendation.disclaimer}
      </div>
    </div>
  )
}
