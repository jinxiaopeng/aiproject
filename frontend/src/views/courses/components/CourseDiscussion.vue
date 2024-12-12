<template>
  <div class="course-discussion">
    <div class="discussion-header">
      <h3>课程讨论</h3>
      <el-button type="primary" :icon="Plus" @click="addDiscussion">发起讨论</el-button>
    </div>

    <!-- 讨论列表 -->
    <div class="discussion-list">
      <el-empty v-if="!discussions.length" description="暂无讨论" />
      <div v-else v-for="discussion in discussions" :key="discussion.id" class="discussion-item">
        <div class="discussion-info">
          <el-avatar :src="discussion.user.avatar" :size="40" />
          <div class="user-info">
            <span class="username">{{ discussion.user.name }}</span>
            <span class="time">{{ formatDate(discussion.created_at) }}</span>
          </div>
          <el-tag v-if="discussion.video_time" size="small" type="info">
            {{ formatTime(discussion.video_time) }}
          </el-tag>
        </div>
        <div class="discussion-content">
          {{ discussion.content }}
        </div>
        <div class="discussion-actions">
          <el-button type="primary" link @click="showReply(discussion)">
            回复 ({{ discussion.replies?.length || 0 }})
          </el-button>
          <el-button type="primary" link @click="likeDiscussion(discussion)">
            <el-icon><StarFilled /></el-icon>
            {{ discussion.likes }}
          </el-button>
        </div>

        <!-- 回复列表 -->
        <div v-if="discussion.showReplies" class="reply-list">
          <div v-for="reply in discussion.replies" :key="reply.id" class="reply-item">
            <div class="reply-info">
              <el-avatar :src="reply.user.avatar" :size="32" />
              <div class="user-info">
                <span class="username">{{ reply.user.name }}</span>
                <span class="time">{{ formatDate(reply.created_at) }}</span>
              </div>
            </div>
            <div class="reply-content">
              {{ reply.content }}
            </div>
          </div>

          <!-- 回复输入框 -->
          <div class="reply-input">
            <el-input
              v-model="replyContent"
              type="textarea"
              :rows="2"
              placeholder="写下你的回复..."
            />
            <div class="reply-actions">
              <el-button @click="hideReply(discussion)">取消</el-button>
              <el-button type="primary" @click="submitReply(discussion)">回复</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 发起讨论对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="发起讨论"
      width="500px"
    >
      <el-form :model="newDiscussion" label-position="top">
        <el-form-item label="视频时间点">
          <el-switch
            v-model="newDiscussion.includeTime"
            active-text="包含当前视频时间点"
          />
        </el-form-item>
        <el-form-item label="讨论内容">
          <el-input
            v-model="newDiscussion.content"
            type="textarea"
            :rows="4"
            placeholder="写下你的想法..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitDiscussion">
            发布
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Plus as PlusIcon,
  Star as StarIcon
} from '@element-plus/icons-vue'
import dayjs from 'dayjs'

interface User {
  id: number
  name: string
  avatar: string
}

interface Reply {
  id: number
  content: string
  created_at: string
  user: User
}

interface Discussion {
  id: number
  content: string
  video_time?: number
  created_at: string
  user: User
  likes: number
  replies?: Reply[]
  showReplies?: boolean
}

const props = defineProps<{
  currentTime: number
  chapterId: number
}>()

const discussions = ref<Discussion[]>([])
const dialogVisible = ref(false)
const replyContent = ref('')
const newDiscussion = ref({
  content: '',
  includeTime: true
})

// 添加讨论
const addDiscussion = () => {
  newDiscussion.value.content = ''
  newDiscussion.value.includeTime = true
  dialogVisible.value = true
}

// 提交讨论
const submitDiscussion = async () => {
  if (!newDiscussion.value.content.trim()) {
    ElMessage.warning('请输入讨论内容')
    return
  }

  try {
    // TODO: 调用API保存讨论
    const discussion: Discussion = {
      id: Date.now(),
      content: newDiscussion.value.content,
      video_time: newDiscussion.value.includeTime ? props.currentTime : undefined,
      created_at: new Date().toISOString(),
      user: {
        id: 1,
        name: '当前用户',
        avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
      },
      likes: 0,
      replies: []
    }
    discussions.value.unshift(discussion)
    dialogVisible.value = false
    ElMessage.success('发布成功')
  } catch (error) {
    ElMessage.error('发布失败')
  }
}

// 显示回复
const showReply = (discussion: Discussion) => {
  discussion.showReplies = true
}

// 隐藏回复
const hideReply = (discussion: Discussion) => {
  discussion.showReplies = false
  replyContent.value = ''
}

// 提交回复
const submitReply = async (discussion: Discussion) => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('请输入回复内容')
    return
  }

  try {
    // TODO: 调用API保存回复
    const reply: Reply = {
      id: Date.now(),
      content: replyContent.value,
      created_at: new Date().toISOString(),
      user: {
        id: 1,
        name: '当前用户',
        avatar: 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'
      }
    }
    discussion.replies = discussion.replies || []
    discussion.replies.push(reply)
    replyContent.value = ''
    ElMessage.success('回复成功')
  } catch (error) {
    ElMessage.error('回复失败')
  }
}

// 点赞讨论
const likeDiscussion = async (discussion: Discussion) => {
  try {
    // TODO: 调用API点赞
    discussion.likes++
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

// 格式化视频时间
const formatTime = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = Math.floor(seconds % 60)
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

// 格式化日期
const formatDate = (date: string) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm')
}
</script>

<style lang="scss" scoped>
.course-discussion {
  padding: 1rem;

  .discussion-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;

    h3 {
      margin: 0;
      font-size: 1.2rem;
    }
  }

  .discussion-list {
    .discussion-item {
      padding: 1rem;
      border: 1px solid var(--el-border-color-light);
      border-radius: 4px;
      margin-bottom: 1rem;

      .discussion-info {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 0.5rem;

        .user-info {
          flex: 1;
          display: flex;
          flex-direction: column;

          .username {
            font-weight: 500;
          }

          .time {
            font-size: 0.9rem;
            color: var(--el-text-color-secondary);
          }
        }
      }

      .discussion-content {
        line-height: 1.6;
        color: var(--el-text-color-regular);
        margin: 0.5rem 0;
      }

      .discussion-actions {
        display: flex;
        gap: 1rem;
        margin-top: 0.5rem;
      }

      .reply-list {
        margin-top: 1rem;
        padding-top: 1rem;
        border-top: 1px solid var(--el-border-color-light);

        .reply-item {
          padding: 0.5rem 1rem;
          margin-bottom: 0.5rem;
          background: var(--el-bg-color-page);
          border-radius: 4px;

          .reply-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.25rem;

            .user-info {
              flex: 1;
              display: flex;
              flex-direction: column;

              .username {
                font-weight: 500;
                font-size: 0.9rem;
              }

              .time {
                font-size: 0.8rem;
                color: var(--el-text-color-secondary);
              }
            }
          }

          .reply-content {
            margin-left: 2.5rem;
            font-size: 0.95rem;
            line-height: 1.5;
          }
        }

        .reply-input {
          margin-top: 1rem;

          .reply-actions {
            margin-top: 0.5rem;
            display: flex;
            justify-content: flex-end;
            gap: 0.5rem;
          }
        }
      }
    }
  }
}
</style>