<template>
    <div class="bg-white rounded-xl shadow-md p-6 hover-scale ">
                    <div class="flex items-center justify-between mb-4  ">
                       
                             <h3 class="text-lg font-semibold text-neutral">老年人口年龄分布</h3>
           <div class="flex items-center justify-between "> <i  class="fa fa-map-marker text-primary text-xl" ></i>
       <label for="region-select" class=" ml-1 text-gray-700 font-medium">当前选择的区域 : {{ area }}</label>
        
      </div>
                    </div>
                  <div class=" h-[250px] " ref="chart_age_dom"></div>
                
             
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="text-lg font-semibold text-neutral">服务资源统计</h3>
                        
                    </div>
                    
                    <div class=" h-[250px]" ref="chart_service_dom"></div>
             
                </div>

</template>

<script setup>
import _ from 'lodash';
import { io } from 'socket.io-client';
import { ref, onMounted, watchEffect , nextTick,toRaw,onUnmounted } from 'vue';
import * as echarts from 'echarts';

const remainder= ref()
const data =ref([])
const area =ref('全市')
var condition = {area:'武汉'}
var rawdata  = null
const sixty_and_above = ref()
const sixty_five_and_above = ref()
const living_support = ref()
const medical = ref()
const entertainment= ref()
const emergency= ref()





const url =ref('http://127.0.0.1:5137/home_page/chart_show')
const fetchData= async (condition) => {
       const response = await fetch(url.value, {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
        
      },
      body: JSON.stringify(condition) 
    });
    
           data.value = await response.json()
            rawdata = toRaw(data.value); 
            sixty_and_above.value =rawdata[0].Proportion_of_the_population_aged_60_and_above
  sixty_five_and_above.value =rawdata[0].Proportion_of_the_population_aged_65_and_above
 remainder.value=100-sixty_and_above.value-sixty_five_and_above.value
living_support.value =rawdata[0].care
medical.value = rawdata[0].medical
entertainment.value = rawdata[0].entertainment
emergency.value = rawdata[0].emergency

 console.log(emergency.value)
 console.log(data.value)
;
return data 
}


onMounted(async () => {
  const socket = io('http://127.0.0.1:5137/');
  
  // 连接成功后注册房间
  const handleConnect = () => {
    socket.emit('register', { room: 'chart_overview' });
  };
  

  const handleDataUpdate = _.debounce((data) => { 
    area.value = data["content"]
    condition["area"] = data["content"];

    if (!isFetching.value) {
      fetchData(condition).then(() => {
        destroyOldCharts()
        initChart();
        initChart_service()

      });
    }
  }, 300); // 300ms防抖，避免高频触发
  
  // 注册事件监听器
  socket.on('connect', handleConnect);
  socket.on('forwarded_name', handleDataUpdate);
  
  
  onUnmounted(() => {
    // 移除事件监听器
    socket.off('connect', handleConnect);
    socket.off('forwarded_name', handleDataUpdate);
    // 关闭socket连接
    socket.disconnect();
  });
});

// 新增：标记请求状态，防止并发冲突
const isFetching = ref(false);



// 新增：销毁旧图表实例
const destroyOldCharts = () => {
  // 根据实际图表库API销毁实例，例如ECharts：
  if (myChart_age ) myChart_age .dispose();

};
























const textureImg = new Image();
textureImg.src = '/chart_texture.png';

const chart_age_dom = ref(null);

let myChart_age  = null;

// 初始化图表
const initChart = () => {
  myChart_age = echarts.init(chart_age_dom.value);
  
  // 设置图表配置
  const option  = { 
            tooltip: {
                trigger: 'item',
                formatter: function(params) {
   
      switch(params.dataIndex) {
        case 0:
          return `
            <div class="style0">
              <p>年龄组：${params.name}</p>
              <p>数值：${params.value-40}%</p>
            </div>
          `;
        case 1:
          return `
            <div class="style1">
              <p>年龄组：${params.name}</p>
              <p>数值：${params.value}%</p>
            </div>
          `;
        case 2:
          return `
            <div class="style2">
              <p>年龄组：${params.name}</p>
              <p>数值：${params.value}%</p>
            </div>
          `;
        default:
          return '';
      }
    }
          
            },
            series: [
                {
                    type: 'pie',
                 
                    sort: false, 
                    data: [
                        { value: remainder.value+40, name: '0-59岁', itemStyle: { color: '#E0E0E0' } }, 
                        { value: sixty_and_above.value, name: '60岁以上', itemStyle: { color: '#ff4500' } }, 
                        { value: sixty_five_and_above.value, name: '65岁以上', itemStyle: { color: {
                              type: 'pattern',
                              image: textureImg,
                              repeat: 'repeat' 
                          }                      
 } }
                    ],
                    radius:'70%',
                     center: ['55%', '50%'],
                  
emphasis: {
  scale: false
}
                }
            ]
        };
  
 option && myChart_age.setOption(option);
};













const chart_service_dom = ref(null);

let myChart_service  = null;
const initChart_service = () => {
  

  myChart_service = echarts.init(chart_service_dom.value);
   const resourceData = {
            categories: ['生活保障', '卫生健康','精神文化','应急支持'],
            values: [living_support.value, medical.value, entertainment.value, emergency.value],
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
                    name: '资源数量 (个)',
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
  myChart_age && myChart_age.resize();
  myChart_service && myChart_service.resize();
};










onMounted(async() => {
      await fetchData(condition);
   
  nextTick(() => {
   
   
    initChart_service();
    initChart( sixty_and_above,sixty_five_and_above, remainder);
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
      myChart_age.dispose();
      myChart_age = null;
    }
    
    if (myChart_service) {
      myChart_service.dispose();
      myChart_service = null;
    }
  });
});        
</script>

<style scoped>

</style>