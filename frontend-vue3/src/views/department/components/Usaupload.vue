<template>
<div class="usaupload">
  <div ref="usauploadRef" style="width:100%; height:500px;"></div>
</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const usauploadRef = ref<HTMLElement | null>(null)
let usaupload: echarts.ECharts | null = null

// 1. 定义好每个用户对应的数据和颜色
// 这样拆分后，图例 (Legend) 就能自动识别并控制每一组数据了
const seriesData = [
  {
    name: '1487',
    color: '#ff715e',
    data: [["24日12:44", "1487", "10.64.105.4", "10.50.50.43", "10.50.50.44", "13.250.177.223", "572MB"]]
  },
  {
    name: '1273',
    color: '#ffaf51',
    data: [["21日13:31", "1273", "10.64.105.244", "10.50.50.49", "10.50.50.34", "13.250.177.223", "19MB"]]
  },
  {
    name: '1183',
    color: '#ffee51',
    data: [["17日14:50", "1183", "10.64.105.165", "10.7.133.20", "10.50.50.40", "13.250.177.223", "19MB"]]
  },
  {
    name: '1169',
    color: '#8c6ac4',
    data: [["27日21:03", "1169", "10.64.105.199", "10.50.50.37", "10.50.50.46", "13.250.177.223", "19MB"]]
  },
  {
    name: '1151',
    color: '#715c87',
    data: [["30日17:19", "1151", "10.64.105.73", "10.50.50.49", "10.7.133.16", "13.250.177.223", "19MB"]]
  }
]

const depOption = {
  backgroundColor: '#080b1a', // 深色背景

  title: {
    text: "五人团伙泄密事件",
    padding: [10, 10],
    textStyle: { color: '#eee' }
  },

  // 2. 配置图例 (Legend)
  // 必须确保 data 里的名字和 series 里的 name 完全一致
  legend: {
    top: 50,
    data: ['1487', '1273', '1183', '1169', '1151'],
    itemGap: 20,
    textStyle: {
      color: '#ccc', // 图例文字颜色
      fontSize: 12
    }
  },

  // 3. Tooltip 配置 (显示详细信息)
  tooltip: {
    trigger: 'item',
    padding: 10,
    backgroundColor: 'rgba(50,50,50,0.9)',
    borderColor: '#777',
    borderWidth: 1,
    textStyle: { color: '#fff' },
    formatter: function (params: any) {
      const dimensions = ["时间", "用户", "源IP", "跳板机1", "跳板机2", "目的IP", "上传流量"];
      let html = `<div style="font-weight:bold; border-bottom:1px solid rgba(255,255,255,0.3); margin-bottom:5px; padding-bottom:5px;">
                    用户: ${params.seriesName}
                  </div>`;

      // params.data 就是当前行的数据数组
      dimensions.forEach((name, index) => {
        const dot = `<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;background-color:${params.color};"></span>`;
        html += `${dot} ${name}: ${params.data[index]}<br/>`;
      });
      return html;
    }
  },

  parallel: {
    bottom: 30,
    left: 40,
    right: 40,
    top: 100,
    parallelAxisDefault: {
      type: 'category',
      axisLabel: {
        rotate: -45,
        color: '#aaa',
        fontSize: 10
      },
      axisLine: {
        lineStyle: { color: '#555' }
      }
    }
  },

  parallelAxis: [
    { dim: 0, name: '时间', data: ["17日14:50", "21日13:31", "24日12:44", "27日21:03", "30日17:19"] },
    { dim: 1, name: '用户', data: ["1487", "1273", "1183", "1169", "1151"] },
    { dim: 2, name: '源IP', data: ["10.64.105.4", "10.64.105.73", "10.64.105.165", "10.64.105.199", "10.64.105.244"] },
    { dim: 3, name: '跳板机1', data: ["10.7.133.20", "10.50.50.37", "10.50.50.43", "10.50.50.49"] },
    { dim: 4, name: '跳板机2', data: ["10.7.133.16", "10.50.50.34", "10.50.50.40", "10.50.50.44", "10.50.50.46"] },
    { dim: 5, name: '目的IP', data: ["13.250.177.223"] },
    { dim: 6, name: '上传流量', data: ["19MB", "572MB"] }
  ],

  // 4. 将处理好的 multiple series 放入配置
  // 使用 map 自动生成 5 个 series 对象
  series: seriesData.map(item => ({
    name: item.name,
    type: 'parallel',
    lineStyle: {
      width: 3,
      opacity: 0.8,
      color: item.color // 直接使用该系列的颜色
    },
    data: item.data
  }))
}

onMounted(() => {
  if (usauploadRef.value) {
    usaupload = echarts.init(usauploadRef.value)
    usaupload.setOption(depOption)
  }
})
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.usaupload {
    border: #ccc 1px solid;
    // margin-right: 10px;
}
</style>
