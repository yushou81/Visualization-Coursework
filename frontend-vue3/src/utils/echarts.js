import * as echarts from 'echarts'
import 'echarts-wordcloud'

export function useEcharts(dom, theme = 'light') {
  if (!dom) return null
  const instance = echarts.init(dom, theme)
  return instance
}

export { echarts }
