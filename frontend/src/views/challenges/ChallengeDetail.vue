<template>
  <div class="challenge-detail">
    <div class="header">
      <el-page-header @back="goBack">
        <template #content>
          <div class="content">
            <h1>{{ challenge.title }}</h1>
            <div class="meta">
              <el-tag size="small" :type="difficultyType">{{ challenge.difficulty }}</el-tag>
              <el-tag size="small" type="info">{{ challenge.category }}</el-tag>
              <span class="points">积分: {{ challenge.points }}</span>
            </div>
          </div>
        </template>
      </el-page-header>
    </div>

    <el-row :gutter="24" class="main-content">
      <el-col :span="16">
        <el-card class="description-card">
          <template #header>
            <div class="card-header">
              <h3>挑战描述</h3>
            </div>
          </template>
          <div class="description" v-html="challenge.description"></div>
        </el-card>

        <el-card class="terminal-card">
          <template #header>
            <div class="card-header">
              <h3>实验终端</h3>
              <div class="terminal-actions">
                <el-button type="primary" @click="startLab" :loading="loading">
                  {{ labStarted ? '重启环境' : '启动环境' }}
                </el-button>
                <el-button type="success" @click="openReportDialog">
                  提交实验报告
                </el-button>
              </div>
            </div>
          </template>
          <div class="terminal-container">
            <div v-if="!labStarted" class="terminal-placeholder">
              <el-empty description="点击上方按钮启动实验环境">
                <template #image>
                  <el-icon :size="64"><Monitor /></el-icon>
                </template>
              </el-empty>
            </div>
            <div v-else class="lab-environment">
              <div class="environment-tabs">
                <el-tabs v-model="activeTab" class="demo-tabs">
                  <el-tab-pane label="终端" name="terminal">
                    <lab-terminal />
                  </el-tab-pane>
                  
                  <el-tab-pane label="测试网站" name="browser">
                    <lab-browser :challenge-id="challengeId" />
                  </el-tab-pane>
                </el-tabs>
              </div>
              
              <flag-submit :challenge-id="challengeId" @success="handleFlagSuccess" />
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :span="8">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>挑战信息</h3>
            </div>
          </template>
          <div class="info-content">
            <div class="info-item">
              <span class="label">创建时间</span>
              <span class="value">{{ formatDate(challenge.createdAt) }}</span>
            </div>
            <div class="info-item">
              <span class="label">完成人数</span>
              <span class="value">{{ challenge.completions }}</span>
            </div>
            <div class="info-item">
              <span class="label">通过率</span>
              <span class="value">{{ challenge.passRate }}%</span>
            </div>
          </div>
        </el-card>

        <el-card class="hints-card">
          <template #header>
            <div class="card-header">
              <h3>提示信息</h3>
            </div>
          </template>
          <div class="hints-content">
            <el-collapse v-if="challenge.hints && challenge.hints.length">
              <el-collapse-item
                v-for="(hint, index) in challenge.hints"
                :key="index"
                :title="'提示 ' + (index + 1)"
              >
                {{ hint }}
              </el-collapse-item>
            </el-collapse>
            <el-empty v-else description="暂无提示" />
          </div>
        </el-card>

        <el-card class="discussion-card">
          <template #header>
            <div class="card-header">
              <h3>讨论区</h3>
            </div>
          </template>
          <discussion-panel :challenge-id="challengeId" />
        </el-card>
      </el-col>
    </el-row>

    <report-dialog
      v-model:visible="reportDialogVisible"
      :challenge-id="challengeId"
      @submitted="handleReportSubmitted"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Monitor } from '@element-plus/icons-vue'
import { format } from 'date-fns'
import ReportDialog from './components/ReportDialog.vue'
import DiscussionPanel from './components/DiscussionPanel.vue'
import LabTerminal from './components/LabTerminal.vue'
import LabBrowser from './components/LabBrowser.vue'
import FlagSubmit from './components/FlagSubmit.vue'
import { getChallengeDetail, startChallenge } from '@/api/challenge'

const route = useRoute()
const router = useRouter()
const challengeId = Number(route.params.id)

const challenge = ref({
  id: 0,
  title: '',
  description: '',
  difficulty: '',
  category: '',
  points: 0,
  createdAt: new Date(),
  completions: 0,
  passRate: 0,
  hints: [] as string[]
})

const loading = ref(false)
const labStarted = ref(false)
const activeTab = ref('terminal')
const reportDialogVisible = ref(false)

const difficultyType = computed(() => {
  switch (challenge.value.difficulty.toLowerCase()) {
    case 'easy':
      return 'success'
    case 'medium':
      return 'warning'
    case 'hard':
      return 'danger'
    default:
      return 'info'
  }
})

const formatDate = (date: Date) => {
  return format(new Date(date), 'yyyy-MM-dd HH:mm')
}

const goBack = () => {
  router.push('/challenges')
}

const startLab = async () => {
  try {
    loading.value = true
    await startChallenge(challengeId)
    labStarted.value = true
    ElMessage.success('实验环境启动成功')
    activeTab.value = 'browser'
  } catch (error) {
    ElMessage.error('启动实验环境失败')
  } finally {
    loading.value = false
  }
}

const openReportDialog = () => {
  if (!labStarted.value) {
    ElMessage.warning('请先启动实验环境')
    return
  }
  reportDialogVisible.value = true
}

const handleReportSubmitted = () => {
  ElMessage.success('报告提交成功')
  reportDialogVisible.value = false
}

const handleFlagSuccess = () => {
  // TODO: 更新挑战状态
  challenge.value.completions++
  challenge.value.passRate = Math.round((challenge.value.completions / 200) * 100)
}

const loadChallengeDetail = async () => {
  try {
    const data = await getChallengeDetail(challengeId)
    challenge.value = data
  } catch (error) {
    ElMessage.error('加载挑战详情失败')
  }
}

onMounted(() => {
  loadChallengeDetail()
})
</script>

<style scoped>
.challenge-detail {
  padding: 24px;
}

.header {
  margin-bottom: 24px;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.content h1 {
  margin: 0;
  font-size: 20px;
  color: #e5eaf3;
}

.meta {
  display: flex;
  align-items: center;
  gap: 12px;
}

.points {
  color: #909399;
  font-size: 14px;
}

.main-content {
  margin-bottom: 24px;
}

.description-card,
.terminal-card,
.info-card,
.hints-card,
.discussion-card {
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
  margin-bottom: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #e5eaf3;
}

.description {
  color: #e5eaf3;
  line-height: 1.6;
}

.terminal-actions {
  display: flex;
  gap: 12px;
}

.terminal-container {
  min-height: 400px;
}

.terminal-placeholder {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.lab-environment {
  height: 100%;
}

.environment-tabs {
  margin-bottom: 16px;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #e5eaf3;
}

.info-item .label {
  color: #909399;
}

.hints-content {
  color: #e5eaf3;
}

:deep(.el-collapse) {
  border: none;
  background: transparent;
}

:deep(.el-collapse-item__header) {
  background: transparent;
  color: #e5eaf3;
  border-bottom: 1px solid rgba(65, 184, 131, 0.1);
}

:deep(.el-collapse-item__content) {
  background: transparent;
  color: #e5eaf3;
  padding: 16px;
}
</style> 