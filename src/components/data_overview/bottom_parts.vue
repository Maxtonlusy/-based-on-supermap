<template>
     
            <div class="lg:col-span-2 bg-white rounded-xl shadow-md  ">
                <div class="p-4 border-b border-gray-200 flex items-center justify-between ">
                 <h3 class="text-lg font-semibold text-neutral">近期事件</h3>
                </div>
                <div class="p-4">
                   
                    <div class="overflow-x-auto">
                       <List/>
                    </div>
                  
                </div>
             
            </div>
</template>

<script setup>
import List from './list.vue'
</script>

<style lang="scss" scoped>

</style>
