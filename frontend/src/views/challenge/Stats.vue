<template>
  <div class="challenge-stats">
    <el-card class="stats-overview">
      <template #header>
        <div class="card-header">
          <h3>训练统计概览</h3>
        </div>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card shadow="hover" class="stat-card">
            <template #header>完成挑战</template>
            <div class="stat-value">0</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="stat-card">
            <template #header>累计训练时长</template>
            <div class="stat-value">0h</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="stat-card">
            <template #header>获得积分</template>
            <div class="stat-value">0</div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="training-history mt-4">
      <template #header>
        <div class="card-header">
          <h3>训练历史</h3>
        </div>
      </template>
      <el-empty description="暂无训练记录" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

// TODO: 添加状态管理和数据获取逻辑
onMounted(() => {
  // 在这里获取统计数据
})
</script>

<style scoped>
.challenge-stats {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.stat-card {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.mt-4 {
  margin-top: 16px;
}
</style> 