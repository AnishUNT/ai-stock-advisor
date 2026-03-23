import { useEffect, useRef } from 'react'
import { createChart, ColorType, CrosshairMode } from 'lightweight-charts'

export default function PriceChart({ history, sma20, sma50 }) {
  const containerRef = useRef(null)
  const chartRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current || !history?.length) return

    const chart = createChart(containerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: 'transparent' },
        textColor: '#64748b',
        fontSize: 11,
        fontFamily: "'DM Sans', sans-serif",
      },
      grid: {
        vertLines: { color: 'rgba(255,255,255,0.04)' },
        horzLines: { color: 'rgba(255,255,255,0.04)' },
      },
      crosshair: {
        mode: CrosshairMode.Normal,
        vertLine: { color: 'rgba(124,58,237,0.5)', labelBackgroundColor: '#7c3aed' },
        horzLine: { color: 'rgba(124,58,237,0.5)', labelBackgroundColor: '#7c3aed' },
      },
      rightPriceScale: {
        borderColor: 'rgba(255,255,255,0.06)',
      },
      timeScale: {
        borderColor: 'rgba(255,255,255,0.06)',
        timeVisible: true,
        secondsVisible: false,
      },
      width: containerRef.current.clientWidth,
      height: 380,
    })

    const candleSeries = chart.addCandlestickSeries({
      upColor: '#00d4aa',
      downColor: '#ef4444',
      borderUpColor: '#00d4aa',
      borderDownColor: '#ef4444',
      wickUpColor: 'rgba(0,212,170,0.6)',
      wickDownColor: 'rgba(239,68,68,0.6)',
    })
    candleSeries.setData(history)

    if (sma20?.length) {
      const s = chart.addLineSeries({ color: '#7c3aed', lineWidth: 1.5, title: 'SMA 20', priceLineVisible: false })
      s.setData(sma20)
    }
    if (sma50?.length) {
      const s = chart.addLineSeries({ color: '#f472b6', lineWidth: 1.5, title: 'SMA 50', priceLineVisible: false })
      s.setData(sma50)
    }

    chart.timeScale().fitContent()
    chartRef.current = chart

    const handleResize = () => {
      if (containerRef.current) {
        chart.applyOptions({ width: containerRef.current.clientWidth })
      }
    }
    const ro = new ResizeObserver(handleResize)
    ro.observe(containerRef.current)

    return () => {
      ro.disconnect()
      chart.remove()
    }
  }, [history, sma20, sma50])

  return <div ref={containerRef} className="w-full rounded-lg overflow-hidden" />
}
