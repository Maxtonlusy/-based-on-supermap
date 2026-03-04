<template>
  <div class="wrapper" style="width: 100px; height: 100px;">
    <label class="title">工具</label>
    <button @click="draw">绘点</button>
  </div>
</template>

<script>
import { inject } from '@vue/runtime-core'
// 移除未使用的lodash.map导入
export default {
  setup() {
    const L = window.L // 假设已全局引入Leaflet库
    const mymap = inject('map') // 假设注入的mymap中，map属性是Leaflet地图实例

    // 定义事件处理函数（单独提取，方便解绑）
    const handleMapClick = (e) => {
      L.circle(e.latlng, {
        radius: 200, // 半径200米
        color: '#f00' // 边框红色
        // 可补充其他样式：fillColor（填充色）、fillOpacity（填充透明度）等
      }).addTo(mymap.map) // 修正：添加到地图实例（mymap.map）
    }

    function draw() {
      // 先解绑之前的事件，避免重复绑定
      mymap.map.off('click', handleMapClick)
      // 重新绑定事件
      mymap.map.on('click', handleMapClick)
    }

    // 暴露draw方法给模板
    return {
      draw
    }
  }
}
</script>

<style lang="css" scoped>
/* 保持原有的样式内容 */
.wrapper {
  padding: 10px;
  button {
    margin-top: 5px;
    padding: 3px 8px;
    cursor: pointer;
  }
}
</style>