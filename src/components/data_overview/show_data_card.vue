<template>
<section id="dashboard" class="mb-10">
            <div class="flex flex-col md:flex-row md:items-center justify-between mb-6">
                <h2 class="text-[clamp(1.5rem,3vw,2rem)] font-bold text-neutral">
                    <i class="fa fa-dashboard text-primary mr-2"></i>数据概览
                </h2>
              
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <!-- 总人口卡片 -->
    <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105">
        <div class="flex items-center justify-between ">
            <h3 class="text-lg font-semibold text-neutral">总人口</h3>
            <div class="h-10 w-10 rounded-full bg-primary/10 flex items-center justify-center">
                <i class="fa fa-users text-primary text-xl"></i>
            </div>
        </div>
        <div class="h-12 flex items-end"> <!-- 固定高度确保对齐 -->
            <p id="all_people_show" class="text-3xl font-bold text-neutral">{{ all_people_show }}人</p>
        </div>
    </div>
    
    <!-- 老年人口卡片 -->
    <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105">
        <div class="flex items-center justify-between ">
            <h3 class="text-lg font-semibold text-neutral">60岁以上人口</h3>
            <div class="h-10 w-10 rounded-full bg-accent/10 flex items-center justify-center">
                <i id="old_icon" class="iconfont icon-a-mingchenglaoren text-accent "></i>
            </div>
        </div>
        <div class="h-12 flex items-end"> <!-- 固定高度确保对齐 -->
            <p id="population_aged_60_and_above" class="text-3xl font-bold text-neutral" >{{population_aged_60_and_above}}人</p>
        </div>
    </div>
    
    <!-- 养老机构卡片 -->
    <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105">
        <div class="flex items-center justify-between ">
            <h3  class="text-lg font-semibold text-neutral">养老机构</h3>
            <div class="h-10 w-10 rounded-full bg-secondary/10 flex items-center justify-center">
                <i class="fa fa-building text-secondary text-xl"></i>
            </div>
        </div>
        <div class="h-12 flex items-end"> <!-- 固定高度确保对齐 -->
            <p id="elderly_care_institution" class="text-3xl font-bold text-neutral" >{{elderly_care_institution}}家</p>
        </div>
    </div>
    
    <!-- 服务人员卡片 -->
    <div class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-all duration-300 hover:scale-105">
        <div class="flex items-center justify-between ">
            <h3 class="text-lg font-semibold text-neutral">银发守护者</h3>
            <div class="h-10 w-10 rounded-full bg-info/10 flex items-center justify-center">
                <i class="iconfont icon-zhiyuanzhe text-info text-xl"></i>
            </div>
        </div>
        <div class="h-12 flex items-end">
            <p id="volunteer" class="text-3xl font-bold text-neutral" >{{volunteer}}位</p>
        </div>
    </div>
</div>
        </section>
</template>

<script setup>

import _ from 'lodash';
import { io } from 'socket.io-client';

import { ref, onMounted, toRaw  } from 'vue';
const all_people_show = ref('');
const population_aged_60_and_above = ref('');
const elderly_care_institution = ref('');
const volunteer =ref('');
var condition = {area:'武汉'}
const data =ref([])
let rawdata  = null
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
    all_people_show.value = rawdata[0].Permanent_population_in_2020.toLocaleString()
    console.log(rawdata)
    elderly_care_institution.value = rawdata[0].care.toLocaleString()
    population_aged_60_and_above.value =  Math.floor(rawdata[0].Proportion_of_the_population_aged_60_and_above * rawdata[0].Permanent_population_in_2020).toLocaleString()
     volunteer.value = rawdata[0].volunteer.toLocaleString()

}












onMounted(async () => {

  await fetchData(condition);
  
});



onMounted(async () => {
  const socket = io('http://127.0.0.1:5137/');
  
  // 连接成功后注册房间
  const handleConnect = () => {
    socket.emit('register', { room: 'card_overview' });
  };
const handleChargeUpdate = _.debounce((data) => { 
    
    condition["area"] = data["content"];
fetchData(condition).then(() => {console.log('okok')})
})
  









socket.on('connect', handleConnect);
  socket.on('charge_data', handleChargeUpdate)
})


















</script>

<style  scoped>
#old_icon{
font-size: 24px; 
}
</style>