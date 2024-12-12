<template>
  <div class="feedback-list">
    <div class="feedback-filters">
      <el-select v-model="filterType" placeholder="反馈类型" clearable>
        <el-option label="内容相关" value="CONTENT" />
        <el-option label="难度相关" value="DIFFICULTY" />
        <el-option label="建议" value="SUGGESTION" />
        <el-option label="问题反馈" value="BUG" />
        <el-option label="其他" value="OTHER" />
      </el-select>
      
      <el-select v-model="filterStatus" placeholder="处理状态" clearable>
        <el-option label="待处理" value="PENDING" />
        <el-option label="处理中" value="PROCESSING" />
        <el-option label="已解决" value="RESOLVED" />
        <el-option label="已拒绝" value="REJECTED" />
      </el-select>
      
      <el-select v-model="sortBy" placeholder="排序方式">
        <el-option label="最新优先" value="latest" />
        <el-option label="最早优先" value="oldest" />
        <el-option label="点赞最多" value="upvotes" />
      </el-select>
    </div>

    <div class="feedback-stats" v-if="feedbackStore.feedbackStats">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>总反馈数</template>
            <div class="stats-value">{{ feedbackStore.feedbackStats.total_feedback }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>待处理</template>
            <div class="stats-value">{{ feedbackStore.feedbackStats.pending_feedback }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>已解决</template>
            <div class="stats-value">{{ feedbackStore.feedbackStats.resolved_feedback }}</div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <template #header>平均评分</template>
            <div class="stats-value">{{ feedbackStore.feedbackStats.average_rating?.toFixed(1) || '-' }}</div>
          </el-card>
        </el-col>
      </el-row>
    </div>

    <el-empty v-if="!feedbackStore.loading && !filteredFeedback.length" description="暂无反馈" />
    
    <el-skeleton :rows="3" animated v-if="feedbackStore.loading" />

    <div v-else class="feedback-items">
      <el-card v-for="feedback in filteredFeedback" :key="feedback.id" class="feedback-item" shadow="hover">
        <div class="feedback-header">
          <div class="feedback-meta">
            <el-tag :type="getTypeTagType(feedback.feedback_type)">{{ getFeedbackTypeLabel(feedback.feedback_type) }}</el-tag>
            <el-tag :type="getStatusTagType(feedback.status)">{{ getFeedbackStatusLabel(feedback.status) }}</el-tag>
            <span class="feedback-time">{{ formatRelativeTime(feedback.created_at) }}</span>
          </div>
          <div class="feedback-actions">
            <el-button-group>
              <el-button size="small" @click="handleVote(feedback.id, true)" :loading="feedbackStore.submitting">
                <el-icon><ThumbUp /></el-icon>
                {{ feedback.upvotes || 0 }}
              </el-button>
              <el-button size="small" @click="handleVote(feedback.id, false)" :loading="feedbackStore.submitting">
                <el-icon><ThumbDown /></el-icon>
                {{ feedback.downvotes || 0 }}
              </el-button>
            </el-button-group>
          </div>
        </div>

        <div class="feedback-content">{{ feedback.content }}</div>

        <div class="feedback-footer">
          <div class="feedback-rating" v-if="feedback.rating">
            <el-rate v-model="feedback.rating" disabled show-score />
          </div>
          <el-button type="primary" link @click="$emit('view-detail', feedback.id)">
            查看详情
          </el-button>
        </div>
      </el-card>
    </div>

    <div class="feedback-pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="totalItems"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { ThumbUp, ThumbDown } from '@element-plus/icons-vue'
import { useFeedbackStore } from '@/stores/feedback'
import { formatRelativeTime } from '@/utils/date'
import type { Feedback } from '@/api/feedback'

const props = defineProps<{
  entityId: number
}>()

const emit = defineEmits<{
  (e: 'view-detail', id: number): void
}>()

const feedbackStore = useFeedbackStore()

const filterType = ref('')
const filterStatus = ref('')
const sortBy = ref('latest')
const currentPage = ref(1)
const pageSize = ref(10)

const totalItems = computed(() => feedbackStore.feedbackList.length)

const filteredFeedback = computed(() => {
  let result = [...feedbackStore.feedbackList]

  // 应用过滤
  if (filterType.value) {
    result = result.filter(f => f.feedback_type === filterType.value)
  }
  if (filterStatus.value) {
    result = result.filter(f => f.status === filterStatus.value)
  }

  // 应用排序
  switch (sortBy.value) {
    case 'latest':
      result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
      break
    case 'oldest':
      result.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
      break
    case 'upvotes':
      result.sort((a, b) => (b.upvotes || 0) - (a.upvotes || 0))
      break
  }

  return result
})

const getFeedbackTypeLabel = (type: string) => {
  const labels: Record<string, string> = {
    CONTENT: '内容相关',
    DIFFICULTY: '难度相关',
    SUGGESTION: '建议',
    BUG: '问题反馈',
    OTHER: '其他'
  }
  return labels[type] || type
}

const getFeedbackStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    PENDING: '待处理',
    PROCESSING: '处理中',
    RESOLVED: '已解决',
    REJECTED: '已拒绝'
  }
  return labels[status] || status
}

const getTypeTagType = (type: string) => {
  const types: Record<string, string> = {
    CONTENT: '',
    DIFFICULTY: 'warning',
    SUGGESTION: 'success',
    BUG: 'danger',
    OTHER: 'info'
  }
  return types[type] || ''
}

const getStatusTagType = (status: string) => {
  const types: Record<string, string> = {
    PENDING: 'info',
    PROCESSING: 'warning',
    RESOLVED: 'success',
    REJECTED: 'danger'
  }
  return types[status] || ''
}

const handleVote = async (feedbackId: number, isUpvote: boolean) => {
  try {
    await feedbackStore.voteFeedback(feedbackId, isUpvote)
    ElMessage.success(isUpvote ? '点赞成功' : '踩踩成功')
  } catch (error) {
    // 错误已在store中处理
  }
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
  loadFeedback()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  loadFeedback()
}

const loadFeedback = async () => {
  const skip = (currentPage.value - 1) * pageSize.value
  await feedbackStore.fetchEntityFeedback(props.entityId, {
    feedback_type: filterType.value || undefined,
    status: filterStatus.value || undefined,
    skip,
    limit: pageSize.value
  })
}

watch([filterType, filterStatus], () => {
  currentPage.value = 1
  loadFeedback()
})

onMounted(async () => {
  await Promise.all([
    loadFeedback(),
    feedbackStore.fetchFeedbackStats(props.entityId)
  ])
})
</script>

<style scoped>
.feedback-list {
  padding: 20px;
}

.feedback-filters {
  margin-bottom: 20px;
  display: flex;
  gap: 16px;
}

.feedback-stats {
  margin-bottom: 24px;
}

.stats-value {
  font-size: 24px;
  font-weight: bold;
  text-align: center;
  color: var(--el-color-primary);
}

.feedback-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feedback-item {
  .feedback-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }

  .feedback-meta {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .feedback-time {
    color: var(--el-text-color-secondary);
    font-size: 14px;
  }

  .feedback-content {
    margin: 12px 0;
    line-height: 1.6;
  }

  .feedback-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 12px;
  }
}

.feedback-pagination {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}
</style> 