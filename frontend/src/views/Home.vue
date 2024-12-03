<template>
  <div class="home">
    <h1>欢迎来到安全学院</h1>
    <div class="content">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>Web安全</span>
              </div>
            </template>
            <div class="card-content">
              学习Web应用安全漏洞与防护
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>系统安全</span>
              </div>
            </template>
            <div class="card-content">
              掌握系统安全加固技术
            </div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card>
            <template #header>
              <div class="card-header">
                <span>密码学</span>
              </div>
            </template>
            <div class="card-content">
              探索现代密码学原理与应用
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'Home'
})
</script>

<style scoped>
.home {
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
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-content {
  color: #666;
  line-height: 1.5;
}

.el-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.el-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}
</style> 