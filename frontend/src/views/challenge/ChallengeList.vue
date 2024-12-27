<template>
  <div class="challenge-list">
    <!-- 筛选器 -->
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-select v-model="category" placeholder="选择分类" clearable>
            <el-option v-for="cat in categories" :key="cat.value" :label="cat.label" :value="cat.value" />
          </el-select>
        </el-col>
        <el-col :span="6">
          <el-select v-model="difficulty" placeholder="选择难度" clearable>
            <el-option v-for="diff in difficulties" :key="diff.value" :label="diff.label" :value="diff.value" />
          </el-select>
        </el-col>
        <el-col :span="12">
          <el-input v-model="searchQuery" placeholder="搜索靶场..." clearable>
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-col>
      </el-row>
    </div>

    <!-- 靶场列表 -->
    <div class="challenge-grid">
      <el-row :gutter="20">
        <el-col v-for="challenge in filteredChallenges" :key="challenge.id" :span="8">
          <el-card class="challenge-card" shadow="hover">
            <div class="challenge-header">
              <h3>{{ challenge.title }}</h3>
              <div class="challenge-tags">
                <el-tag :type="getDifficultyType(challenge.difficulty)">{{ challenge.difficulty }}</el-tag>
                <el-tag>{{ challenge.category }}</el-tag>
              </div>
            </div>
            <div class="challenge-content">
              <p>{{ challenge.description }}</p>
              <div class="challenge-meta">
                <span>
                  <el-icon><User /></el-icon>
                  {{ challenge.solvedCount }} 人完成
                </span>
                <span>
                  <el-icon><Star /></el-icon>
                  {{ challenge.points }} 分
                </span>
              </div>
            </div>
            <div class="challenge-footer">
              <el-button type="primary" @click="startChallenge(challenge.id)">开始训练</el-button>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, User, Star } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()
const searchQuery = ref('')
const category = ref('')
const difficulty = ref('')

// 分类选项
const categories = [
  { label: 'Web安全', value: 'web' },
  { label: '系统安全', value: 'system' },
  { label: '密码学', value: 'crypto' },
  { label: '逆向工程', value: 'reverse' }
]

// 难度选项
const difficulties = [
  { label: '入门', value: 'easy' },
  { label: '进阶', value: 'medium' },
  { label: '高级', value: 'hard' }
]

// 模拟靶场数据
const challenges = ref([
  {
    id: 1,
    title: 'SQL注入基础训练',
    description: '通过实践学习SQL注入的基本原理和防御方法',
    category: 'web',
    difficulty: 'easy',
    points: 100,
    solvedCount: 150
  },
  // ... 其他靶场数据
])

// 过滤靶场列表
const filteredChallenges = computed(() => {
  return challenges.value.filter(challenge => {
    const matchQuery = challenge.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                      challenge.description.toLowerCase().includes(searchQuery.value.toLowerCase())
    const matchCategory = !category.value || challenge.category === category.value
    const matchDifficulty = !difficulty.value || challenge.difficulty === difficulty.value
    return matchQuery && matchCategory && matchDifficulty
  })
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

// 开始训练
const startChallenge = (id: number) => {
  router.push(`/challenge/${id}`)
}
</script>

<style scoped>
.challenge-list {
  padding: 20px;
}

.filter-section {
  margin-bottom: 20px;
}

.challenge-grid {
  margin-top: 20px;
}

.challenge-card {
  margin-bottom: 20px;
  height: 100%;
}

.challenge-header {
  margin-bottom: 15px;
}

.challenge-header h3 {
  margin: 0 0 10px 0;
}

.challenge-tags {
  display: flex;
  gap: 8px;
}

.challenge-content {
  margin-bottom: 15px;
}

.challenge-meta {
  display: flex;
  justify-content: space-between;
  color: #666;
  margin-top: 10px;
}

.challenge-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.challenge-footer {
  text-align: right;
}
</style>
``` 