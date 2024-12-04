<template>
  <div class="lab-list">
    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索实验..."
        class="search-input"
        :prefix-icon="Search"
        clearable
        @input="handleSearch"
      />
      <el-select
        v-model="filterDifficulty"
        placeholder="难度等级"
        class="filter-select"
        clearable
      >
        <el-option label="简单" value="easy" />
        <el-option label="中等" value="medium" />
        <el-option label="困难" value="hard" />
      </el-select>
      <el-select
        v-model="filterCategory"
        placeholder="实验分类"
        class="filter-select"
        clearable
      >
        <el-option label="Web安全" value="web" />
        <el-option label="系统安全" value="system" />
        <el-option label="网络安全" value="network" />
        <el-option label="密码学" value="crypto" />
      </el-select>
    </div>

    <!-- 实验列表 -->
    <div class="lab-grid">
      <el-row :gutter="20">
        <el-col 
          v-for="lab in filteredLabs" 
          :key="lab.id" 
          :xs="24" 
          :sm="12" 
          :md="8"
        >
          <el-card class="lab-card" shadow="hover">
            <div class="lab-header">
              <div class="lab-title">
                <h3>{{ lab.title }}</h3>
                <el-tag :type="getDifficultyType(lab.difficulty)">
                  {{ getDifficultyText(lab.difficulty) }}
                </el-tag>
              </div>
              <div class="lab-category">
                <el-tag type="info">{{ lab.category }}</el-tag>
              </div>
            </div>
            
            <div class="lab-content">
              <p class="lab-description">{{ lab.description }}</p>
              <div class="lab-meta">
                <div class="meta-item">
                  <el-icon><Timer /></el-icon>
                  <span>预计用时：{{ lab.duration }}</span>
                </div>
                <div class="meta-item">
                  <el-icon><User /></el-icon>
                  <span>{{ lab.participants }}人参与</span>
                </div>
              </div>
              <div class="lab-progress">
                <div class="progress-text">
                  <span>完成率</span>
                  <span>{{ lab.completionRate }}%</span>
                </div>
                <el-progress 
                  :percentage="lab.completionRate"
                  :status="getProgressStatus(lab.completionRate)"
                />
              </div>
            </div>
            
            <div class="lab-footer">
              <div class="lab-tags">
                <el-tag 
                  v-for="tag in lab.tags" 
                  :key="tag"
                  size="small"
                  effect="plain"
                >
                  {{ tag }}
                </el-tag>
              </div>
              <el-button 
                type="primary" 
                @click="handleStartLab(lab)"
              >
                开始实验
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

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Timer, User } from '@element-plus/icons-vue'

interface Lab {
  id: number
  title: string
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
  category: string
  duration: string
  participants: number
  completionRate: number
  tags: string[]
}

export default defineComponent({
  name: 'LabList',
  components: {
    Search,
    Timer,
    User
  },
  setup() {
    const router = useRouter()
    const searchQuery = ref('')
    const filterDifficulty = ref('')
    const filterCategory = ref('')
    const loading = ref(false)
    const hasMore = ref(true)
    
    // 模拟实验数据
    const labs = ref<Lab[]>([
      {
        id: 1,
        title: 'SQL注入漏洞实验',
        description: '通过实验了解SQL注入原理，掌握SQL注入的检测和防护方法',
        difficulty: 'medium',
        category: 'Web安全',
        duration: '2小时',
        participants: 1234,
        completionRate: 85,
        tags: ['SQL注入', 'Web安全', '漏洞利用']
      },
      {
        id: 2,
        title: 'XSS跨站脚本实验',
        description: '学习XSS漏洞的原理和分类，掌握XSS漏洞的防护措施',
        difficulty: 'easy',
        category: 'Web安全',
        duration: '1.5小时',
        participants: 890,
        completionRate: 92,
        tags: ['XSS', 'Web安全', '漏洞防护']
      },
      {
        id: 3,
        title: '缓冲区溢出实验',
        description: '深入理解缓冲区溢出原理，学习栈溢出和堆溢出的利用方法',
        difficulty: 'hard',
        category: '系统安全',
        duration: '3小时',
        participants: 567,
        completionRate: 65,
        tags: ['缓冲区溢出', '系统安全', '漏洞利用']
      }
    ])
    
    // 过滤实验
    const filteredLabs = computed(() => {
      return labs.value.filter(lab => {
        const matchQuery = lab.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
                          lab.description.toLowerCase().includes(searchQuery.value.toLowerCase())
        const matchDifficulty = !filterDifficulty.value || lab.difficulty === filterDifficulty.value
        const matchCategory = !filterCategory.value || lab.category === filterCategory.value
        
        return matchQuery && matchDifficulty && matchCategory
      })
    })
    
    // 获取难度等级文本
    const getDifficultyText = (difficulty: string) => {
      const difficultyMap = {
        easy: '简单',
        medium: '中等',
        hard: '困难'
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
      // TODO: 实现搜索逻辑
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
    
    // 开始实验
    const handleStartLab = (lab: Lab) => {
      router.push(`/lab/${lab.id}`)
    }
    
    return {
      searchQuery,
      filterDifficulty,
      filterCategory,
      loading,
      hasMore,
      filteredLabs,
      Search,
      getDifficultyText,
      getDifficultyType,
      getProgressStatus,
      handleSearch,
      loadMore,
      handleStartLab
    }
  }
})
</script>

<style scoped>
.lab-list {
  padding: 20px;
}

.filter-section {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

.search-input {
  width: 300px;
}

.filter-select {
  width: 160px;
}

.lab-grid {
  margin-bottom: 24px;
}

.lab-card {
  height: 100%;
  margin-bottom: 20px;
  transition: transform 0.3s;
}

.lab-card:hover {
  transform: translateY(-5px);
}

.lab-header {
  margin-bottom: 16px;
}

.lab-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.lab-title h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 500;
}

.lab-category {
  margin-bottom: 16px;
}

.lab-description {
  margin: 0 0 16px;
  font-size: 14px;
  color: var(--text-color-secondary);
  height: 40px;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.lab-meta {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
  font-size: 13px;
  color: var(--text-color-secondary);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.lab-progress {
  margin-bottom: 16px;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 13px;
  color: var(--text-color-secondary);
}

.lab-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.lab-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.load-more {
  text-align: center;
  margin-top: 24px;
}

@media (max-width: 768px) {
  .filter-section {
    flex-direction: column;
  }
  
  .search-input,
  .filter-select {
    width: 100%;
  }
  
  .lab-footer {
    flex-direction: column;
    gap: 16px;
  }
  
  .lab-tags {
    justify-content: center;
  }
  
  .lab-footer .el-button {
    width: 100%;
  }
}
</style> 