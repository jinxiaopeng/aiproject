<template>
  <div class="challenge-container">
    <!-- 顶部统计卡片 -->
    <div class="stats-row">
      <el-card class="stats-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Trophy /></el-icon>
            <span>总训练数</span>
          </div>
        </template>
        <div class="stats-value">{{ stats.totalChallenges }}</div>
      </el-card>
      
      <el-card class="stats-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Star /></el-icon>
            <span>已完成</span>
          </div>
        </template>
        <div class="stats-value success">{{ stats.completedChallenges }}</div>
      </el-card>
      
      <el-card class="stats-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Timer /></el-icon>
            <span>进行中</span>
          </div>
        </template>
        <div class="stats-value warning">{{ stats.inProgressChallenges }}</div>
      </el-card>
      
      <el-card class="stats-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <el-icon><Medal /></el-icon>
            <span>总积分</span>
          </div>
        </template>
        <div class="stats-value primary">{{ stats.totalPoints }}</div>
      </el-card>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">
      <!-- 左侧面板 -->
      <div class="left-panel">
        <!-- 过滤器 -->
        <div class="filter-section">
          <ChallengeFilter
            :initial-filters="filters"
            @filter-change="handleFilterChange"
          />
        </div>
        
        <!-- 进度概览 -->
        <div class="progress-section">
          <ChallengeProgress :stats="stats" />
        </div>
      </div>

      <!-- 右侧靶场列表 -->
      <div class="right-panel">
        <div class="challenges-section">
          <!-- 列表头部 -->
          <div class="section-header">
            <div class="header-left">
              <h2>靶场列表</h2>
              <el-tag type="info" class="count-tag">
                共 {{ filteredChallenges.length }} 个靶场
              </el-tag>
            </div>
            <div class="header-right">
              <el-button
                type="primary"
                @click="handleAddChallenge"
                class="add-challenge-btn"
              >
                <el-icon><Plus /></el-icon>
                添加题库
              </el-button>
              <el-radio-group v-model="viewMode" size="large">
                <el-radio-button label="grid">
                  <el-icon><Grid /></el-icon>
                </el-radio-button>
                <el-radio-button label="list">
                  <el-icon><List /></el-icon>
                </el-radio-button>
              </el-radio-group>
            </div>
          </div>

          <!-- 靶场卡片网格 -->
          <div 
            class="challenges-grid"
            :class="{ 'list-view': viewMode === 'list' }"
          >
            <ChallengeCard
              v-for="challenge in filteredChallenges"
              :key="challenge.id"
              :challenge="challenge"
              @status-change="handleStatusChange"
              @challenge-complete="handleChallengeComplete"
              @update-stats="handleStatsUpdate"
            />
          </div>

          <!-- 分页器 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="totalChallenges"
              :page-sizes="[12, 24, 36, 48]"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import {
  Trophy,
  Star,
  Timer,
  Medal,
  Grid,
  List,
  Plus
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import ChallengeFilter from './components/ChallengeFilter.vue'
import ChallengeProgress from './components/ChallengeProgress.vue'
import ChallengeCard from './components/ChallengeCard.vue'
import { useRouter } from 'vue-router'
import { useStore } from '../../stores/challenge'

// 定义Challenge接口
interface Challenge {
  id: number
  title: string
  description: string
  category: string
  difficulty: 'beginner' | 'easy' | 'medium' | 'hard' | 'expert'
  points: number
  status: 'not_started' | 'in_progress' | 'completed'
  completionRate: number
  tags: string[]
  solvedCount: number
  totalAttempts: number
  environment?: {
    type: string
    port: number
    status: 'not_started' | 'in_progress' | 'completed'
  }
}

// 定义Filters接口
interface Filters {
  categories: string[]
  difficulty: string | null
  status: string
  search: string
}

const router = useRouter()
const store = useStore()

// 统计数据
const stats = ref({
  totalChallenges: 30,
  completedChallenges: 15,
  inProgressChallenges: 3,
  totalPoints: 1250
})

// 过滤器状态
const filters = ref<Filters>({
  categories: [],
  difficulty: null,
  status: 'all',
  search: ''
})

// 视图控制
const viewMode = ref('grid')
const currentPage = ref(1)
const pageSize = ref(12)
const totalChallenges = ref(50)

// 使用store中的challenges替换模拟数据
const challenges = computed(() => store.getChallenges().map(c => ({
  ...c,
  solvedCount: c.solvedCount || 0,
  totalAttempts: c.totalAttempts || 0
})))

// 计算过滤后的靶场列表
const filteredChallenges = computed(() => {
  let result = challenges.value

  // 应过滤条件
  if (filters.value.categories.length > 0) {
    result = result.filter(c => filters.value.categories.includes(c.category))
  }
  if (filters.value.difficulty) {
    result = result.filter(c => c.difficulty === filters.value.difficulty)
  }
  if (filters.value.status && filters.value.status !== 'all') {
    result = result.filter(c => c.status === filters.value.status)
  }
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    result = result.filter(c => 
      c.title.toLowerCase().includes(search) || 
      c.description.toLowerCase().includes(search)
    )
  }

  return result
})

// 处理过滤器变化
const handleFilterChange = (newFilters: Filters) => {
  filters.value = newFilters
  currentPage.value = 1 // 重置页码
}

// 处理分页
const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// 处理挑战状态变化
const handleStatusChange = (challengeId: number, newStatus: 'not_started' | 'in_progress' | 'completed') => {
  const challenge = challenges.value.find(c => c.id === challengeId)
  if (challenge) {
    const oldStatus = challenge.status
    challenge.status = newStatus
    
    // 更新进行中的数量
    if (newStatus === 'in_progress' && oldStatus === 'not_started') {
      stats.value.inProgressChallenges++
      challenge.completionRate = 0
    } else if (newStatus === 'completed' && oldStatus === 'in_progress') {
      stats.value.inProgressChallenges--
      challenge.completionRate = 100
    }
  }
}

// 更新统计数据
const updateStats = (challengeId: number) => {
  const challenge = challenges.value.find(c => c.id === challengeId)
  if (challenge) {
    stats.value.completedChallenges++
    stats.value.totalPoints += challenge.points
  }
}

// 处理挑战完成事件
const handleChallengeComplete = (challengeId: number) => {
  updateStats(challengeId)
}

// 处理统计数据更新
const handleStatsUpdate = (challengeId: number, solvedCount: number, totalAttempts: number) => {
  const challenge = challenges.value.find(c => c.id === challengeId)
  if (challenge) {
    challenge.solvedCount = solvedCount
    challenge.totalAttempts = totalAttempts
    challenge.completionRate = (solvedCount / totalAttempts) * 100
  }
}

// 添加题库处理函数
const handleAddChallenge = () => {
  // 跳转到添加题库页面
  router.push('/challenge/add')
}

// 生命周期钩子
onMounted(async () => {
  // 这里可以加载初始数据
  // await loadChallenges()
})
</script>

<style scoped lang="scss">
.challenge-container {
  padding: 24px;
  min-height: 100vh;
  background: #1a1b2e;
  position: relative;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(41, 41, 61, 0.95), rgba(28, 28, 45, 0.95));
    z-index: 0;
  }

  > * {
    position: relative;
    z-index: 1;
  }

  .stats-row {
    display: flex;
    gap: 20px;
    margin-bottom: 24px;

    .stats-card {
      flex: 1;
      background: rgba(30, 35, 45, 0.95);
      border: 1px solid rgba(255, 255, 255, 0.1);

      :deep(.el-card__header) {
        padding: 12px 16px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      }

      .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        color: rgba(255, 255, 255, 0.8);
        font-size: 14px;

        .el-icon {
          font-size: 16px;
        }
      }

      .stats-value {
        padding: 16px;
        font-size: 32px;
        font-weight: 600;
        text-align: center;
        font-family: 'Roboto', sans-serif;

        // 默认颜色
        color: rgba(255, 255, 255, 0.95);

        // 不同状态的颜色
        &.success { color: var(--el-color-success); }
        &.warning { color: var(--el-color-warning); }
        &.primary { color: var(--el-color-primary); }
      }
    }
  }

  .main-content {
    display: grid;
    grid-template-columns: 350px 1fr;
    gap: 24px;
    min-height: calc(100vh - 200px);

    .left-panel {
      display: flex;
      flex-direction: column;
      gap: 24px;

      .filter-section,
      .progress-section,
      .achievement-section {
        background: rgba(41, 41, 61, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        transition: all 0.3s ease;

        &:hover {
          border-color: var(--primary-color);
          background: rgba(45, 45, 68, 0.85);
        }
      }

      .achievement-section {
        flex: 1;
        min-height: 400px;
        overflow: auto;

        &::-webkit-scrollbar {
          width: 4px;
        }

        &::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.05);
        }

        &::-webkit-scrollbar-thumb {
          background: var(--primary-color);
          border-radius: 2px;
        }
      }
    }

    .right-panel {
      .challenges-section {
        background: rgba(41, 41, 61, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 8px;
        padding: 16px;
        height: 100%;
        display: flex;
        flex-direction: column;

        .section-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 16px;

          .header-left {
            display: flex;
            align-items: center;
            gap: 8px;

            h2 {
              color: var(--text-color);
              font-size: 20px;
              margin: 0;
            }

            .count-tag {
              font-size: 13px;
            }
          }
        }

        .challenges-grid {
          flex: 1;
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 16px;
          margin-bottom: 16px;
          padding: 8px;
          align-content: start;
          
          &.list-view {
            grid-template-columns: 1fr;
            max-width: 900px;
            margin: 0 auto;
            gap: 8px;
          }

          &::-webkit-scrollbar {
            width: 4px;
          }

          &::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
          }

          &::-webkit-scrollbar-thumb {
            background: var(--primary-color);
            border-radius: 2px;
          }
        }

        .pagination-wrapper {
          display: flex;
          justify-content: center;
          margin-top: auto;
          padding-top: 16px;
          border-top: 1px solid var(--border-color);
        }
      }
    }
  }
}

// 响应式布局
@media (max-width: 1400px) {
  .challenge-container {
    .main-content {
      grid-template-columns: 280px 1fr;
    }
  }
}

@media (max-width: 1200px) {
  .challenge-container {
    .stats-row {
      grid-template-columns: repeat(2, 1fr);
    }

    .main-content {
      grid-template-columns: 1fr;

      .left-panel {
        flex-direction: row;
        
        .filter-section,
        .progress-section,
        .achievement-section {
          flex: 1;
        }
      }

      .challenges-section {
        .challenges-grid {
          grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
          gap: 12px;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .challenge-container {
    padding: 16px;

    .stats-row {
      grid-template-columns: 1fr;
    }

    .main-content {
      .left-panel {
        flex-direction: column;
      }

      .challenges-section {
        .challenges-grid {
          grid-template-columns: 1fr;
        }
      }
    }
  }
}

.add-challenge-btn {
  margin-right: 16px;
}
</style> 