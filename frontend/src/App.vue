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

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

// 计算属性
const isAuthenticated = computed(() => userStore.isAuthenticated)
const username = computed(() => userStore.userInfo?.username || '')
const userAvatar = computed(() => userStore.userInfo?.avatar || '')

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
      await userStore.logout()
      router.push('/login')
      break
  }
}
</script>

<style>
.app-container {
  min-height: 100vh;
}

.header {
  background: rgba(26, 28, 44, 0.95);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 64px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
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
  background: linear-gradient(120deg, #bd34fe 30%, #47caff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 1px;
}

.right {
  display: flex;
  gap: 16px;
  align-items: center;
}

.avatar-container {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.avatar-container:hover {
  background: rgba(255, 255, 255, 0.1);
}

.username {
  color: #ffffff;
  font-size: 14px;
}

.main-content {
  padding-top: 64px;
  min-height: calc(100vh - 64px);
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

/* Element Plus 样式覆盖 */
:deep(.el-button) {
  --el-button-hover-text-color: #bd34fe;
  --el-button-hover-bg-color: transparent;
  --el-button-hover-border-color: transparent;
}

:deep(.el-button--primary) {
  --el-button-bg-color: #bd34fe;
  --el-button-border-color: #bd34fe;
  --el-button-hover-bg-color: #47caff;
  --el-button-hover-border-color: #47caff;
}

:deep(.el-dropdown-menu__item:not(.is-disabled):focus) {
  background-color: rgba(189, 52, 254, 0.1);
  color: #bd34fe;
}

/* 响应式样式 */
@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .logo-text {
    font-size: 20px;
  }

  .right {
    gap: 8px;
  }

  .username {
    display: none;
  }
}
</style> 