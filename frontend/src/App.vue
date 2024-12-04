<template>
  <div class="app-container">
    <!-- 全局加载状态 -->
    <global-loading :loading="loading" :message="loadingMessage" />
    
    <!-- 导航栏 -->
    <el-header class="header" height="60px">
      <div class="nav-container">
        <div class="left">
          <router-link to="/" class="logo">
            <img src="@/assets/security.svg" alt="Logo" class="logo-img">
            <h2 class="logo-text">安全学院</h2>
          </router-link>
          <el-menu 
            mode="horizontal" 
            :router="true" 
            class="nav-menu"
            :default-active="activeMenu"
          >
            <el-menu-item index="/">首页</el-menu-item>
            <el-menu-item index="/courses">课程中心</el-menu-item>
            <el-menu-item index="/labs">在线实验</el-menu-item>
            <el-menu-item index="/knowledge">知识库</el-menu-item>
          </el-menu>
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
            <el-button type="text" @click="$router.push('/login')">登录</el-button>
            <el-button type="primary" @click="$router.push('/register')">注册</el-button>
          </template>
        </div>
      </div>
    </el-header>

    <!-- 面包屑 -->
    <div v-if="showBreadcrumb" class="breadcrumb-container">
      <breadcrumb />
    </div>

    <!-- 内容区 -->
    <div class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive :include="cachedViews">
            <component :is="Component" />
          </keep-alive>
        </transition>
      </router-view>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import GlobalLoading from '@/components/common/GlobalLoading.vue'
import Breadcrumb from '@/components/common/Breadcrumb.vue'
import { ElMessage } from 'element-plus'

export default defineComponent({
  name: 'App',
  components: {
    GlobalLoading,
    Breadcrumb
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    // 加载状态
    const loading = ref(false)
    const loadingMessage = ref('加载中...')
    
    // 计算属性
    const isAuthenticated = computed(() => !!userStore.token)
    const username = computed(() => userStore.userInfo?.username || '')
    const userAvatar = computed(() => userStore.userInfo?.avatar || '')
    const activeMenu = computed(() => route.path)
    const showBreadcrumb = computed(() => route.path !== '/')
    
    // 需要缓存的页面
    const cachedViews = ['Home', 'CourseList', 'Knowledge']
    
    // 处理下拉菜单命令
    const handleCommand = async (command: string) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'settings':
          router.push('/settings')
          break
        case 'logout':
          try {
            userStore.logout()
            ElMessage.success('已退出登录')
            router.push('/login')
          } catch (error) {
            ElMessage.error('退出登录失败')
          }
          break
      }
    }
    
    return {
      loading,
      loadingMessage,
      isAuthenticated,
      username,
      userAvatar,
      activeMenu,
      showBreadcrumb,
      cachedViews,
      handleCommand
    }
  }
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
  background-color: #f5f7fa;
  color: #333;
  line-height: 1.5;
}

.app-container {
  min-height: 100vh;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
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
  display: flex;
  align-items: center;
  text-decoration: none;
  margin-right: 40px;
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 8px;
}

.logo-text {
  font-size: 20px;
  color: #1890ff;
  margin: 0;
}

.nav-menu {
  border: none;
}

.right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.avatar-container {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
  color: #666;
}

.breadcrumb-container {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  z-index: 999;
  background: #fff;
  padding: 0 20px;
  border-bottom: 1px solid #eee;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  margin-top: 60px;
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