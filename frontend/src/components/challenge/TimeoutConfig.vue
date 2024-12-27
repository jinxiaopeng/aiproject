<!-- 靶场超时配置组件 -->
<template>
  <div class="timeout-config">
    <a-card title="超时配置" :bordered="false">
      <template #extra>
        <a-button type="primary" size="small" @click="saveConfig" :loading="saving">
          保存配置
        </a-button>
      </template>
      
      <a-form :model="timeoutConfig" layout="vertical">
        <a-form-item label="总运行时间限制 (秒)">
          <a-input-number
            v-model:value="timeoutConfig.total_timeout"
            :min="300"
            :max="86400"
            style="width: 200px"
          />
          <span class="form-help">
            靶场实例的最长运行时间，超过后将自动停止 (5分钟 - 24小时)
          </span>
        </a-form-item>
        
        <a-form-item label="空闲时间限制 (秒)">
          <a-input-number
            v-model:value="timeoutConfig.idle_timeout"
            :min="300"
            :max="43200"
            style="width: 200px"
          />
          <span class="form-help">
            无操作的最长时间，超过后将自动停止 (5分钟 - 12小时)
          </span>
        </a-form-item>
        
        <a-form-item label="清理检查间隔 (秒)">
          <a-input-number
            v-model:value="timeoutConfig.cleanup_interval"
            :min="60"
            :max="3600"
            style="width: 200px"
          />
          <span class="form-help">
            系统检查超时进程的时间间隔 (1分钟 - 1小时)
          </span>
        </a-form-item>
      </a-form>
      
      <!-- 预设配置 -->
      <div class="preset-configs">
        <a-divider>预设配置</a-divider>
        <a-space>
          <a-button size="small" @click="applyPreset('short')">
            短会话 (1小时)
          </a-button>
          <a-button size="small" @click="applyPreset('medium')">
            中等会话 (4小时)
          </a-button>
          <a-button size="small" @click="applyPreset('long')">
            长会话 (8小时)
          </a-button>
        </a-space>
      </div>
    </a-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, watch } from 'vue'
import { message } from 'ant-design-vue'
import type { TimeoutConfig } from '@/types/challenge'
import { updateChallengeConfig } from '@/api/challenge'

// 预设配置
const PRESET_CONFIGS = {
  short: {
    total_timeout: 3600,    // 1小时
    idle_timeout: 1800,     // 30分钟
    cleanup_interval: 300   // 5分钟
  },
  medium: {
    total_timeout: 14400,   // 4小时
    idle_timeout: 3600,     // 1小时
    cleanup_interval: 300   // 5分钟
  },
  long: {
    total_timeout: 28800,   // 8小时
    idle_timeout: 7200,     // 2小时
    cleanup_interval: 300   // 5分钟
  }
}

export default defineComponent({
  name: 'TimeoutConfig',
  
  props: {
    challengeId: {
      type: Number,
      required: true
    },
    initialConfig: {
      type: Object as () => TimeoutConfig,
      required: true
    }
  },
  
  emits: ['update:config', 'saved'],
  
  setup(props, { emit }) {
    // 超时配置
    const timeoutConfig = ref<TimeoutConfig>({
      total_timeout: 3600,
      idle_timeout: 1800,
      cleanup_interval: 300,
      ...props.initialConfig
    })
    
    // 保存状态
    const saving = ref(false)
    
    // 监听配置变化
    watch(timeoutConfig, (newConfig) => {
      emit('update:config', newConfig)
    }, { deep: true })
    
    // 保存配置
    const saveConfig = async () => {
      try {
        saving.value = true
        await updateChallengeConfig(props.challengeId, {
          timeout_config: timeoutConfig.value
        })
        message.success('配置已保存')
        emit('saved', timeoutConfig.value)
      } catch (error) {
        message.error('保存配置失败')
        console.error('Failed to save timeout config:', error)
      } finally {
        saving.value = false
      }
    }
    
    // 应用预设配置
    const applyPreset = (preset: keyof typeof PRESET_CONFIGS) => {
      timeoutConfig.value = { ...PRESET_CONFIGS[preset] }
      message.info('已应用预设配置')
    }
    
    return {
      timeoutConfig,
      saving,
      saveConfig,
      applyPreset
    }
  }
})
</script>

<style scoped>
.timeout-config {
  margin-bottom: 24px;
}

.form-help {
  margin-left: 8px;
  color: rgba(0, 0, 0, 0.45);
  font-size: 12px;
}

.preset-configs {
  margin-top: 16px;
  text-align: center;
}
</style> 