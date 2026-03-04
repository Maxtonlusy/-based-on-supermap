<template>

    <div ref="chartRef" class="w-full h-[200px]"></div>

</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import * as echarts from 'echarts';
import 'echarts-wordcloud'; 










const chartRef = ref(null);
const chartInstance = ref(null);
const data=ref(null) 
const one =ref(1)
const two =ref(2)
const three =ref(3)
const four =ref(4)


const words = ref([
  { name: '糖尿病', value: one.value },
  { name: '高血压', value:two.value},
  { name: '老年痴呆', value: three.value},
  { name: '癌症', value: four.value },

]);




const fetchdata = async () => {
         const response = await fetch('http://127.0.0.1:5137/health_page/chart_cloud')
  

    const fullData = await response.json();

data.value=fullData
console.log(data.value[0][1])
one.value =data.value[0][1]
two.value =data.value[1][1]
three.value =data.value[2][1]
four.value =data.value[3][1]


 }












// 初始化图表
const initChart = () => {
  if (chartInstance.value) {
    chartInstance.value.dispose();
  }
  
  chartInstance.value = echarts.init(chartRef.value);
  
  const option = {
    series: [{
      type: 'wordCloud',
      gridSize: 10,
      sizeRange: [12, 50],
      rotationRange: [-90, 90],
      shape: 'circle',
      width: '100%',
      height: '100%',
      data: words.value
    }]
  };
  
  chartInstance.value.setOption(option);
};

onMounted(async() => {  await fetchdata ();
  
  // 确保DOM元素已挂载
  if (chartRef.value) {
    initChart();
    
    // 监听窗口大小变化，重绘图表
    window.addEventListener('resize', () => {
      chartInstance.value?.resize();
    });
  }
});

// 监听数据变化，更新图表
watch(words, () => {
  if (chartInstance.value) {
    chartInstance.value.setOption({
      series: [{
        data: words.value
      }]
    });
  }
});
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
