<template>
  <div class="settings-panel">
    <div class="panel-header">
      <h3>监控预警设置</h3>
      <el-button 
        type="primary" 
        :loading="saving" 
        :icon="CheckIcon"
        @click="saveSettings"
      >
        保存设置
      </el-button>
    </div>

    <div class="settings-content">
      <!-- 预警类型设置 -->
      <div class="settings-section">
        <div class="section-title">
          <span class="title">预警类型</span>
          <el-tooltip content="配置需要监控的预警类型" placement="top">
            <el-icon><InfoIcon /></el-icon>
          </el-tooltip>
        </div>
        
        <div class="alert-types">
          <div 
            v-for="type in alertTypes" 
            :key="type.value"
            class="type-item"
            :class="{ active: localSettings[type.value + 'Alert'] }"
            @click="toggleAlertType(type.value)"
          >
            <div class="type-icon">
              <el-icon :class="type.icon"></el-icon>
            </div>
            <div class="type-info">
              <span class="name">{{ type.label }}</span>
              <span class="desc">{{ type.desc }}</span>
            </div>
            <div class="type-switch">
              <el-switch 
                v-model="localSettings[type.value + 'Alert']"
                :active-color="type.color"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 通知方式设置 -->
      <div class="settings-section">
        <div class="section-title">
          <span class="title">通知方式</span>
          <el-tooltip content="配置预警通知的接收方式" placement="top">
            <el-icon><InfoIcon /></el-icon>
          </el-tooltip>
        </div>

        <div class="notify-methods">
          <div 
            v-for="method in notifyMethods" 
            :key="method.value"
            class="method-item"
            :class="{ active: localSettings.notifyMethods.includes(method.value) }"
          >
            <el-checkbox 
              v-model="localSettings.notifyMethods" 
              :label="method.value"
            >
              <div class="method-content">
                <div class="method-icon">
                  <el-icon :class="method.icon"></el-icon>
                </div>
                <div class="method-info">
                  <span class="name">{{ method.label }}</span>
                  <span class="desc">{{ method.desc }}</span>
                </div>
              </div>
            </el-checkbox>
          </div>
        </div>
      </div>

      <!-- 阈值设置 -->
      <div class="settings-section">
        <div class="section-title">
          <span class="title">预警阈值</span>
          <el-tooltip content="配置触发预警的条件阈值" placement="top">
            <el-icon><InfoIcon /></el-icon>
          </el-tooltip>
        </div>

        <div class="threshold-settings">
          <el-form :model="localSettings" label-position="top">
            <el-form-item label="登录失败次数">
              <el-input-number 
                v-model="localSettings.loginFailThreshold" 
                :min="1" 
                :max="10"
                controls-position="right"
              />
              <span class="unit">次/小时</span>
            </el-form-item>

            <el-form-item label="敏感操作频率">
              <el-input-number 
                v-model="localSettings.operationFreqThreshold" 
                :min="1" 
                :max="100"
                controls-position="right"
              />
              <span class="unit">次/分钟</span>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Check as CheckIcon,
  InfoFilled as InfoIcon,
  User,
  Warning,
  Shield,
  Bell,
  Message,
  Cellphone,
  ChatDotRound
} from '@element-plus/icons-vue'
import type { MonitorSettings } from '@/api/monitor'
import { updateMonitorSettings } from '@/api/monitor'

interface LocalSettings extends MonitorSettings {
  loginFailThreshold: number
  operationFreqThreshold: number
}

interface AlertType {
  label: string
  value: 'login' | 'operation' | 'security'
  desc: string
  icon: string
  color: string
  threshold?: string
  thresholdLabel?: string
  thresholdDesc?: string
}

interface NotifyMethod {
  label: string
  value: string
  desc: string
  icon: string
}

const props = defineProps<{
  modelValue: MonitorSettings
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: MonitorSettings): void
  (e: 'change'): void
}>()

const saving = ref(false)
const localSettings = ref<LocalSettings>({
  ...props.modelValue,
  loginFailThreshold: 3,
  operationFreqThreshold: 10
})

// 预警类型配置
const alertTypes: AlertType[] = [
  {
    label: '登录安全预警',
    value: 'login',
    desc: '监控异常登录行为，包括登录失败次数、异地登录等',
    icon: 'User',
    color: '#ff4d4f',
    threshold: 'loginFailThreshold',
    thresholdLabel: '登录失败阈值',
    thresholdDesc: '单位时间内允许的最大登录失败次数'
  },
  {
    label: '敏感操作预警',
    value: 'operation',
    desc: '监控数据删除、权限变更等敏感操作',
    icon: 'Warning',
    color: '#ff9900',
    threshold: 'operationFreqThreshold',
    thresholdLabel: '操作频率阈值',
    thresholdDesc: '单位时间内允许的最大敏感操作次数'
  },
  {
    label: '系统安全预警',
    value: 'security',
    desc: '监控系统异常、资源使用等安全事件',
    icon: 'Shield',
    color: '#ff4d4f',
    threshold: '',
    thresholdLabel: '',
    thresholdDesc: ''
  }
]

// 通知方式配置
const notifyMethods: NotifyMethod[] = [
  {
    label: '站内消息',
    value: 'message',
    desc: '实时接收系统内的预警通知',
    icon: 'Bell'
  },
  {
    label: '邮件通知',
    value: 'email',
    desc: '发送预警邮件到指定邮箱',
    icon: 'Message'
  },
  {
    label: '短信通知',
    value: 'sms',
    desc: '发送预警短信到指定手机',
    icon: 'Cellphone'
  },
  {
    label: '钉钉通知',
    value: 'dingtalk',
    desc: '通过钉钉机器人发送预警消息',
    icon: 'ChatDotRound'
  }
]

// 切换预警类型
const toggleAlertType = (type: 'login' | 'operation' | 'security') => {
  const key = `${type}Alert` as keyof LocalSettings
  localSettings.value[key] = !localSettings.value[key]
}

// 保存设置
const saveSettings = async () => {
  saving.value = true
  try {
    const { loginFailThreshold, operationFreqThreshold, ...settings } = localSettings.value
    await updateMonitorSettings(settings)
    emit('update:modelValue', settings)
    emit('change')
    ElMessage.success('设置已保存')
  } catch (error) {
    console.error('Failed to save settings:', error)
    ElMessage.error('保存设置失败')
  } finally {
    saving.value = false
  }
}

// 监听外部值变化
watch(() => props.modelValue, (newVal) => {
  localSettings.value = {
    ...newVal,
    loginFailThreshold: localSettings.value.loginFailThreshold,
    operationFreqThreshold: localSettings.value.operationFreqThreshold
  }
}, { deep: true })
</script>

<style lang="scss" scoped>
.settings-panel {
  .panel-header {
    padding: 20px 24px;
    border-bottom: 1px solid var(--el-border-color-light);
    display: flex;
    justify-content: space-between;
    align-items: center;

    h3 {
      margin: 0;
      font-size: 18px;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
  }

  .settings-content {
    padding: 24px;
  }

  .settings-section {
    margin-bottom: 32px;

    &:last-child {
      margin-bottom: 0;
    }

    .section-title {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 16px;

      .title {
        font-size: 16px;
        font-weight: 500;
        color: var(--el-text-color-primary);
      }

      .el-icon {
        font-size: 16px;
        color: var(--el-text-color-secondary);
      }
    }
  }

  .alert-types {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .type-item {
      display: flex;
      align-items: center;
      gap: 16px;
      padding: 16px;
      background: var(--el-fill-color-light);
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;

      &:hover {
        background: var(--el-fill-color);
      }

      &.active {
        background: var(--el-color-primary-light-9);
      }

      .type-icon {
        width: 40px;
        height: 40px;
        border-radius: 8px;
        background: var(--el-color-primary-light-8);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        color: var(--el-color-primary);
      }

      .type-info {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 4px;

        .name {
          font-weight: 500;
          color: var(--el-text-color-primary);
        }

        .desc {
          font-size: 12px;
          color: var(--el-text-color-secondary);
        }
      }
    }
  }

  .notify-methods {
    display: flex;
    flex-direction: column;
    gap: 12px;

    .method-item {
      padding: 16px;
      background: var(--el-fill-color-light);
      border-radius: 8px;
      transition: all 0.3s ease;

      &:hover {
        background: var(--el-fill-color);
      }

      &.active {
        background: var(--el-color-primary-light-9);
      }

      .method-content {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-left: 8px;

        .method-icon {
          width: 32px;
          height: 32px;
          border-radius: 6px;
          background: var(--el-color-primary-light-8);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 16px;
          color: var(--el-color-primary);
        }

        .method-info {
          flex: 1;
          display: flex;
          flex-direction: column;
          gap: 2px;

          .name {
            font-weight: 500;
            color: var(--el-text-color-primary);
          }

          .desc {
            font-size: 12px;
            color: var(--el-text-color-secondary);
          }
        }
      }
    }
  }

  .threshold-settings {
    padding: 16px;
    background: var(--el-fill-color-light);
    border-radius: 8px;

    .el-form {
      max-width: 300px;
    }

    .el-form-item {
      margin-bottom: 20px;

      &:last-child {
        margin-bottom: 0;
      }
    }

    .unit {
      margin-left: 8px;
      color: var(--el-text-color-secondary);
    }
  }
}
</style> 