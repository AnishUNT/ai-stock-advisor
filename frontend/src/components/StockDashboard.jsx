import CompanyHeader from './CompanyHeader'
import MetricsGrid from './MetricsGrid'
import PriceChart from './PriceChart'
import RiskSection from './RiskSection'
import Recommendation from './Recommendation'
import NewsSection from './NewsSection'
import Skeleton from './Skeleton'

export default function StockDashboard({ ticker, stockData, recommendation, loading, loadingAI }) {
  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-24 rounded-2xl" />
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[...Array(4)].map((_, i) => <Skeleton key={i} className="h-20 rounded-xl" />)}
        </div>
        <Skeleton className="h-96 rounded-2xl" />
      </div>
    )
  }

  if (!stockData) return null

  const { info, history, sma20, sma50, indicators, risk, news } = stockData

  return (
    <div className="space-y-4">
      {/* Company Header */}
      <CompanyHeader ticker={ticker} info={info} indicators={indicators} />

      {/* Metrics Row */}
      <MetricsGrid indicators={indicators} risk={risk} />

      {/* Price Chart */}
      <div className="card p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="font-semibold text-slate-200">Price History</h2>
          <div className="flex items-center gap-4 text-xs text-slate-500">
            <span className="flex items-center gap-1.5">
              <span className="w-3 h-0.5 bg-[#7c3aed] inline-block rounded" />
              SMA 20
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-3 h-0.5 bg-[#f472b6] inline-block rounded" />
              SMA 50
            </span>
          </div>
        </div>
        <PriceChart history={history} sma20={sma20} sma50={sma50} />
      </div>

      {/* Risk + AI Recommendation */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <RiskSection risk={risk} />
        <Recommendation recommendation={recommendation} loading={loadingAI} />
      </div>

      {/* News */}
      {news?.length > 0 && <NewsSection news={news} />}
    </div>
  )
}
