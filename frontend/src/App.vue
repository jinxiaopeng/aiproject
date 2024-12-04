<template>
  <div class="app-container">
    <el-config-provider :locale="zhCn">
      <!-- 顶部导航栏 -->
      <el-header class="header" v-if="showHeader">
        <div class="logo">
          <router-link to="/">Web安全智能学习平台</router-link>
        </div>
        
        <div class="nav-menu">
          <router-link to="/" class="nav-item">首页</router-link>
          <router-link to="/courses" class="nav-item">课程</router-link>
          <router-link to="/labs" class="nav-item">实验室</router-link>
        </div>
        
        <div class="user-menu">
          <template v-if="isLoggedIn">
            <el-dropdown @command="handleCommand">
              <div class="avatar-container">
                <el-avatar :size="32" :src="userInfo?.avatar || defaultAvatar" />
                <span class="username">{{ userInfo?.username }}</span>
              </div>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">
                    <el-icon><User /></el-icon>个人中心
                  </el-dropdown-item>
                  <el-dropdown-item command="settings">
                    <el-icon><Setting /></el-icon>账号设置
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <router-link to="/login" class="login-btn">
              <el-button type="primary">登录</el-button>
            </router-link>
          </template>
        </div>
      </el-header>
      
      <!-- 主要内容区域 -->
      <router-view />
    </el-config-provider>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { User, Setting, SwitchButton } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isLoggedIn = computed(() => authStore.token)
const userInfo = computed(() => authStore.userInfo)
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

// 是否显示头部导航栏（登录页面不显示）
const showHeader = computed(() => route.name !== 'Login')

// 处理下拉菜单命令
const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/profile/settings')
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

<style lang="scss" scoped>
.app-container {
  height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 20px;
  height: 60px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  
  .logo {
    a {
      color: #fff;
      font-size: 20px;
      font-weight: bold;
      text-decoration: none;
      
      &:hover {
        color: #409EFF;
      }
    }
  }
  
  .nav-menu {
    display: flex;
    gap: 20px;
    
    .nav-item {
      color: #fff;
      text-decoration: none;
      font-size: 16px;
      padding: 8px 12px;
      border-radius: 4px;
      transition: all 0.3s;
      
      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }
      
      &.router-link-active {
        color: #409EFF;
        background: rgba(64, 158, 255, 0.1);
      }
    }
  }
  
  .user-menu {
    .avatar-container {
      display: flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      padding: 4px 8px;
      border-radius: 4px;
      transition: all 0.3s;
      
      &:hover {
        background: rgba(255, 255, 255, 0.1);
      }
      
      .username {
        color: #fff;
        font-size: 14px;
      }
    }
  }
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
  
  .el-icon {
    margin-right: 4px;
  }
}
</style> 