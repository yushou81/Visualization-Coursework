import * as echarts from 'echarts'

const colorPalette = [
  '#ff6b6b',
  '#ffa500',
  '#ffee51',
  '#8c6ac4',
  '#715c87',
  '#e098c7',
  '#8fd3e8'
]

const theme = {
  color: colorPalette,
  title: {
    textStyle: {
      fontWeight: 'normal',
      color: '#e5e7eb'
    }
  },
  visualMap: {
    color: ['#ff715e', '#ffee51']
  },
  toolbox: {
    color: ['#fff']
  },
  tooltip: {
    backgroundColor: 'rgba(15,15,15,0.8)',
    borderColor: '#666',
    textStyle: { color: '#e5e7eb' }
  },
  legend: {
    textStyle: { color: '#e5e7eb' }
  },
  textStyle: {
    color: '#e5e7eb'
  },
  line: {
    symbol: 'circle'
  }
}

echarts.registerTheme('halloween', theme)

export default theme
