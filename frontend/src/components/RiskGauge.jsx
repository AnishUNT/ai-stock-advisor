export default function RiskGauge({ score, level }) {
  // Semicircle gauge from 180° to 0° (left to right)
  // score 1-10 maps to angle 180° to 0°
  const clamp = Math.max(1, Math.min(10, score))
  const angleDeg = 180 - ((clamp - 1) / 9) * 180 // 180 at score=1, 0 at score=10

  const cx = 110, cy = 95, r = 72
  const toXY = (deg) => ({
    x: cx + r * Math.cos((deg * Math.PI) / 180),
    y: cy - r * Math.sin((deg * Math.PI) / 180),
  })

  // Arc path helper
  const arcPath = (startDeg, endDeg) => {
    const s = toXY(startDeg)
    const e = toXY(endDeg)
    const largeArc = Math.abs(endDeg - startDeg) > 180 ? 1 : 0
    // Going counterclockwise (sweep=0)
    return `M ${s.x} ${s.y} A ${r} ${r} 0 ${largeArc} 0 ${e.x} ${e.y}`
  }

  const needle = toXY(angleDeg)
  const color = level === 'Low' ? '#00d4aa' : level === 'Medium' ? '#fbbf24' : '#ef4444'

  // Tick labels
  const ticks = [
    { deg: 180, label: '1' },
    { deg: 120, label: '4' },
    { deg: 60, label: '7' },
    { deg: 0, label: '10' },
  ]

  return (
    <svg viewBox="0 0 220 130" className="w-64">
      {/* Background track */}
      <path d={arcPath(180, 0)} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="14" strokeLinecap="round" />

      {/* Colored sections */}
      <path d={arcPath(180, 120)} fill="none" stroke="rgba(0,212,170,0.35)" strokeWidth="14" />
      <path d={arcPath(120, 60)} fill="none" stroke="rgba(251,191,36,0.35)" strokeWidth="14" />
      <path d={arcPath(60, 0)} fill="none" stroke="rgba(239,68,68,0.35)" strokeWidth="14" />

      {/* Needle arc (progress) */}
      {angleDeg < 180 && (
        <path d={arcPath(180, angleDeg)} fill="none" stroke={color} strokeWidth="5" strokeLinecap="round" />
      )}

      {/* Tick marks */}
      {ticks.map(({ deg, label }) => {
        const inner = { x: cx + (r - 10) * Math.cos((deg * Math.PI) / 180), y: cy - (r - 10) * Math.sin((deg * Math.PI) / 180) }
        const labelPos = { x: cx + (r + 18) * Math.cos((deg * Math.PI) / 180), y: cy - (r + 18) * Math.sin((deg * Math.PI) / 180) }
        return (
          <text key={deg} x={labelPos.x} y={labelPos.y + 4} textAnchor="middle" fill="#475569" fontSize="9" fontFamily="monospace">
            {label}
          </text>
        )
      })}

      {/* Needle dot */}
      <circle cx={needle.x} cy={needle.y} r="5" fill={color} />
      <line x1={cx} y1={cy} x2={needle.x} y2={needle.y} stroke={color} strokeWidth="2.5" strokeLinecap="round" opacity="0.9" />
      <circle cx={cx} cy={cy} r="5" fill="#1a1a2e" stroke={color} strokeWidth="2" />

      {/* Score */}
      <text x={cx} y={cy + 22} textAnchor="middle" fill="white" fontSize="22" fontWeight="700" fontFamily="monospace">
        {score.toFixed(1)}
      </text>
      <text x={cx} y={cy + 36} textAnchor="middle" fill="#64748b" fontSize="10">
        {level} Risk
      </text>
    </svg>
  )
}
