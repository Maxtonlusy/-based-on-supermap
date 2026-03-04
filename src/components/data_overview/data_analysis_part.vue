<template>
 
            <!-- 数据分析区域 -->
            <div class="bg-white rounded-xl shadow-md overflow-hidden hover-scale p-4">
                <div class="p-4 border-b border-gray-200 flex items-center justify-between">
                    <h2 class="text-xl font-bold text-neutral">
                        <i class="fa fa-bar-chart text-primary mr-2"></i>数据分析
                    </h2>
                   
                </div>
                <div class="p-4">
                    <div class="space-y-6">
                        <!-- 老龄化趋势分析 -->
                        <div>
                            <h3 class="font-semibold mb-3">老年人需求分析</h3>
                            <div class="h-[200px]">
                                <div id="lineChart" class="w-full h-full" ref="demand_analysis"></div>
                            </div>
                        </div>
                        
                        
                        <div>
                            <h3 class="font-semibold mb-3">服务需求预测</h3>
                            <div class="h-[300px]">
                               <textarea name="" id="" class="w-full h-full scrollbar-hidden">健康医疗领域，农村占比显著高于城市、镇与整体水平。这反映出农村在医疗资源配置、医疗服务可及性等方面存在短板，居民对健康医疗的刚性需求更为强烈。未来，应重点向农村倾斜医疗资源，比如加强农村基层医疗机构建设、充实医疗人才队伍、推广远程医疗等，以满足农村日益增长的健康医疗需求，助力乡村医疗振兴。
便民代办方面，城市占比相对突出。这既体现城市便民服务体系更成熟，也暗示城市居民对高效、便捷的代办服务有较高需求。随着城市生活节奏加快，可进一步优化城市便民代办服务，拓展服务范围、提升数字化水平，让居民能更便利地办理各类事务，提升城市生活品质与治理效能。
镇的各项占比相对平稳，说明镇在这些领域的需求处于相对均衡状态，但也需关注其潜在需求变化，逐步完善各领域服务，为镇域发展提供有力支撑。整体数据则为宏观层面把握不同区域需求差异、统筹资源配置提供了依据，有助于更精准地制定服务策略，推动城乡服务均衡发展，更好地服务社会大众。</textarea>
                            </div>
                        </div>
                         </div>
                       </div>
                    </div>

</template>

<script setup>
import { ref, onMounted, watchEffect , nextTick,toRaw  } from 'vue';
import * as echarts from 'echarts';
const demand_analysis = ref(null);
let myChart_demand  = null;
let rawdata =null
const data =ref([]);
let overallData =null ;
let cityData = null;
let townData = null;
let ruralData = null;       
const fetchData= async () => {
        const response = await fetch('http://127.0.0.1:5137/home_page/chart_demand');
        
        if (!response.ok) {
            throw new Error(`HTTP错误! 状态: ${response.status}`);
        }
           data.value = await response.json()
  

; // 解析响应体（如果需要）
return data 
}






















// 初始化图表
const initChart = (overallData,cityData,townData,ruralData) => {
   const demand = ['精神文化','生活保障', '健康医疗','便民代办'];

  
  // 初始化实例
  myChart_demand = echarts.init(demand_analysis.value);
  
  // 设置图表配置
  const option = {
               
                
                // 提示框配置
                tooltip: {
                    trigger: 'axis',
                    backgroundColor: 'rgba(255, 255, 255, 0.9)',
                    borderColor: '#eee',
                    borderWidth: 1,
                    textStyle: { color: '#333' },
                    padding: 10,
                    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.1)',
                    formatter: function(params) {
                        let result = `${params[0].name}<br/>`;
                        params.forEach(item => {
                            result += `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background-color:${item.color};margin-right:5px;"></span>${item.seriesName}: ${item.value}<br/>`;
                        });
                        return result;
                    }
                },
                
                
                legend: {
                    data: ['整体', '城市', '镇', '农村'],
                    top: 0,
                    textStyle: { color: '#666' },
                    icon: 'circle',
                    itemWidth: 8,
                    itemHeight: 8,
                    itemGap: 20,
                    // 放小隐藏图例
                    media: [
                        {
                            query: { maxWidth: 768 },
                            option: {
                                legend: { show: false }
                            }
                        }
                    ]
                },
                
                // 网格配置
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    top: '15%',
                    containLabel: true
                },
                
                // 工具栏配置
                toolbox: {
                    feature: {
                        saveAsImage: { 
                            show: true,
                            title: '保存图片',
                            pixelRatio: 2
                        }
                    },
                    right: 10
                },
                
                // x轴配置
                xAxis: {
                    type: 'category',
                   
                    data: demand,
                    axisLine: { lineStyle: { color: '#ddd' } },
                    axisTick: { show: false },
                    axisLabel: {
                        color: '#666',
                        interval: 0,
                        fontSize: 12
                    }
                },
                
                // y轴配置
                yAxis: {
                    type: 'value',
                    axisLine: { show: false },
                    axisTick: { show: false },
                    splitLine: { lineStyle: { color: '#f0f0f0' } },
                    axisLabel: {
                        color: '#666',
                        fontSize: 12,
                        formatter: '{value}'
                    },
                    name : '占比',
                     
                },
                
                
                series: [
                    {
                        name: '整体',
                        type: 'line',
                        data: overallData,
                        symbol: 'circle',
                        symbolSize: 6,
                        lineStyle: {
                            width: 3,
                            color: '#165DFF'
                        },
                        itemStyle: {
                            color: '#165DFF',
                            borderWidth: 2,
                            borderColor: '#fff',
                            shadowBlur: 4,
                            shadowColor: 'rgba(22, 93, 255, 0.5)'
                        },
                        emphasis: {
                            symbolSize: 8
                        },
                        areaStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0, color: 'rgba(22, 93, 255, 0.2)'
                                }, {
                                    offset: 1, color: 'rgba(22, 93, 255, 0)'
                                }]
                            }
                        },
                        smooth: true
                    },
                    {
                        name: '城市',
                        type: 'line',
                        data: cityData,
                        symbol: 'circle',
                        symbolSize: 6,
                        lineStyle: {
                            width: 3,
                            color: '#36CFC9'
                        },
                        itemStyle: {
                            color: '#36CFC9',
                            borderWidth: 2,
                            borderColor: '#fff',
                            shadowBlur: 4,
                            shadowColor: 'rgba(54, 207, 201, 0.5)'
                        },
                        emphasis: {
                            symbolSize: 8
                        },
                        areaStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0, color: 'rgba(54, 207, 201, 0.2)'
                                }, {
                                    offset: 1, color: 'rgba(54, 207, 201, 0)'
                                }]
                            }
                        },
                        smooth: true
                    },
                    {
                        name: '镇',
                        type: 'line',
                        data: townData,
                        symbol: 'circle',
                        symbolSize: 6,
                        lineStyle: {
                            width: 3,
                            color: '#722ED1'
                        },
                        itemStyle: {
                            color: '#722ED1',
                            borderWidth: 2,
                            borderColor: '#fff',
                            shadowBlur: 4,
                            shadowColor: 'rgba(114, 46, 209, 0.5)'
                        },
                        emphasis: {
                            symbolSize: 8
                        },
                        areaStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0, color: 'rgba(114, 46, 209, 0.2)'
                                }, {
                                    offset: 1, color: 'rgba(114, 46, 209, 0)'
                                }]
                            }
                        },
                        smooth: true
                    },
                    {
                        name: '农村',
                        type: 'line',
                        data: ruralData,
                        symbol: 'circle',
                        symbolSize: 6,
                        lineStyle: {
                            width: 3,
                            color: '#FAAD14'
                        },
                        itemStyle: {
                            color: '#FAAD14',
                            borderWidth: 2,
                            borderColor: '#fff',
                            shadowBlur: 4,
                            shadowColor: 'rgba(250, 173, 20, 0.5)'
                        },
                        emphasis: {
                            symbolSize: 8
                        },
                        areaStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 0,
                                y2: 1,
                                colorStops: [{
                                    offset: 0, color: 'rgba(250, 173, 20, 0.2)'
                                }, {
                                    offset: 1, color: 'rgba(250, 173, 20, 0)'
                                }]
                            }
                        },
                        smooth: true
                    }
                ],
                
                
                animation: true,
                animationDuration: 1500,
                animationEasing: 'cubicOut'
            };
            
           
  
 option && myChart_demand.setOption(option);
};
const handleResize = () => {
  myChart_demand && myChart_demand.resize();

};
onMounted(async() => {
await fetchData()
         rawdata = toRaw(data.value); 
           overallData =Object.values(rawdata[0])
           console.log(overallData)
           cityData =Object.values(rawdata[1])
           townData =Object.values(rawdata[2])
           ruralData =Object.values(rawdata[3])
  nextTick(() => {
    initChart(overallData,cityData,townData,ruralData);

    window.addEventListener('resize', handleResize);
  });
});

watchEffect((onCleanup) => {
  onCleanup(() => {

    window.removeEventListener('resize', handleResize);
    
    
    if (myChart_demand) {
      myChart_demand.dispose();
      myChart_demand = null;
    }
    
   
  });
});        


</script>

<style lang="scss" scoped>
.scrollbar-hidden {

  scrollbar-width: none;  
  -ms-overflow-style: none;  
}

</style>