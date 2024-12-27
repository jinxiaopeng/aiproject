<template>
  <div class="lab-stats">
    <el-card class="stats-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><Monitor /></el-icon>
            实验环境
          </h3>
          <el-tag 
            :type="getStatusType()" 
            effect="dark"
          >
            {{ getStatusText() }}
          </el-tag>
        </div>
      </template>
      
      <div class="stats-content">
        <div class="stats-grid">
          <div class="stats-item">
            <div class="item-label">总实验数</div>
            <div class="item-value">{{ stats.total_labs }}</div>
            <div class="item-desc">实验环境总数</div>
          </div>
          <div class="stats-item success">
            <div class="item-label">活跃实验</div>
            <div class="item-value">{{ stats.active_labs }}</div>
            <div class="item-desc">正在进行</div>
          </div>
          <div class="stats-item danger">
            <div class="item-label">异常实验</div>
            <div class="item-value">{{ stats.error_labs }}</div>
            <div class="item-desc">需要处理</div>
          </div>
          <div class="stats-item warning">
            <div class="item-label">资源使用</div>
            <div class="item-value">{{ stats.resource_usage }}%</div>
            <div class="item-desc">总体使用率</div>
          </div>
        </div>

        <el-divider />
        
        <div class="lab-types">
          <h4>实验类型分布</h4>
          <div class="type-list">
            <div v-for="(count, type) in stats.lab_types" :key="type" class="type-item">
              <span class="type-name">{{ formatLabType(type) }}</span>
              <el-progress 
                :percentage="getTypePercentage(count)" 
                :color="getTypeColor(type)"
                :format="() => count"
                :stroke-width="8"
              />
            </div>
          </div>
        </div>

        <el-divider />
        
        <div class="resource-usage">
          <h4>资源使用情况</h4>
          <div class="resource-list">
            <div class="resource-item">
              <span class="resource-name">CPU使用率</span>
              <el-progress 
                :percentage="stats.resources.cpu_usage" 
                :color="getResourceColor(stats.resources.cpu_usage)"
                :stroke-width="8"
              />
            </div>
            <div class="resource-item">
              <span class="resource-name">内存使用</span>
              <el-progress 
                :percentage="stats.resources.memory_usage" 
                :color="getResourceColor(stats.resources.memory_usage)"
                :stroke-width="8"
              />
            </div>
            <div class="resource-item">
              <span class="resource-name">存储空间</span>
              <el-progress 
                :percentage="stats.resources.storage_usage" 
                :color="getResourceColor(stats.resources.storage_usage)"
                :stroke-width="8"
              />
            </div>
            <div class="resource-item">
              <span class="resource-name">网络带宽</span>
              <el-progress 
                :percentage="stats.resources.network_usage" 
                :color="getResourceColor(stats.resources.network_usage)"
                :stroke-width="8"
              />
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Monitor } from '@element-plus/icons-vue'

interface LabStats {
  total_labs: number
  active_labs: number
  error_labs: number
  resource_usage: number
  lab_types: {
    web_security: number
    system_security: number
    network_security: number
    crypto: number
    reverse: number
  }
  resources: {
    cpu_usage: number
    memory_usage: number
    storage_usage: number
    network_usage: number
  }
}

const props = defineProps<{
  stats: LabStats
}>()

// 获取状态类型
const getStatusType = () => {
  if (props.stats.error_labs > 5) return 'danger'
  if (props.stats.error_labs > 0) return 'warning'
  if (props.stats.resource_usage > 80) return 'warning'
  return 'success'
}

// 获取状态文本
const getStatusText = () => {
  if (props.stats.error_labs > 5) return '多个异常'
  if (props.stats.error_labs > 0) return '存在异常'
  if (props.stats.resource_usage > 80) return '资源紧张'
  return '运行正常'
}

// 格式化实验类型名称
const formatLabType = (type: string) => {
  const typeMap: Record<string, string> = {
    web_security: 'Web安全',
    system_security: '系统安全',
    network_security: '网络安全',
    crypto: '密码学',
    reverse: '逆向分析'
  }
  return typeMap[type] || type
}

// 获取实验类型颜色
const getTypeColor = (type: string) => {
  const colorMap: Record<string, string> = {
    web_security: '#409EFF',
    system_security: '#67C23A',
    network_security: '#E6A23C',
    crypto: '#909399',
    reverse: '#F56C6C'
  }
  return colorMap[type] || '#909399'
}

// 计算总实验数
const getTotalLabs = () => {
  return Object.values(props.stats.lab_types).reduce((sum, value) => sum + value, 0)
}

// 计算百分比
const getTypePercentage = (count: number) => {
  const total = getTotalLabs()
  if (total === 0) return 0
  return Math.round((count / total) * 100)
}

// 获取资源使用颜色
const getResourceColor = (usage: number) => {
  if (usage >= 80) return '#F56C6C'
  if (usage >= 60) return '#E6A23C'
  return '#67C23A'
}
</script>

<style lang="scss" scoped>
.lab-stats {
  .stats-card {
    background: var(--el-bg-color);
    border: none;
    
    :deep(.el-card__header) {
      padding: 15px 20px;
      border-bottom: 1px solid var(--el-border-color-light);
    }
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h3 {
      margin: 0;
      font-size: 16px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--el-text-color-primary);

      .el-icon {
        font-size: 18px;
        color: var(--el-color-primary);
      }
    }
  }

  .stats-content {
    padding: 10px 0;
  }

  .stats-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
    padding: 10px 0;

    .stats-item {
      text-align: center;
      
      .item-label {
        font-size: 13px;
        color: var(--el-text-color-secondary);
        margin-bottom: 5px;
      }
      
      .item-value {
        font-size: 24px;
        font-weight: bold;
        color: var(--el-text-color-primary);
      }

      .item-desc {
        font-size: 12px;
        color: var(--el-text-color-secondary);
        margin-top: 4px;
      }

      &.success .item-value {
        color: var(--el-color-success);
      }

      &.warning .item-value {
        color: var(--el-color-warning);
      }

      &.danger .item-value {
        color: var(--el-color-danger);
      }
    }
  }

  .lab-types {
    padding: 10px 0;

    h4 {
      margin: 0 0 12px;
      font-size: 14px;
      color: var(--el-text-color-primary);
    }

    .type-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .type-item {
      display: flex;
      align-items: center;
      gap: 12px;

      .type-name {
        width: 80px;
        font-size: 13px;
        color: var(--el-text-color-secondary);
      }

      :deep(.el-progress) {
        flex: 1;
      }
    }
  }

  .resource-usage {
    padding: 10px 0;

    h4 {
      margin: 0 0 12px;
      font-size: 14px;
      color: var(--el-text-color-primary);
    }

    .resource-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    .resource-item {
      display: flex;
      align-items: center;
      gap: 12px;

      .resource-name {
        width: 80px;
        font-size: 13px;
        color: var(--el-text-color-secondary);
      }

      :deep(.el-progress) {
        flex: 1;
      }
    }
  }
}
</style> 