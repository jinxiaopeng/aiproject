<template>
  <div class="network-monitor">
    <div class="monitor-section">
      <h4>网络连接</h4>
      <el-table :data="networkConnections" style="width: 100%">
        <el-table-column prop="source" label="源地址" />
        <el-table-column prop="destination" label="目标地址" />
        <el-table-column prop="protocol" label="协议" />
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'ESTABLISHED' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="monitor-section">
      <h4>流量统计</h4>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-value">{{ stats.bytesReceived }}</div>
            <div class="stat-label">接收流量 (bytes)</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-value">{{ stats.bytesSent }}</div>
            <div class="stat-label">发送流量 (bytes)</div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-value">{{ stats.packetsDropped }}</div>
            <div class="stat-label">丢包数</div>
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="monitor-section">
      <h4>异常检测</h4>
      <el-timeline>
        <el-timeline-item
          v-for="(alert, index) in alerts"
          :key="index"
          :type="alert.level"
          :timestamp="alert.time"
        >
          {{ alert.message }}
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// 模拟数据
const networkConnections = ref([
  {
    source: '192.168.1.100:8080',
    destination: '192.168.1.200:443',
    protocol: 'TCP',
    status: 'ESTABLISHED'
  },
  {
    source: '192.168.1.100:53',
    destination: '8.8.8.8:53',
    protocol: 'UDP',
    status: 'ACTIVE'
  }
])

const stats = ref({
  bytesReceived: '1.2 GB',
  bytesSent: '800 MB',
  packetsDropped: 12
})

const alerts = ref([
  {
    time: '2024-01-01 10:00:00',
    level: 'warning',
    message: '检测到异常流量模式'
  },
  {
    time: '2024-01-01 09:45:00',
    level: 'info',
    message: '新建连接: 192.168.1.100 -> 192.168.1.200'
  }
])

onMounted(() => {
  // 这里可以添加实时数据获取逻辑
})
</script>

<style lang="scss" scoped>
.network-monitor {
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