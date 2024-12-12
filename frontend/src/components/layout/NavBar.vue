<template>
  <el-menu mode="horizontal" router>
    <el-menu-item index="/">首页</el-menu-item>
    <el-menu-item index="/knowledge">知识图谱</el-menu-item>
    <div class="flex-grow" />
    <template v-if="isLoggedIn">
      <el-menu-item>
        <el-dropdown trigger="click">
          <span class="user-menu">
            <el-avatar :size="32" :src="userInfo?.avatar">{{ username?.charAt(0) }}</el-avatar>
            <span class="username">{{ username }}</span>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item :icon="User" @click="router.push('/profile')">
                个人中心
              </el-dropdown-item>
              <el-dropdown-item :icon="Setting" @click="router.push('/settings')">
                账号设置
              </el-dropdown-item>
              <el-dropdown-item :icon="Bell" @click="router.push('/monitor')">
                监控预警
              </el-dropdown-item>
              <el-dropdown-item divided :icon="SwitchButton" @click="handleLogout">
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-menu-item>
    </template>
    <template v-else>
      <el-menu-item index="/login">登录</el-menu-item>
    </template>
  </el-menu>
</template>

<script setup lang="ts">
import { ArrowDown, User, Setting, Bell, SwitchButton } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()
const { isLoggedIn, username, userInfo } = storeToRefs(authStore)

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped lang="scss">
.flex-grow {
  flex-grow: 1;
}

.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  
  .username {
    font-size: 14px;
  }
}

.el-dropdown-menu__item {
  display: flex;
  align-items: center;
  gap: 8px;
  
  .el-icon {
    margin-right: 4px;
  }
}
</style> 