<template>



 <div class="bg-white rounded-lg card-shadow p-5 mb-6">
 <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <h3 class="font-semibold text-gray-800">筛选条件</h3>
                <button @click="refresh()" class="text-primary text-sm hover:text-primary/80 transition-custom flex items-center self-start md:self-auto">
                    <i class="fa fa-refresh mr-1"></i> 重置筛选
                </button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                    <label for="filterStatus" class="block text-sm font-medium text-gray-700 mb-1">反馈状态</label>
                   <select 
            v-model="status" 
            class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom"
        >
            <option value="all">全部状态</option>
            <option value="未开始">待处理</option>
            <option value="进行中">处理中</option>
            <option value="已完成">已处理</option>
            <option value="已取消">不能处理</option>
        </select>
                </div>
                
                <div>
                    <label for="filterType" class="block text-sm font-medium text-gray-700 mb-1">反馈类型</label>
                    <select v-model="type" id="filterType" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom">
                        <option value="all">全部类型</option>
  <option value="生活事务类">生活事务类</option>
  <option value="健康医疗类">健康医疗类</option>
  <option value="信息咨询类">信息咨询类</option>
  <option value="情感社交类">情感社交类</option>
   <option value="紧急">紧急</option>
                    </select>
                </div>
             
                <div >
                    <label for="filterDate" class="block text-sm font-medium text-gray-700 mb-1">提交日期</label>
                    <select v-model="date" id="filterType" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom">
                        <option value="all">全部</option>
                        <option value="today">今天</option>
                        <option value="within_three_days">三天以内</option>
                        <option value="three_days_ago">三天以前</option>
                   
                    </select>
                    
                </div>






<div class="flex h-1/2 justify-center items-end mt-auto gap-4 "> <button  @click="filter_consition"  class="bg-primary hover:bg-primary/90 text-white font-medium py-2 px-6 rounded-md transition-custom flex items-center justify-center whitespace-nowrap">
                    <i class="fa fa-filter mr-2"></i> 应用筛选
                </button>
                
            </div>
            </div>



            
       
  
  <table class="border-collapse w-full"> 
    <!-- 表头部分 -->
    <thead>
      <tr class="bg-gray-100">
        <th class="p-3 border border-gray-200">任务编号</th>
        <th class="p-3 border border-gray-200">标题</th>
        <th class="p-3 border border-gray-200">状态</th>
        <th class="p-3 border border-gray-200">类型</th>
     
        <th class="p-3 border border-gray-200">时间</th>
        <th class="p-3 border border-gray-200">价值</th>
  
          <th class="p-3 border border-gray-200">操作</th>

      </tr>
    </thead>
   
    <tbody>
       <tr 
          v-for="item in data" 
          :key="item.id" 
          class="hover:bg-gray-50"
        >
          <td class="p-3 border border-gray-200 text-center">{{ item.url }}</td>
          <td class="p-3 border border-gray-200 text-center">{{ item.title}}</td>
        
           <td class="p-3 border border-gray-200 text-center">{{ item.status}}</td>
           <td class="p-3 border border-gray-200 text-center">{{ item.type}}</td>
          <td class="p-3 border border-gray-200 text-center">{{ item.time}} </td>
          <td class="p-3 border border-gray-200 text-center">{{ item.value}} </td>
            <td class="p-3 border border-gray-200 text-center"><span @click="task_show(item.url)" class="w-full h-full text-success cursor-pointer">操作</span></td>
        </tr>
    </tbody>








    


  </table>



  

  <div v-if=" allPage> 0" class="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="text-sm text-gray-600 whitespace-nowrap">
                    共有 {{ allPage }} 页
                </div>
                
                <div class="flex items-center ">
                
                     <button 
                    @click="prepage" 
                       class="page-item"
                       :disabled="startPage"
                    >
                        <i class="fa fa-chevron-left"></i>
                    </button> 
                  
                    <div 
                        v-for="page in totalPages" 
                        :key="page"
                        @click="goToPage(page)"
                         :class="[
        'page-item', 
        { 
            'page-item-disabled': currentPage === totalPages,
            'bg-blue-500 text-white': currentPage === page  
        }
    ]"
                    >
                        {{ page }}
                    </div>
                    
                    <!-- 下一页按钮 -->
                    <button 
                     @click="nextpage" 
                        class="page-item"
                        :disabled="isLastPage"
                    >

                        <i class="fa fa-chevron-right"></i>
                    </button>
                </div></div>



   <div v-show="task"  class="bg-white rounded-xl shadow-sm  max-w-2xl mx-auto w-[60%] fixed z-10000 top-16 left-12 border-2 border-gray-300">
        <div class=" max-w-md mx-auto bg-white rounded-xl p-6 ">
      
        <div class="user-card text-neutral-600 text-base mb-5 pb-3 border-b border-neutral-300">
            关联卡号：<span class="font-semibold text-primary ">{{ now_card}}</span>
        </div>





   <label class="content-label block text-neutral-400 text-sm mb-2">需求:</label>
      <div  class="h-[60px] w-full mb-2">     
    
        <audio ref="audio" controls >


</audio></div>
         <div class="w-full mb-2">
            <label class="content-label block text-neutral-400 text-sm mb-2">位置：{{ now_position }}</label>
            <iframe src="../../../public/admin/map_html/task_mimcry.html" class="h-[120px] w-full" frameborder="0"></iframe>
                
            </div>
          <form action=""></form>
           <div class=" mb-1">
            <label class="content-label block text-neutral-400 text-sm mb-2">提交标题：</label>
             <input  v-model="now_title"  class="h-[30px] w-full shadow-md bg-neutral-100 text-neutral-500 text-base leading-relaxed p-3 rounded-lg mb-4"></input>           
        </div> 
        <div class=" mb-2">
            <label  class="content-label block text-neutral-400 text-sm mb-2">提交描述：</label>
             <textarea v-model="now_description" class="h-[90px] w-full shadow-md bg-neutral-100 text-neutral-500 text-base leading-relaxed p-3 rounded-lg mb-4" name="" id=""></textarea>

            
           
        </div>
          <div  class="flex justify-end gap-3">
            
             <input v-model="now_value" type="number"  class="w-[120px]  rounded-lg bg-white  text-neutral-400 font-semiboldtext-xl border border-gray-300 px-3 py-1 font-bold cursor-pointer"placeholder='请输入价值' >
           
      </input>
            
            <select v-model="now_type" class="  rounded-lg bg-white  text-neutral-400 font-semiboldtext-xl border border-gray-300 px-3 py-1 font-bold cursor-pointer"  >

  <option value="生活事务类">生活事务类</option>
  <option value="健康医疗类">健康医疗类</option>
  <option value="信息咨询类">信息咨询类</option>
  <option value="情感社交类">情感社交类</option>
  <option value="紧急">紧急</option>
        </select>
            
            
            
            
            
            
            <button @click="sub_data" class="  rounded-lg bg-white  text-neutral-400 font-semiboldtext-xl border border-gray-300 px-3 py-1 font-bold cursor-pointer" >
            确认
        </button>
        <button @click="hidden_task" class="  rounded-lg bg-white  text-neutral-400 font-semiboldtext-xl border border-gray-300 px-3 py-1 font-bold cursor-pointer" >
            关闭
        </button ></div>

          
        </div>
        
  
      </div>


   <div v-show="sos_task"  class="bg-white rounded-xl shadow-sm  max-w-2xl mx-auto w-[30%] fixed z-10000 top-20 left-12 border-2 border-gray-300">
        <div class=" max-w-md mx-auto bg-white rounded-xl p-6 ">
      
        <div class="user-card text-neutral-600 text-base mb-5 pb-3 border-b border-neutral-300">
            关联卡号：<span class="font-semibold text-primary ">{{ sos_card}}</span>
        </div>





   <label class="content-label block text-neutral-400 text-sm mb-2">姓名:{{ sos_name }}</label>
    <label class="content-label block text-neutral-400 text-sm mb-2">电话:{{ sos_phone }}</label>
    <label class="content-label block text-neutral-400 text-sm mb-2">紧急联系人电话:{{ sos_contact_phone }}</label>
    <label class="content-label block text-neutral-400 text-sm mb-2">可能疾病:{{ sos_disease}}</label>
     <label class="content-label block text-neutral-400 text-sm mb-2">注意:{{ sos_remark}}</label>
         <div class="w-full mb-2">
            <label class="content-label block text-neutral-400 text-sm mb-2">位置：{{position_sos }}</label>
            <iframe src="../../../public/admin/map_html/task_mimcry.html" class="h-[120px] w-full" frameborder="0"></iframe>
                
            </div>
          
       
          <div  class="flex justify-end gap-3">
            
          
           
      </input>
            
          
        <button @click="sos_sos_show" class="  rounded-lg bg-white  text-neutral-400 font-semiboldtext-xl border border-gray-300 px-3 py-1 font-bold cursor-pointer" >
            关闭
        </button ></div>

          
        </div>
        
  
      </div>


     </div>





<div v-if="sos_info" @click="click_sos_info_show" class="fixed w-[100px] h-[80px] bottom-1/2 right-0 bg-red-500 rounded-lg justify-center content-center">警告!</div>












        
</template>

<script setup>
import _ from 'lodash';
import { io } from 'socket.io-client';

import { ref,onMounted,computed,onUnmounted } from 'vue';
const data = ref([])
const count = ref([])
const currentPage = ref(1)
const allPage = ref(1)
const totalPages = ref([]);
const status = ref('all')

const type = ref('all')
const date = ref('all')

const task =ref(false);
const now_title= ref(null);
const now_position= ref(null);
const now_url= ref(null);


const now_type = ref("生活事务类");



const now_value = ref(null);
const audio= ref(null);


const sos_info =ref(false);
const sos_task =ref(false);

const sos_card = ref(''); 
const sos_name = ref(''); 
const sos_phone = ref('');
const sos_contact_phone = ref(''); 
const position_sos = ref('');
const sos_value= ref(null)
const sos_disease= ref('')
const sos_remark= ref('')



const now_card =ref('')
const now_description =ref('')

function sendToClient_point(data) {
 const message = data
  socket.emit('task_point', { from: "task", content: message });
}
var condition = {page:currentPage.value,date:date.value,status:status.value,type:type.value}


function sos_info_show(){sos_info.value =! sos_info.value

}

function sos_sos_show(){sos_task.value =! sos_task.value

}
function click_sos_info_show(){sos_info.value =! sos_info.value;
sos_task.value =! sos_task.value
console.log(sos_value.value)
const condition ={'card':sos_value.value['content']['card']}
console.log(condition)
const sos_task_task= async (condition) => {

  const response = await fetch('http://127.0.0.1:5137/user/user_health', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
        
      },
      body: JSON.stringify(condition) 
    });
  

    const fullData = await response.json();
    console.log(fullData)
 
    sos_card.value=fullData[0]['card']
sos_name.value=fullData[0]['name'] 
sos_phone.value=fullData[0]['phone'] 
 sos_contact_phone.value =fullData[0]['contact_phone'] 
sos_disease.value =fullData[0]['disease']
sos_remark.value =fullData[0]['remarker']  }
sos_task_task(condition)






const sos_data ={'url':sos_value.value['content']['url']}

const sos_task_fetch= async (condition) => {

  const response = await fetch('http://127.0.0.1:5137/task/task_mimicry', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
        
      },
      body: JSON.stringify(condition) 
    });
  

    const fullData = await response.json();

position_sos.value=fullData[0]['position']
 }
sos_task_fetch(sos_data)




sendToClient_point(sos_value.value['content']['url'])










}


function hidden_task(){task.value =! task.value}




const socket = io('http://127.0.0.1:5137');

  
  const handleConnect = () => {
    socket.emit('register', { room: 'task_list' });
  };

socket.on('sos', (data) => {console.log(data)
sos_value.value=data
sos_info_show()})
function task_show(data){
  task.value =! task.value
const condition ={'url':data}
const point_task= async (condition) => {

  const response = await fetch('http://127.0.0.1:5137/task/task_mimicry', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
        
      },
      body: JSON.stringify(condition) 
    });
  

    const fullData = await response.json();
    console.log(fullData )
    now_card.value =fullData[0]['card']
    now_title.value =fullData[0]['title']
    now_url.value=fullData[0]['url']
    now_description.value=fullData[0]['description']
    now_position.value=fullData[0]['position']
    audio.value.src =`http://127.0.0.1:5137/assets/uploads/${fullData[0]['url']} `
 }
point_task(condition)




 


sendToClient_point(data)
console.log(data)
}









function sub_data(){

const data ={'card':now_card.value,'title':now_title.value ,'description':now_description.value,'value':now_value.value,'type':now_type.value,'url':now_url.value}
const adjust_task= async (condition) => {

  const response = await fetch('http://127.0.0.1:5137/task/adjust_task', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
        
      },
      body: JSON.stringify(condition) 
    });
        const fullData = await response.json();
        if(fullData==='ok'){window.location.reload();}
 }
 
adjust_task(data)



}











const fetchData= async (condition) => {

  const response = await fetch('http://127.0.0.1:5137/task/task_list', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
        
      },
      body: JSON.stringify(condition) 
    });
  

    const fullData = await response.json();

 data.value = fullData;






 }
 



const fetchlist= async (condition) => {console.log(condition)
         const response = await fetch('http://127.0.0.1:5137/task/task_list_all', {
      method: 'POST', 
      headers: {
        'Content-Type': 'application/json', 
        
      },
      body: JSON.stringify(condition) 
    });
  

    const fullData = await response.json();

 count.value = fullData;
 console.log(count.value)


 allPage.value = Math.ceil( count.value/ 10)
 console.log(allPage.value)
if(allPage.value >4){
totalPages.value = [1,2,3,4] 
}else{totalPages.value = allPage.value}  

 }





onMounted(async () => {
handleConnect()  
  await fetchData(condition);
await fetchlist(condition)

});






async function goToPage(page) {  
  currentPage.value = page;
 var condition = {page:currentPage.value,date:date.value,status:status.value,type:type.value}
 await fetchData(condition);  
  
  
}


async function prepage() { 
  currentPage.value -=1;
var condition = {page:currentPage.value,date:date.value,status:status.value,type:type.value}
    await fetchData(condition);  
 
    const startPage = totalPages.value[0]

let number_list = null
    if (currentPage.value < startPage) { const pushData = [];
for (let i = startPage; i > startPage - 4 && i >  0; i=i-1) {
          number_list =i-1
          pushData.push(number_list);
          
        }
          totalPages.value = pushData.reverse();

    }

  } 


const isLastPage = computed(() => {
  
  return currentPage.value >= allPage.value;
});
const startPage =  computed(() => {
  if( currentPage.value===1){  return true;}

});





async function nextpage() { 
  currentPage.value +=1;
var condition = {page:currentPage.value,date:date.value,status:status.value,type:type.value}
  console.log(condition)

  await fetchData(condition);  
  
    const totalItems = count.value;
  
    const totalPagesCount = Math.ceil(totalItems / 5);
 const maxDisplayedPage = totalPages.value[totalPages.value.length - 1];
 console.log(maxDisplayedPage)
   if (currentPage.value > maxDisplayedPage) {
      
      if (totalPages.value.includes(totalPagesCount)) {

        totalPages.value = totalPages.value.map(page => page + 4);
      } else {
  
        const pushData = [];
 
        const startPage = Math.min(currentPage.value, totalPagesCount);
       
        for (let i = startPage; i < startPage + 4 && i <= totalPagesCount; i++) {
          pushData.push(i);
        }
        totalPages.value = pushData;
      }
    }
  } 


const filter_consition = () => {
var condition = {page:currentPage.value,date:date.value,status:status.value,type:type.value}
fetchData(condition)
fetchlist(condition)

}

const refresh =()=>{
  currentPage.value=1
  data.value ="all"
  type.value ="all"
  status.value ='all'
var condition = {page:currentPage.value,date:date.value,status:status.value,type:type.value}
fetchData(condition)


}










</script>
<style scoped>
.page-item:disabled {
  opacity: 0.6;
  cursor: not-allowed;

}
i{font-size: 28px;}
</style>









  