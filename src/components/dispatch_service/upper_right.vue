<template>
 <div class="flex items-center justify-between  flex-col ">
  <div class=" bg-white  p-5 border border-primary/10 card-glow w-full h-1/2">
    <div id="chart_leaderboard_dom" ref="chart_leaderboard_dom" class="w-full h-full" ></div>
        
          </div>
          
          <!-- 统计卡片4 -->
<div class=" bg-white  p-5 border border-primary/10 card-glow w-full h-1/2">
    <div id="chart_review_dom" ref="chart_review_dom" class="w-full h-full" ></div>
        
          </div>
          
             

          </div>
</template>

<script setup>
import {ref, onMounted, watchEffect , nextTick  } from 'vue';
import * as echarts from 'echarts';
const chart_review_dom = ref(null);


const _task= async () => {

  const response = await fetch('http://127.0.0.1:5137/task/task_chart_value')
     const fullData = await response.json();
     const chartData = [
      { name: '闪电队', score: 92, color: '#3B82F6' },
      { name: '猛虎队', score: 85, color: '#10B981' },
      { name: '雄鹰队', score: 78, color: '#8B5CF6' },
      { name: '猎豹队', score: 72, color: '#EAB308' },
      { name: '鲨鱼队', score: 65, color: '#EF4444' }
    ];
     for(let i = 0; i < fullData.length; i++){chartData[i]['name']=fullData[i]['name'];
     chartData[i]['score']=fullData[i]['value']
     }

console.log(fullData)
 initChart_leaderboard(chartData);    
 }



let myChart_review  = null;
const initChart = () => {
  
  // 初始化实例
  myChart_review = echarts.init(chart_review_dom.value);
  
  // 设置图表配置
  const option = {
            title: {
                text: '用户满意度维度评估',
                left: 'right',
                textStyle: {
                    fontSize: 16,
                    color: '#333'
                }
            },
            tooltip: {
                trigger: 'axis',
                formatter: '{b}: {c}'
            },
            radar: {
                indicator: [
                    { name: '准确性', max: 100 },
                    { name: '相关性', max: 100 },
                    { name: '完整性', max: 100 },
                    { name: '可操作性', max: 100 },
                    { name: '代表性', max: 100 },
                    { name: '情感真实性', max: 100 },

                ],axisNameGap: 8,
                shape: 'polygon',
                splitArea: {
                    areaStyle: {
                        color: ['#f0f7ff', '#e6f3ff', '#dcefff']
                    }
                },
                axisLine: {
                    lineStyle: {
                        color: '#99c2ff'
                    }
                }
            },
            series: [{
                name: '满意度数据',
                type: 'radar',
                data: [
                    {
                        value: [85, 92, 78, 88, 90, 82],
                        name: '当前版本',
                        lineStyle: {
                            width: 2,
                            color: '#409eff'
                        },
                        itemStyle: {
                            color: '#409eff',
                            borderColor: '#fff',
                            borderWidth: 2
                        },
                        areaStyle: {
                            color: 'rgba(64, 158, 255, 0.2)'
                        }
                    }
                ]
            }]
        };

  
 option && myChart_review.setOption(option);
};









const chart_leaderboard_dom = ref(null);
const teamData = [
      { name: '闪电队', score: 92, color: '#3B82F6' },
      { name: '猛虎队', score: 85, color: '#10B981' },
      { name: '雄鹰队', score: 78, color: '#8B5CF6' },
      { name: '猎豹队', score: 72, color: '#EAB308' },
      { name: '鲨鱼队', score: 65, color: '#EF4444' }
    ];
 const averageScore = teamData.reduce((sum, team) => sum + team.score, 0) / teamData.length;
// 图表实例
let myChart_leaderboard = null;

const initChart_leaderboard = (data) => {
  
  // 初始化实例
myChart_leaderboard= echarts.init(chart_leaderboard_dom.value);
  
  // 设置图表配置
  const option = {

    title: {
                text: '友善值排行榜',
                left: 'right',
                top:10,
                textStyle: {
                    fontSize: 20,
                    color: '#333'
                }
            },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          backgroundColor: 'rgba(255, 255, 255, 0.9)',
          borderColor: '#eee',
          borderWidth: 1,
          padding: 10,
          textStyle: {
            color: '#333'
          },
          formatter: function(params) {
            return `${params[0].name}: ${params[1].value}`;
          }
        },
        grid: {
        
          right: '14%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          max: 100,
          splitLine: {
            lineStyle: {
              color: '#f0f0f0'
            }
          },
          axisLabel: {
            formatter: '{value} '
          }
        },
        yAxis: {
          type: 'category',
          data: data.map(item => item.name),
          axisLine: {
            show: false
          },
          axisTick: {
            show: false
          },
          inverse: true
        },
        series: [
          // 参考线
          {
            type: 'line',
            data: data.map(() => averageScore),
            symbol: 'none',
            lineStyle: {
              color: '#e5e7eb',
              type: 'dashed'
            },
            tooltip: {
              formatter: `平均值: ${averageScore.toFixed(1)}`
            },
            z: 1
          },
          // 条形图
          {
            name: '值',
            type: 'bar',
            data: data.map(item => item.score),
            barWidth: '60%',
            itemStyle: {
              color: function(params) {
                return data[params.dataIndex].color;
              },
              borderRadius: [0, 4, 4, 0]
            },
            label: {
              show: true,
              position: 'right',
              formatter: '{c} '
            },
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowColor: 'rgba(0, 0, 0, 0.3)'
              }
            },
            z: 2
          }
        ]
      };
      

  
 option && myChart_leaderboard.setOption(option);
};










































const handleResize = () => {
  myChart_review && myChart_review.resize();
 myChart_leaderboard && myChart_leaderboard.resize();
};


// 组件挂载时初始化图表
onMounted(() => {
_task()
  nextTick(() => {
   initChart();
   
    window.addEventListener('resize', handleResize);
  });
});

// 组件卸载时清理
watchEffect((onCleanup) => {
  onCleanup(() => {
    // 移除事件监听
    window.removeEventListener('resize', handleResize);
    
    // 销毁图表实例
    if (myChart_review) {
      myChart_review.dispose();
      myChart_review = null;
    }
    if (myChart_review) {
      myChart_leaderboard.dispose();
      myChart_leaderboard= null;
    }
  
  });
});        
</script>

<style scoped>

</style>