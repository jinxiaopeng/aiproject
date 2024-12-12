<template>
  <div class="feedback-detail">
    <el-skeleton :rows="3" animated v-if="feedbackStore.loading" />
    
    <template v-else-if="feedbackStore.currentFeedback">
      <div class="feedback-header">
        <div class="feedback-meta">
          <el-tag :type="getTypeTagType(feedbackStore.currentFeedback.feedback_type)">
            {{ getFeedbackTypeLabel(feedbackStore.currentFeedback.feedback_type) }}
          </el-tag>
          <el-tag :type="getStatusTagType(feedbackStore.currentFeedback.status)">
            {{ getFeedbackStatusLabel(feedbackStore.currentFeedback.status) }}
          </el-tag>
          <span class="feedback-time">{{ formatDate(feedbackStore.currentFeedback.created_at) }}</span>
        </div>
        <div class="feedback-actions">
          <el-button-group>
            <el-button size="small" @click="handleVote(true)" :loading="feedbackStore.submitting">
              <el-icon><ThumbUp /></el-icon>
              {{ feedbackStore.currentFeedback.upvotes || 0 }}
            </el-button>
            <el-button size="small" @click="handleVote(false)" :loading="feedbackStore.submitting">
              <el-icon><ThumbDown /></el-icon>
              {{ feedbackStore.currentFeedback.downvotes || 0 }}
            </el-button>
          </el-button-group>
        </div>
      </div>

      <div class="feedback-content">
        {{ feedbackStore.currentFeedback.content }}
      </div>

      <div class="feedback-rating" v-if="feedbackStore.currentFeedback.rating">
        <el-rate v-model="feedbackStore.currentFeedback.rating" disabled show-score />
      </div>

      <div class="admin-reply" v-if="feedbackStore.currentFeedback.admin_reply">
        <div class="reply-header">
          <el-icon><ChatRound /></el-icon>
          <span>管理员回复</span>
        </div>
        <div class="reply-content">
          {{ feedbackStore.currentFeedback.admin_reply }}
        </div>
      </div>

      <div class="admin-actions" v-if="isAdmin">
        <el-form :model="adminForm" label-width="80px">
          <el-form-item label="状态">
            <el-select v-model="adminForm.status">
              <el-option label="待处理" value="PENDING" />
              <el-option label="处理中" value="PROCESSING" />
              <el-option label="已解决" value="RESOLVED" />
              <el-option label="已拒绝" value="REJECTED" />
            </el-select>
          </el-form-item>
          <el-form-item label="回复">
            <el-input
              v-model="adminForm.admin_reply"
              type="textarea"
              :rows="3"
              placeholder="请输入回复内容"
            />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleAdminSubmit" :loading="feedbackStore.submitting">
              提交
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <div class="comments-section">
        <div class="comments-header">
          <h3>评论 ({{ feedbackStore.currentFeedback.comments?.length || 0 }})</h3>
          <el-button type="primary" @click="showCommentForm = true">添加评论</el-button>
        </div>

        <el-dialog
          v-model="showCommentForm"
          title="添加评论"
          width="500px"
          :close-on-click-modal="false"
        >
          <el-form :model="commentForm" label-width="0">
            <el-form-item>
              <el-input
                v-model="commentForm.content"
                type="textarea"
                :rows="4"
                placeholder="请输入评论内容"
              />
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="showCommentForm = false">取消</el-button>
              <el-button type="primary" @click="handleCommentSubmit" :loading="feedbackStore.submitting">
                提交
              </el-button>
            </span>
          </template>
        </el-dialog>

        <div class="comments-list">
          <el-empty v-if="!feedbackStore.currentFeedback.comments?.length" description="暂无评论" />
          
          <div v-else class="comment-items">
            <div v-for="comment in feedbackStore.currentFeedback.comments" :key="comment.id" class="comment-item">
              <div class="comment-header">
                <div class="comment-user">
                  <el-avatar :size="32">{{ getNameAvatar(comment.user_id.toString()) }}</el-avatar>
                  <span>用户{{ comment.user_id }}</span>
                </div>
                <span class="comment-time">{{ formatRelativeTime(comment.created_at) }}</span>
              </div>
              <div class="comment-content">
                {{ comment.content }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <el-empty v-else description="反馈不存在" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ThumbUp, ThumbDown, ChatRound } from '@element-plus/icons-vue'
import { useFeedbackStore } from '@/stores/feedback'
import { formatDate, formatRelativeTime } from '@/utils/date'
import { getNameAvatar } from '@/utils/user'

const props = defineProps<{
  feedbackId: number
}>()

const feedbackStore = useFeedbackStore()

const isAdmin = computed(() => true) // TODO: 从用户store获取

const showCommentForm = ref(false)
const commentForm = ref({
  content: ''
})

const adminForm = ref({
  status: '',
  admin_reply: ''
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

const handleVote = async (isUpvote: boolean) => {
  if (!feedbackStore.currentFeedback) return
  
  try {
    await feedbackStore.voteFeedback(feedbackStore.currentFeedback.id, isUpvote)
    ElMessage.success(isUpvote ? '点赞成功' : '踩踩成功')
  } catch (error) {
    // 错误已在store中处理
  }
}

const handleCommentSubmit = async () => {
  if (!feedbackStore.currentFeedback) return
  
  try {
    if (!commentForm.value.content.trim()) {
      ElMessage.warning('请输入评论内容')
      return
    }
    
    await feedbackStore.addComment(
      feedbackStore.currentFeedback.id,
      commentForm.value.content
    )
    
    showCommentForm.value = false
    commentForm.value.content = ''
    ElMessage.success('评论成功')
  } catch (error) {
    // 错误已在store中处理
  }
}

const handleAdminSubmit = async () => {
  if (!feedbackStore.currentFeedback) return
  
  try {
    await feedbackStore.updateFeedback(feedbackStore.currentFeedback.id, {
      status: adminForm.value.status,
      admin_reply: adminForm.value.admin_reply
    })
    ElMessage.success('更新成功')
  } catch (error) {
    // 错误已在store中处理
  }
}

// 初始化加载反馈详情
feedbackStore.fetchFeedbackDetail(props.feedbackId)
</script>

<style scoped>
.feedback-detail {
  padding: 20px;
}

.feedback-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  margin: 20px 0;
  line-height: 1.6;
}

.feedback-rating {
  margin: 16px 0;
}

.admin-reply {
  margin: 24px 0;
  padding: 16px;
  background-color: var(--el-color-primary-light-9);
  border-radius: 4px;

  .reply-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 8px;
    color: var(--el-color-primary);
  }

  .reply-content {
    line-height: 1.6;
  }
}

.admin-actions {
  margin: 24px 0;
  padding: 16px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
}

.comments-section {
  margin-top: 32px;

  .comments-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;

    h3 {
      margin: 0;
    }
  }
}

.comment-items {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment-item {
  padding: 16px;
  border: 1px solid var(--el-border-color);
  border-radius: 4px;

  .comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }

  .comment-user {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .comment-time {
    color: var(--el-text-color-secondary);
    font-size: 14px;
  }

  .comment-content {
    line-height: 1.6;
  }
}
</style> 