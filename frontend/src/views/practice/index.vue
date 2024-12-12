# 创建新文件
<template>
  <div class="practice-container">
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
          <el-option label="密码学" value="crypto" />
          <el-option label="逆向工程" value="reverse" />
        </el-select>
      </div>
    </div>

    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Timer /></el-icon>
              <span>训练时长</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.totalHours || 0 }}</span>
            <span class="stats-label">小时</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Flag /></el-icon>
              <span>完成数</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.completedCount || 0 }}</span>
            <span class="stats-label">个</span>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stats-card">
          <template #header>
            <div class="stats-header">
              <el-icon><Trophy /></el-icon>
              <span>积分</span>
            </div>
          </template>
          <div class="stats-content">
            <span class="stats-value">{{ userStats.points || 0 }}</span>
            <span class="stats-label">分</span>
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
            <span class="stats-value">#{{ userStats.rank || '-' }}</span>
            <span class="stats-label">名</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 靶场列表 -->
    <div class="labs-list">
      <el-row :gutter="20">
        <el-col 
          v-for="lab in filteredLabs" 
          :key="lab.id"
          :xs="24"
          :sm="12"
          :md="8"
          :lg="8"
        >
          <el-card class="lab-card" shadow="hover">
            <div class="lab-header">
              <div class="lab-title">
                <h3>{{ lab.title }}</h3>
                <el-tag 
                  :type="getDifficultyType(lab.difficulty)"
                  size="small"
                >
                  {{ lab.difficulty }}
                </el-tag>
                <el-tag size="small">{{ lab.category }}</el-tag>
              </div>
              <div class="lab-points">
                {{ lab.points }} 分
              </div>
            </div>
            <div class="lab-content">
              <p>{{ lab.description }}</p>
            </div>
            <div class="lab-footer">
              <div class="lab-stats">
                <span>完成率: {{ lab.completionRate }}%</span>
                <span>解题人数: {{ lab.solvedCount }}</span>
              </div>
              <el-button 
                type="primary" 
                @click="handleStartLab(lab.id)"
                :disabled="lab.status === 'maintenance'"
              >
                {{ getLabButtonText(lab) }}
              </el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Timer, Flag, Trophy, Rank } from '@element-plus/icons-vue'
import { labApi } from '@/api/lab'

const router = useRouter()
const searchQuery = ref('')
const filterDifficulty = ref('')
const filterCategory = ref('')

// 用户统计数据
const userStats = ref({
  totalHours: 0,
  completedCount: 0,
  points: 0,
  rank: '-'
})

// 靶场列表数据
const labs = ref([])

// 获取用户统计数据
const getUserStats = async () => {
  try {
    const response = await labApi.getUserStats()
    userStats.value = response.data
  } catch (error) {
    ElMessage.error('获取用户统计数据失败')
  }
}

// 获取靶场列表
const getLabs = async () => {
  try {
    const response = await labApi.getLabList()
    labs.value = response.data
  } catch (error) {
    ElMessage.error('获取靶场列表失败')
  }
}

// 过滤靶场
const filteredLabs = computed(() => {
  return labs.value.filter(lab => {
    const matchQuery = lab.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                      lab.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchDifficulty = !filterDifficulty.value || lab.difficulty === filterDifficulty.value
    const matchCategory = !filterCategory.value || lab.category === filterCategory.value
    
    return matchQuery && matchDifficulty && matchCategory
  })
})

// 获取难度标签类型
const getDifficultyType = (difficulty: string) => {
  const types = {
    easy: 'success',
    medium: 'warning',
    hard: 'danger'
  }
  return types[difficulty] || 'info'
}

// 获取按钮文本
const getLabButtonText = (lab: any) => {
  if (lab.status === 'maintenance') return '维护中'
  return '开始训练'
}

// 处理搜索
const handleSearch = () => {
  // 实时搜索，不需要额外处理
}

// 处理开始训练
const handleStartLab = async (labId: number) => {
  try {
    await labApi.startLab(labId)
    router.push(`/practice/${labId}`)
  } catch (error) {
    ElMessage.error('启动靶场失败')
  }
}

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([
    getLabs(),
    getUserStats()
  ])
})
</script>

<style scoped>
.practice-container {
  padding: 20px;
}

.header {
  margin-bottom: 24px;
}

.header-content {
  margin-bottom: 16px;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  color: var(--el-text-color-primary);
}

.header-content p {
  margin: 8px 0 0;
  color: var(--el-text-color-secondary);
}

.header-actions {
  display: flex;
  gap: 16px;
}

.search-input {
  width: 300px;
}

.stats-row {
  margin-bottom: 24px;
}

.stats-card {
  height: 100%;
}

.stats-header {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stats-content {
  text-align: center;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  color: var(--el-color-primary);
}

.stats-label {
  margin-left: 4px;
  color: var(--el-text-color-secondary);
}

.lab-card {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.lab-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.lab-title {
  flex: 1;
}

.lab-title h3 {
  margin: 0 0 8px;
  font-size: 16px;
}

.lab-title .el-tag {
  margin-right: 8px;
}

.lab-points {
  font-weight: bold;
  color: var(--el-color-success);
}

.lab-content {
  flex: 1;
  margin-bottom: 12px;
}

.lab-content p {
  margin: 0;
  color: var(--el-text-color-secondary);
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.lab-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lab-stats {
  display: flex;
  gap: 16px;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}
</style> 