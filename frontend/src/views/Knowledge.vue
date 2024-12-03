<template>
  <div class="knowledge">
    <h1>知识库</h1>
    <div class="content">
      <el-empty description="知识库开发中..." />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Knowledge'
})
</script>

<style scoped>
.knowledge {
  padding: 20px;
}

h1 {
  text-align: center;
  margin-bottom: 40px;
  color: #1890ff;
}

.content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}
</style> 