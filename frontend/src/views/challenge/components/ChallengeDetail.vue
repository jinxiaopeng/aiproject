<template>
  <div class="challenge-detail">
    <!-- 题目信息 -->
    <div class="challenge-header">
      <h2>{{ challenge.title }}</h2>
      <div class="challenge-meta">
        <el-tag 
          :type="getDifficultyType(challenge.difficulty)"
          effect="dark"
          size="small"
        >
          {{ getDifficultyLabel(challenge.difficulty) }}
        </el-tag>
        <span class="points">{{ challenge.points }} pts</span>
      </div>
    </div>

    <!-- 标签栏 -->
    <el-tabs class="challenge-tabs">
      <el-tab-pane label="题目" name="description">
        <div class="description-content">
          <p>{{ challenge.description }}</p>
          
          <!-- 前置知识 -->
          <div class="prerequisites" v-if="challenge.prerequisites?.length">
            <h4>前置知识</h4>
            <ul>
              <li v-for="prereq in challenge.prerequisites" :key="prereq">
                {{ prereq }}
              </li>
            </ul>
          </div>

          <!-- 推荐工具 -->
          <div class="tools" v-if="challenge.tools?.length">
            <h4>推荐工具</h4>
            <div class="tools-list">
              <el-tag
                v-for="tool in challenge.tools"
                :key="tool"
                effect="dark"
                size="small"
              >
                {{ tool }}
              </el-tag>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="WriteUp" name="writeup">
        <div class="writeup-content">
          <el-empty description="完成挑战后解锁WriteUp" />
        </div>
      </el-tab-pane>

      <el-tab-pane label="解题记录" name="records">
        <div class="records-content">
          <el-empty description="暂无解题记录" />
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 靶场信息 -->
    <div class="challenge-actions">
      <div class="status-info">
        <span class="label">靶场状态：</span>
        <el-tag 
          :type="challenge.status === 'running' ? 'success' : 'info'"
          effect="dark"
        >
          {{ challenge.status === 'running' ? '运行中' : '未启动' }}
        </el-tag>
      </div>

      <div class="action-buttons">
        <el-button
          type="primary"
          :icon="challenge.status === 'running' ? Link : VideoPlay"
          @click="handleAction"
        >
          {{ challenge.status === 'running' ? '访问靶场' : '启动靶场' }}
        </el-button>

        <el-button
          v-if="challenge.status === 'running'"
          type="warning"
          icon="Refresh"
          @click="handleReset"
        >
          重置靶场
        </el-button>
      </div>

      <!-- Flag提交 -->
      <div class="flag-submit">
        <el-input
          v-model="flagInput"
          placeholder="请输入flag"
          :disabled="challenge.status === 'completed'"
        >
          <template #append>
            <el-button
              type="primary"
              @click="submitFlag"
              :disabled="challenge.status === 'completed'"
            >
              提交
            </el-button>
          </template>
        </el-input>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { VideoPlay, Link } from '@element-plus/icons-vue'
import type { Challenge } from '@/types/challenge'
import { ElMessage } from 'element-plus'

// Props
defineProps<{
  challenge: Challenge
}>()

// Emits
const emit = defineEmits<{
  (e: 'start'): void
  (e: 'reset'): void
  (e: 'submit-flag', flag: string): void
}>()

// Flag输入
const flagInput = ref('')

// 获取难度标签
const getDifficultyLabel = (difficulty: string) => {
  const labels = {
    beginner: '入门',
    easy: '简单',
    medium: '中等',
    hard: '困难',
    expert: '专家'
  }
  return labels[difficulty] || difficulty
}

// 获取难度类型
const getDifficultyType = (difficulty: string) => {
  const types = {
    beginner: 'info',
    easy: 'success',
    medium: 'warning',
    hard: 'danger',
    expert: 'danger'
  }
  return types[difficulty] || 'info'
}

// 处理靶场操作
const handleAction = () => {
  if (challenge.status === 'running') {
    // 访问靶场
    window.open(challenge.targetUrl, '_blank')
  } else {
    // 启动靶场
    emit('start')
  }
}

// 处理重置
const handleReset = () => {
  ElMessage.warning('确定要重置靶场环境吗？')
  emit('reset')
}

// 提交flag
const submitFlag = () => {
  if (!flagInput.value) {
    ElMessage.warning('请输入flag')
    return
  }
  emit('submit-flag', flagInput.value)
  flagInput.value = ''
}
</script>

<style scoped lang="scss">
.challenge-detail {
  background: rgba(16, 16, 24, 0.95);
  border-radius: 8px;
  overflow: hidden;

  .challenge-header {
    padding: 20px;
    border-bottom: 1px solid var(--border-color);

    h2 {
      margin: 0 0 10px 0;
      color: var(--text-color);
      font-size: 24px;
    }

    .challenge-meta {
      display: flex;
      align-items: center;
      gap: 12px;

      .points {
        color: var(--primary-color);
        font-weight: 500;
      }
    }
  }

  .challenge-tabs {
    :deep(.el-tabs__header) {
      margin: 0;
      border-bottom: 1px solid var(--border-color);
      padding: 0 20px;
      background: rgba(255, 255, 255, 0.02);
    }

    :deep(.el-tabs__content) {
      padding: 20px;
    }
  }

  .description-content {
    color: var(--text-color);
    line-height: 1.6;

    .prerequisites, .tools {
      margin-top: 20px;

      h4 {
        margin: 0 0 10px 0;
        color: var(--text-secondary);
      }
    }

    .prerequisites ul {
      margin: 0;
      padding-left: 20px;
      
      li {
        margin-bottom: 8px;
        &:last-child { margin-bottom: 0; }
      }
    }

    .tools-list {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
  }

  .challenge-actions {
    padding: 20px;
    border-top: 1px solid var(--border-color);
    display: flex;
    flex-direction: column;
    gap: 16px;

    .status-info {
      display: flex;
      align-items: center;
      gap: 8px;

      .label {
        color: var(--text-secondary);
      }
    }

    .action-buttons {
      display: flex;
      gap: 12px;
    }

    .flag-submit {
      margin-top: 8px;
      max-width: 500px;
    }
  }
}
</style> 
</style> 