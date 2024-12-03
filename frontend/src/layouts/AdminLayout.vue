<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <el-aside width="240px" class="sidebar">
      <div class="sidebar-header">
        <img src="@/assets/security.svg" alt="Logo" class="logo">
        <span class="title">后台管理</span>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        class="sidebar-menu"
        :router="true"
        :collapse="isCollapse"
      >
        <el-menu-item index="/admin">
          <el-icon><DataBoard /></el-icon>
          <template #title>控制台</template>
        </el-menu-item>

        <el-menu-item index="/admin/users">
          <el-icon><User /></el-icon>
          <template #title>用户管理</template>
        </el-menu-item>

        <el-sub-menu index="courses">
          <template #title>
            <el-icon><Reading /></el-icon>
            <span>课程管理</span>
          </template>
          <el-menu-item index="/admin/courses">课程列表</el-menu-item>
          <el-menu-item index="/admin/courses/categories">课程分类</el-menu-item>
        </el-sub-menu>

        <el-sub-menu index="labs">
          <template #title>
            <el-icon><Monitor /></el-icon>
            <span>实验管理</span>
          </template>
          <el-menu-item index="/admin/labs">实验列表</el-menu-item>
          <el-menu-item index="/admin/labs/environments">环境管理</el-menu-item>
        </el-sub-menu>

        <el-menu-item index="/admin/settings">
          <el-icon><Setting /></el-icon>
          <template #title>系统设置</template>
        </el-menu-item>
      </el-menu>

      <div class="sidebar-footer">
        <el-button 
          type="text" 
          class="collapse-btn"
          @click="toggleCollapse"
        >
          <el-icon>
            <component :is="isCollapse ? 'Expand' : 'Fold'" />
          </el-icon>
        </el-button>
      </div>
    </el-aside>

    <!-- 主要内容区域 -->
    <el-container class="main-container">
      <!-- 顶部导航栏 -->
      <el-header height="64px" class="header">
        <div class="header-left">
          <el-breadcrumb>
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-right">
          <el-tooltip content="全屏" placement="bottom">
            <el-button
              type="text"
              class="action-btn"
              @click="toggleFullscreen"
            >
              <el-icon><FullScreen /></el-icon>
            </el-button>
          </el-tooltip>

          <el-tooltip content="消息" placement="bottom">
            <el-badge :value="3" class="action-badge">
              <el-button
                type="text"
                class="action-btn"
                @click="showMessages"
              >
                <el-icon><Bell /></el-icon>
              </el-button>
            </el-badge>
          </el-tooltip>

          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info">
              <el-avatar :size="32" :src="userStore.userInfo?.avatar">
                {{ userStore.userInfo?.username?.charAt(0).toUpperCase() }}
              </el-avatar>
              <span class="username">{{ userStore.userInfo?.username }}</span>
              <el-icon><CaretBottom /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="settings">系统设置</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 内容区域 -->
      <el-main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store'
import { ElMessage } from 'element-plus'
import {
  DataBoard,
  User,
  Reading,
  Monitor,
  Setting,
  Expand,
  Fold,
  FullScreen,
  Bell,
  CaretBottom
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const isCollapse = ref(false)

// 当前激活的菜单项
const activeMenu = computed(() => route.path)

// 当前路由名称
const currentRoute = computed(() => {
  const routeMap: Record<string, string> = {
    '/admin': '控制台',
    '/admin/users': '用户管理',
    '/admin/courses': '课程管理',
    '/admin/labs': '实验管理',
    '/admin/settings': '系统设置'
  }
  return routeMap[route.path] || '未知页面'
})

// 切换侧边栏折叠状态
const toggleCollapse = () => {
  isCollapse.value = !isCollapse.value
}

// 切换全屏
const toggleFullscreen = () => {
  if (!document.fullscreenElement) {
    document.documentElement.requestFullscreen()
  } else {
    document.exitFullscreen()
  }
}

// 显示消息
const showMessages = () => {
  ElMessage.info('消息功能开发中...')
}

// 处理下拉菜单命令
const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/admin/profile')
      break
    case 'settings':
      router.push('/admin/settings')
      break
    case 'logout':
      userStore.logout()
      router.push('/login')
      ElMessage.success('已退出登录')
      break
  }
}
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  display: flex;
}

/* 侧边栏样式 */
.sidebar {
  height: 100vh;
  background: #001529;
  color: #fff;
  display: flex;
  flex-direction: column;
  transition: width 0.3s;
  overflow: hidden;
}

.sidebar-header {
  height: 64px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(255, 255, 255, 0.05);
}

.logo {
  width: 32px;
  height: 32px;
}

.title {
  font-size: 18px;
  font-weight: 500;
  white-space: nowrap;
}

.sidebar-menu {
  flex: 1;
  border-right: none;
  background: transparent;
}

.sidebar-menu :deep(.el-menu) {
  border-right: none;
}

.sidebar-menu :deep(.el-menu-item),
.sidebar-menu :deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.65);
}

.sidebar-menu :deep(.el-menu-item:hover),
.sidebar-menu :deep(.el-sub-menu__title:hover) {
  color: #fff;
  background: rgba(255, 255, 255, 0.05);
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  color: #fff;
  background: #1890ff;
}

.sidebar-footer {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.collapse-btn {
  color: rgba(255, 255, 255, 0.65);
  font-size: 20px;
}

.collapse-btn:hover {
  color: #fff;
}

/* 主容器样式 */
.main-container {
  flex: 1;
  overflow: hidden;
}

/* 顶部导航栏样式 */
.header {
  background: #fff;
  border-bottom: 1px solid #f0f0f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.action-btn {
  padding: 8px;
  font-size: 20px;
  color: #666;
}

.action-btn:hover {
  color: #1890ff;
}

.action-badge :deep(.el-badge__content) {
  top: 8px;
  right: 8px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background: #f5f5f5;
}

.username {
  font-size: 14px;
  color: #666;
}

/* 主要内容区域样式 */
.main-content {
  background: #f0f2f5;
  height: calc(100vh - 64px);
  overflow-y: auto;
  padding: 24px;
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 