<template >
 <div v-if="showFilter" id="filter-user-modal" class="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-black bg-opacity-0  justify-center items-center z-50">
      <div class="bg-white rounded-xl p-6 card-shadow w-96">
        <h3 class="text-lg font-bold text-neutral-700 mb-6">筛选用户</h3>

        <form id="filter-user-form" @submit="handleSubmit" method="POST" action="/filter_user"   enctype="multipart/form-data">
          <div class="mb-4">
            <label class="block text-sm font-medium text-neutral-700 mb-1">姓名</label>
            <input v-model="username" type="text" name="username" class="w-full px-4 py-2.5 rounded-lg border border-neutral-300 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all">
          </div>
           <div class="mb-4">
            <label class="block text-sm font-medium text-neutral-700 mb-1">健康状态</label>
            <select v-model="status" name="status" class="w-full px-4 py-2.5 rounded-lg border border-neutral-300 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all">
              <option value="healthy">健康</option>
              <option value="unhealthy">不健康</option>
              <option value="subhealthy">亚健康</option>
              <option value="all">全部</option>
            </select>
          </div>
          <div class="mb-4">
            <label class="block text-sm font-medium text-neutral-700 mb-1">区域</label>
            <select  v-model="position" name="position" class="w-full px-4 py-2.5 rounded-lg border border-neutral-300 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-all">
              <option value="all">全市</option>
             <option value="jianghan">江汉区</option>
            <option value="jiangan">江岸区</option>
            <option value="qiaokou">硚口区</option>
            <option value="hanyang">汉阳区</option>
            <option value="wuchang">武昌区</option>
            <option value="hongshan">洪山区</option>
            <option value="dongxihu">东西湖区</option>
            <option value="huangpi">黄陂区</option>
            <option value="xinzhou">新洲区</option>
            <option value="jiangxia">江夏区</option>
            <option value="caidian">蔡甸区</option>
            <option value="jiangshan">青山区</option>
            <option value=" Hannan">汉南区</option>
            </select>
          </div>
          <div class="flex justify-end space-x-3">
            <button id="withdraw_filter_user" @click="toggleFilter"  type="button" class="px-5 py-2.5 bg-white border border-neutral-300 rounded-lg text-neutral-700 hover:bg-neutral-50 transition-colors" >取消</button>
            <button type="submit" class="px-5 py-2.5 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors">确认</button>
          </div>
        </form>
      </div>
    </div>


</template>

<script setup>
import { ref } from 'vue'
const username = ref('');
const status = ref('');
const position = ref('');


const showFilter = ref(true)
const toggleFilter = () => {
  showFilter.value = !showFilter.value
}




const handleSubmit = () => {
    event.preventDefault();
  console.log('表单提交了，用户名：', username.value);
}

</script>

<style lang="scss" scoped>

</style>