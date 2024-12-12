<template>
  <div class="realtime-monitor">
    <el-card class="monitor-card">
      <template #header>
        <div class="card-header">
          <span>实时系统监控</span>
          <el-button type="primary" size="small" @click="refreshData">刷新</el-button>
        </div>
      </template>
      
      <el-row :gutter="20">
        <!-- CPU使用率 -->
        <el-col :span="8">
          <div class="metric-card">
            <div class="metric-title">CPU使用率</div>
            <el-progress 
              type="dashboard" 
              :percentage="Math.round(metrics.cpu_usage || 0)"
              :color="getDynamicColor(metrics.cpu_usage)"
            />
            <div class="metric-value">{{ Math.round(metrics.cpu_usage || 0) }}%</div>
          </div>
        </el-col>
        
        <!-- 内存使用率 -->
        <el-col :span="8">
          <div class="metric-card">
            <div class="metric-title">内存使用率</div>
            <el-progress 
              type="dashboard" 
              :percentage="Math.round(metrics.memory_usage || 0)"
              :color="getDynamicColor(metrics.memory_usage)"
            />
            <div class="metric-value">{{ Math.round(metrics.memory_usage || 0) }}%</div>
          </div>
        </el-col>
        
        <!-- 磁盘使用率 -->
        <el-col :span="8">
          <div class="metric-card">
            <div class="metric-title">磁盘使用率</div>
            <el-progress 
              type="dashboard" 
              :percentage="Math.round(metrics.disk_usage || 0)"
              :color="getDynamicColor(metrics.disk_usage)"
            />
            <div class="metric-value">{{ Math.round(metrics.disk_usage || 0) }}%</div>
          </div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" class="mt-4">
        <!-- 网络流量 -->
        <el-col :span="12">
          <div class="metric-card">
            <div class="metric-title">网络流量</div>
            <div class="network-metrics">
              <div class="network-item">
                <i class="el-icon-upload"></i>
                <span>上传: {{ formatNetworkSpeed(metrics.network_out) }}</span>
              </div>
              <div class="network-item">
                <i class="el-icon-download"></i>
                <span>下载: {{ formatNetworkSpeed(metrics.network_in) }}</span>
              </div>
            </div>
          </div>
        </el-col>
        
        <!-- 系统信息 -->
        <el-col :span="12">
          <div class="metric-card">
            <div class="metric-title">系统信息</div>
            <div class="system-metrics">
              <div class="system-item">
                <span>系统负载: {{ metrics.system_load?.toFixed(2) || '0.00' }}</span>
              </div>
              <div class="system-item">
                <span>进程数: {{ metrics.process_count || 0 }}</span>
              </div>
            </div>
          </div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getLatestMonitorData } from '@/api/monitor'

const metrics = ref({
  cpu_usage: 0,
  memory_usage: 0,
  disk_usage: 0,
  network_in: 0,
  network_out: 0,
  system_load: 0,
  process_count: 0
})

let refreshInterval: number | null = null

const refreshData = async () => {
  try {
    const data = await getLatestMonitorData()
    if (data && data.length > 0) {
      metrics.value = data[0]
    }
  } catch (error) {
    console.error('Failed to fetch realtime monitor data:', error)
  }
}

const getDynamicColor = (value: number) => {
  if (value >= 90) return '#F56C6C'
  if (value >= 70) return '#E6A23C'
  return '#67C23A'
}

const formatNetworkSpeed = (speed: number) => {
  if (speed < 1) {
    return `${(speed * 1024).toFixed(2)} KB/s`
  }
  return `${speed.toFixed(2)} MB/s`
}

onMounted(() => {
  refreshData()
  // 每30秒刷新一次数据
  refreshInterval = setInterval(refreshData, 30000)
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})
</script>

<style lang="scss" scoped>
.realtime-monitor {
  .monitor-card {
    margin-bottom: 20px;
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .metric-card {
    text-align: center;
    padding: 20px;
    
    .metric-title {
      font-size: 16px;
      color: #606266;
      margin-bottom: 15px;
    }
    
    .metric-value {
      font-size: 20px;
      font-weight: bold;
      margin-top: 10px;
      color: #303133;
    }
  }
  
  .network-metrics, .system-metrics {
    padding: 10px;
    
    .network-item, .system-item {
      margin: 10px 0;
      font-size: 14px;
      color: #606266;
      
      i {
        margin-right: 8px;
      }
    }
  }
  
  .mt-4 {
    margin-top: 20px;
  }
}
</style> 