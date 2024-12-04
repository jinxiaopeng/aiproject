<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <el-aside width="240px" class="aside">
      <div class="logo">
        <img src="@/assets/security.svg" alt="Logo" class="logo-img">
        <h1>管理后台</h1>
      </div>
      
      <el-menu
        :default-active="activeMenu"
        class="menu"
        :router="true"
      >
        <el-menu-item index="/admin/dashboard">
          <el-icon><DataLine /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        
        <el-sub-menu index="user">
          <template #title>
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </template>
          <el-menu-item index="/admin/users">用户列表</el-menu-item>
          <el-menu-item index="/admin/roles">角色管理</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="course">
          <template #title>
            <el-icon><Reading /></el-icon>
            <span>课程管理</span>
          </template>
          <el-menu-item index="/admin/courses">课程列表</el-menu-item>
          <el-menu-item index="/admin/lessons">课时管理</el-menu-item>
          <el-menu-item index="/admin/categories">分类管理</el-menu-item>
        </el-sub-menu>
        
        <el-sub-menu index="lab">
          <template #title>
            <el-icon><Monitor /></el-icon>
            <span>实验管理</span>
          </template>
          <el-menu-item index="/admin/labs">实验列表</el-menu-item>
          <el-menu-item index="/admin/environments">环境管理</el-menu-item>
        </el-sub-menu>
        
        <el-menu-item index="/admin/knowledge">
          <el-icon><Document /></el-icon>
          <span>知识库管理</span>
        </el-menu-item>
        
        <el-menu-item index="/admin/feedback">
          <el-icon><ChatDotRound /></el-icon>
          <span>反馈管理</span>
        </el-menu-item>
        
        <el-menu-item index="/admin/settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <!-- 主内容区 -->
    <el-container class="main">
      <!-- 顶部导航 -->
      <el-header class="header">
        <div class="header-left">
          <el-icon 
            class="collapse-btn"
            @click="isCollapse = !isCollapse"
          >
            <Fold v-if="!isCollapse" />
            <Expand v-else />
          </el-icon>
          
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/admin' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentRoute.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        
        <div class="header-right">
          <el-tooltip content="全屏" placement="bottom">
            <el-icon class="action-icon" @click="toggleFullscreen">
              <FullScreen v-if="!isFullscreen" />
              <Aim v-else />
            </el-icon>
          </el-tooltip>
          
          <el-tooltip content="消息" placement="bottom">
            <el-badge :value="3" class="action-icon">
              <el-icon><Bell /></el-icon>
            </el-badge>
          </el-tooltip>
          
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="user-info">
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
        </div>
      </el-header>

      <!-- 内容区 -->
      <el-main class="content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  DataLine,
  User,
  Reading,
  Monitor,
  Document,
  ChatDotRound,
  Setting,
  Fold,
  Expand,
  FullScreen,
  Aim,
  Bell
} from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'

export default defineComponent({
  name: 'AdminLayout',
  components: {
    DataLine,
    User,
    Reading,
    Monitor,
    Document,
    ChatDotRound,
    Setting,
    Fold,
    Expand,
    FullScreen,
    Aim,
    Bell
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const userStore = useUserStore()
    
    const isCollapse = ref(false)
    const isFullscreen = ref(false)
    
    // 计算属性
    const activeMenu = computed(() => route.path)
    const currentRoute = computed(() => route)
    const username = computed(() => userStore.userInfo?.username || '')
    const userAvatar = computed(() => userStore.userInfo?.avatar || '')
    
    // 切换全屏
    const toggleFullscreen = () => {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen()
        isFullscreen.value = true
      } else {
        document.exitFullscreen()
        isFullscreen.value = false
      }
    }
    
    // 处理下拉菜单命令
    const handleCommand = async (command: string) => {
      switch (command) {
        case 'profile':
          router.push('/profile')
          break
        case 'settings':
          router.push('/admin/settings')
          break
        case 'logout':
          try {
            userStore.logout()
            ElMessage.success('已退出登录')
            router.push('/login')
          } catch (error) {
            ElMessage.error('退出失败，请重试')
          }
          break
      }
    }
    
    // 监听全屏变化
    const handleFullscreenChange = () => {
      isFullscreen.value = !!document.fullscreenElement
    }
    
    onMounted(() => {
      document.addEventListener('fullscreenchange', handleFullscreenChange)
    })
    
    onUnmounted(() => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange)
    })
    
    return {
      isCollapse,
      isFullscreen,
      activeMenu,
      currentRoute,
      username,
      userAvatar,
      toggleFullscreen,
      handleCommand
    }
  }
})
</script>

<style scoped>
.admin-layout {
  height: 100vh;
  display: flex;
}

.aside {
  background-color: #001529;
  color: #fff;
  height: 100vh;
  overflow-x: hidden;
  transition: width 0.3s;
}

.logo {
  height: 60px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logo-img {
  width: 32px;
  height: 32px;
}

.logo h1 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
  color: #fff;
}

.menu {
  border-right: none;
  background-color: transparent;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item),
:deep(.el-sub-menu__title) {
  color: rgba(255, 255, 255, 0.65);
}

:deep(.el-menu-item:hover),
:deep(.el-sub-menu__title:hover) {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}

:deep(.el-menu-item.is-active) {
  color: #fff;
  background-color: var(--primary-color);
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.header {
  background: #fff;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  color: var(--text-color-secondary);
}

.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.action-icon {
  font-size: 20px;
  cursor: pointer;
  color: var(--text-color-secondary);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.username {
  font-size: 14px;
  color: var(--text-color);
}

.content {
  flex: 1;
  overflow: auto;
  background-color: #f5f7fa;
  padding: 20px;
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

@media (max-width: 768px) {
  .aside {
    position: fixed;
    z-index: 1000;
    transform: translateX(-100%);
  }
  
  .aside.is-expanded {
    transform: translateX(0);
  }
  
  .header {
    padding: 0 16px;
  }
  
  .username {
    display: none;
  }
}
</style> 