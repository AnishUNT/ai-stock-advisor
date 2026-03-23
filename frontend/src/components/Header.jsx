export default function Header() {
  return (
    <header className="border-b border-white/5 bg-black/30 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-[#7c3aed] to-[#00d4aa] flex items-center justify-center text-white font-bold text-sm">
            AI
          </div>
          <span className="font-mono font-bold text-lg gradient-text">AI Stock Advisor</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="px-2 py-0.5 rounded-full text-xs font-semibold bg-gradient-to-r from-[#7c3aed]/20 to-[#f472b6]/20 border border-[#7c3aed]/30 text-[#c084fc]">
            BETA
          </span>
          <span className="text-slate-500 text-sm hidden sm:inline">Multi-agent AI analysis</span>
        </div>
      </div>
    </header>
  )
}
