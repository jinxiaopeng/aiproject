<!-- 训练指南组件 -->
<template>
  <div class="training-guide">
    <el-card class="guide-card">
      <template #header>
        <div class="guide-header">
          <h2>{{ challenge.title }}</h2>
          <div class="guide-meta">
            <el-tag type="success">{{ challenge.category }}</el-tag>
            <el-tag :type="difficultyType">{{ challenge.difficulty }}</el-tag>
            <el-tag type="info">{{ challenge.points }} 分</el-tag>
          </div>
        </div>
      </template>

      <!-- 靶场描述 -->
      <div class="guide-section">
        <h3>靶场描述</h3>
        <p>{{ challenge.description }}</p>
      </div>

      <!-- 学习目标 -->
      <div v-if="challenge.objectives" class="guide-section">
        <h3>学习目标</h3>
        <ul>
          <li v-for="(objective, index) in challenge.objectives" :key="index">
            {{ objective }}
          </li>
        </ul>
      </div>

      <!-- 前置知识 -->
      <div v-if="challenge.prerequisites" class="guide-section">
        <h3>前置知识</h3>
        <el-collapse>
          <el-collapse-item 
            v-for="(prereq, index) in challenge.prerequisites" 
            :key="index"
            :title="prereq.title"
          >
            <p>{{ prereq.description }}</p>
            <div v-if="prereq.links" class="prereq-links">
              <h4>相关资料</h4>
              <ul>
                <li v-for="(link, linkIndex) in prereq.links" :key="linkIndex">
                  <el-link 
                    :href="link.url" 
                    target="_blank"
                    type="primary"
                  >
                    {{ link.title }}
                  </el-link>
                </li>
              </ul>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <!-- 环境信息 -->
      <div v-if="challenge.environment" class="guide-section">
        <h3>环境信息</h3>
        <el-descriptions border>
          <el-descriptions-item label="环境类型">
            {{ challenge.environment.type }}
          </el-descriptions-item>
          <el-descriptions-item v-if="challenge.environment.version" label="版本">
            {{ challenge.environment.version }}
          </el-descriptions-item>
          <el-descriptions-item v-if="challenge.environment.ports" label="端口">
            {{ challenge.environment.ports.join(', ') }}
          </el-descriptions-item>
        </el-descriptions>
        
        <div v-if="challenge.environment.notice" class="env-notice">
          <el-alert
            type="warning"
            :title="challenge.environment.notice"
            :closable="false"
            show-icon
          />
        </div>

        <div v-if="challenge.environment.setup" class="env-setup">
          <h4>环境配置步骤</h4>
          <el-steps direction="vertical">
            <el-step 
              v-for="(step, index) in challenge.environment.setup" 
              :key="index"
              :title="step"
            />
          </el-steps>
        </div>
      </div>

      <!-- 注意事项 -->
      <div v-if="challenge.notices" class="guide-section">
        <h3>注意事项</h3>
        <el-alert
          v-for="(notice, index) in challenge.notices"
          :key="index"
          type="info"
          :title="notice"
          :closable="false"
          show-icon
          style="margin-bottom: 10px"
        />
      </div>

      <!-- 提示信息 -->
      <div class="guide-section">
        <h3>提示信息</h3>
        <div v-if="challenge.hints" class="hints-list">
          <el-card 
            v-for="(hint, index) in challenge.hints" 
            :key="index"
            shadow="hover"
            class="hint-card"
          >
            <template #header>
              <div class="hint-header">
                <span>提示 {{ index + 1 }}</span>
                <el-button
                  v-if="!isHintUnlocked(index)"
                  type="primary"
                  link
                  @click="unlockHint(index)"
                >
                  解锁 (-{{ getHintCost(index) }} 积分)
                </el-button>
              </div>
            </template>
            <div v-if="isHintUnlocked(index)" class="hint-content">
              {{ hint }}
            </div>
            <div v-else class="hint-locked">
              <el-icon><Lock /></el-icon>
              <span>提示已锁定</span>
            </div>
          </el-card>
        </div>
        <el-empty v-else description="暂无提示" />
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Lock } from '@element-plus/icons-vue'
import type { Challenge } from '@/types/challenge'
import { getUnlockedHints, unlockHint as unlockHintApi } from '@/api/training'

const props = defineProps<{
  challenge: Challenge
}>()

// 状态
const unlockedHints = ref<number[]>([])

// 计算属性
const difficultyType = computed(() => {
  switch (props.challenge.difficulty) {
    case 'easy': return 'info'
    case 'medium': return 'warning'
    case 'hard': return 'danger'
    default: return 'info'
  }
})

// 检查提示是否已解锁
const isHintUnlocked = (index: number) => 
  unlockedHints.value.includes(index)

// 获取提示解锁成本
const getHintCost = (index: number) => 
  10 * (index + 1)  // 每个提示消耗递增的积分

// 解锁提示
const unlockHint = async (index: number) => {
  try {
    const { data } = await unlockHintApi(props.challenge.id, index)
    unlockedHints.value.push(index)
    ElMessage.success('提示解锁成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '提示解锁失败')
  }
}

// 加载已解锁的提示
const loadUnlockedHints = async () => {
  try {
    const { data } = await getUnlockedHints(props.challenge.id)
    unlockedHints.value = data
  } catch (error) {
    ElMessage.error('加载提示信息失败')
  }
}

// 初始化
onMounted(loadUnlockedHints)
</script>

<style scoped>
.training-guide {
  padding: 20px;
}

.guide-card {
  margin-bottom: 20px;
}

.guide-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.guide-header h2 {
  margin: 0;
}

.guide-meta {
  display: flex;
  gap: 10px;
}

.guide-section {
  margin-bottom: 30px;
}

.guide-section h3 {
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.prereq-links {
  margin-top: 15px;
}

.prereq-links h4 {
  margin-bottom: 10px;
}

.env-notice {
  margin: 15px 0;
}

.env-setup {
  margin-top: 15px;
}

.hints-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.hint-card {
  height: 100%;
}

.hint-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.hint-content {
  line-height: 1.6;
}

.hint-locked {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 20px;
  color: #909399;
}

.hint-locked .el-icon {
  font-size: 24px;
}
</style> 