<template >
 <div id="bar" class="w-[400px] h-0 flex items-center 
            border-t-[50px] border-r-[80px] border-b-0 border-l-[80px]
        border-[#2E86C1] border-r-transparent 
            border-b-transparent border-l-transparent rotate-90 fixed top-1/2 -translate-y-1/2 left-[-161px]">

      <div id="container" class="absolute flex justify-center right-[60px] bottom-[-12px] gap-3 ">

    <i id="filter_icon_qiehuanditu" @click="del_botton" class="iconfont icon-shanchudangan   text-base-100  -rotate-90" style="display: inline-block;" ></i>
       <i id="filter_icon_shaixuan"  @click="toggleFilter"  class="z-1000 iconfont icon-shaixuan  text-base-100  -rotate-90" style="display: inline-block;" ></i>
       <i id="filter_icon_fuwu" @click="choice_point" class="z-1000 iconfont icon-fuwu  text-base-100  -rotate-90" style="display: inline-block;" ></i></div>
</div>
</template>

<script setup>
import { io } from 'socket.io-client';
import { ref} from 'vue';
   
    const socket = io('http://127.0.0.1:5137');
 socket.on('connect', () => {
        console.log('Socket连接成功，客户端ID:', socket.id); })
socket.emit('register', { room: 'bar_record' });
function toggleFilter () {
socket.emit('record_data', { content: 'ok' });

}

 function choice_point() {

    socket.emit('record_data', { content: 'okok' });

}

function del_botton(){

    socket.emit('record_data', { content: 'okokok' });

}
</script>

<style scoped>

i{
    font-size:50px;

}
</style>