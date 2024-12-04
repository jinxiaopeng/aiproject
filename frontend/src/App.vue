<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <el-header class="header" height="64px">
      <div class="nav-container">
        <div class="left">
          <router-link to="/" class="logo">
            <span class="logo-text">CYBER-EDU</span>
          </router-link>
          <div class="nav-links">
            <el-button text @click="$router.push('/explore')">探索</el-button>
            <el-button text @click="$router.push('/courses')">课程</el-button>
            <el-button text @click="$router.push('/labs')">实验室</el-button>
            <el-button text @click="$router.push('/knowledge')">知识图谱</el-button>
          </div>
        </div>
        <div class="right">
          <template v-if="isAuthenticated">
            <el-dropdown trigger="click" @command="handleCommand">
              <div class="avatar-container">
                <el-avatar :size="32" :src="userAvatar" />
                <span class="username">{{ username }}</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                  <el-dropdown-item command="settings">系统设置</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <el-button text @click="$router.push('/login')">登录</el-button>
            <el-button type="primary" @click="$router.push('/register')">加入我们</el-button>
          </template>
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
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 64px;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 64px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.left {
  display: flex;
  align-items: center;
  gap: 40px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.logo {
  text-decoration: none;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #1890ff;
  transition: color 0.3s;
}

.logo-text:hover {
  color: #40a9ff;
}

.right {
  display: flex;
  gap: 16px;
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