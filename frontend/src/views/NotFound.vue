<template>
  <div class="not-found">
    <div class="content">
      <img src="@/assets/404.svg" alt="404" class="error-image">
      <h1>404</h1>
      <h2>页面不存在</h2>
      <p>抱歉，您访问的页面不存在或已被删除</p>
      <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'NotFound'
})
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f5f7fa;
}

.content {
  text-align: center;
  padding: 40px;
}

.error-image {
  width: 200px;
  height: 200px;
  margin-bottom: 24px;
}

h1 {
  font-size: 72px;
  color: var(--primary-color);
  margin: 0 0 16px;
}

h2 {
  font-size: 24px;
  color: var(--text-color);
  margin: 0 0 16px;
}

p {
  font-size: 16px;
  color: var(--text-color-secondary);
  margin: 0 0 24px;
}

.el-button {
  padding: 12px 24px;
  font-size: 16px;
}
</style> 