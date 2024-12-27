<template>
  <div class="discussion-panel">
    <div class="panel-header">
      <h3>讨论区</h3>
      <el-button type="primary" @click="showCommentDialog = true">
        发表讨论
      </el-button>
    </div>

    <!-- 评论列表 -->
    <div class="comment-list" v-loading="loading">
      <div v-if="comments.length === 0" class="no-comments">
        暂无讨论，来发表第一条评论吧
      </div>
      
      <div v-else class="comment-item" v-for="comment in comments" :key="comment.id">
        <div class="comment-header">
          <div class="user-info">
            <el-avatar :size="32" :src="comment.userAvatar" />
            <span class="username">{{ comment.username }}</span>
            <el-tag size="small" v-if="comment.isAuthor" type="success">作者</el-tag>
          </div>
          <span class="time">{{ formatTime(comment.createdAt) }}</span>
        </div>
        
        <div class="comment-content" v-html="formatContent(comment.content)"></div>
        
        <div class="comment-footer">
          <div class="actions">
            <el-button 
              text 
              size="small"
              @click="handleLike(comment)"
              :class="{ active: comment.isLiked }"
            >
              <el-icon><Share /></el-icon>
              <span>{{ comment.likes || '点赞' }}</span>
            </el-button>
            <el-button 
              text 
              size="small"
              @click="handleReply(comment)"
            >
              <el-icon><ChatRound /></el-icon>
              <span>回复</span>
            </el-button>
          </div>
        </div>

        <!-- 回复列表 -->
        <div class="reply-list" v-if="comment.replies && comment.replies.length > 0">
          <div class="reply-item" v-for="reply in comment.replies" :key="reply.id">
            <div class="reply-header">
              <div class="user-info">
                <el-avatar :size="24" :src="reply.userAvatar" />
                <span class="username">{{ reply.username }}</span>
                <el-tag size="small" v-if="reply.isAuthor" type="success">作者</el-tag>
              </div>
              <span class="time">{{ formatTime(reply.createdAt) }}</span>
            </div>
            <div class="reply-content">
              <template v-if="reply.replyTo">
                回复 <span class="reply-to">@{{ reply.replyTo }}</span>：
              </template>
              {{ reply.content }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 加载更多 -->
    <div v-if="hasMore" class="load-more">
      <el-button text @click="loadMore">
        加载更多
      </el-button>
    </div>

    <!-- 评论对话框 -->
    <el-dialog
      v-model="showCommentDialog"
      :title="replyTo ? '回复评论' : '发表讨论'"
      width="50%"
    >
      <el-form
        ref="commentForm"
        :model="commentForm"
        :rules="commentRules"
      >
        <el-form-item prop="content">
          <el-input
            v-model="commentForm.content"
            type="textarea"
            :rows="4"
            :placeholder="replyTo ? `回复 @${replyTo.username}` : '分享你的想法...'"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCommentDialog = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="submitComment"
            :loading="submitting"
          >
            发布
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  ChatRound,
  Share
} from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

interface Comment {
  id: number
  content: string
  username: string
  userAvatar: string
  createdAt: string
  likes: number
  isLiked: boolean
  isAuthor: boolean
  replies?: Reply[]
}

interface Reply {
  id: number
  content: string
  username: string
  userAvatar: string
  createdAt: string
  replyTo?: string
  isAuthor: boolean
}

const props = defineProps<{
  challengeId: number
}>()

// 状态变量
const loading = ref(false)
const submitting = ref(false)
const hasMore = ref(true)
const showCommentDialog = ref(false)
const comments = ref<Comment[]>([])
const replyTo = ref<Comment | null>(null)
const commentForm = ref({
  content: ''
})

// 表单验证规则
const commentRules: FormRules = {
  content: [
    { required: true, message: '请输入评论内容', trigger: 'blur' },
    { min: 2, message: '评论内容太短', trigger: 'blur' }
  ]
}

// 格式化时间
const formatTime = (time: string) => {
  return formatDistanceToNow(new Date(time), {
    addSuffix: true,
    locale: zhCN
  })
}

// 格式化内容
const formatContent = (content: string) => {
  // 处理@提及
  content = content.replace(/@(\w+)/g, '<span class="mention">@$1</span>')
  // 处理代码块
  content = content.replace(/`([^`]+)`/g, '<code>$1</code>')
  return content
}

// 加载评论
const loadComments = async () => {
  try {
    loading.value = true
    // TODO: 调用API加载评论
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟数据
    comments.value = [
      {
        id: 1,
        content: '这个靶场设计得很好，帮助我更好地理解了SQL注入原理',
        username: 'john_doe',
        userAvatar: 'https://avatars.githubusercontent.com/u/1234567',
        createdAt: '2024-01-20T10:00:00Z',
        likes: 12,
        isLiked: false,
        isAuthor: false,
        replies: [
          {
            id: 101,
            content: '感谢分享，我也学到了很多',
            username: 'alice',
            userAvatar: 'https://avatars.githubusercontent.com/u/7654321',
            createdAt: '2024-01-20T10:30:00Z',
            isAuthor: true
          }
        ]
      }
    ]
  } finally {
    loading.value = false
  }
}

// 加载更多
const loadMore = async () => {
  // TODO: 实现加载更多逻辑
  hasMore.value = false
}

// 点赞
const handleLike = async (comment: Comment) => {
  try {
    // TODO: 调用API处理点赞
    comment.isLiked = !comment.isLiked
    comment.likes += comment.isLiked ? 1 : -1
  } catch (error) {
    ElMessage.error('操作失败，请重试')
  }
}

// 回复
const handleReply = (comment: Comment) => {
  replyTo.value = comment
  showCommentDialog.value = true
}

// 提交评论
const submitComment = async () => {
  try {
    submitting.value = true
    // TODO: 调用API提交评论
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success('发布成功')
    showCommentDialog.value = false
    commentForm.value.content = ''
    replyTo.value = null
    
    // 重新加载评论
    await loadComments()
  } catch (error) {
    ElMessage.error('发布失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 初始加载
loadComments()
</script>

<style scoped>
.discussion-panel {
  padding: 20px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h3 {
  margin: 0;
  color: #e5eaf3;
}

.comment-list {
  margin-bottom: 20px;
}

.no-comments {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}

.comment-item {
  padding: 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.username {
  color: #e5eaf3;
  font-weight: 500;
}

.time {
  color: #909399;
  font-size: 12px;
}

.comment-content {
  color: #e5eaf3;
  line-height: 1.6;
  margin-bottom: 12px;
}

.comment-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.actions {
  display: flex;
  gap: 16px;
}

.actions .el-button {
  color: #909399;
}

.actions .el-button.active {
  color: #409eff;
}

.reply-list {
  margin-top: 12px;
  padding-left: 40px;
  background: rgba(255, 255, 255, 0.02);
  border-radius: 4px;
}

.reply-item {
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.reply-item:last-child {
  border-bottom: none;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.reply-content {
  color: #e5eaf3;
  padding-left: 32px;
}

.reply-to {
  color: #409eff;
}

.mention {
  color: #409eff;
  cursor: pointer;
}

code {
  background: rgba(255, 255, 255, 0.05);
  padding: 2px 4px;
  border-radius: 4px;
  font-family: monospace;
}

.load-more {
  text-align: center;
  margin-top: 20px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style> 