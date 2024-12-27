<template>
  <div class="security-monitor">
    <div class="monitor-section">
      <h4>威胁检测</h4>
      <el-table :data="threats" style="width: 100%">
        <el-table-column prop="time" label="时间" width="180" />
        <el-table-column prop="type" label="类型" width="120" />
        <el-table-column prop="source" label="来源" />
        <el-table-column prop="level" label="威胁等级" width="100">
          <template #default="scope">
            <el-tag :type="getThreatLevelType(scope.row.level)">
              {{ scope.row.level }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'blocked' ? 'success' : 'danger'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="monitor-section">
      <h4>安全统计</h4>
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.totalThreats }}</div>
            <div class="stat-label">总威胁数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.blockedThreats }}</div>
            <div class="stat-label">已阻止</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.highRiskThreats }}</div>
            <div class="stat-label">高风险</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value">{{ stats.lastUpdate }}</div>
            <div class="stat-label">最后更新</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="monitor-section">
      <h4>安全日志</h4>
      <el-timeline>
        <el-timeline-item
          v-for="(log, index) in securityLogs"
          :key="index"
          :type="log.level"
          :timestamp="log.time"
        >
          {{ log.message }}
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 模拟数据
const threats = ref([
  {
    time: '2024-01-01 10:30:00',
    type: 'SQL注入',
    source: '192.168.1.100',
    level: 'high',
    status: 'blocked'
  },
  {
    time: '2024-01-01 10:15:00',
    type: 'XSS攻击',
    source: '192.168.1.200',
    level: 'medium',
    status: 'detected'
  }
])

const stats = ref({
  totalThreats: 125,
  blockedThreats: 98,
  highRiskThreats: 12,
  lastUpdate: '10:30:00'
})

const securityLogs = ref([
  {
    time: '2024-01-01 10:30:00',
    level: 'danger',
    message: '检测到SQL注入攻击尝试'
  },
  {
    time: '2024-01-01 10:15:00',
    level: 'warning',
    message: '检测到可疑的网络扫描活动'
  }
])

const getThreatLevelType = (level: string) => {
  const types = {
    high: 'danger',
    medium: 'warning',
    low: 'info'
  }
  return types[level as keyof typeof types] || 'info'
}

onMounted(() => {
  // 这里可以添加实时数据获取逻辑
})
</script>

<style lang="scss" scoped>
.security-monitor {
  .monitor-section {
    margin-bottom: 20px;

    h4 {
      margin-bottom: 15px;
    }
  }

  .stat-card {
    text-align: center;
    padding: 20px;
    background-color: var(--el-bg-color-overlay);
    border-radius: 4px;

    .stat-value {
      font-size: 24px;
      font-weight: bold;
      color: var(--el-color-primary);
    }

    .stat-label {
      margin-top: 8px;
      color: var(--el-text-color-secondary);
    }
  }
}
</style> 