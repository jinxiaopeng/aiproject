# 创建新文件
<template>
  <div class="practice-detail">
    <div class="header">
      <div class="header-content">
        <h1>{{ lab.title }}</h1>
        <div class="lab-meta">
          <el-tag 
            :type="getDifficultyType(lab.difficulty)"
            size="small"
          >
            {{ lab.difficulty }}
          </el-tag>
          <el-tag size="small">{{ lab.category }}</el-tag>
          <span class="points">{{ lab.points }} 分</span>
        </div>
      </div>
      <div class="header-actions">
        <el-button 
          type="primary" 
          @click="handleStartLab"
          :loading="loading"
          :disabled="labStatus === 'running'"
        >
          {{ getActionButtonText() }}
        </el-button>
        <el-button 
          type="danger" 
          @click="handleStopLab"
          :disabled="labStatus !== 'running'"
        >
          停止实验
        </el-button>
      </div>
    </div>

    <el-row :gutter="20">
      <!-- 左侧内容区 -->
      <el-col :span="16">
        <el-card class="description-card">
          <template #header>
            <div class="card-header">
              <h3>实验说明</h3>
            </div>
          </template>
          <div class="description-content" v-html="lab.description"></div>
        </el-card>

        <el-card class="terminal-card">
          <template #header>
            <div class="card-header">
              <h3>实验终端</h3>
              <el-tag 
                :type="getStatusType(labStatus)"
                size="small"
              >
                {{ getStatusText(labStatus) }}
              </el-tag>
            </div>
          </template>
          <div class="terminal-content">
            <div v-if="labStatus === 'running' || labStatus === 'created'" class="terminal-info">
              <p>实验环境已启动，等待初始化...</p>
              <p v-if="instanceUrl">
                访问地址：
                <el-link 
                  :href="instanceUrl" 
                  target="_blank" 
                  type="primary"
                >
                  {{ instanceUrl }}
                </el-link>
              </p>
              <p v-else>
                <el-icon class="is-loading"><Loading /></el-icon>
                正在准备实验环境，请稍候...
              </p>
            </div>
            <div v-else class="terminal-placeholder">
              点击"开始实验"启动实验环境
            </div>
          </div>
        </el-card>

        <el-card class="submit-card">
          <template #header>
            <div class="card-header">
              <h3>提交 Flag</h3>
            </div>
          </template>
          <div class="submit-content">
            <el-input
              v-model="flag"
              placeholder="输入你找到的 Flag"
              :disabled="labStatus !== 'running'"
            >
              <template #append>
                <el-button 
                  type="primary" 
                  @click="handleSubmitFlag"
                  :disabled="labStatus !== 'running'"
                >
                  提交
                </el-button>
              </template>
            </el-input>
          </div>
        </el-card>
      </el-col>

      <!-- 右侧信息区 -->
      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>实验信息</h3>
            </div>
          </template>
          <div class="info-content">
            <div class="info-item">
              <span class="label">完成人数</span>
              <span class="value">{{ lab.solvedCount || 0 }}</span>
            </div>
            <div class="info-item">
              <span class="label">完成率</span>
              <span class="value">{{ lab.completionRate || 0 }}%</span>
            </div>
            <div class="info-item">
              <span class="label">创建时间</span>
              <span class="value">{{ lab.created_at ? formatDate(lab.created_at) : '未知' }}</span>
            </div>
          </div>
        </el-card>

        <el-card class="hints-card">
          <template #header>
            <div class="card-header">
              <h3>实验提示</h3>
            </div>
          </template>
          <div class="hints-content">
            <el-collapse v-if="lab.hints && lab.hints.length">
              <el-collapse-item 
                v-for="(hint, index) in lab.hints" 
                :key="index"
                :title="'提示 ' + (index + 1)"
              >
                {{ hint }}
              </el-collapse-item>
            </el-collapse>
            <div v-else class="no-hints">
              暂无提示
            </div>
          </div>
        </el-card>

        <el-card class="notes-card">
          <template #header>
            <div class="card-header">
              <h3>实验笔记</h3>
              <el-button 
                type="primary" 
                link
                @click="handleSaveNotes"
              >
                保存
              </el-button>
            </div>
          </template>
          <div class="notes-content">
            <el-input
              v-model="notes"
              type="textarea"
              :rows="6"
              placeholder="记录你的实验过程..."
            />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading as LoadingIcon } from '@element-plus/icons-vue'
import { labApi, noteApi } from '@/api'
import { formatDate } from '@/utils/date'

const route = useRoute()
const router = useRouter()
const labId = Number(route.params.id)

// 状态变量
const loading = ref(false)
const lab = ref({
  id: 0,
  title: '',
  description: '',
  difficulty: '' as 'easy' | 'medium' | 'hard',
  category: '',
  points: 0,
  hints: [] as string[],
  solvedCount: 0,
  completionRate: 0,
  created_at: null as string | null
})
const labStatus = ref<'not_started' | 'created' | 'running' | 'stopped' | 'completed' | 'error'>('not_started')
const instanceUrl = ref('')
const flag = ref('')
const notes = ref('')

// 获取靶场详情
const getLabDetail = async () => {
  try {
    console.log('获取靶场详情:', labId)
    const response = await labApi.getLabDetail(labId)
    console.log('靶场详情响应:', response)
    if (response.data) {
      lab.value = response.data
    } else {
      ElMessage.error('获取靶场详情失败：响应数据为空')
    }
  } catch (error: any) {
    console.error('获取靶场详情失败:', error)
    if (error?.response) {
      console.error('错误响应:', {
        status: error.response?.status,
        data: error.response?.data,
        headers: error.response?.headers
      })
      ElMessage.error(error.response?.data?.detail || '获取靶场详情失败')
    } else if (error?.request) {
      console.error('请求错误:', error.request)
      ElMessage.error('网络请求失败，请检查网络连接')
    } else {
      console.error('其他错误:', error.message)
      ElMessage.error('获取靶场详情失败')
    }
  }
}

// 获取靶场状态
const getLabStatus = async () => {
  try {
    console.log('获取靶场状态:', labId)
    const response = await labApi.getStatus(labId)
    console.log('靶场状态响应:', response)
    if (response.data) {
      labStatus.value = response.data.status
      if (response.data.instance_url) {
        instanceUrl.value = response.data.instance_url
      }
    }
  } catch (error: any) {
    console.error('获取靶场状态失败:', error)
    if (error?.response) {
      console.error('错误响应:', {
        status: error.response?.status,
        data: error.response?.data,
        headers: error.response?.headers
      })
    }
  }
}

// 启动靶场
const handleStartLab = async () => {
  loading.value = true
  try {
    const response = await labApi.startLab(labId)
    console.log('启动靶场响应:', response.data)
    
    if (response.data.status === 'success') {
      labStatus.value = 'created'
      ElMessage.success(response.data.message)
      
      // 开始轮询状态
      const checkStatus = async () => {
        const statusResponse = await labApi.getStatus(labId)
        console.log('检查状态:', statusResponse.data)
        
        if (statusResponse.data.status === 'running') {
          labStatus.value = 'running'
          instanceUrl.value = statusResponse.data.instance_url
          return true
        }
        return false
      }
      
      // 每5秒检查一次，最多检查12次（1分钟）
      let attempts = 0
      const statusInterval = setInterval(async () => {
        attempts++
        try {
          const isReady = await checkStatus()
          if (isReady || attempts >= 12) {
            clearInterval(statusInterval)
            if (!isReady && attempts >= 12) {
              ElMessage.warning('靶场启动超时，请稍后刷新页面查看状态')
            }
          }
        } catch (error) {
          console.error('检查状态失败:', error)
          clearInterval(statusInterval)
        }
      }, 5000)
    }
  } catch (error) {
    console.error('启动靶场失败:', error)
    ElMessage.error('启动靶场失败')
  } finally {
    loading.value = false
  }
}

// 停止靶场
const handleStopLab = async () => {
  try {
    await labApi.stopLab(labId)
    labStatus.value = 'stopped'
    instanceUrl.value = ''
    ElMessage.success('靶场已停止')
  } catch (error) {
    console.error('停止靶场失败:', error)
    ElMessage.error('停止靶场失败')
  }
}

// 提交 Flag
const handleSubmitFlag = async () => {
  if (!flag.value) {
    ElMessage.warning('请输入 Flag')
    return
  }

  try {
    const response = await labApi.submit(labId, flag.value)
    if (response.data.correct) {
      ElMessage.success('Flag 正确！')
      labStatus.value = 'completed'
    } else {
      ElMessage.error('Flag 错误，请重试')
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败')
  }
}

// 保存笔记
const handleSaveNotes = async () => {
  try {
    await noteApi.updateNote(labId, { content: notes.value })
    ElMessage.success('笔记保存成功')
  } catch (error) {
    console.error('保存笔记失败:', error)
    ElMessage.error('保存笔记失败')
  }
}

// 获取难度标签类型
const getDifficultyType = (difficulty: string): string => {
  const types: Record<string, string> = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return types[difficulty] || 'info'
}

// 获取状态标签类型
const getStatusType = (status: string): string => {
  const types: Record<string, string> = {
    created: 'warning',
    running: 'success',
    stopped: 'info',
    completed: 'success',
    error: 'danger',
    not_started: 'info'
  }
  return types[status] || 'info'
}

// 获取状态文本
const getStatusText = (status: string): string => {
  const texts: Record<string, string> = {
    created: '初始化中',
    running: '运行中',
    stopped: '已停止',
    completed: '已完成',
    error: '错误',
    not_started: '未开始'
  }
  return texts[status] || status
}

// 获取操作按钮文本
const getActionButtonText = () => {
  if (loading.value) return '启动中...'
  if (labStatus.value === 'running') return '正在运行'
  if (labStatus.value === 'created') return '初始化中'
  if (labStatus.value === 'completed') return '重新开始'
  return '开始实验'
}

// 定时检查靶场状态
let statusTimer: number
const startStatusCheck = () => {
  statusTimer = window.setInterval(() => {
    if (labStatus.value === 'running' || labStatus.value === 'created') {
      getLabStatus()
    }
  }, 30000) // 每30秒检查一次
}

onMounted(() => {
  getLabDetail()
  getLabStatus()
  startStatusCheck()
})

onBeforeUnmount(() => {
  if (statusTimer) {
    clearInterval(statusTimer)
  }
})
</script>

<style scoped>
.practice-detail {
  padding: 20px;
}

.header {
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.header-content h1 {
  margin: 0 0 12px;
  font-size: 24px;
}

.lab-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.points {
  font-weight: bold;
  color: var(--el-color-success);
}

.header-actions {
  display: flex;
  gap: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
}

.description-card,
.terminal-card,
.submit-card {
  margin-bottom: 20px;
}

.terminal-content {
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.terminal-info {
  text-align: center;
}

.terminal-placeholder {
  color: var(--el-text-color-secondary);
}

.info-content {
  .info-item {
    display: flex;
    justify-content: space-between;
    margin-bottom: 12px;

    .label {
      color: var(--el-text-color-secondary);
    }

    .value {
      font-weight: bold;
    }
  }
}

.hints-card,
.notes-card {
  margin-top: 20px;
}

.no-hints {
  color: var(--el-text-color-secondary);
  text-align: center;
  padding: 20px;
}

.is-loading {
  animation: rotating 2s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style> 