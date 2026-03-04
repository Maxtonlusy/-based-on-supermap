<template>
   <div class="relative grid grid-cols-1 lg:grid-cols-3 gap-6 mb-10">

            <div class="lg:col-span-2 bg-white rounded-xl shadow-md overflow-hidden flex  flex-col">
                <div class="p-4 border-b border-gray-200 flex items-center justify-between ">
                    <h2 class="text-xl font-bold text-neutral">
                        <i class="fa fa-map text-primary mr-2"></i>老龄化率与服务资源
                    </h2>
                   
                    
                </div>
              <div ref="map" class="w-full h-full"></div>

            </div>
            
          
            <div class="space-y-6">
               <Show_data_chart/> </div>







        </div>
        
</template>

<script setup>
import { ref ,onMounted } from 'vue';
import Show_data_chart from "./show_data_chart.vue"


const map = ref(null);

onMounted(() => {
  
  const iframe = document.createElement('iframe');
  iframe.src = 'map_html/data_overview.html';

  
  iframe.style.width = '100%';
  iframe.style.height = '100%';
  map.value.appendChild(iframe);

})
</script>

<style lang="scss" scoped>

</style>