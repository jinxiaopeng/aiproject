<template>
  <div class="sidebar">
    <div class="logo">
      <span>Web安全学习导航</span>
    </div>
    <el-menu
      default-active="1"
      class="el-menu-vertical"
      background-color="#001529"
      text-color="#fff"
      active-text-color="#409EFF"
    >
      <el-menu-item index="1">
        <el-icon><Share /></el-icon>
        <span>知识图谱</span>
      </el-menu-item>
      <el-menu-item index="2">
        <el-icon><Histogram /></el-icon>
        <span>学习路径</span>
      </el-menu-item>
      <el-menu-item index="3">
        <el-icon><Document /></el-icon>
        <span>知识文档</span>
      </el-menu-item>
      <el-menu-item index="4">
        <el-icon><Setting /></el-icon>
        <span>系统设置</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { Share, Histogram, Document, Setting } from '@element-plus/icons-vue'
</script>

<style scoped>
.sidebar {
  height: 100%;
  background: #001529;
}

.logo {
  height: 64px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  color: #fff;
  font-size: 18px;
  font-weight: 500;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.el-menu {
  border-right: none;
}

.el-menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
}
</style> 