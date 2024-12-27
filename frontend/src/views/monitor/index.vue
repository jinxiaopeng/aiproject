<template>
  <div class="monitor-dashboard">
    <div class="page-header">
      <h2>监控预警中心</h2>
      <div class="header-actions">
        <el-button-group>
          <el-button 
            :type="activeTab === 'learning' ? 'primary' : 'default'"
            @click="activeTab = 'learning'"
          >
            学习监控
          </el-button>
          <el-button 
            :type="activeTab === 'security' ? 'primary' : 'default'"
            @click="activeTab = 'security'"
          >
            安全监控
          </el-button>
          <el-button 
            :type="activeTab === 'system' ? 'primary' : 'default'"
            @click="activeTab = 'system'"
          >
            系统监控
          </el-button>
        </el-button-group>
        <el-button type="primary" :icon="Refresh" @click="refreshData">
          刷新
        </el-button>
      </div>
    </div>

    <!-- 告警通知栏 -->
    <div v-if="hasAlerts" class="alert-banner">
      <el-alert
        v-for="alert in activeAlerts"
        :key="alert.id"
        :title="alert.title"
        :description="alert.description"
        :type="alert.type"
        :closable="true"
        show-icon
        @close="dismissAlert(alert.id)"
      />
    </div>

    <!-- 监控内容区域 -->
    <div class="monitor-content">
      <transition name="fade" mode="out-in">
        <keep-alive>
          <component 
            :is="currentComponent" 
            @alert="handleAlert"
            @refresh="handleRefresh"
          />
        </keep-alive>
      </transition>
    </div>

    <!-- 快速操作抽屉 -->
    <el-drawer
      v-model="drawerVisible"
      title="快速操作"
      direction="rtl"
      size="300px"
    >
      <div class="quick-actions">
        <el-collapse v-model="activeActions">
          <el-collapse-item title="常用操作" name="common">
            <div class="action-list">
              <el-button 
                v-for="action in commonActions" 
                :key="action.id"
                :type="action.type"
                :icon="action.icon"
                @click="handleQuickAction(action)"
              >
                {{ action.name }}
              </el-button>
            </div>
          </el-collapse-item>
          <el-collapse-item title="实验环境" name="env">
            <div class="action-list">
              <el-button 
                v-for="action in envActions" 
                :key="action.id"
                :type="action.type"
                :icon="action.icon"
                @click="handleQuickAction(action)"
              >
                {{ action.name }}
              </el-button>
            </div>
          </el-collapse-item>
          <el-collapse-item title="系统维护" name="system">
            <div class="action-list">
              <el-button 
                v-for="action in systemActions" 
                :key="action.id"
                :type="action.type"
                :icon="action.icon"
                @click="handleQuickAction(action)"
              >
                {{ action.name }}
              </el-button>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>
    </el-drawer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, defineAsyncComponent } from 'vue'
import { Refresh, Setting, Monitor, Warning, Tools } from '@element-plus/icons-vue'

// 异步加载组件
const LearningMonitor = defineAsyncComponent(() => import('./LearningMonitor.vue'))
const SecurityMonitor = defineAsyncComponent(() => import('./SecurityMonitor.vue'))
const SystemMonitor = defineAsyncComponent(() => import('./SystemMonitor.vue'))

// 当前激活的标签页
const activeTab = ref('learning')

// 当前组件
const currentComponent = computed(() => {
  const components = {
    learning: LearningMonitor,
    security: SecurityMonitor,
    system: SystemMonitor
  }
  return components[activeTab.value]
})

// 告警数据
const activeAlerts = ref([
  {
    id: 1,
    title: '高危漏洞预警',
    description: '检测到SQL注入漏洞，请及时处理',
    type: 'error'
  },
  {
    id: 2,
    title: '系统资源告警',
    description: '实验环境内存使用率超过90%',
    type: 'warning'
  }
])

// 是否有告警
const hasAlerts = computed(() => activeAlerts.value.length > 0)

// 抽屉控制
const drawerVisible = ref(false)
const activeActions = ref(['common'])

// 快速操作列表
const commonActions = [
  {
    id: 'refresh',
    name: '刷新数据',
    type: 'primary',
    icon: Refresh
  },
  {
    id: 'settings',
    name: '监控设置',
    type: 'default',
    icon: Setting
  }
]

const envActions = [
  {
    id: 'restart_all',
    name: '重启所有环境',
    type: 'warning',
    icon: Tools
  },
  {
    id: 'stop_all',
    name: '停止所有环境',
    type: 'danger',
    icon: Monitor
  }
]

const systemActions = [
  {
    id: 'clear_cache',
    name: '清理缓存',
    type: 'info',
    icon: Tools
  },
  {
    id: 'system_check',
    name: '系统检查',
    type: 'primary',
    icon: Monitor
  }
]

// 刷新数据
const refreshData = async () => {
  // TODO: 实现刷新逻辑
}

// 处理告警
const handleAlert = (alert: any) => {
  activeAlerts.value.push(alert)
}

// 关闭告警
const dismissAlert = (id: number) => {
  const index = activeAlerts.value.findIndex(alert => alert.id === id)
  if (index !== -1) {
    activeAlerts.value.splice(index, 1)
  }
}

// 处理子组件刷新请求
const handleRefresh = () => {
  refreshData()
}

// 处理快速操作
const handleQuickAction = async (action: any) => {
  try {
    // TODO: 实现快速操作逻辑
  } catch (error) {
    console.error('Failed to execute quick action:', error)
  }
}

// 自动刷新定时器
let refreshTimer: number | null = null

onMounted(() => {
  refreshData()
  // 每5分钟自动刷新一次
  refreshTimer = window.setInterval(refreshData, 5 * 60 * 1000)
})

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer)
  }
})
</script>

<style lang="scss" scoped>
.monitor-dashboard {
  padding: 20px;

  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;

    h2 {
      margin: 0;
      font-size: 24px;
      font-weight: 500;
    }

    .header-actions {
      display: flex;
      gap: 16px;
    }
  }

  .alert-banner {
    margin-bottom: 20px;

    .el-alert {
      margin-bottom: 12px;

      &:last-child {
        margin-bottom: 0;
      }
    }
  }

  .monitor-content {
    background: var(--el-bg-color);
    border-radius: 4px;
    min-height: 600px;
  }

  .quick-actions {
    .action-list {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      padding: 12px;
    }
  }
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>