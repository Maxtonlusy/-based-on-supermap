<template>
  <div class="flex items-center justify-between  flex-col ">
  <div class=" bg-white  p-5 border border-primary/10 card-glow w-full h-1/2">
    <div id="total_number_of_events_chart_dom" ref="total_number_of_events_chart_dom" class="w-full h-full" ></div>
        
          </div>
          
          <!-- 统计卡片4 -->
          <div class=" bg-white  p-5 border border-primary/10 card-glow w-full h-1/2">
           <div class="w-full h-full" ref="chart_service_dom"></div>
          </div>
          </div>

         
  


</template>

<script setup>
import { ref, onMounted, watchEffect , nextTick } from 'vue';
import * as echarts from 'echarts';
const total_number_of_events_chart_dom = ref(null);
const type_count_resolved = ref('');
const type_count_rejected = ref('');
const type_count_doing = ref('');
const type_count_pending = ref('');
const type_count_life = ref('');             
const type_count_medical = ref('');            
const type_count_information = ref('');   
const type_count_mood = ref('');              









let myChart_event  = null;

const _task= async () => {

  const response = await fetch('http://127.0.0.1:5137/task/task_chart')
     const fullData = await response.json();
   
  type_count_resolved.value = fullData['type_count_resolved'];
type_count_rejected.value = fullData['type_count_rejected'];
type_count_doing.value = fullData['type_count_doing'];
type_count_pending.value = fullData['type_count_pending'];
type_count_life.value = fullData['type_count_life'];
type_count_medical.value = fullData['type_count_medical'];
type_count_information.value = fullData['type_count_information'];
type_count_mood.value = fullData['type_count_mood'];
initChart_service()
 console.log(fullData)
    initChart();
 }

const initChart = () => {
  
  // 初始化实例
  myChart_event = echarts.init(total_number_of_events_chart_dom.value);
  
  // 设置图表配置
  const option = {
            // 设置标题
            title: {
                text: '需求处理状态',
                left: 'center',
                textStyle: {
                  color: '#333',
                    fontSize: 18,
                   
                }
            },
            
            // 设置图例
            legend: {
                orient: 'horizontal',
                bottom: 0,
                textStyle: {
                    fontSize: 10
                },
                itemGap: 20,
                data: ['已结束', '正处理', '未指派','已拒绝'],
                 width: 600
            },
            
            // 提示框配置
            tooltip: {
                trigger: 'item',
                formatter: '{a} <br/>{b}: {c} ({d}%)',
                backgroundColor: 'rgba(255, 255, 255, 0.9)',
                borderColor: '#ddd',
                borderWidth: 1,
                textStyle: {
                    color: '#333'
                },
                padding: 10,
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)'
            },
            
            // 系列配置 - 饼图
            series: [
                {
                    name: '数据占比',
                    type: 'pie',
                    radius: ['40%', '70%'], // 内外半径，控制环的厚度
                    center: ['50%', '50%'],
                    avoidLabelOverlap: false,
                    
                    // 弧线样式
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.1)'
                    },
                    
                    // 标签设置（中间文本）
                    label: {
                        show: false
                       
                    },
                    
                    // 连接线标签设置（外侧文本）
                    labelLine: {
                        show: false
                      
                    },
                    

                    data: [
                        { value: type_count_resolved.value, name: '已结束', itemStyle: { color: '#10B981' } },
                        { value: type_count_doing.value, name: '正处理', itemStyle: { color: '#EAB308' } },
                        { value: type_count_pending.value , name: '未指派', itemStyle: { color: '#8B5CF6' } },
                          { value: type_count_rejected.value , name: '已拒绝', itemStyle: { color: '#EF4444' } }
                    ]
                }
            ],
            
            // 动画配置
            animation: true,
            animationDuration: 1000,
            animationEasing: 'cubicOut',
            animationDelay: function (idx) {
                return idx * 100;
            }
        };

  
 option && myChart_event.setOption(option);
};









const chart_service_dom = ref(null);

let myChart_service  = null;
const initChart_service = () => {
  

  myChart_service = echarts.init(chart_service_dom.value);

   const resourceData = {
            categories: ['生活事务','健康医疗','信息咨询','情感社交'],
            values: [type_count_life.value,type_count_medical.value,type_count_information.value, type_count_mood.value],
            colors: ['#219ebc', '#06d6a0', '#9b5de5', '#f72585']
        };
 
  const source_map_option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    },
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    borderColor: '#ddd',
                    borderWidth: 1,
                    textStyle: { color: '#333' },
                    formatter: function(params) {
                        return `${params[0].name}: ${params[0].value} 个`;
                    }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: resourceData.categories,
                    axisLine: {
                        lineStyle: {
                            color: '#999'
                        }
                    },
                    axisLabel: {
                        color: '#666',
                        fontSize: 12
                    }
                },
                yAxis: {
                    type: 'value',
                    name: '需求统计',
                    nameTextStyle: {
                        color: '#666',
                        fontSize: 12
                    },
                    axisLine: {
                        show: false
                    },
                    splitLine: {
                        lineStyle: {
                            color: '#eee'
                        }
                    },
                    axisLabel: {
                        color: '#666',
                        fontSize: 12,
                        formatter: '{value}'
                    }
                },
                series: [
                    {
                        data: resourceData.values,
                        type: 'bar',
                        barWidth: '60%',
                        itemStyle: {
                            color: function(params) {
                                return resourceData.colors[params.dataIndex];
                            },
                            borderRadius: [6, 6, 0, 0]
                        },
                        label: {
                            show: true,
                            position: 'top',
                            color: '#333',
                            fontSize: 12
                        },
                        emphasis: {
                            itemStyle: {
                                shadowBlur: 10,
                                shadowOffsetX: 0,
                                shadowColor: 'rgba(0, 0, 0, 0.3)'
                            }
                        },
               
                        animationDuration: 1500,
                        animationEasing: 'elasticOut'
                    }
                ]
            };
  
 source_map_option && myChart_service.setOption(source_map_option);
};








const handleResize = () => {
  myChart_event && myChart_event.resize();
   myChart_service && myChart_service.resize();

};

// 组件挂载时初始化图表
onMounted(() => {
  _task()

  nextTick(() => {

    // initChart();
    window.addEventListener('resize', handleResize);
  });
});

// 组件卸载时清理
watchEffect((onCleanup) => {
  onCleanup(() => {
    // 移除事件监听
    window.removeEventListener('resize', handleResize);
    
    // 销毁图表实例
    if (myChart_age) {
      myChart_event.dispose();
      myChart_event = null;
    }
    

  });
});        





</script>

<style lang="scss" scoped>

</style>