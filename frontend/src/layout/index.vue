<template>
  <div class="layout-container">
    <div class="layout-header">
      <div class="header-left">
        <router-link to="/" class="logo">
          <span class="logo-text">Web安全学习平台</span>
        </router-link>
        <div class="nav-links">
          <el-button text @click="$router.push('/explore')">
            <el-icon><Monitor /></el-icon>
            安全实验
          </el-button>
          <el-button text @click="$router.push('/courses')">
            <el-icon><Reading /></el-icon>
            学习课程
          </el-button>
          <el-button text @click="$router.push('/labs')">
            <el-icon><Operation /></el-icon>
            靶场训练
          </el-button>
          <el-button text @click="$router.push('/knowledge')">
            <el-icon><Share /></el-icon>
            知识图谱
          </el-button>
        </div>
      </div>
      
      <div class="header-right">
        <template v-if="isAuthenticated">
          <el-button text @click="$router.push('/challenge')">
            <el-icon><Trophy /></el-icon>
            每日挑战
          </el-button>
          
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="avatar-container">
              <el-avatar :size="32" :src="userInfo?.avatar || defaultAvatar" />
              <span class="username">{{ userInfo?.username }}</span>
              <el-icon class="el-icon--right"><CaretBottom /></el-icon>
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
          <el-button text @click="$router.push('/auth/login')">登录</el-button>
          <el-button type="primary" @click="$router.push('/auth/register')">注册账号</el-button>
        </template>
      </div>
    </div>

    <div class="layout-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
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
  User, 
  Setting, 
  SwitchButton, 
  Trophy, 
  CaretBottom,
  Monitor,
  Reading,
  Operation,
  Share
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const isAuthenticated = computed(() => !!authStore.token)
const userInfo = computed(() => authStore.userInfo)
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

const handleCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      await router.push('/profile')
      break
    case 'settings':
      await router.push('/settings')
      break
    case 'logout':
      try {
        await authStore.logout()
        ElMessage.success('退出登录成功')
        router.push('/auth/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
      break
  }
}
</script>

<style lang="scss" scoped>
.layout-container {
  min-height: 100vh;
  background: #0a192f;
  color: #e6f1ff;
}

.layout-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  padding: 0 40px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(10, 25, 47, 0.85);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(136, 146, 176, 0.1);
  z-index: 1000;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 40px;

  .logo {
    text-decoration: none;
    
    .logo-text {
      font-size: 22px;
      font-weight: bold;
      background: linear-gradient(120deg, #64ffda, #00ff88);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      transition: opacity 0.3s;
      
      &:hover {
        opacity: 0.8;
      }
    }
  }

  .nav-links {
    display: flex;
    gap: 24px;

    .el-button {
      color: #8892b0;
      font-size: 15px;
      display: flex;
      align-items: center;
      gap: 6px;
      
      .el-icon {
        font-size: 16px;
      }
      
      &:hover {
        color: #64ffda;
      }
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;

  .el-button {
    color: #8892b0;
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
    
    &:hover {
      color: #64ffda;
    }

    .el-icon {
      font-size: 16px;
    }
  }

  .el-button--primary {
    color: #0a192f;
    background: #64ffda;
    border: none;
    padding: 8px 20px;
    font-weight: 500;
    
    &:hover {
      background: #00ff88;
      transform: translateY(-1px);
    }
  }
}

.avatar-container {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 12px;
  border-radius: 6px;
  transition: all 0.3s;
  border: 1px solid rgba(136, 146, 176, 0.1);
  
  &:hover {
    border-color: #64ffda;
    background: rgba(100, 255, 218, 0.1);
  }
  
  .username {
    color: #e6f1ff;
    font-size: 14px;
  }

  .el-icon {
    color: #8892b0;
    font-size: 12px;
    transition: transform 0.3s;
  }

  &:hover .el-icon {
    transform: rotate(180deg);
    color: #64ffda;
  }
}

.layout-content {
  padding-top: 64px;
  min-height: calc(100vh - 64px);
}

:deep(.el-dropdown-menu) {
  background: rgba(10, 25, 47, 0.95);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(136, 146, 176, 0.1);
  padding: 4px;
  border-radius: 6px;
}

:deep(.el-dropdown-menu__item) {
  color: #8892b0;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  
  &:hover {
    background: rgba(100, 255, 218, 0.1);
    color: #64ffda;
  }
  
  .el-icon {
    font-size: 16px;
  }

  &.is-disabled {
    color: rgba(136, 146, 176, 0.4);
  }

  &.el-dropdown-menu__item--divided {
    border-top-color: rgba(136, 146, 176, 0.1);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style> 