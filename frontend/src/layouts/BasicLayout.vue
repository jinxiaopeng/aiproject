<!-- 基础布局组件 -->
<template>
  <a-layout class="layout">
    <!-- 顶部导航 -->
    <a-layout-header class="header">
      <div class="logo">
        <img src="@/assets/logo.png" alt="Logo" />
        <span>靶场训练平台</span>
      </div>
      
      <div class="header-right">
        <!-- 通知中心 -->
        <notification-center class="notification" />
        
        <!-- 用户菜单 -->
        <a-dropdown>
          <a class="user-menu" @click.prevent>
            <a-avatar :src="userAvatar" />
            <span class="username">{{ username }}</span>
          </a>
          <template #overlay>
            <a-menu>
              <a-menu-item key="profile">
                <user-outlined />
                个人中心
              </a-menu-item>
              <a-menu-item key="settings">
                <setting-outlined />
                设置
              </a-menu-item>
              <a-menu-divider />
              <a-menu-item key="logout" @click="handleLogout">
                <logout-outlined />
                退出登录
              </a-menu-item>
            </a-menu>
          </template>
        </a-dropdown>
      </div>
    </a-layout-header>
    
    <!-- 侧边栏 -->
    <a-layout>
      <a-layout-sider
        v-model:collapsed="collapsed"
        :trigger="null"
        collapsible
        class="sider"
      >
        <a-menu
          v-model:selectedKeys="selectedKeys"
          v-model:openKeys="openKeys"
          mode="inline"
          theme="dark"
        >
          <a-menu-item key="dashboard">
            <dashboard-outlined />
            <span>仪表盘</span>
          </a-menu-item>
          
          <a-sub-menu key="challenges">
            <template #title>
              <experiment-outlined />
              <span>靶场训练</span>
            </template>
            <a-menu-item key="web">Web安全</a-menu-item>
            <a-menu-item key="system">系统安全</a-menu-item>
            <a-menu-item key="crypto">密码学</a-menu-item>
          </a-sub-menu>
          
          <a-menu-item key="ranking">
            <trophy-outlined />
            <span>排行榜</span>
          </a-menu-item>
          
          <a-menu-item key="discussion">
            <message-outlined />
            <span>讨论区</span>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      
      <!-- 主要内容区 -->
      <a-layout-content class="content">
        <router-view></router-view>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import {
  UserOutlined,
  SettingOutlined,
  LogoutOutlined,
  DashboardOutlined,
  ExperimentOutlined,
  TrophyOutlined,
  MessageOutlined
} from '@ant-design/icons-vue'
import NotificationCenter from '@/components/common/NotificationCenter.vue'

export default defineComponent({
  name: 'BasicLayout',
  
  components: {
    UserOutlined,
    SettingOutlined,
    LogoutOutlined,
    DashboardOutlined,
    ExperimentOutlined,
    TrophyOutlined,
    MessageOutlined,
    NotificationCenter
  },
  
  setup() {
    const router = useRouter()
    const collapsed = ref(false)
    const selectedKeys = ref<string[]>(['dashboard'])
    const openKeys = ref<string[]>(['challenges'])
    
    // 模拟用户数据
    const username = ref('测试用户')
    const userAvatar = ref('https://joeschmoe.io/api/v1/random')
    
    // 处理退出登录
    const handleLogout = () => {
      // 清除用户信息
      localStorage.removeItem('token')
      // 跳转到登录页
      router.push('/login')
    }
    
    return {
      collapsed,
      selectedKeys,
      openKeys,
      username,
      userAvatar,
      handleLogout
    }
  }
})
</script>

<style scoped>
.layout {
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.logo {
  display: flex;
  align-items: center;
}

.logo img {
  height: 32px;
  margin-right: 12px;
}

.logo span {
  font-size: 18px;
  font-weight: 600;
  color: #1890ff;
}

.header-right {
  display: flex;
  align-items: center;
}

.notification {
  margin-right: 24px;
}

.user-menu {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
  color: rgba(0, 0, 0, 0.65);
}

.sider {
  box-shadow: 2px 0 8px 0 rgba(29, 35, 41, 0.05);
}

.content {
  margin: 24px;
  padding: 24px;
  background: #fff;
  min-height: 280px;
}
</style> 