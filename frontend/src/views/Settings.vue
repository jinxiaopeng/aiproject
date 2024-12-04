<template>
  <div class="settings">
    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <h2>系统设置</h2>
          <el-button 
            type="primary"
            :loading="saving"
            @click="handleSave"
          >
            保存设置
          </el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="settingsForm"
        label-width="120px"
      >
        <!-- 界面设置 -->
        <div class="section-title">界面设置</div>

        <el-form-item label="主题">
          <el-radio-group v-model="settingsForm.theme">
            <el-radio-button label="light">浅色</el-radio-button>
            <el-radio-button label="dark">深色</el-radio-button>
            <el-radio-button label="auto">跟随系统</el-radio-button>
          </el-radio-group>
        </el-form-item>

        <el-form-item label="主色调">
          <el-color-picker v-model="settingsForm.primaryColor" />
        </el-form-item>

        <el-form-item label="字体大小">
          <el-select v-model="settingsForm.fontSize">
            <el-option label="小" value="small" />
            <el-option label="中" value="medium" />
            <el-option label="大" value="large" />
          </el-select>
        </el-form-item>

        <!-- 实验环境设置 -->
        <div class="section-title">实验环境设置</div>

        <el-form-item label="默认终端">
          <el-select v-model="settingsForm.terminal">
            <el-option label="内置终端" value="builtin" />
            <el-option label="系统终端" value="system" />
          </el-select>
        </el-form-item>

        <el-form-item label="自动保存">
          <el-switch v-model="settingsForm.autoSave" />
        </el-form-item>

        <el-form-item label="保存间隔" v-if="settingsForm.autoSave">
          <el-input-number
            v-model="settingsForm.saveInterval"
            :min="1"
            :max="60"
            :step="1"
          />
          <span class="unit">分钟</span>
        </el-form-item>

        <!-- 隐私设置 -->
        <div class="section-title">隐私设置</div>

        <el-form-item label="数据收集">
          <el-switch v-model="settingsForm.dataCollection" />
          <div class="setting-description">
            允许收集使用数据以改进产品体验
          </div>
        </el-form-item>

        <el-form-item label="错误报告">
          <el-switch v-model="settingsForm.errorReporting" />
          <div class="setting-description">
            自动发送错误报告以帮助修复问题
          </div>
        </el-form-item>

        <!-- 高级设置 -->
        <div class="section-title">高级设置</div>

        <el-form-item label="代理设置">
          <el-input v-model="settingsForm.proxy" placeholder="http://proxy.example.com:8080" />
        </el-form-item>

        <el-form-item label="实验环境内存">
          <el-slider
            v-model="settingsForm.memory"
            :min="1"
            :max="8"
            :step="1"
            :marks="{
              1: '1GB',
              2: '2GB',
              4: '4GB',
              8: '8GB'
            }"
          />
        </el-form-item>

        <el-form-item label="日志级别">
          <el-select v-model="settingsForm.logLevel">
            <el-option label="错误" value="error" />
            <el-option label="警告" value="warning" />
            <el-option label="信息" value="info" />
            <el-option label="调试" value="debug" />
          </el-select>
        </el-form-item>

        <!-- 实验数据 -->
        <div class="section-title">实验数据</div>

        <el-form-item>
          <el-button type="danger" @click="handleClearData">
            清除所有实验数据
          </el-button>
          <div class="setting-description danger">
            此操作将清除所有本地实验数据，且无法恢复
          </div>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance } from 'element-plus'

export default defineComponent({
  name: 'Settings',
  setup() {
    const formRef = ref<FormInstance>()
    const saving = ref(false)
    
    // 设置表单数据
    const settingsForm = ref({
      // 界面设置
      theme: 'light',
      primaryColor: '#1890ff',
      fontSize: 'medium',
      
      // 实验环境设置
      terminal: 'builtin',
      autoSave: true,
      saveInterval: 5,
      
      // 隐私设置
      dataCollection: true,
      errorReporting: true,
      
      // 高级设置
      proxy: '',
      memory: 2,
      logLevel: 'info'
    })
    
    // 保存设置
    const handleSave = async () => {
      try {
        saving.value = true
        // TODO: 调用保存API
        await new Promise(resolve => setTimeout(resolve, 1000))
        ElMessage.success('设置已保存')
      } catch (error) {
        ElMessage.error('保存失败，请重试')
      } finally {
        saving.value = false
      }
    }
    
    // 清除数据
    const handleClearData = () => {
      ElMessageBox.confirm(
        '此操作将清除所有本地实验数据，是否继续？',
        '警告',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          // TODO: 调用清除数据API
          await new Promise(resolve => setTimeout(resolve, 1000))
          ElMessage.success('数据已清除')
        } catch (error) {
          ElMessage.error('清除失败，请重试')
        }
      }).catch(() => {
        // 取消操作
      })
    }
    
    return {
      formRef,
      saving,
      settingsForm,
      handleSave,
      handleClearData
    }
  }
})
</script>

<style scoped>
.settings {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 500;
}

.section-title {
  font-size: 16px;
  font-weight: 500;
  color: var(--text-color);
  margin: 24px 0 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--border-color);
}

.setting-description {
  margin-top: 8px;
  font-size: 12px;
  color: var(--text-color-secondary);
}

.setting-description.danger {
  color: var(--error-color);
}

.unit {
  margin-left: 8px;
  color: var(--text-color-secondary);
}

:deep(.el-slider__marks-text) {
  margin-top: 8px;
  color: var(--text-color-secondary);
}

@media (max-width: 768px) {
  .settings {
    padding: 16px;
  }
  
  .card-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .card-header .el-button {
    width: 100%;
  }
}
</style> 