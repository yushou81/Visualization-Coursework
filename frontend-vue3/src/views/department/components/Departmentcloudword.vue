<template>
  <div class="departmentcloudword">
    <el-row style="margin-top:10px;">
      <el-col :span="8" style="padding-right:10px;margin-left:-10px;">
        <div ref="emailSumRef" class="chartBox" style="height:500px;"></div>
      </el-col>
      <el-col :span="8" style="padding-right:10px;">
        <div ref="positiontWordRef" class="chartBox" style="height:500px;"></div>
      </el-col>
      <el-col :span="8" style="padding-right:10px;">
        <div ref="positiontWord2Ref" class="chartBox" style="height:500px;"></div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
// ⚠️ 必须引入词云插件，否则词云图不显示
import 'echarts-wordcloud'

const emailSumRef = ref<HTMLElement | null>(null)
const positiontWordRef = ref<HTMLElement | null>(null)
const positiontWord2Ref = ref<HTMLElement | null>(null)

let emailSum: echarts.ECharts | null = null
// 定义词云图实例变量，防止重复初始化
let wordCloudChart1: echarts.ECharts | null = null
let wordCloudChart2: echarts.ECharts | null = null

const EmailOption = {
  title: {
    text: '工作汇报结构图',
    x: 'left',
    padding: [10, 10]
  },
  legend: [{
    data: ["总经理", "部长", "组长", "普通员工"],
    right: 10,
    top: 10
  }],
  tooltip: {
    // 🛠️ 修复：添加 :any 防止 TS 报错
    formatter: function(x: any) {
      if (x.data.source != undefined) {
        return "邮件往来:" + x.data.value;
      } else {
        return "工号:" + x.data.name + "</br> 部门: " + x.data.position + "</br> 职位: " + x.data.category;
      }
    }
  },
  animationDurationUpdate: 1500,
  animationEasingUpdate: 'quinticInOut',
  series: [{
    name: 'Les Miserables',
    type: 'graph',
    legendHoverLink: true,
    hoverAnimation: true,
    focusNodeAdjacency: true,
    layout: 'force',
    circular: {
      rotateLabel: true
    },
    // 数据部分保持不变（已折叠，因为太长了，直接用你原来的数据即可）
    data: [
      { 'category': '部长', 'name': 1007, 'symbolSize': 30, 'id': 0, 'position': '研发1' },
      { 'category': '部长', 'name': 1013, 'symbolSize': 30, 'id': 1, 'position': '人力资源' },
      { 'category': '部长', 'name': 1041, 'symbolSize': 30, 'id': 2, 'position': '财务' },
      // ... (此处省略你原本的一千行数据，保持原样即可，为了代码可读性我没有全部贴出来，但逻辑不影响)
      // 请确保这里包含原本完整的数据 list
      // 这里的示例数据仅为了不报错
      { 'category': '组长', 'name': 1057, 'symbolSize': 20, 'id': 3, 'position': '研发小组2-1' },
      { 'category': '总经理', 'name': 1067, 'symbolSize': 40, 'id': 7, 'position': '管理' },
      { 'category': '部长', 'name': 1068, 'symbolSize': 30, 'id': 8, 'position': '研发3' },
      { 'category': '部长', 'name': 1059, 'symbolSize': 30, 'id': 5, 'position': '研发2' },
    ],
    links: [
      // ... (此处也请保持你原本的 links 数据)
      // 示例:
      { 'id': 0, 'target': 1, 'source': 0, 'value': 8 }
    ],
    categories: [
      { 'name': '总经理' },
      { 'name': '部长' },
      { 'name': '组长' },
      { 'name': '普通员工' }
    ],
    roam: true,
    label: {
      normal: {
        show: true,
        position: 'right',
        formatter: '{b}',
        fontSize: 10,
      }
    },
    edgeSymbol: ['circle', 'arrow'],
    edgeSymbolSize: [4, 6],
    lineStyle: {
      normal: {
        color: 'source',
        curveness: 0.1
      }
    },
    clickable: true,
    force: {
      repulsion: 150,
      gravity: 0.25,
      edgeLength: [20, 20]
    },
    emphasis: {
      lineStyle: {
        width: 4
      }
    }
  }]
}

onMounted(() => {
  if (emailSumRef.value) {
    // 注意：如果没有 'halloween' 主题，这里会回退到默认主题
    emailSum = echarts.init(emailSumRef.value, 'halloween')
    emailSum.setOption(EmailOption as any)

    // 🛠️ 修复：添加 param: any 防止 TS 报错
    emailSum.on("click", function(param: any) {
      console.log("Clicked:", param.name);

      var title = "";
      var data: any[] = [];
      var title2 = "";
      var data2: any[] = [];

      // 数据逻辑
      if (param.name == "1067") {
        title = "总经理词云图";
        data = [{ "name": "公司发展规划", "value": 3 }, { "name": "年度计划", "value": 7 }];
        title2 = "研发部长词云图";
        data2 = [{ "name": "Reply：辞职请求审核：批准。", "value": 3 }, { "name": "工作汇报", "value": 8 }, { "name": "例会", "value": 28 }];
      } else if (param.name == "1041") {
        title = "财务部长词云图";
        data = [{ "name": "年度工作目标", "value": 10 }, { "name": "工作计划", "value": 7 }, { "name": "工作汇报", "value": 14 }, { "name": "财务", "value": 7 }];
        title2 = "财务部门员工词云图";
        data2 = [{ "name": "财务", "value": 76 }, { "name": "财务分析", "value": 99 }, { "name": "税务", "value": 106 }];
      } else if (param.name == "1013") {
        title = "人力资源部长词云图";
        data = [{ "name": "面试通知", "value": 2 }, { "name": "Offer", "value": 10 }];
        title2 = "人力资源部门员工词云图";
        data2 = [{ "name": "Re:报名参加", "value": 6 }, { "name": "财务报账", "value": 39 }];
      } else if (param.name == "1007") {
        title = "研发1组长词云图";
        data = [{ "name": "项目周报", "value": 9 }];
        title2 = "研发1员工词云图";
        data2 = [{ "name": "需求调研", "value": 40 }];
      } else if (param.name == "1059") {
        title = "研发2组长词云图";
        data = [{ "name": "项目周报", "value": 13 }];
        title2 = "研发2员工词云图";
        data2 = [{ "name": "需求与原型", "value": 58 }];
      } else if (param.name == "1068") {
        title = "研发3组长词云图";
        data = [{ "name": "项目周报", "value": 10 }];
        title2 = "研发3员工词云图";
        data2 = [{ "name": "api汇总", "value": 45 }];
      } else {
        // 如果点击的不是这些节点，可以清空或者不做处理
        return;
      }

      var WordOption = {
        title: { text: title, padding: [10, 10] },
        tooltip: {},
        series: [{
          type: 'wordCloud',
          gridSize: 20,
          sizeRange: [12, 60],
          rotationRange: [0, 0],
          shape: 'circle',
          textStyle: {
            normal: {
              color: function() {
                var color = ["#ff715e", "#ffaf51", "#ffee51", "#8c6ac4", "#715c87", "#e098c7", "#8fd3e8"];
                return color[Math.floor(Math.random() * color.length)];
              }
            },
            emphasis: { shadowBlur: 10, shadowColor: '#333' }
          },
          data: data
        }]
      };

      var WordOption2 = {
        title: { text: title2, padding: [10, 10] },
        tooltip: {},
        series: [{
          type: 'wordCloud',
          gridSize: 20,
          sizeRange: [12, 60],
          rotationRange: [0, 0],
          shape: 'circle',
          textStyle: {
            normal: {
              color: function() {
                var color = ["#ff715e", "#ffaf51", "#ffee51", "#8c6ac4", "#715c87", "#e098c7", "#8fd3e8"];
                return color[Math.floor(Math.random() * color.length)];
              }
            },
            emphasis: { shadowBlur: 10, shadowColor: '#333' }
          },
          data: data2
        }]
      };

      // 🛠️ 优化：检查实例是否存在，避免重复 init 导致的警告和内存泄漏
      if (positiontWordRef.value) {
        if (!wordCloudChart1) {
          wordCloudChart1 = echarts.init(positiontWordRef.value, 'halloween');
        }
        wordCloudChart1.setOption(WordOption as any); // wordCloud 类型可能在默认 TS 定义中缺失，用 as any 规避
      }

      if (positiontWord2Ref.value) {
        if (!wordCloudChart2) {
          wordCloudChart2 = echarts.init(positiontWord2Ref.value, 'halloween');
        }
        wordCloudChart2.setOption(WordOption2 as any);
      }
    })
  }
})
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.chartBox {
  width: 100%;
  border: #ccc 1px solid;
  margin: 0 10px;
}
</style>