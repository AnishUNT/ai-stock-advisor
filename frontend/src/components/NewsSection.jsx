import { useState } from 'react'

export default function NewsSection({ news }) {
  const [expanded, setExpanded] = useState(false)
  const displayed = expanded ? news : news.slice(0, 3)

  return (
    <div className="card p-5 space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold text-slate-200">Latest News</h2>
        <span className="text-xs text-slate-600 bg-white/5 px-2 py-0.5 rounded-full">{news.length} articles</span>
      </div>

      <div className="space-y-2">
        {displayed.map((item, i) => (
          <a
            key={i}
            href={item.link}
            target="_blank"
            rel="noopener noreferrer"
            className="block p-3 rounded-xl bg-white/2 border border-white/5 hover:border-[#7c3aed]/30 hover:bg-[#7c3aed]/5 transition-all group"
          >
            <div className="text-sm text-slate-200 group-hover:text-white transition-colors leading-snug mb-1">
              {item.title}
            </div>
            <div className="flex items-center gap-2 text-xs text-slate-600">
              <span>{item.publisher}</span>
              <span>•</span>
              <span>{item.published}</span>
              <span className="ml-auto text-[#7c3aed] opacity-0 group-hover:opacity-100 transition-opacity">→</span>
            </div>
          </a>
        ))}
      </div>

      {news.length > 3 && (
        <button
          onClick={() => setExpanded(!expanded)}
          className="text-xs text-slate-500 hover:text-[#00d4aa] transition-colors w-full text-center py-1"
        >
          {expanded ? 'Show less ↑' : `Show ${news.length - 3} more ↓`}
        </button>
      )}
    </div>
  )
}
