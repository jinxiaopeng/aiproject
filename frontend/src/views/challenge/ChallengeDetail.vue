<template>
  <div class="challenge-detail-container">
    <el-card v-if="challenge" class="challenge-card">
      <div class="challenge-header">
        <h2>{{ challenge.title }}</h2>
        <div class="challenge-meta">
          <el-tag :type="getDifficultyType(challenge.difficulty)">
            {{ challenge.difficulty }}
          </el-tag>
          <el-tag type="info">{{ challenge.category }}</el-tag>
          <span class="points">{{ challenge.points }} pts</span>
        </div>
      </div>

      <div class="challenge-content">
        <div class="description">
          <h3>题目描述</h3>
          <p>{{ challenge.description }}</p>
        </div>

        <div v-if="challenge.docker_image" class="instance-section">
          <h3>题目环境</h3>
          <div v-if="instance" class="instance-info">
            <el-alert
              title="题目环境已启动"
              type="success"
              description="环境将在2小时后自动销毁，请及时完成挑战"
              show-icon
            />
            <div class="instance-url">
              <p>访问地址：<a :href="instance.instance_url" target="_blank">{{ instance.instance_url }}</a></p>
              <p v-if="challenge.docker_image.includes('webgoat')" class="webgoat-note">
                注意：WebGoat首次访问可能需要等待1-2分钟才能完全启动，如果无法访问请稍等片刻后刷新页面。
              </p>
            </div>
            <el-button type="danger" @click="stopInstance" :loading="stopping">
              销毁环境
            </el-button>
          </div>
          <div v-else class="instance-actions">
            <el-button 
              type="primary" 
              @click="createInstance" 
              :loading="loading"
              :disabled="loading"
            >
              {{ loading ? '正在启动环境...' : '启动环境' }}
            </el-button>
            <div v-if="loading" class="startup-status">
              <el-progress :percentage="startupProgress" :status="startupStatus">
                <template #default="{ percentage }">
                  <span class="progress-label">{{ startupMessage }}</span>
                </template>
              </el-progress>
            </div>
          </div>
        </div>

        <div class="submit-section">
          <h3>提交Flag</h3>
          <el-form @submit.prevent="submitFlag">
            <el-form-item>
              <el-input
                v-model="flagInput"
                placeholder="输入flag"
                :prefix-icon="Flag"
              >
                <template #append>
                  <el-button 
                    type="primary" 
                    @click="submitFlag"
                    :loading="submitting"
                  >
                    提交
                  </el-button>
                </template>
              </el-input>
            </el-form-item>
          </el-form>
        </div>

        <div class="submissions-section">
          <h3>提交记录</h3>
          <el-table :data="submissions" style="width: 100%">
            <el-table-column prop="submitted_at" label="提交时间" width="180">
              <template #default="{ row }">
                {{ formatTime(row.submitted_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="submitted_flag" label="提交的Flag" />
            <el-table-column prop="is_correct" label="结果" width="100">
              <template #default="{ row }">
                <el-tag :type="row.is_correct ? 'success' : 'danger'">
                  {{ row.is_correct ? '正确' : '错误' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="points_awarded" label="得分" width="100" />
          </el-table>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Flag } from '@element-plus/icons-vue'
import dayjs from 'dayjs'
import type { Challenge, ChallengeInstance, ChallengeSubmission } from '@/api/challenge'
import {
  getChallenge,
  createInstance as createInstanceApi,
  stopInstance as stopInstanceApi,
  submitFlag as submitFlagApi,
  getSubmissions
} from '@/api/challenge'

const route = useRoute()
const challenge = ref<Challenge | null>(null)
const instance = ref<ChallengeInstance | null>(null)
const submissions = ref<ChallengeSubmission[]>([])
const flagInput = ref('')
const loading = ref(false)
const stopping = ref(false)
const startupProgress = ref(0)
const startupStatus = ref('primary')
const startupMessage = ref('')
const submitting = ref(false)

// 获取题目详情
const fetchChallenge = async () => {
  try {
    const { data } = await getChallenge(Number(route.params.id))
    challenge.value = data
  } catch (error) {
    console.error('Failed to fetch challenge:', error)
    ElMessage.error('获取题目详情失败')
  }
}

// 获取提交记录
const fetchSubmissions = async () => {
  try {
    const { data } = await getSubmissions(Number(route.params.id))
    submissions.value = data
  } catch (error) {
    console.error('Failed to fetch submissions:', error)
    ElMessage.error('获取提交记录失败')
  }
}

// 创建实例
const createInstance = async () => {
  if (!challenge.value) return
  
  loading.value = true
  startupProgress.value = 0
  startupStatus.value = 'primary'
  startupMessage.value = '正在拉取镜像...'
  
  try {
    // 启动进度模拟
    const progressInterval = setInterval(() => {
      if (startupProgress.value < 90) {
        startupProgress.value += 10
        
        if (startupProgress.value === 20) {
          startupMessage.value = '正在创建容器...'
        } else if (startupProgress.value === 50) {
          startupMessage.value = '等待容器启动...'
        } else if (startupProgress.value === 80) {
          startupMessage.value = '正在进行健康检查...'
        }
      }
    }, 2000)

    const { data } = await createInstanceApi(challenge.value.id)
    clearInterval(progressInterval)
    startupProgress.value = 100
    startupStatus.value = 'success'
    startupMessage.value = '环境启动成功'
    
    instance.value = data
    ElMessage.success('环境启动成功')
  } catch (error: any) {
    clearInterval(progressInterval)
    startupProgress.value = 100
    startupStatus.value = 'exception'
    startupMessage.value = error.response?.data?.detail || '启动环境失败'
    
    ElMessage.error({
      message: error.response?.data?.detail || '启动环境失败',
      duration: 5000
    })
  } finally {
    setTimeout(() => {
      loading.value = false
      startupProgress.value = 0
    }, 2000)
  }
}

// 停止实例
const stopInstance = async () => {
  if (!challenge.value) return
  
  stopping.value = true
  try {
    await stopInstanceApi(challenge.value.id)
    instance.value = null
    ElMessage.success('环境已销毁')
  } catch (error: any) {
    ElMessage.error({
      message: error.response?.data?.detail || '销毁环境失败',
      duration: 5000
    })
  } finally {
    stopping.value = false
  }
}

// 提交flag
const submitFlag = async () => {
  if (!challenge.value || !flagInput.value) return
  
  submitting.value = true
  try {
    const { data } = await submitFlagApi(challenge.value.id, flagInput.value)
    if (data.success) {
      ElMessage.success(data.message)
      flagInput.value = ''
      fetchSubmissions()
    } else {
      ElMessage.error(data.message)
    }
  } catch (error) {
    console.error('Failed to submit flag:', error)
    ElMessage.error('提交失败')
  } finally {
    submitting.value = false
  }
}

// 获取难度对应的类型
const getDifficultyType = (difficulty: string) => {
  const types = {
    EASY: 'success',
    MEDIUM: 'warning',
    HARD: 'danger'
  }
  return types[difficulty] || 'info'
}

// 格式化时间
const formatTime = (time: string) => {
  return dayjs(time).format('YYYY-MM-DD HH:mm:ss')
}

onMounted(() => {
  fetchChallenge()
  fetchSubmissions()
})
</script>

<style lang="scss" scoped>
.challenge-detail-container {
  padding: 20px;
}

.challenge-card {
  margin-bottom: 20px;
}

.challenge-header {
  margin-bottom: 20px;
}

.challenge-meta {
  margin-top: 10px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.points {
  font-size: 14px;
  color: #666;
}

.challenge-content {
  margin-top: 20px;
}

.description {
  margin-bottom: 30px;
}

.instance-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.instance-info {
  margin-top: 20px;
}

.instance-url {
  margin: 20px 0;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #ebeef5;
}

.instance-url a {
  color: #409eff;
  text-decoration: none;
}

.instance-url a:hover {
  text-decoration: underline;
}

.instance-actions {
  margin-top: 20px;
}

.startup-status {
  margin-top: 20px;
  padding: 15px;
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid #ebeef5;
}

.progress-label {
  font-size: 14px;
  color: #606266;
}

.flag-submission {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.submission-form {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.submission-history {
  margin-top: 30px;
}

.submission-item {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  background-color: #fff;
  border: 1px solid #ebeef5;
}

.submission-item.correct {
  border-left: 4px solid #67c23a;
}

.submission-item.incorrect {
  border-left: 4px solid #f56c6c;
}

.submission-time {
  font-size: 12px;
  color: #909399;
}

.webgoat-note {
  margin-top: 10px;
  padding: 10px;
  background-color: #fdf6ec;
  border-left: 4px solid #e6a23c;
  color: #666;
  font-size: 14px;
}
</style> 