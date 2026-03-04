<template>

    <div ref="chart_age_dom" class="w-full h-[200px]"></div>

</template>

<script setup>
import { onMounted, ref, watch,nextTick } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud'; 










const data=ref(null) 
const one =ref(1)
const two =ref(2)
const three =ref(3)
// const four =ref(4)


// const words = ref([
//   { name: '健康', value: one.value },
//   { name: '不健康', value:two.value},
//   { name: '亚健康', value: three.value},


// ]);




const fetchdata = async () => {
         const response = await fetch('http://127.0.0.1:5137/health_page/chart_health')
  

    const fullData = await response.json();

data.value=fullData
console.log(fullData)
console.log('okok')
one.value =data.value[0][1]
two.value =data.value[1][1]
three.value =data.value[2][1]



 }





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
              <p>${params.name}</p>
              <p>${params.value}人</p>
            </div>
          `;
        case 1:
          return `
            <div class="style1">
             <p>${params.name}</p>
               <p>${params.value}人</p>
            </div>
          `;
        case 2:
          return `
            <div class="style2">
                <p>${params.name}</p>
              <p>${params.value}人</p>
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
                        { value: one.value, name: "健康", itemStyle: { color: '#E0E0E0' } }, 
                        { value: two.value, name: '不健康', itemStyle: { color: '#ff4500' } }, 
                        { value: three.value, name: '亚健康', itemStyle: { color:    '#ff4500'                   
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
onMounted(async() => {
      await fetchdata();
   
  nextTick(() => {
   
   

    initChart( );
    // window.addEventListener('resize', handleResize);
  });
 
});

// // 组件卸载时清理
// watchEffect((onCleanup) => {
//   onCleanup(() => {
//     // 移除事件监听
//     window.removeEventListener('resize', handleResize);
    
//     // 销毁图表实例
//     if (myChart_age) {
//       myChart_age.dispose();
//       myChart_age = null;
//     }
    
//     if (myChart_service) {
//       myChart_service.dispose();
//       myChart_service = null;
//     }
//   });
// });        
</script>

<style scoped>
.word-cloud-container {
  width: 100%;
  height: 400px;
}

.chart-wrapper {
  width: 100%;
  height: 100%;
}
</style>
