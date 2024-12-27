<template>
  <div class="challenge-detail">
    <el-row :gutter="20" v-loading="loading">
      <!-- 左侧：靶场信息 -->
      <el-col :span="16">
        <el-card class="main-content">
          <template #header>
            <div class="challenge-header">
              <h2>{{ challenge.title }}</h2>
              <div class="challenge-meta">
                <el-tag :type="getDifficultyType(challenge.difficulty)">
                  {{ challenge.difficulty }}
                </el-tag>
                <el-tag>{{ challenge.category }}</el-tag>
                <el-tag type="info">{{ challenge.points }} 分</el-tag>
              </div>
            </div>
          </template>

          <!-- 靶场描述 -->
          <div class="section">
            <h3>靶场描述</h3>
            <p>{{ challenge.description }}</p>
          </div>

          <!-- 学习目标 -->
          <div class="section" v-if="challenge.objectives?.length">
            <h3>学习目标</h3>
            <ul>
              <li v-for="(objective, index) in challenge.objectives" :key="index">
                {{ objective }}
              </li>
            </ul>
          </div>

          <!-- 训练环境 -->
          <div class="section" v-if="challenge.environment">
            <h3>训练环境</h3>
            <el-descriptions border>
              <el-descriptions-item label="环境类型">
                {{ challenge.environment.type }}
              </el-descriptions-item>
              <el-descriptions-item label="访问地址" v-if="challenge.environment.url">
                <el-link type="primary" :href="challenge.environment.url" target="_blank">
                  {{ challenge.environment.url }}
                </el-link>
              </el-descriptions-item>
              <el-descriptions-item label="端口" v-if="challenge.environment.port">
                {{ challenge.environment.port }}
              </el-descriptions-item>
            </el-descriptions>
          </div>

          <!-- 训练步骤 -->
          <div class="section" v-if="challenge.steps?.length">
            <h3>训练步骤</h3>
            <training-steps 
              :steps="challenge.steps"
              :current-step="currentStep"
              @step-complete="handleStepComplete"
            />
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：提示和帮助 -->
      <el-col :span="8">
        <el-card class="side-content">
          <template #header>
            <div class="side-header">
              <h3>提示与帮助</h3>
            </div>
          </template>

          <!-- 提示列表 -->
          <div class="hints-section" v-if="challenge.hints?.length">
            <div v-for="(hint, index) in challenge.hints" :key="index" class="hint-item">
              <el-card shadow="hover">
                <template #header>
                  <div class="hint-header">
                    <span>提示 {{ index + 1 }}</span>
                    <el-button
                      v-if="!unlockedHints.includes(index)"
                      type="primary"
                      link
                      @click="unlockHint(index)"
                    >
                      解锁 (-{{ getHintCost(index) }} 积分)
                    </el-button>
                  </div>
                </template>
                <div v-if="unlockedHints.includes(index)" class="hint-content">
                  {{ hint }}
                </div>
                <div v-else class="hint-locked">
                  <el-icon><Lock /></el-icon>
                  <span>提示已锁定</span>
                </div>
              </el-card>
            </div>
          </div>

          <!-- 相关资源 -->
          <div class="resources-section" v-if="challenge.resources?.length">
            <h4>相关资源</h4>
            <ul>
              <li v-for="(resource, index) in challenge.resources" :key="index">
                <el-link :href="resource.url" target="_blank">
                  {{ resource.title }}
                </el-link>
              </li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock } from '@element-plus/icons-vue'
import TrainingSteps from '@/components/training/TrainingSteps.vue'
import { getChallenge, getHint } from '@/api/challenge'
import type { Challenge } from '@/types/challenge'

const route = useRoute()
const currentStep = ref(0)
const unlockedHints = ref<number[]>([])
const loading = ref(false)

// 靶场数据
const challenge = ref<Challenge>({
  id: 0,
  title: '',
  description: '',
  category: '',
  difficulty: 'easy',
  points: 0,
  objectives: [],
  environment: {
    type: '',
    url: '',
    port: 0
  },
  steps: [],
  hints: [],
  resources: []
})

// 获取难度标签类型
const getDifficultyType = (difficulty: string) => {
  const types: Record<string, string> = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return types[difficulty] || 'info'
}

// 获取提示解锁成本
const getHintCost = (index: number) => {
  return 10 * (index + 1)
}

// 解锁提示
const unlockHint = async (index: number) => {
  try {
    const response = await getHint(challenge.value.id, index)
    if (response.data.hint) {
      unlockedHints.value.push(index)
      challenge.value.hints[index] = response.data.hint
      ElMessage.success('提示解锁成功')
    }
  } catch (error) {
    ElMessage.error('解锁提示失败')
  }
}

// 处理步骤完成
const handleStepComplete = (step: number) => {
  currentStep.value = step + 1
  if (currentStep.value >= challenge.value.steps.length) {
    ElMessage.success('恭喜你完成了所有训练步骤！')
  }
}

// 加载靶场数据
const loadChallengeData = async () => {
  loading.value = true
  try {
    const challengeId = parseInt(route.params.id as string)
    const response = await getChallenge(challengeId)
    challenge.value = response.data
  } catch (error) {
    ElMessage.error('加载靶场数据失败')
  } finally {
    loading.value = false
  }
}

// 初始化
onMounted(() => {
  loadChallengeData()
})
</script>

<style scoped>
.challenge-detail {
  padding: 20px;
}

.challenge-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.challenge-header h2 {
  margin: 0;
}

.challenge-meta {
  display: flex;
  gap: 10px;
}

.section {
  margin-bottom: 30px;
}

.section h3 {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.side-content {
  position: sticky;
  top: 20px;
}

.hints-section {
  margin-bottom: 30px;
}

.hint-item {
  margin-bottom: 15px;
}

.hint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hint-locked {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #909399;
  padding: 20px 0;
}

.resources-section h4 {
  margin-bottom: 15px;
}

.resources-section ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.resources-section li {
  margin-bottom: 10px;
}
</style> 