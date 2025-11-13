const echarts = require('echarts/lib/echarts')

const colorPalette = [
  '#ff6b6b',
  '#ffa500',
  '#ffd93d',
  '#6bf178',
  '#4d96ff',
  '#8c54ff',
  '#ff92f4',
  '#ffab76'
]

const axisCommon = {
  axisLine: {
    lineStyle: {
      color: '#9fa8da'
    }
  },
  axisTick: {
    lineStyle: {
      color: '#9fa8da'
    }
  },
  axisLabel: {
    color: '#f2f2f2'
  },
  splitLine: {
    lineStyle: {
      color: 'rgba(255, 255, 255, 0.15)'
    }
  },
  splitArea: {
    areaStyle: {
      color: ['rgba(255, 255, 255, 0.02)', 'rgba(255, 255, 255, 0.05)']
    }
  }
}

const theme = {
  color: colorPalette,
  backgroundColor: '#0f0f1a',
  textStyle: {
    color: '#f8f8f2'
  },
  title: {
    textStyle: {
      color: '#ffe066',
      fontWeight: 'normal'
    },
    subtextStyle: {
      color: '#cfd8dc'
    }
  },
  line: Object.assign({
    smooth: true,
    symbol: 'circle',
    symbolSize: 6
  }, axisCommon),
  bar: Object.assign({
    barMaxWidth: 20
  }, axisCommon),
  pie: {
    itemStyle: {
      normal: {
        borderColor: '#0f0f1a',
        borderWidth: 1
      }
    }
  },
  radar: Object.assign({
    name: {
      textStyle: {
        color: '#ffe066'
      }
    }
  }, axisCommon),
  toolbox: {
    iconStyle: {
      normal: {
        borderColor: '#f2f2f2'
      }
    }
  },
  legend: {
    textStyle: {
      color: '#f2f2f2'
    }
  },
  tooltip: {
    backgroundColor: 'rgba(20, 20, 35, 0.95)',
    axisPointer: {
      lineStyle: {
        color: '#ffe066'
      },
      crossStyle: {
        color: '#ffe066'
      }
    }
  },
  timeline: {
    lineStyle: {
      color: '#6bf178'
    },
    itemStyle: {
      normal: {
        color: '#6bf178',
        borderWidth: 1
      }
    },
    controlStyle: {
      normal: {
        color: '#6bf178',
        borderColor: '#6bf178'
      }
    }
  },
  visualMap: {
    color: ['#ff6b6b', '#ffa500', '#ffd93d']
  }
}

if (echarts && echarts.registerTheme) {
  echarts.registerTheme('halloween', theme)
}
