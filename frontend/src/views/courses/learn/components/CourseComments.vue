<template>
  <div class="course-comments">
    <div class="comment-input">
      <el-input
        v-model="newComment"
        type="textarea"
        :rows="3"
        placeholder="写下你的评论..."
      />
      <el-button type="primary" @click="submitComment" :disabled="!newComment.trim()">
        发布评论
      </el-button>
    </div>
    
    <div class="comments-list">
      <div v-for="comment in comments" :key="comment.id" class="comment-item">
        <div class="comment-header">
          <el-avatar :size="32" :src="comment.avatar">{{ comment.username.charAt(0) }}</el-avatar>
          <span class="username">{{ comment.username }}</span>
          <span class="time">{{ comment.time }}</span>
        </div>
        <p class="comment-content">
          {{ comment.content }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Comment {
  id: number
  username: string
  avatar: string
  content: string
  time: string
}

const props = defineProps<{
  comments: Comment[]
}>()

const emit = defineEmits<{
  (e: 'add-comment', content: string): void
}>()

const newComment = ref('')

const submitComment = () => {
  if (!newComment.value.trim()) return
  emit('add-comment', newComment.value)
  newComment.value = ''
}
</script>

<style lang="scss" scoped>
.course-comments {
  padding: 20px;

  .comment-input {
    margin-bottom: 20px;
    
    .el-button {
      margin-top: 10px;
      float: right;
    }
  }

  .comments-list {
    margin-top: 40px;
    
    .comment-item {
      margin-bottom: 20px;
      padding-bottom: 20px;
      border-bottom: 1px solid var(--el-border-color-lighter);

      &:last-child {
        border-bottom: none;
      }

      .comment-header {
        display: flex;
        align-items: center;
        margin-bottom: 8px;

        .username {
          margin-left: 8px;
          font-weight: bold;
        }

        .time {
          margin-left: 12px;
          color: var(--el-text-color-secondary);
          font-size: 12px;
        }
      }

      .comment-content {
        margin: 8px 0 0 40px;
        line-height: 1.6;
        font-size: 14px;
        color: var(--el-text-color-primary);
        white-space: pre-wrap;
        word-break: break-all;
      }
    }
  }
}
</style> 