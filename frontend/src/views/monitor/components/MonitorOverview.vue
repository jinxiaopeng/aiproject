<template>
  <div class="overview-section">
    <el-row :gutter="20">
      <!-- 登录预警 -->
      <el-col :span="8">
        <div class="stat-card">
          <div class="card-header">
            <span class="title">登录预警</span>
            <el-button link type="primary" @click="handleViewDetail('login')">
              查看详情
            </el-button>
          </div>
          <div class="card-body">
            <div class="main-value">{{ stats.loginAlerts || 0 }}</div>
            <div class="sub-title">今日登录行为预警</div>
            <div class="stat-items">
              <div class="stat-item">
                <span class="label">未处理</span>
                <span class="value">{{ stats.loginPending || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="label">已处理</span>
                <span class="value">{{ stats.loginHandled || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 操作预警 -->
      <el-col :span="8">
        <div class="stat-card">
          <div class="card-header">
            <span class="title">操作预警</span>
            <el-button link type="primary" @click="handleViewDetail('operation')">
              查看详情
            </el-button>
          </div>
          <div class="card-body">
            <div class="main-value">{{ stats.operationAlerts || 0 }}</div>
            <div class="sub-title">敏感操作行为预警</div>
            <div class="stat-items">
              <div class="stat-item">
                <span class="label">未处理</span>
                <span class="value">{{ stats.operationPending || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="label">已处理</span>
                <span class="value">{{ stats.operationHandled || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-col>

      <!-- 安全预警 -->
      <el-col :span="8">
        <div class="stat-card">
          <div class="card-header">
            <span class="title">安全预警</span>
            <el-button link type="primary" @click="handleViewDetail('security')">
              查看详情
            </el-button>
          </div>
          <div class="card-body">
            <div class="main-value">{{ stats.securityAlerts || 0 }}</div>
            <div class="sub-title">系统安全威胁预警</div>
            <div class="stat-items">
              <div class="stat-item">
                <span class="label">未处理</span>
                <span class="value">{{ stats.securityPending || 0 }}</span>
              </div>
              <div class="stat-item">
                <span class="label">已处理</span>
                <span class="value">{{ stats.securityHandled || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface MonitorStats {
  loginAlerts: number
  loginPending: number
  loginHandled: number
  operationAlerts: number
  operationPending: number
  operationHandled: number
  securityAlerts: number
  securityPending: number
  securityHandled: number
}

const props = defineProps<{
  stats: MonitorStats
}>()

const emit = defineEmits<{
  (e: 'view-detail', type: string): void
}>()

// 查看详情
const handleViewDetail = (type: string) => {
  emit('view-detail', type)
}
</script>

<style lang="scss" scoped>
.overview-section {
  margin-bottom: 24px;
}

.stat-card {
  background: #00b96b;
  border-radius: 8px;
  padding: 20px;
  height: 100%;
  color: white;

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    .title {
      font-size: 16px;
      font-weight: 500;
    }

    :deep(.el-button) {
      color: rgba(255, 255, 255, 0.85);
      font-size: 13px;

      &:hover {
        color: white;
      }
    }
  }

  .card-body {
    .main-value {
      font-size: 36px;
      font-weight: 600;
      margin-bottom: 8px;
    }

    .sub-title {
      font-size: 14px;
      opacity: 0.85;
      margin-bottom: 16px;
    }

    .stat-items {
      display: flex;
      gap: 24px;

      .stat-item {
        .label {
          font-size: 13px;
          opacity: 0.85;
          margin-right: 8px;
        }

        .value {
          font-weight: 500;
        }
      }
    }
  }
}
</style> 