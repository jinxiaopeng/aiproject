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
                <el-avatar :size="32" :src="userInfo?.avatar || defaultAvatar" />
                <span class="username">{{ userInfo?.username }}</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><UserIcon /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><SettingIcon /></el-icon>账号设置
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButtonIcon /></el-icon>退出登录
                  </el-dropdown-item>
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
import { ElMessage } from 'element-plus'
import { 
  User as UserIcon,
  Setting as SettingIcon,
  SwitchButton as SwitchButtonIcon
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// 计算属性
const isAuthenticated = computed(() => !!authStore.token)
const userInfo = computed(() => authStore.userInfo)
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

// 处理下拉菜单命令
const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      await router.push('/profile/index')
      break
    case 'settings':
      await router.push('/profile/settings')
      break
    case 'logout':
      try {
        await authStore.logout()
        ElMessage.success('退出登录成功')
        router.push('/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
      break
  }
}
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
  background: #1a1c2c;
  color: #fff;
}

.app-container {
  min-height: 100vh;
}

.header {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 64px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
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

.nav-links .el-button {
  color: rgba(255, 255, 255, 0.8);
}

.nav-links .el-button:hover {
  color: #fff;
}

.logo {
  text-decoration: none;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
  transition: color 0.3s;
}

.logo-text:hover {
  color: #79bbff;
}

.right {
  display: flex;
  gap: 16px;
  align-items: center;
}

.right .el-button {
  color: rgba(255, 255, 255, 0.8);
}

.right .el-button:hover {
  color: #fff;
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
  font-size: 14px;
  color: #fff;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 84px 20px 20px;
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

:deep(.el-dropdown-menu) {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-dropdown-menu__item) {
  color: #fff;
  display: flex;
  align-items: center;
  gap: 8px;
  
  &:hover {
    background: rgba(255, 255, 255, 0.1);
  }
  
  .el-icon {
    margin-right: 4px;
  }
}

:deep(.el-button--primary) {
  background: linear-gradient(45deg, #409EFF, #36D1DC);
  border: none;
  
  &:hover {
    background: linear-gradient(45deg, #36D1DC, #409EFF);
  }
}
</style> 