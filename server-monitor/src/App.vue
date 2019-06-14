<template>
  <section>
    <el-row type="flex" justify="center" style="margin-bottom: 20px; margin-top: 20px;">
        <div
          style="text-align:center;color:#303133;font-family: Arial;font-weight:bold;font-size:20px;"
        >数据更新时间：{{update_time}}</div>
    </el-row>
    <el-row type="flex" justify="center" style="margin-bottom: 20px; margin-top: 20px;">
      <el-card>
        <el-row type="flex">
          <el-col style="width:30%">
            <div
              style="margin:0px 0px 0px 10px;color:#303133;font-family: Arial;font-weight:bold;font-size:25px;"
            >名称：{{info1.name}}</div>
            <div
              style="margin:0px 0px 0px 10px;color:#303133;font-family: Arial;font-weight:bold;font-size:25px;"
            >当前连接数：{{info1.conn}}</div>
          </el-col>
          <el-col style="width:50%">
            <v-chart :options="pie1"/>
          </el-col>
          <el-col style="width:50%">
            <v-chart :options="line1"/>
          </el-col>
        </el-row>
      </el-card>
    </el-row>
  </section>
</template>

<script>
import ECharts from 'vue-echarts'
import 'echarts/lib/component/title'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/legend'
import 'echarts/lib/chart/line'
import 'echarts/lib/chart/pie'
import axios from 'axios'

export default {
  components: {
    'v-chart': ECharts
  },
  data() {
    return {
      update_time: '-',
      info1: {
        name: '-',
        conn: 0,
      },
      pie1: {
        title: {
          text: '磁盘空间',
          x: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: "{b}"
        },
        series: [
          {
            name: '磁盘空间',
            animationType: 'scale',
            animationEasing: 'elasticOut',
            animationDelay: function (idx) {
              return Math.random() * 200;
            },
            type: 'pie',
            radius: '55%',
            center: ['50%', '50%'],
            data: [
              { value: 0, name: '-' },
              { value: 0, name: '-' },
            ],
            itemStyle: {
              emphasis: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ],
      },
      line1: {
        title: {
          text: '服务器负载',
        },
        tooltip: {
          trigger: 'axis'
        },
        xAxis: {
          type: 'category',
          data: ['0', '0', '0', '0', '0', '0', '0']
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          showSymbol: false,
          data: [0, 0, 0, 0, 0, 0, 0],
          type: 'line',
          smooth: true,
          animationEasing: function (k) {
            if ((k *= 2) < 1) { return 0.5 * k * k * k; }
            return 0.5 * ((k -= 2) * k * k + 2);}
        }],
        color: ['#2F4554']
      },
    }
  },
  mounted() {
    axios({
        method: "GET",
        url: "http://localhost:5000/systemMonitor"
      }).then(data => {
          this.update_time = data.data["update_time"]
          this.info1.name = 'Raspberry Pi';
          this.info1.conn = data.data["user"]
          this.pie1.series[0].data[0].name = '已使用' + data.data["disk"]["used"] + 'G'
          this.pie1.series[0].data[0].value = data.data["disk"]["used"]
          this.pie1.series[0].data[1].name = '剩余' + (data.data["disk"]["size"] - data.data["disk"]["used"]) + 'G'
          this.pie1.series[0].data[1].value = data.data["disk"]["size"] - data.data["disk"]["used"]
          this.pie1.title.text = '磁盘空间' 
          this.line1.xAxis.data = data.data["uptime"]["time"].reverse()
          this.line1.series[0].data = data.data["uptime"]["average"].reverse()
        })
  }
}
</script>
