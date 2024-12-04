<template>
  <div class="forbidden-container">
    <div class="forbidden-content">
      <el-result
        icon="warning"
        title="403 无权访问"
        sub-title="抱歉，您没有权限访问此页面"
      >
        <template #extra>
          <el-button type="primary" @click="$router.push('/')">返回首页</el-button>
        </template>
      </el-result>
    </div>
  </div>
</template>

<style scoped>
.forbidden-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.forbidden-content {
  max-width: 600px;
  width: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 40px;
}

@media (max-width: 768px) {
  .forbidden-content {
    padding: 20px;
  }
}
</style> 