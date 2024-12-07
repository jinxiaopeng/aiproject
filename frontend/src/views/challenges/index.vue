<template>
  <div class="challenges-container">
    <!-- 头部区域 -->
    <div class="header">
      <div class="header-content">
        <h1>靶场训练</h1>
        <p>在这里你可以通过实践来提升你的网络安全技能</p>
      </div>
      <div class="header-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索靶场..."
          class="search-input"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select v-model="filterDifficulty" placeholder="难度" clearable>
          <el-option label="入门" value="easy" />
          <el-option label="进阶" value="medium" />
          <el-option label="高级" value="hard" />
        </el-select>
        <el-select v-model="filterCategory" placeholder="分类" clearable>
          <el-option label="Web安全" value="web" />
          <el-option label="系统安全" value="system" />
          <el-option label="网络安全" value="network" />
        </el-select>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Trophy /></el-icon>
              <span>总分</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.totalPoints }}</span>
            <span class="stats-label">分</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Flag /></el-icon>
              <span>已完成</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.completedChallenges }}</span>
            <span class="stats-label">个</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Timer /></el-icon>
              <span>总时长</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.totalHours }}</span>
            <span class="stats-label">小时</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Rank /></el-icon>
              <span>排名</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">#{{ userStats.rank }}</span>
            <span class="stats-label">名</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 靶场列表 -->
    <div class="challenges-list">
      <el-row :gutter="20">
        <el-col 
          v-for="challenge in filteredChallenges" 
          :key="challenge.id"
          :xs="24"
          :sm="12"
          :md="8"
        >
          <el-card class="challenge-card" shadow="hover">
            <div class="challenge-header">
              <div class="challenge-title">
                <h3>{{ challenge.title }}</h3>
                <el-tag :type="getDifficultyType(challenge.difficulty)">
                  {{ getDifficultyText(challenge.difficulty) }}
                </el-tag>
              </div>
              <div class="challenge-category">
                <el-tag type="info">{{ challenge.category }}</el-tag>
              </div>
            </div>
            
            <div class="challenge-content">
              <p class="challenge-description">{{ challenge.description }}</p>
              <div class="challenge-meta">
                <div class="meta-item">
                  <el-icon><Trophy /></el-icon>
                  <span>{{ challenge.points }} 分</span>
                </div>
                <div class="meta-item">
                  <el-icon><User /></el-icon>
                  <span>{{ challenge.solvedCount }}人已解</span>
                </div>
              </div>
              <div class="challenge-progress">
                <div class="progress-text">
                  <span>完成率</span>
                  <span>{{ challenge.completionRate }}%</span>
                </div>
                <el-progress 
                  :percentage="challenge.completionRate"
                  :status="getProgressStatus(challenge.completionRate)"
                />
              </div>
            </div>

            <div class="challenge-footer">
              <el-button 
                type="primary" 
                @click="startChallenge(challenge)"
                :disabled="challenge.status === 'maintenance'"
              >
                {{ challenge.status === 'maintenance' ? '维护中' : '开始挑战' }}
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <!-- 加载更多 -->
    <div v-if="hasMore" class="load-more">
      <el-button 
        :loading="loading"
        @click="loadMore"
      >
        加载更多
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Search,
  Trophy,
  Flag,
  Timer,
  Rank,
  User
} from '@element-plus/icons-vue'

interface Challenge {
  id: number
  title: string
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
  category: string
  points: number
  solvedCount: number
  completionRate: number
  status: 'online' | 'maintenance'
}

const router = useRouter()
const searchQuery = ref('')
const filterDifficulty = ref('')
const filterCategory = ref('')
const loading = ref(false)
const hasMore = ref(true)

// 用户统计数据
const userStats = ref({
  totalPoints: 1250,
  completedChallenges: 8,
  totalHours: 24,
  rank: 128
})

// 模拟靶场数据
const challenges = ref<Challenge[]>([
  {
    id: 1,
    title: 'SQL注入基础训练',
    description: '通过一系列精心设计的SQL注入挑战，掌握SQL注入的基本原理和技巧',
    difficulty: 'easy',
    category: 'Web安全',
    points: 100,
    solvedCount: 1234,
    completionRate: 85,
    status: 'online'
  },
  {
    id: 2,
    title: 'XSS跨站脚本训练',
    description: '学习和实践各种类型的XSS攻击，提高Web安全防护能力',
    difficulty: 'medium',
    category: 'Web安全',
    points: 200,
    solvedCount: 890,
    completionRate: 72,
    status: 'online'
  },
  {
    id: 3,
    title: '文件上传漏洞训练',
    description: '通过实践掌握文件上传漏洞的利用和防护方法',
    difficulty: 'hard',
    category: 'Web安全',
    points: 300,
    solvedCount: 567,
    completionRate: 45,
    status: 'online'
  },
  {
    id: 4,
    title: 'Linux提权训练',
    description: '在模拟环境中练习Linux系统的权限提升技术',
    difficulty: 'medium',
    category: '系统安全',
    points: 250,
    solvedCount: 678,
    completionRate: 65,
    status: 'online'
  },
  {
    id: 5,
    title: '网络嗅探训练',
    description: '学习使用抓包工具分析网络流量，发现安全问题',
    difficulty: 'easy',
    category: '网络安全',
    points: 150,
    solvedCount: 945,
    completionRate: 88,
    status: 'maintenance'
  }
])

// 过滤靶场
const filteredChallenges = computed(() => {
  return challenges.value.filter(challenge => {
    const matchQuery = challenge.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                      challenge.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchDifficulty = !filterDifficulty.value || challenge.difficulty === filterDifficulty.value
    const matchCategory = !filterCategory.value || challenge.category === filterCategory.value
    
    return matchQuery && matchDifficulty && matchCategory
  })
})

// 获取难度等级文本
const getDifficultyText = (difficulty: string) => {
  const difficultyMap = {
    easy: '入门',
    medium: '进阶',
    hard: '高级'
  }
  return difficultyMap[difficulty as keyof typeof difficultyMap]
}

// 获取难度等级标签类型
const getDifficultyType = (difficulty: string) => {
  const typeMap = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return typeMap[difficulty as keyof typeof typeMap]
}

// 获取进度条状态
const getProgressStatus = (rate: number) => {
  if (rate >= 90) return 'success'
  if (rate >= 60) return 'warning'
  return 'exception'
}

// 搜索处理
const handleSearch = () => {
  // 使用 computed 属性自动处理过滤
}

// 加载更多
const loadMore = async () => {
  try {
    loading.value = true
    // TODO: 实现加载更多逻辑
    await new Promise(resolve => setTimeout(resolve, 1000))
    hasMore.value = false
  } finally {
    loading.value = false
  }
}

// 开始挑战
const startChallenge = (challenge: Challenge) => {
  router.push({
    name: 'ChallengeDetail',
    params: { id: challenge.id.toString() }
  })
}
</script>

<style scoped>
.challenges-container {
  padding: 20px;
}

.header {
  margin-bottom: 24px;
}

.header-content {
  margin-bottom: 16px;
}

.header-content h1 {
  margin: 0 0 8px;
  color: #e5eaf3;
  font-size: 24px;
}

.header-content p {
  margin: 0;
  color: #909399;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.search-input {
  width: 300px;
}

.stats-row {
  margin-bottom: 24px;
}

.stats-card {
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.stats-header {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #e5eaf3;
}

.stats-content {
  text-align: center;
  padding: 12px 0;
}

.stats-value {
  font-size: 24px;
  font-weight: 600;
  color: #e5eaf3;
}

.stats-label {
  margin-left: 4px;
  color: #909399;
}

.challenges-list {
  margin-bottom: 24px;
}

.challenge-card {
  height: 100%;
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
}

.challenge-header {
  margin-bottom: 16px;
}

.challenge-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.challenge-title h3 {
  margin: 0;
  color: #e5eaf3;
  font-size: 16px;
}

.challenge-description {
  color: #909399;
  margin: 0 0 16px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.challenge-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #909399;
}

.challenge-progress {
  margin-bottom: 16px;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  margin-bottom: 4px;
  color: #909399;
}

.challenge-footer {
  display: flex;
  justify-content: flex-end;
}

.load-more {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
}

:deep(.el-input__inner) {
  color: #e5eaf3;
}

:deep(.el-select .el-input__wrapper) {
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1);
}

:deep(.el-tag) {
  background: transparent;
}

:deep(.el-progress-bar__outer) {
  background: rgba(255, 255, 255, 0.05);
}

:deep(.el-button) {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: #e5eaf3;
}

:deep(.el-button:hover) {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
}

:deep(.el-button--primary) {
  background: #409eff;
  border-color: #409eff;
}

:deep(.el-button--primary:hover) {
  background: #66b1ff;
  border-color: #66b1ff;
}
</style> 