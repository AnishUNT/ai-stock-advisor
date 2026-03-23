export default function ErrorBanner({ message, onDismiss }) {
  return (
    <div className="flex items-start gap-3 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400">
      <span className="text-lg mt-0.5">⚠️</span>
      <div className="flex-1 text-sm">{message}</div>
      <button onClick={onDismiss} className="text-red-500/60 hover:text-red-400 transition-colors text-lg leading-none">
        ×
      </button>
    </div>
  )
}
