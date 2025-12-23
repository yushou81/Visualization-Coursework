<template>
  <div class="personal-page app-container">
    <el-card shadow="hover" class="search-card">
      <div class="search-header">
        <div class="title">员工信息查询</div>
        <el-alert
          v-if="serverDown"
          title="抱歉，后台服务器已关闭，无法查询员工个人信息！"
          type="warning"
          show-icon
          class="server-alert"
        />
      </div>

      <el-row :gutter="20" align="middle">
        <el-col :xs="24" :sm="24" :md="14" :lg="16">
          <el-form class="search-form" @submit.prevent>
            <el-form-item label="员工编号">
              <el-input
                v-model="id"
                placeholder="请输入员工编号"
                clearable
                @keyup.enter="fetchData(id)"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="fetchData(id)">搜索一下</el-button>
            </el-form-item>
          </el-form>
        </el-col>
        <el-col :xs="24" :sm="24" :md="10" :lg="8">
          <div class="basic-card">
            <div class="info-row">
              <span class="label">员工编号</span>
              <span class="value">{{ id || '-' }}</span>
            </div>
            <div class="info-row">
              <span class="label">所处部门</span>
              <span class="value">{{ data.department.department || '-' }}</span>
            </div>
            <div class="info-row">
              <span class="label">职位</span>
              <span class="value">{{ data.department.position || '-' }}</span>
            </div>
            <div class="info-row">
              <span class="label">工位IP</span>
              <span class="value">{{ data.ip || '-' }}</span>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>

    <el-row :gutter="20" class="section-row">
      <el-col :xs="24" :sm="12" :md="12" :lg="6">
        <el-card shadow="hover" class="chart-card">
          <div id="chartWord" class="chart-box medium"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="12" :lg="6">
        <el-card shadow="hover" class="chart-card">
          <div id="emailWord" class="chart-box medium"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="12" :lg="6">
        <el-card shadow="hover" class="chart-card">
          <div id="emailRecWord" class="chart-box medium"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="12" :md="12" :lg="6">
        <el-card shadow="hover" class="chart-card">
          <div id="webPie" class="chart-box medium"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="section-row">
      <el-col :xs="24" :sm="24" :md="12" :lg="8">
        <el-card shadow="hover" class="chart-card">
          <div id="checkTime" class="chart-box large"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="12" :lg="16">
        <el-card shadow="hover" class="chart-card">
          <div id="loginParallel" class="chart-box large"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="section-row">
      <el-col :xs="24" :sm="24" :md="24" :lg="12">
        <el-card shadow="hover" class="chart-card">
          <div id="upDownFlow" class="chart-box large"></div>
        </el-card>
      </el-col>
      <el-col :xs="24" :sm="24" :md="24" :lg="12">
        <el-card shadow="hover" class="chart-card">
          <div id="protoFlow" class="chart-box large"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import request from '@/utils/request'
import * as echarts from 'echarts'

import 'echarts-wordcloud'


export default {
  name: 'personal',
  data() {
    return {
      serverDown: false,
      chartWord: "",
      emailWord: "",
      emailRecWord: "",
      loginParallel: "",
      webPie: '',
      checkTime: "",
      upDownFlow: "",
      protoFlow: "",
      id: "",
      data: {
        ip: "",
        department: {
          department: "",
          position: ""
        }
      }

    }
  },
  created() {},
  methods: {
    initChart(refName, domId) {
      if (this[refName] && this[refName].dispose) {
        this[refName].dispose()
      }
      const dom = document.getElementById(domId)
      if (!dom) return null
      this[refName] = echarts.init(dom, 'halloween')
      return this[refName]
    },
    fetchData(params) {;
      if (params > 1000 && params < 1600) {
        var url = "/" + params;
        request({
          url: url,
          method: 'get'
        }).then(response => {
          console.log(response);
          this.serverDown = false;
          if (response.data.ip == null) {
            this.$message.error('查无此人');
            this.data = {
              ip: "",
              department: {
                department: "",
                position: ""
              }
            };
          } else {
            this.data = response.data;
            this.domainWord(this.data.domain);
            this.EmailWord(this.data.email_subject);
            this.WebPie(this.data.tag_count);
            this.CheckTime(this.data.check_day_time);
            this.EmailRecWord(this.data.receive_email_subject);
            this.NetworkFlow();
            this.LoginParallel();
          }

        }).catch( error => {
          this.serverDown = true;
          this.$message.error('抱歉，服务器已经关闭！');
        })
      } else {
        this.$message.error('请输入正确的id');
      }

    },
    domainWord(params) {
      var option = {
        title: {
          text: "访问域名词云图",
          padding: [10, 10]
        },
        tooltip: {},
        series: [{
          type: 'wordCloud',
          gridSize: 20,
          sizeRange: [12, 50],
          rotationRange: [0, 0],
          shape: 'circle',
          textStyle: {
            normal: {
              color: function() {
                var color = [
                  "#ff715e",
                  "#ffaf51",
                  "#ffee51",
                  "#8c6ac4",
                  "#715c87",
                  "#e098c7",
                  "#8fd3e8"
                ];
                var x = Math.round(Math.random() * 5);
                return color[x];
              }
            },
            emphasis: {
              shadowBlur: 10,
              shadowColor: '#333'
            }
          },
          data: params
        }]
      };

      const chart = this.initChart('chartWord', 'chartWord')
      chart && chart.setOption(option)
    },

    EmailWord(params) {
      var option = {
        title: {
          text: "邮件发送主题词云图",
          padding: [10, 10]
        },
        tooltip: {},
        series: [{
          type: 'wordCloud',
          gridSize: 20,
          sizeRange: [12, 50],
          rotationRange: [0, 0],
          shape: 'circle',
          textStyle: {
            normal: {
              color: function() {
                var color = [
                  "#ff715e",
                  "#ffaf51",
                  "#ffee51",
                  "#8c6ac4",
                  "#715c87",
                  "#e098c7",
                  "#8fd3e8"
                ];
                var x = Math.round(Math.random() * 5);
                return color[x];
              }
            },
            emphasis: {
              shadowBlur: 10,
              shadowColor: '#333'
            }
          },
          data: params
        }]
      };

      const chart = this.initChart('emailWord', 'emailWord')
      chart && chart.setOption(option)
    },



    EmailRecWord(params) {
      var option = {
        title: {
          text: "邮件接收主题词云图",
          padding: [10, 10]
        },
        tooltip: {},
        series: [{
          type: 'wordCloud',
          gridSize: 20,
          sizeRange: [12, 36],
          rotationRange: [0, 0],
          shape: 'circle',
          textStyle: {
            normal: {
              color: function() {
                var color = [
                  "#ff715e",
                  "#ffaf51",
                  "#ffee51",
                  "#8c6ac4",
                  "#715c87"
                ];
                var x = Math.round(Math.random() * 5);
                return color[x];
              }
            },
            emphasis: {
              shadowBlur: 10,
              shadowColor: '#333'
            }
          },
          data: params
        }]
      };

      const chart = this.initChart('emailRecWord', 'emailRecWord')
      chart && chart.setOption(option)
    },


    WebPie(params) {
      var option = {
        title: {
          text: '访问域名类别占比',
          x: 'left',
          padding: [10, 10]
        },
        tooltip: {
          trigger: 'item',
          formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        calculable: true,
        series: [{
          name: '面积模式',
          type: 'pie',
          radius: [20, 160],
          roseType: 'area',
          data: params
        }]
      };

      const chart = this.initChart('webPie', 'webPie')
      chart && chart.setOption(option)
    },


    CheckTime(params) {

      var cellSize = [80, 80];
      var pieRadius = 30;


      function getPieSeries(scatterData, chart) {

        return echarts.util.map(scatterData, function(item, index) {

          var center = chart.convertToPixel('calendar', item);
          return {
            id: index + 'pie',
            type: 'pie',
            center: center,
            tooltip: {
              formatter: function(x) {

                if (x.data.name == "工作") {
                  return "工作时间： " + item[2] + "-" + item[3];
                } else {
                  return x.data.name + "时间: " + x.data.value;
                }

              }

            },
            label: {
              normal: {
                formatter: '{c}',
                position: 'inside'
              }
            },
            radius: pieRadius,
            data: [{
                name: '工作',
                value: item[1]
              },
              {
                name: '生活',
                value: 24 - item[1]
              },

            ]
          };
        });
      }

      var scatterData = params;
      var thisTitle=this.id+"打卡上班时长日历图";

      var option = {
        title: {
          text: thisTitle,
          padding: [10, 10]
        },
        tooltip: {},
        legend: {
          data: ['工作', '生活'],
          top: 10,
          right:10
        },
        calendar: {
          // top: 'middle',
          left: 'center',
          bottom:20,
          top:70,
          orient: 'vertical',
          cellSize: cellSize,
          splitLine: {
            show: true,
            lineStyle: {
              color: '#ccc',
              width: 2,
              type: 'solid'
            }
          },
          yearLabel: {
            show: false,
            textStyle: {
              fontSize: 30
            }
          },
          dayLabel: {
            margin: 20,
            firstDay: 1,
            nameMap: ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'],
            color: "#ffaf51",
          },
          monthLabel: {
            show: false
          },
          itemStyle: {
            normal: {
              color: 'rgba(0,0,0,0)',
              borderWidth: 1,
              borderColor: '#ccc'
            }
          },
          range: ['2017-11']
        },
        series: [{
          id: 'label',
          type: 'scatter',
          coordinateSystem: 'calendar',
          symbolSize: 1,
          label: {
            normal: {
              show: true,
              formatter: function(params) {
                return echarts.format.formatTime('dd', params.value[0]);
              },
              offset: [-cellSize[0] / 2 + 10, -cellSize[1] / 2 + 10],
              textStyle: {
                color: "#ff715e",
                fontSize: 14
              }
            }
          },
          data: scatterData
        }]
      };



      const chart = this.initChart('checkTime', 'checkTime')
      if (!chart) return
      chart.setOption(option)
      setTimeout(() => {
        const pieSeries = getPieSeries(scatterData, chart)
        chart.setOption({
          series: option.series.concat(pieSeries)
        })
      }, 10)
    },


    LoginParallel() {
      var url = "/login/" + this.id;
      request({
        url: url,
        method: 'get'
      }).then(response => {
        var option = {
          title: {
            text: "登录服务器平行坐标图",
            padding: [10, 10]
          },

          tooltip: {
            trigger: 'item'
          },
          visualMap: {
            type: 'piecewise',
            categories: response.data.parallels[1],
            dimension: 1,
            orient: 'horizontal',
            top: 10,
            textStyle: {
              color: "##333"
            },
            left: 'center',
            inRange: {
              color: ["#ff715e",
                "#ffaf51",
                "#ffee51",
                "#8c6ac4",
                "#715c87"
              ]
            },
            seriesIndex: [0]
          },
          parallel:{
            bottom:20,
            left:20,
            top:70,
          },

          parallelAxis: [{
              dim: 0,
              name: 'sip',
              type: 'category',
              data: response.data.parallels[0]
            },
            {
              dim: 1,
              name: 'user',
              type: 'category',
              data: response.data.parallels[1]
            },
            {
              dim: 2,
              name: 'date'
            },
            {
              dim: 3,
              name: 'time',
              type: 'category',
              data: response.data.parallels[3]
            },
            {
              dim: 4,
              name: 'dip',
              type: 'category',
              data: response.data.parallels[4]
            },
            {
              dim: 5,
              name: 'state',
              type: 'category',
              data: response.data.parallels[5]
            }
          ],
          series: {
            type: 'parallel',
            smooth: 0.3,

            lineStyle: {
              width: 1
            },
            data: response.data.data

          }
        };

        const chart = this.initChart('loginParallel', 'loginParallel')
        chart && chart.setOption(option)
      })
    },

    NetworkFlow() {

      var url = "/tcplog/" + this.id;
      request({
        url: url,
        method: 'get'
      }).then(response => {
        // console.log(response);

        var option = {
          tooltip: {
            trigger: 'axis'
          },

          title: {
            text: '上传下载流量图',
            padding: [10, 10]
          },
          legend: {
            data: ['upload', 'download'],
            right: 50,
            top: 10
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },
          dataZoom: [{
            startValue: '2017-11-01'
          }, {
            type: 'inside'
          }],
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: response.data.xAxis
          },
          yAxis: {
            type: 'value',
            max: 'dataMax'
          },
          series: [{
              name: 'upload',
              type: 'line',
              data: response.data.upAxis
            },
            {
              name: 'download',
              type: 'line',
              data: response.data.downAxis
            }
          ]
        };
        var option2 = {
          tooltip: {
            trigger: 'axis'
          },
          title: {
            text: '按协议划分流量图',
            padding: [10, 10]
          },
          legend: {
            data: response.data.legend,
            right: 50,
            top: 10
          },
          grid: {
            left: '3%',
            right: '4%',
            bottom: '10%',
            containLabel: true
          },
          toolbox: {
            feature: {
              saveAsImage: {}
            }
          },

          dataZoom: [{
            startValue: '2017-11-01'
          }, {
            type: 'inside'
          }],
          xAxis: {
            type: 'category',
            boundaryGap: false,
            data: response.data.xAxis
          },
          yAxis: {
            type: 'value',
            max: 'dataMax'
          },
          series: response.data.protocols
        };

        const protoChart = this.initChart('protoFlow', 'protoFlow')
        protoChart && protoChart.setOption(option2)

        const flowChart = this.initChart('upDownFlow', 'upDownFlow')
        flowChart && flowChart.setOption(option)
      })
    },
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.personal-page {
  padding: 0;

  .search-card {
    margin-bottom: 20px;
    border-radius: 8px;

    :deep(.el-card__body) {
      padding: 20px;
    }
  }

  .search-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;

    .title {
      font-size: 18px;
      font-weight: 600;
      color: #303133;
    }

    .server-alert {
      width: 100%;
      margin-left: 16px;
      flex: 1;
    }
  }

  .search-form {
    display: flex;
    flex-wrap: wrap;
    align-items: center;

    :deep(.el-form-item) {
      margin-right: 12px;
      margin-bottom: 0;
    }
  }

  .basic-card {
    background: #f7f9fc;
    border: 1px solid #ebeef5;
    border-radius: 10px;
    padding: 16px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 8px;

    .info-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      color: #606266;
      font-size: 14px;

      .label {
        color: #909399;
      }

      .value {
        color: #ff715e;
        font-weight: 600;
      }
    }
  }

  .section-row {
    margin-top: 20px;
  }

  .chart-card {
    height: 100%;
    border-radius: 8px;
    transition: all 0.2s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
    }

    :deep(.el-card__body) {
      padding: 16px;
    }
  }

  .chart-box {
    width: 100%;
    height: 360px;
  }

  .chart-box.medium {
    height: 380px;
  }

  .chart-box.large {
    height: 500px;
  }
}
</style>
