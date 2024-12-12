<template>
  <div class="layout-container">
    <div class="layout-header" role="navigation" aria-label="主导航">
      <div class="header-left">
        <router-link to="/" class="logo" aria-label="返回首页">
          <div class="logo-container">
            <img src="@/assets/logo.png" alt="Web安全学习平台Logo" class="logo-image" />
            <span class="logo-text">安智领航</span>
          </div>
        </router-link>

        <el-button 
          class="mobile-menu-btn"
          text
          @click="toggleMobileMenu"
          aria-label="切换菜单"
        >
          <el-icon><Menu /></el-icon>
        </el-button>

        <div class="nav-links" :class="{ 'mobile-active': isMobileMenuOpen }">
          <el-dropdown 
            trigger="hover" 
            @visible-change="handleDropdownVisibility"
            aria-label="基础学习菜单"
          >
            <el-button 
              text
              class="nav-button"
              :class="{ 'is-active': activeMenu === 'basic' }"
              @mouseenter="handleMenuHover('basic')"
            >
              <el-icon><Reading /></el-icon>
              基础学习
              <el-icon class="el-icon--right"><CaretBottom /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/courses')">
                  <el-icon><Reading /></el-icon>课程学习
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/knowledge')">
                  <el-icon><Share /></el-icon>知识图谱
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/learning-path')">
                  <el-icon><Guide /></el-icon>学习路径
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <el-dropdown trigger="hover">
            <el-button text>
              <el-icon><Monitor /></el-icon>
              实践训练
              <el-icon class="el-icon--right"><CaretBottom /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/explore')">
                  <el-icon><Monitor /></el-icon>安全实验
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/practice')">
                  <el-icon><Operation /></el-icon>靶场训练
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/reports')">
                  <el-icon><Document /></el-icon>实验报告
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

          <el-dropdown trigger="hover">
            <el-button text>
              <el-icon><Trophy /></el-icon>
              挑战提升
              <el-icon class="el-icon--right"><CaretBottom /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="$router.push('/daily-challenge')">
                  <el-icon><Trophy /></el-icon>每日挑战
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/leaderboard')">
                  <el-icon><Medal /></el-icon>排行榜
                </el-dropdown-item>
                <el-dropdown-item @click="$router.push('/achievements')">
                  <el-icon><Star /></el-icon>成就徽章
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <div class="header-right">
        <el-input
          v-model="searchKeyword"
          class="search-input"
          placeholder="搜索..."
          :prefix-icon="Search"
          aria-label="搜索"
        />
        
        <el-badge :value="unreadCount" class="notification-badge" aria-label="未读通知">
          <el-button text aria-label="通知中心">
            <el-icon><Bell /></el-icon>
          </el-button>
        </el-badge>

        <template v-if="isAuthenticated">
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="avatar-container">
              <el-avatar :size="32" :src="userInfo?.avatar || defaultAvatar" />
              <span class="username">{{ userInfo?.username }}</span>
              <el-icon class="el-icon--right"><CaretBottom /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="messages">
                  <el-icon><Message /></el-icon>消息中心
                </el-dropdown-item>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人中心
                </el-dropdown-item>
                <el-dropdown-item command="settings">
                  <el-icon><Setting /></el-icon>账号设置
                </el-dropdown-item>
                <el-dropdown-item command="monitor">
                  <el-icon><Bell /></el-icon>监控预警
                </el-dropdown-item>
                <el-dropdown-item divided command="admin" v-if="isAdmin">
                  <el-icon><Management /></el-icon>管理后台
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
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  User, 
  Setting, 
  SwitchButton 
} from '@element-plus/icons-vue'
import {
  TrophyBase as Trophy,
  CaretBottom,
  Monitor,
  Reading,
  Operation,
  Share,
  Guide,
  Document,
  Medal,
  Star,
  Bell,
  Search,
  Message,
  Management,
  Menu
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const searchKeyword = ref('')
const unreadCount = ref(0)

const isAuthenticated = computed(() => {
  const token = authStore.token
  const userInfo = authStore.userInfo
  return !!token && !!userInfo
})

const isAdmin = computed(() => {
  return userInfo.value?.role === 'admin'
})

onMounted(async () => {
  if (authStore.token && !authStore.userInfo) {
    try {
      await authStore.getUserInfo()
    } catch (error) {
      console.error('Failed to get user info:', error)
    }
  }
})

const userInfo = computed(() => authStore.userInfo)
const defaultAvatar = 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png'

const handleCommand = async (command: string) => {
  switch (command) {
    case 'messages':
      await router.push('/messages')
      break
    case 'profile':
      await router.push('/profile')
      break
    case 'settings':
      await router.push('/settings')
      break
    case 'monitor':
      await router.push('/monitor')
      break
    case 'admin':
      await router.push('/admin')
      break
    case 'logout':
      try {
        authStore.logout()
        ElMessage.success('退出登录成功')
        router.push('/auth/login')
      } catch (error) {
        console.error('Logout error:', error)
      }
      break
  }
}

const isMobileMenuOpen = ref(false)
const activeMenu = ref('')

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const handleMenuHover = (menu: string) => {
  activeMenu.value = menu
}

const handleDropdownVisibility = (visible: boolean) => {
  // 可以添加额外的逻辑，比如记录状态或触发事件
}

const handleClickOutside = (event: MouseEvent) => {
  const navLinks = document.querySelector('.nav-links')
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn')
  
  if (isMobileMenuOpen.value && 
      navLinks && 
      !navLinks.contains(event.target as Node) &&
      mobileMenuBtn && 
      !mobileMenuBtn.contains(event.target as Node)) {
    isMobileMenuOpen.value = false
  }
}

const handleResize = () => {
  if (window.innerWidth > 768) {
    isMobileMenuOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
})
</script>

<style lang="scss" scoped>
.layout-container {
  min-height: 100vh;
  background: var(--bg-dark);
  color: var(--text-primary);
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
  background: rgba(13, 27, 42, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(255, 127, 80, 0.1);
  z-index: 1000;

  @media (max-width: 768px) {
    padding: 0 16px;
  }
}

.header-left {
  display: flex;
  align-items: center;
  gap: 40px;

  .logo {
    text-decoration: none;
    
    .logo-container {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 8px 0;
      
      .logo-image {
        width: 36px;
        height: 36px;
        object-fit: contain;
        transition: transform 0.3s ease;
      }
      
      .logo-text {
        font-size: 22px;
        font-weight: bold;
        color: var(--text-primary);
        background: linear-gradient(135deg, #ff7f50, #ff4f00);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        transition: opacity 0.3s;
      }
    }
    
    &:hover {
      .logo-image {
        transform: scale(1.1);
      }
      
      .logo-text {
        opacity: 0.8;
      }
    }
  }

  .nav-links {
    display: flex;
    gap: 24px;

    .el-button {
      color: var(--text-secondary);
      font-size: 15px;
      display: flex;
      align-items: center;
      gap: 6px;
      
      .el-icon {
        font-size: 16px;
      }

      &:hover {
        background: rgba(255, 127, 80, 0.1);
        color: var(--text-primary);
      }
    }
  }

  .mobile-menu-btn {
    display: none;
    margin-left: auto;
    
    @media (max-width: 768px) {
      display: block;
    }
  }
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;

  .el-button {
    color: var(--text-secondary);
    font-size: 14px;
    display: flex;
    align-items: center;
    gap: 6px;
    
    &:hover {
      color: var(--text-primary);
    }

    .el-icon {
      font-size: 16px;
    }
  }

  .el-button--primary {
    color: var(--bg-dark);
    background: var(--accent);
    border: none;
    padding: 8px 20px;
    font-weight: 500;
    
    &:hover {
      background: var(--accent-light);
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
  border: 1px solid rgba(255, 127, 80, 0.1);

  &:hover {
    border-color: rgba(255, 127, 80, 0.2);
    background: rgba(255, 127, 80, 0.1);
  }

  .username {
    color: var(--text-primary);
    font-size: 14px;
  }

  .el-icon {
    color: var(--text-secondary);
    font-size: 12px;
    transition: transform 0.3s;
  }

  &:hover .el-icon {
    transform: rotate(180deg);
  }
}

.layout-content {
  padding-top: 64px;
  min-height: calc(100vh - 64px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.search-input {
  width: 200px;
  margin-right: 16px;
  
  :deep(.el-input__wrapper) {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    
    &:hover {
      border-color: rgba(255, 127, 80, 0.3);
    }
    
    &:focus-within {
      border-color: rgba(255, 127, 80, 0.5);
      box-shadow: 0 0 0 2px rgba(255, 127, 80, 0.1);
    }
  }
  
  :deep(.el-input__inner) {
    color: var(--text-primary);
    
    &::placeholder {
      color: var(--text-disabled);
    }
  }

  @media (max-width: 768px) {
    display: none;
  }
  
  :deep(.el-input__wrapper) {
    &:focus-within {
      box-shadow: 0 0 0 2px rgba(100, 255, 218, 0.2);
    }
  }
}

.notification-badge {
  margin-right: 16px;
  
  :deep(.el-badge__content) {
    background-color: rgba(245, 108, 108, 0.9);
  }
}

.nav-links {
  @media (max-width: 768px) {
    position: absolute;
    top: 64px;
    left: 0;
    right: 0;
    background: rgba(26, 29, 33, 0.98);
    padding: 16px;
    flex-direction: column;
    gap: 16px;
    transform: translateY(-100%);
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    
    &.mobile-active {
      transform: translateY(0);
      opacity: 1;
      visibility: visible;
    }
  }
}

.nav-button {
  position: relative;
  color: var(--text-secondary);
  
  &::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 50%;
    width: 0;
    height: 2px;
    background: var(--accent);
    transition: all 0.3s ease;
    transform: translateX(-50%);
  }
  
  &:hover {
    color: var(--text-primary);
    
    &::after {
      width: 100%;
    }
  }
  
  &.is-active {
    color: var(--text-primary);
    
    &::after {
      width: 100%;
      background: var(--accent);
    }
  }
  
  &:focus-visible {
    outline: 2px solid var(--accent);
    outline-offset: 2px;
  }
}

:deep(*:focus-visible) {
  outline: 2px solid rgba(65, 184, 131, 0.5);
  outline-offset: 2px;
}

.el-dropdown-menu {
  background: var(--bg-dark);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 127, 80, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  
  .el-dropdown-menu__item {
    color: var(--text-secondary);
    
    &:hover {
      background: rgba(255, 127, 80, 0.1);
      color: var(--text-primary);
    }
    
    .el-icon {
      color: var(--accent);
    }
  }
}

:deep(.el-dropdown-menu) {
  background: var(--bg-dark);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 127, 80, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.nav-links, .header-right {
  :deep(.el-button) {
    &:focus-visible {
      outline: 2px solid #64ffda;
      outline-offset: 2px;
    }
  }
}

.el-dropdown-menu {
  animation: dropdownFade 0.2s ease-out;
}

@keyframes dropdownFade {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

// 覆盖 element-plus 的默认样式
:deep(.el-button) {
  &.el-button--text {
    &:focus,
    &:hover {
      background: rgba(65, 184, 131, 0.05);
      border-color: transparent;
    }
  }
}
</style> 