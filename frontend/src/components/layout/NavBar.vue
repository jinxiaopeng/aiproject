<template>
  <div class="navbar">
    <div class="left-menu">
      <hamburger
        :is-active="!isCollapse"
        class="hamburger-container"
        @toggle-click="toggleSideBar"
      />
      <breadcrumb class="breadcrumb-container" />
    </div>

    <div class="right-menu">
      <header-search class="right-menu-item" />
      
      <el-dropdown class="avatar-container right-menu-item" trigger="click">
        <div class="avatar-wrapper">
          <el-avatar :size="30" :src="userInfo?.avatar" />
          <span class="user-name">{{ userInfo?.username }}</span>
          <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </div>
        
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item :icon="User" @click="router.push('/profile')">
              个人中心
            </el-dropdown-item>
            <el-dropdown-item :icon="Setting" @click="router.push('/settings')">
              账号设置
            </el-dropdown-item>
            <el-dropdown-item divided :icon="SwitchButton" @click="handleLogout">
              退出登录
            </el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ArrowDown, User, Setting, SwitchButton } from '@element-plus/icons-vue'
import { useAppStore } from '@/stores/app'
import { useAuthStore } from '@/stores/auth'
import Hamburger from '@/components/Hamburger.vue'
import Breadcrumb from '@/components/Breadcrumb.vue'
import HeaderSearch from '@/components/HeaderSearch.vue'

const router = useRouter()
const appStore = useAppStore()
const authStore = useAuthStore()

const isCollapse = computed(() => appStore.sidebar.opened)
const userInfo = computed(() => authStore.userInfo)

const toggleSideBar = () => {
  appStore.toggleSidebar()
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    ElMessage.success('退出登录成功')
    router.push('/auth/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  height: 50px;
  overflow: hidden;
  position: relative;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);

  .hamburger-container {
    line-height: 46px;
    height: 100%;
    float: left;
    cursor: pointer;
    transition: background 0.3s;
    -webkit-tap-highlight-color: transparent;

    &:hover {
      background: rgba(0, 0, 0, 0.025);
    }
  }

  .breadcrumb-container {
    float: left;
  }

  .right-menu {
    float: right;
    height: 100%;
    line-height: 50px;
    display: flex;
    align-items: center;

    &:focus {
      outline: none;
    }

    .right-menu-item {
      display: inline-block;
      padding: 0 8px;
      height: 100%;
      font-size: 18px;
      color: #5a5e66;
      vertical-align: text-bottom;

      &.hover-effect {
        cursor: pointer;
        transition: background 0.3s;

        &:hover {
          background: rgba(0, 0, 0, 0.025);
        }
      }
    }

    .avatar-container {
      margin-right: 30px;

      .avatar-wrapper {
        margin-top: 5px;
        position: relative;
        display: flex;
        align-items: center;
        cursor: pointer;

        .user-name {
          margin: 0 5px;
          color: #606266;
        }

        .el-icon-caret-bottom {
          font-size: 12px;
        }
      }
    }
  }
}
</style> 