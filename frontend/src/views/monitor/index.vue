<template>
  <div class="monitor-container">
    <!-- 顶部统计卡片 -->
    <div class="overview-section">
      <MonitorOverview 
        :stats="monitorStats" 
        @view-detail="handleViewDetail"
        @refresh="loadMonitorStats"
      />
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <el-row :gutter="24">
        <!-- 左侧区域：预警列表和趋势图表 -->
        <el-col :span="17">
          <!-- 预警列表 -->
          <div class="content-section">
            <div class="section-header">
              <h2>预警记录</h2>
              <div class="header-actions">
                <el-radio-group v-model="timeRange" size="small">
                  <el-radio-button label="today">今日</el-radio-button>
                  <el-radio-button label="week">本周</el-radio-button>
                  <el-radio-button label="month">本月</el-radio-button>
                </el-radio-group>
              </div>
            </div>
            <AlertList 
              ref="alertListRef"
              :time-range="timeRange"
              class="alert-list"
              @refresh="loadMonitorStats"
            />
          </div>

          <!-- 趋势图表 -->
          <div class="chart-section">
            <div class="section-header">
              <h2>预警趋势</h2>
            </div>
            <MonitorChart 
              :time-range="timeRange"
              class="trend-chart"
            />
          </div>
        </el-col>

        <!-- 右侧区域：监控设置 -->
        <el-col :span="7">
          <div class="side-section">
            <MonitorSettingsPanel
              v-model="settings" 
              @change="handleSettingsChange"
            />
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MonitorOverview from './components/MonitorOverview.vue'
import MonitorSettingsPanel from './components/MonitorSettings.vue'
import AlertList from './components/AlertList.vue'
import MonitorChart from './components/MonitorChart.vue'
import { getMonitorStats, getMonitorSettings, type MonitorStats } from '@/api/monitor'
import type { MonitorSettings as IMonitorSettings } from '@/api/monitor'
import { ElMessage } from 'element-plus'

const monitorStats = ref<MonitorStats>({
  loginAlerts: 0,
  loginPending: 0,
  loginHandled: 0,
  operationAlerts: 0,
  operationPending: 0,
  operationHandled: 0,
  securityAlerts: 0,
  securityPending: 0,
  securityHandled: 0
})

const settings = ref<IMonitorSettings>({
  loginAlert: true,
  operationAlert: true,
  securityAlert: true,
  notifyMethods: []
})

const timeRange = ref('today')
const alertListRef = ref()

// 加载监控统计数据
const loadMonitorStats = async () => {
  try {
    const { data } = await getMonitorStats()
    monitorStats.value = data
  } catch (error) {
    console.error('Failed to load monitor stats:', error)
    ElMessage.error('加载统计数据失败')
  }
}

// 加载监控设置
const loadMonitorSettings = async () => {
  try {
    const { data } = await getMonitorSettings()
    settings.value = data
  } catch (error) {
    console.error('Failed to load monitor settings:', error)
    ElMessage.error('加载设置失败')
  }
}

// 查看详情
const handleViewDetail = (type: string) => {
  alertListRef.value?.filterByType(type)
}

// 处理设置变更
const handleSettingsChange = () => {
  loadMonitorStats()
}

onMounted(() => {
  loadMonitorStats()
  loadMonitorSettings()
})
</script>

<style lang="scss" scoped>
.monitor-container {
  min-height: calc(100vh - 84px);
  padding: 20px;
  background: var(--el-bg-color-page);

  .overview-section {
    margin-bottom: 24px;
  }

  .main-content {
    .content-section,
    .chart-section,
    .side-section {
      background: var(--el-bg-color);
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
      overflow: hidden;
      margin-bottom: 24px;

      &:last-child {
        margin-bottom: 0;
      }
    }

    .content-section {
      height: calc(100vh - 480px);
      display: flex;
      flex-direction: column;

      .alert-list {
        flex: 1;
        overflow: auto;
      }
    }

    .chart-section {
      height: 360px;
      display: flex;
      flex-direction: column;

      .trend-chart {
        flex: 1;
      }
    }

    .side-section {
      height: calc(100vh - 280px);
    }

    .section-header {
      padding: 16px 24px;
      border-bottom: 1px solid var(--el-border-color-light);
      display: flex;
      justify-content: space-between;
      align-items: center;

      h2 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
        color: var(--el-text-color-primary);
      }

      .header-actions {
        display: flex;
        gap: 12px;
        align-items: center;
      }
    }
  }
}
</style> 