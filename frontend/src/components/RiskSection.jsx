import RiskGauge from './RiskGauge'

export default function RiskSection({ risk }) {
  const levelColor = {
    Low: '#00d4aa',
    Medium: '#fbbf24',
    High: '#ef4444',
  }[risk?.level] || '#94a3b8'

  return (
    <div className="card p-5 space-y-4">
      <h2 className="font-semibold text-slate-200">Risk Assessment</h2>

      <div className="flex flex-col items-center">
        <RiskGauge score={risk?.score || 5} level={risk?.level || 'Medium'} />
      </div>

      {risk?.factors?.length > 0 && (
        <div className="space-y-2">
          <div className="text-xs text-slate-500 uppercase tracking-wider">Risk Factors</div>
          {risk.factors.map((f, i) => (
            <div key={i} className="flex items-start gap-2 text-sm text-slate-300">
              <span style={{ color: levelColor }} className="mt-0.5 shrink-0">●</span>
              <span>{f}</span>
            </div>
          ))}
        </div>
      )}

      {(!risk?.factors || risk.factors.length === 0) && (
        <p className="text-sm text-slate-500">No significant risk factors identified.</p>
      )}
    </div>
  )
}
