<template>
  <div class="security-stats">
    <el-card class="stats-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h3>
            <el-icon><Warning /></el-icon>
            安全告警
          </h3>
          <el-tag 
            :type="getAlertLevelType()" 
            effect="dark"
          >
            {{ getAlertLevelText() }}
          </el-tag>
        </div>
      </template>
      
      <div class="stats-content">
        <div class="stats-grid">
          <div class="stats-item">
            <div class="item-label">总告警</div>
            <div class="item-value">{{ stats.total_alerts }}</div>
            <div class="item-trend" :class="getTrendClass(stats.alert_trend)">
              {{ stats.alert_trend > 0 ? '+' : '' }}{{ stats.alert_trend }}%
            </div>
          </div>
          <div class="stats-item warning">
            <div class="item-label">待处理</div>
            <div class="item-value">{{ stats.pending_alerts }}</div>
            <div class="item-desc">需要及时处理</div>
          </div>
          <div class="stats-item danger">
            <div class="item-label">严重告警</div>
            <div class="item-value">{{ stats.critical_alerts }}</div>
            <div class="item-desc">高危漏洞</div>
          </div>
          <div class="stats-item">
            <div class="item-label">今日攻击</div>
            <div class="item-value">{{ stats.recent_attacks }}</div>
            <div class="item-desc">检测到的攻击</div>
          </div>
        </div>

        <el-divider />
        
        <div class="attack-types">
          <h4>攻击类型分布</h4>
          <div class="type-list">
            <div v-for="(count, type) in stats.attack_types" :key="type" class="type-item">
              <span class="type-name">{{ formatAttackType(type) }}</span>
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
        
        <div class="blocked-ips">
          <div class="blocked-header">
            <span>已封禁IP</span>
            <el-tag size="small" type="danger">{{ stats.blocked_ips }}</el-tag>
          </div>
          <el-progress 
            :percentage="getBlockedPercentage()" 
            :color="getProgressColor"
            :format="format"
            :stroke-width="10"
          />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { Warning } from '@element-plus/icons-vue'

interface SecurityStats {
  total_alerts: number
  pending_alerts: number
  critical_alerts: number
  recent_attacks: number
  blocked_ips: number
  alert_trend: number
  attack_types: {
    sql_injection: number
    xss: number
    file_upload: number
    command_injection: number
    unauthorized_access: number
  }
}

const props = defineProps<{
  stats: SecurityStats
}>()

// 获取告警等级类型
const getAlertLevelType = () => {
  if (props.stats.critical_alerts > 5) return 'danger'
  if (props.stats.critical_alerts > 0) return 'warning'
  if (props.stats.pending_alerts > 10) return 'warning'
  return 'success'
}

// 获取告警等级文本
const getAlertLevelText = () => {
  if (props.stats.critical_alerts > 5) return '严重威胁'
  if (props.stats.critical_alerts > 0) return '需要注意'
  if (props.stats.pending_alerts > 10) return '需要处理'
  return '状态正常'
}

// 获取趋势样式
const getTrendClass = (trend: number) => {
  return {
    'trend-up': trend > 0,
    'trend-down': trend < 0,
    'trend-stable': trend === 0
  }
}

// 格式化攻击类型名称
const formatAttackType = (type: string) => {
  const typeMap: Record<string, string> = {
    sql_injection: 'SQL注入',
    xss: 'XSS攻击',
    file_upload: '文件上传',
    command_injection: '命令注入',
    unauthorized_access: '未授权访问'
  }
  return typeMap[type] || type
}

// 计算攻击类型百分比
const getTypePercentage = (count: number) => {
  const total = Object.values(props.stats.attack_types).reduce((a, b) => a + b, 0)
  return Math.round((count / total) * 100)
}

// 获取攻击类型颜色
const getTypeColor = (type: string) => {
  const colorMap: Record<string, string> = {
    sql_injection: '#F56C6C',
    xss: '#E6A23C',
    file_upload: '#409EFF',
    command_injection: '#F56C6C',
    unauthorized_access: '#67C23A'
  }
  return colorMap[type] || '#909399'
}

// 计算封禁IP百分比
const getBlockedPercentage = () => {
  // 假设最大封禁IP数为1000
  return Math.min((props.stats.blocked_ips / 1000) * 100, 100)
}

// 进度条颜色
const getProgressColor = (percentage: number) => {
  if (percentage < 30) return '#67C23A'
  if (percentage < 70) return '#E6A23C'
  return '#F56C6C'
}

// 进度条格式化
const format = (percentage: number) => {
  return `${props.stats.blocked_ips}/1000`
}
</script>

<style lang="scss" scoped>
.security-stats {
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
        color: var(--el-color-danger);
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

      .item-trend {
        font-size: 12px;
        margin-top: 4px;

        &.trend-up {
          color: var(--el-color-danger);
        }
        &.trend-down {
          color: var(--el-color-success);
        }
        &.trend-stable {
          color: var(--el-text-color-secondary);
        }
      }

      &.warning .item-value {
        color: var(--el-color-warning);
      }

      &.danger .item-value {
        color: var(--el-color-danger);
      }
    }
  }

  .attack-types {
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

  .blocked-ips {
    padding: 10px 0;

    .blocked-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      
      span {
        font-size: 13px;
        color: var(--el-text-color-secondary);
      }
    }
  }
}
</style> 