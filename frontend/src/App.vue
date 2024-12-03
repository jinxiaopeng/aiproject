<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <el-header class="header">
      <div class="nav-container">
        <div class="left">
          <h2 class="logo">安全学院</h2>
          <el-menu mode="horizontal" :router="true" class="nav-menu">
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/learning">课程中心</el-menu-item>
            <el-menu-item index="/labs">在线实验</el-menu-item>
            <el-menu-item index="/knowledge">知识库</el-menu-item>
          </el-menu>
        </div>
        <div class="right">
          <el-button type="text">登录</el-button>
          <el-button type="primary">注册</el-button>
        </div>
      </div>
    </el-header>

    <!-- 内容区 -->
    <div class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'App'
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.app-container {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 60px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.left {
  display: flex;
  align-items: center;
}

.logo {
  font-size: 20px;
  color: #1890ff;
  margin-right: 40px;
  cursor: pointer;
}

.nav-menu {
  border: none;
}

.right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: calc(100vh - 60px);
}

/* 路由过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 