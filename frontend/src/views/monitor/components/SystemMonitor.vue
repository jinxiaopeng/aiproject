<template>
  <div class="system-monitor">
    <div class="monitor-section">
      <h4>系统资源</h4>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-label">CPU 使用率</div>
            <el-progress type="dashboard" :percentage="systemStats.cpuUsage" />
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-label">内存使用率</div>
            <el-progress type="dashboard" :percentage="systemStats.memoryUsage" />
          </div>
        </el-col>
        <el-col :span="8">
          <div class="stat-card">
            <div class="stat-label">磁盘使用率</div>
            <el-progress type="dashboard" :percentage="systemStats.diskUsage" />
          </div>
        </el-col>
      </el-row>
    </div>

    <div class="monitor-section">
      <h4>进程信息</h4>
      <el-table :data="processes" style="width: 100%">
        <el-table-column prop="pid" label="PID" width="100" />
        <el-table-column prop="name" label="进程名称" />
        <el-table-column prop="cpu" label="CPU %" width="100" />
        <el-table-column prop="memory" label="内存 %" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'running' ? 'success' : 'warning'">
              {{ scope.row.status }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="monitor-section">
      <h4>系统日志</h4>
      <el-timeline>
        <el-timeline-item
          v-for="(log, index) in systemLogs"
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
const systemStats = ref({
  cpuUsage: 45,
  memoryUsage: 60,
  diskUsage: 75
})

const processes = ref([
  {
    pid: 1234,
    name: 'python.exe',
    cpu: 2.5,
    memory: 1.8,
    status: 'running'
  },
  {
    pid: 5678,
    name: 'node.exe',
    cpu: 1.2,
    memory: 3.5,
    status: 'running'
  }
])

const systemLogs = ref([
  {
    time: '2024-01-01 10:15:00',
    level: 'warning',
    message: '系统负载较高'
  },
  {
    time: '2024-01-01 10:00:00',
    level: 'info',
    message: '系统服务启动成功'
  }
])

onMounted(() => {
  // 这里可以添加实时数据获取逻辑
})
</script>

<style lang="scss" scoped>
.system-monitor {
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

    .stat-label {
      margin-bottom: 15px;
      color: var(--el-text-color-regular);
    }
  }
}
</style> 