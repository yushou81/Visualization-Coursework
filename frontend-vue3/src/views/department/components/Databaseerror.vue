<template>
<div class="databaseerror">
  <div ref="databaseerrorRef" style="width:100%; height:500px;"></div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const databaseerrorRef = ref<HTMLElement | null>(null)
let databaseerror: echarts.ECharts | null = null

const depOption = {
  title: {
    text: '70服务器崩溃事件',
    padding: [10, 10]
  },
  tooltip: {
    trigger: 'axis',
    // 添加 :any 防止 TS 报错
    formatter: function(x: any) {
      console.log(x);
      var str = x[0].name + "</br>";
      for (var i = 0; i < x.length; i++) {
        if (x[i].data != undefined) {
          str += x[i].seriesName + " : " + x[i].data + "</br>";
        }
      }
      return str;
    }
  },
  legend: {
    data: ['1376_download', '1487_download', '1080_download', '1284_download',
      '1376_upload', '1487_upload', '1080_upload', '1284_upload'
    ],
    right: 10,
    top: 10,
    left: 320
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: ["16日下午7:22", "16日下午7:33", "16日下午7:49", "16日下午8:00", "16日下午8:04",
      "16日下午8:19", "16日下午8:31", "16日下午8:36", "16日下午8:40", "16日下午8:54",
      "16日下午9:17", "16日下午9:45", "16日下午9:47", "16日下午10:04", "16日下午11:22"]
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      name: '1376_download',
      type: 'line',
      markArea: {
        silent: true,
        itemStyle: {
          normal: {
            color: 'transparent',
            borderWidth: 1,
            borderType: 'dashed'
          }
        },
        data: [
          [{
            name: 'alert@hightech.com报警区间',
            xAxis: "16日下午8:00",
            yAxis: '0'
          }, {
            xAxis: "16日下午8:31",
            yAxis: 'max'
          }]
        ]
      },
      // ✅ 修复：将空位填充为 null
      data: [14567, 862, 600013884, 120006184, 90007539, 7156, null, null, null, null, null, null, null, null, null]
    },
    {
      name: '1487_download',
      type: 'line',
      // ✅ 修复：将空位填充为 null
      data: [null, null, null, null, null, null, 8791, 120006971, 114, 180005414, null, null, null, null, null]
    },
    {
      name: '1080_download',
      type: 'line',
      // ✅ 修复：将空位填充为 null
      data: [null, null, null, null, null, null, null, null, null, 2205, null, null, null, null, null]
    },
    {
      name: '1284_download',
      type: 'line',
      // ✅ 修复：将空位填充为 null
      data: [null, null, null, null, null, null, null, null, null, null, null, 210010078, 210002407, 8495, 6312]
    },
    {
      name: '1376_upload',
      type: 'line',
      // ✅ 修复：将空位填充为 null
      data: [90012335, 90006941, 13993, 9854, 30010003, 21000407, null, null, null, null, null, null, null, null, null]
    },
    {
      name: '1487_upload',
      type: 'line',
      // ✅ 修复：将空位填充为 null
      data: [null, null, null, null, null, null, 120010452, 9057, 60008657, 4342, null, null, null, null, null]
    },
    {
      name: '1080_upload',
      type: 'line',
      // ✅ 修复：将空位填充为 null
      data: [null, null, null, null, null, null, null, null, null, null, 1537, null, null, null, null]
    },
    {
      name: '1284_upload',
      type: 'line',
      // ✅ 修复：将空位填充为 null
      data: [null, null, null, null, null, null, null, null, null, null, null, 120017301, 5767, 360008782, 4756]
    }
  ]
} // ✅ 这里正确结束 depOption 对象，之前你这里后面多了两个 }

onMounted(() => {
  if (databaseerrorRef.value) {
    databaseerror = echarts.init(databaseerrorRef.value, 'halloween')
    // 添加 as any 避免类型检查报错
    databaseerror.setOption(depOption as any)
  }
})
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.databaseerror {
    border: #ccc 1px solid;
    // margin-right: 10px;
}
</style>
