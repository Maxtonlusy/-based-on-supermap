<template>

            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
                <h3 class="font-semibold text-gray-800">筛选条件</h3>
                <button class="text-primary text-sm hover:text-primary/80 transition-custom flex items-center self-start md:self-auto">
                    <i class="fa fa-refresh mr-1"></i> 重置筛选
                </button>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div>
                    <label for="filterStatus" class="block text-sm font-medium text-gray-700 mb-1">反馈状态</label>
                    <select id="filterStatus" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom">
                        <option value="all">全部状态</option>
                        <option value="pending">待处理</option>
                        <option value="processing">处理中</option>
                        <option value="resolved">已解决</option>
                        <option value="closed">已关闭</option>
                    </select>
                </div>
                
                <div>
                    <label for="filterType" class="block text-sm font-medium text-gray-700 mb-1">反馈类型</label>
                    <select id="filterType" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom">
                        <option value="all">全部类型</option>
                        <option value="bug">系统bug</option>
                        <option value="feature">功能建议</option>
                        <option value="data">数据问题</option>
                        <option value="performance">性能问题</option>
                        <option value="other">其他问题</option>
                    </select>
                </div>
                
                <div>
                    <label for="filterPriority" class="block text-sm font-medium text-gray-700 mb-1">优先级</label>
                    <select id="filterPriority" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom">
                        <option value="all">全部优先级</option>
                        <option value="low">低</option>
                        <option value="medium">中</option>
                        <option value="high">高</option>
                    </select>
                </div>
                
                <div>
                    <label for="filterDate" class="block text-sm font-medium text-gray-700 mb-1">提交日期</label>
                    <input type="date" id="filterDate" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom">
                </div>
            </div>
            
            <div class="mt-4 flex flex-col sm:flex-row gap-3">
                <div class="relative flex-grow">
                    <input type="text" placeholder="搜索反馈标题、内容或提交人..." class="pl-9 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-custom w-full">
                    <i class="fa fa-search absolute left-3 top-1/2 -translate-y-1/2 text-neutral"></i>
                </div>
                
                <button class="bg-primary hover:bg-primary/90 text-white font-medium py-2 px-6 rounded-md transition-custom flex items-center justify-center whitespace-nowrap">
                    <i class="fa fa-filter mr-2"></i> 应用筛选
                </button>
                
                <button class="border border-gray-300 hover:border-gray-400 text-gray-700 font-medium py-2 px-6 rounded-md transition-custom flex items-center justify-center whitespace-nowrap">
                    <i class="fa fa-download mr-2"></i> 导出数据
                </button>
            </div>
     
</template>

<script>
export default {
    setup () {
        

        return {}
    }
}
</script>

<style lang="scss" scoped>

</style>