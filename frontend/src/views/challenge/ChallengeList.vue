`<template>
  <div class="challenge-container">
    <div class="filter-section">
      <el-select v-model="selectedCategory" placeholder="选择分类" clearable>
        <el-option
          v-for="category in categories"
          :key="category.key"
          :label="category.value"
          :value="category.key"
        />
      </el-select>
      
      <el-select v-model="selectedDifficulty" placeholder="选择难度" clearable>
        <el-option label="简单" value="EASY" />
        <el-option label="中等" value="MEDIUM" />
        <el-option label="困难" value="HARD" />
      </el-select>
    </div>

    <el-row :gutter="20" class="challenge-list">
      <el-col v-for="challenge in challenges" :key="challenge.id" :span="8">
        <el-card 
          class="challenge-card" 
          :class="{ 'is-solved': challenge.is_solved }"
          shadow="hover"
        >
          <div class="challenge-header">
            <h3>{{ challenge.title }}</h3>
            <el-tag :type="getDifficultyType(challenge.difficulty)">
              {{ challenge.difficulty }}
            </el-tag>
          </div>
          
          <div class="challenge-category">
            <el-tag type="info">{{ challenge.category }}</el-tag>
            <span class="points">{{ challenge.points }} pts</span>
          </div>
          
          <p class="description">{{ challenge.description }}</p>
          
          <div class="challenge-footer">
            <span class="solved-count">
              <el-icon><User /></el-icon>
              {{ challenge.solved_count }} 人已解出
            </span>
            
            <el-button 
              type="primary" 
              @click="router.push(`/challenges/${challenge.id}`)"
            >
              {{ challenge.is_solved ? '查看详情' : '开始挑战' }}
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 挑战对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="currentChallenge?.title"
      width="60%"
      destroy-on-close
    >
      <template v-if="currentChallenge">
        <div class="challenge-detail">
          <p class="description">{{ currentChallenge.description }}</p>
          
          <div v-if="instanceUrl" class="instance-info">
            <el-alert
              title="题目环境已启动"
              type="success"
              description="环境将在2小时后自动销毁，请及时完成挑战"
              show-icon
            />
            <div class="instance-url">
              访问地址：<a :href="instanceUrl" target="_blank">{{ instanceUrl }}</a>
            </div>
          </div>
          
          <el-form @submit.prevent="submitFlag" class="flag-form">
            <el-form-item>
              <el-input
                v-model="flagInput"
                placeholder="输入flag"
                :prefix-icon="Flag"
              >
                <template #append>
                  <el-button type="primary" @click="submitFlag">
                    提交
                  </el-button>
                </template>
              </el-input>
            </el-form-item>
          </el-form>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Flag } from '@element-plus/icons-vue'
import type { Challenge } from '@/api/challenge'
import {
  getCategories,
  getChallenges,
  createInstance,
  submitFlag as submitFlagApi
} from '@/api/challenge'

const router = useRouter()
const categories = ref([])
const challenges = ref<Challenge[]>([])
const selectedCategory = ref('')
const selectedDifficulty = ref('')
const dialogVisible = ref(false)
const currentChallenge = ref<Challenge | null>(null)
const instanceUrl = ref('')
const flagInput = ref('')

// 获取分类列表
const fetchCategories = async () => {
  try {
    const response = await getCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
    ElMessage.error('获取分类失败')
  }
}

// 获取题目列表
const fetchChallenges = async () => {
  try {
    const params = {
      category: selectedCategory.value || undefined,
      difficulty: selectedDifficulty.value || undefined
    }
    const response = await getChallenges(params)
    challenges.value = response.data
  } catch (error) {
    console.error('Failed to fetch challenges:', error)
    ElMessage.error('获取题目列表失败')
  }
}

// 打开题目
const openChallenge = async (challenge: Challenge) => {
  currentChallenge.value = challenge
  dialogVisible.value = true
  flagInput.value = ''
  instanceUrl.value = ''
  
  if (challenge.docker_image) {
    try {
      const response = await createInstance(challenge.id)
      instanceUrl.value = response.data.instance_url
    } catch (error) {
      console.error('Failed to create instance:', error)
      ElMessage.error('启动题目环境失败')
    }
  }
}

// 提交flag
const submitFlag = async () => {
  if (!currentChallenge.value || !flagInput.value) return
  
  try {
    const response = await submitFlagApi(currentChallenge.value.id, flagInput.value)
    if (response.data.success) {
      ElMessage.success(response.data.message)
      dialogVisible.value = false
      fetchChallenges() // 刷新题目列表
    } else {
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('Failed to submit flag:', error)
    ElMessage.error('提交失败')
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

// 监听筛选条件变化
watch([selectedCategory, selectedDifficulty], () => {
  fetchChallenges()
})

onMounted(() => {
  fetchCategories()
  fetchChallenges()
})
</script>

<style lang="scss" scoped>
.challenge-container {
  padding: 20px;
  
  .filter-section {
    margin-bottom: 20px;
    display: flex;
    gap: 20px;
  }
  
  .challenge-list {
    margin-top: 20px;
  }
  
  .challenge-card {
    margin-bottom: 20px;
    background: #1a1a1a;
    border: 1px solid #333;
    
    &.is-solved {
      border-color: #67c23a;
    }
    
    .challenge-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      
      h3 {
        margin: 0;
        color: #fff;
      }
    }
    
    .challenge-category {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      
      .points {
        color: #ffd700;
        font-weight: bold;
      }
    }
    
    .description {
      color: #999;
      margin: 10px 0;
      height: 40px;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }
    
    .challenge-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 10px;
      
      .solved-count {
        color: #999;
        display: flex;
        align-items: center;
        gap: 5px;
      }
    }
  }
}

.challenge-detail {
  .description {
    margin-bottom: 20px;
    white-space: pre-wrap;
  }
  
  .instance-info {
    margin: 20px 0;
    
    .instance-url {
      margin-top: 10px;
      
      a {
        color: #409eff;
        text-decoration: none;
        
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
  
  .flag-form {
    margin-top: 20px;
  }
}
</style>` 