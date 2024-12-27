<template>
  <div class="daily-challenge">
    <div class="page-header">
      <h1 class="title">每日挑战</h1>
      <div class="stats">
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <el-icon><Calendar /></el-icon>
              <span>连续打卡</span>
            </div>
          </template>
          <div class="stat-value">{{ stats.streak }} 天</div>
        </el-card>
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <el-icon><Trophy /></el-icon>
              <span>总积分</span>
            </div>
          </template>
          <div class="stat-value">{{ stats.totalPoints }}</div>
        </el-card>
        <el-card class="stat-card">
          <template #header>
            <div class="card-header">
              <el-icon><Star /></el-icon>
              <span>完成率</span>
            </div>
          </template>
          <div class="stat-value">{{ stats.completionRate }}%</div>
        </el-card>
      </div>
    </div>

    <div class="challenge-content" v-loading="loading">
      <template v-if="currentChallenge">
        <el-card class="challenge-card">
          <template #header>
            <div class="challenge-header">
              <div class="challenge-title">
                <h2>{{ currentChallenge.title }}</h2>
                <el-tag :type="getDifficultyType(currentChallenge.difficulty)">
                  {{ currentChallenge.difficulty }}
                </el-tag>
              </div>
              <div class="challenge-meta">
                <span class="points">
                  <el-icon><Medal /></el-icon>
                  {{ currentChallenge.points }} 积分
                </span>
                <el-button 
                  type="primary" 
                  :disabled="isCompleted"
                  @click="submitChallenge"
                >
                  {{ isCompleted ? '已完成' : '提交答案' }}
                </el-button>
              </div>
            </div>
          </template>
          
          <div class="challenge-description">
            <div class="markdown-content" v-html="renderedDescription"></div>
          </div>

          <div class="challenge-input" v-if="!isCompleted">
            <el-input
              v-model="userAnswer"
              type="textarea"
              :rows="4"
              placeholder="请输入你的答案..."
              :maxlength="1000"
              show-word-limit
            />
          </div>

          <div class="challenge-hints" v-if="currentChallenge.hints?.length">
            <h3>提示</h3>
            <el-collapse>
              <el-collapse-item 
                v-for="(hint, index) in currentChallenge.hints" 
                :key="index"
                :title="'提示 ' + (index + 1)"
              >
                {{ hint }}
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-card>

        <el-card class="discussion-card">
          <template #header>
            <div class="card-header">
              <h3>讨论区</h3>
              <el-button type="primary" @click="showCommentDialog = true">
                发表评论
              </el-button>
            </div>
          </template>
          
          <div class="comments-list">
            <div v-if="comments.length === 0" class="no-comments">
              暂无评论，来发表第一条评论吧！
            </div>
            <div 
              v-for="comment in comments" 
              :key="comment.id" 
              class="comment-item"
            >
              <div class="comment-header">
                <div class="user-info">
                  <el-avatar :size="32" :src="comment.userAvatar" />
                  <span class="username">{{ comment.username }}</span>
                </div>
                <span class="comment-time">{{ formatTime(comment.createTime) }}</span>
              </div>
              <div class="comment-content">{{ comment.content }}</div>
            </div>
          </div>
        </el-card>
      </template>

      <el-empty v-else description="今日挑战尚未开放" />
    </div>

    <!-- 评论对话框 -->
    <el-dialog
      v-model="showCommentDialog"
      title="发表评论"
      width="500px"
    >
      <el-form :model="commentForm" ref="commentFormRef">
        <el-form-item 
          prop="content"
          :rules="[
            { required: true, message: '请输入评论内容', trigger: 'blur' },
            { min: 2, max: 500, message: '评论长度在 2 到 500 个字符', trigger: 'blur' }
          ]"
        >
          <el-input
            v-model="commentForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入你的评论..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCommentDialog = false">取消</el-button>
          <el-button type="primary" @click="submitComment">
            发表评论
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Calendar, Trophy, Star, Medal } from '@element-plus/icons-vue'
import { marked } from 'marked'
import DOMPurify from 'dompurify'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'

dayjs.extend(relativeTime)

// 统计数据
const stats = ref({
  streak: 0,
  totalPoints: 0,
  completionRate: 0
})

// 当前挑战
const currentChallenge = ref<any>(null)
const loading = ref(true)
const isCompleted = ref(false)
const userAnswer = ref('')

// 评论相关
const comments = ref<any[]>([])
const showCommentDialog = ref(false)
const commentForm = ref({
  content: ''
})
const commentFormRef = ref()

// 计算属性
const renderedDescription = computed(() => {
  if (!currentChallenge.value?.description) return ''
  const rawHtml = marked(currentChallenge.value.description)
  return DOMPurify.sanitize(rawHtml)
})

// 方法
const getDifficultyType = (difficulty: string) => {
  const types: Record<string, string> = {
    '简��': 'success',
    '中等': 'warning',
    '困难': 'danger'
  }
  return types[difficulty] || 'info'
}

const formatTime = (time: string) => {
  return dayjs(time).fromNow()
}

const fetchDailyChallenge = async () => {
  try {
    loading.value = true
    // TODO: 调用API获取每日挑战数据
    // 模拟数据
    currentChallenge.value = {
      id: 1,
      title: 'Web安全基础 - XSS攻击检测',
      difficulty: '中等',
      points: 100,
      description: `
## 任务描述

在给定的输入框中，尝试检测可能存在的XSS漏洞。

### 要求
1. 分析以下代码片段中可能存在的XSS漏洞
2. 提供至少3种不同的XSS payload
3. 说明如何修复这些漏洞

\`\`\`html
<div class="user-input">
  <h2>Welcome, <%= username %>!</h2>
  <div class="message"><%= message %></div>
</div>
\`\`\`
      `,
      hints: [
        '考虑输入验证和转义',
        '注意HTML属性中的注入点',
        '检查JavaScript上下文中的数据处理'
      ]
    }
    
    // 获取统计数据
    stats.value = {
      streak: 7,
      totalPoints: 850,
      completionRate: 85
    }
    
    // 获取评论数据
    comments.value = [
      {
        id: 1,
        username: '安全专家',
        userAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        content: '这个挑战很有意思，帮助我更好地理解了XSS漏洞的原理。',
        createTime: '2023-12-15T10:30:00'
      }
    ]
  } catch (error) {
    ElMessage.error('获取每日挑战失败')
    console.error('获取每日挑战失败:', error)
  } finally {
    loading.value = false
  }
}

const submitChallenge = async () => {
  if (!userAnswer.value.trim()) {
    ElMessage.warning('请输入你的答案')
    return
  }
  
  try {
    // TODO: 调用API提交答案
    ElMessage.success('提交成功！')
    isCompleted.value = true
  } catch (error) {
    ElMessage.error('提交失败')
    console.error('提交答案失败:', error)
  }
}

const submitComment = async () => {
  if (!commentForm.value.content.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  try {
    // TODO: 调用API提交评论
    comments.value.unshift({
      id: Date.now(),
      username: '当前用户',
      userAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
      content: commentForm.value.content,
      createTime: new Date().toISOString()
    })
    
    showCommentDialog.value = false
    commentForm.value.content = ''
    ElMessage.success('评论发表成功')
  } catch (error) {
    ElMessage.error('评论��表失败')
    console.error('提交评论失败:', error)
  }
}

onMounted(() => {
  fetchDailyChallenge()
})
</script>

<style lang="scss" scoped>
.daily-challenge {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;

  .page-header {
    margin-bottom: 24px;

    .title {
      font-size: 28px;
      margin-bottom: 24px;
      color: var(--text-primary);
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;

      .stat-card {
        background: var(--bg-dark);
        border: 1px solid rgba(255, 127, 80, 0.1);

        .card-header {
          display: flex;
          align-items: center;
          gap: 8px;
          color: var(--text-secondary);
          font-size: 14px;

          .el-icon {
            font-size: 16px;
            color: var(--accent);
          }
        }

        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: var(--text-primary);
          text-align: center;
          padding: 12px 0;
        }
      }
    }
  }

  .challenge-content {
    display: grid;
    gap: 24px;

    .challenge-card {
      background: var(--bg-dark);
      border: 1px solid rgba(255, 127, 80, 0.1);

      .challenge-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 16px;

        .challenge-title {
          display: flex;
          align-items: center;
          gap: 12px;

          h2 {
            margin: 0;
            font-size: 20px;
            color: var(--text-primary);
          }
        }

        .challenge-meta {
          display: flex;
          align-items: center;
          gap: 16px;

          .points {
            display: flex;
            align-items: center;
            gap: 4px;
            color: var(--text-secondary);
            font-size: 14px;

            .el-icon {
              color: #f7ba2a;
            }
          }
        }
      }

      .challenge-description {
        margin: 24px 0;

        .markdown-content {
          color: var(--text-primary);
          line-height: 1.6;

          :deep(h2) {
            font-size: 20px;
            margin: 24px 0 16px;
            color: var(--accent);
          }

          :deep(h3) {
            font-size: 18px;
            margin: 20px 0 12px;
          }

          :deep(p) {
            margin: 12px 0;
          }

          :deep(ul) {
            padding-left: 24px;
            margin: 12px 0;
          }

          :deep(code) {
            background: rgba(255, 127, 80, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
          }

          :deep(pre) {
            background: rgba(0, 0, 0, 0.2);
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;

            code {
              background: none;
              padding: 0;
            }
          }
        }
      }

      .challenge-input {
        margin: 24px 0;
      }

      .challenge-hints {
        margin-top: 24px;

        h3 {
          font-size: 18px;
          margin-bottom: 16px;
          color: var(--text-primary);
        }
      }
    }

    .discussion-card {
      background: var(--bg-dark);
      border: 1px solid rgba(255, 127, 80, 0.1);

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        h3 {
          margin: 0;
          font-size: 18px;
          color: var(--text-primary);
        }
      }

      .comments-list {
        .no-comments {
          text-align: center;
          color: var(--text-secondary);
          padding: 24px;
        }

        .comment-item {
          padding: 16px 0;
          border-bottom: 1px solid rgba(255, 127, 80, 0.1);

          &:last-child {
            border-bottom: none;
          }

          .comment-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;

            .user-info {
              display: flex;
              align-items: center;
              gap: 8px;

              .username {
                font-weight: 500;
                color: var(--text-primary);
              }
            }

            .comment-time {
              font-size: 12px;
              color: var(--text-secondary);
            }
          }

          .comment-content {
            color: var(--text-primary);
            line-height: 1.6;
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .daily-challenge {
    padding: 16px;

    .challenge-header {
      flex-direction: column;
      align-items: flex-start;

      .challenge-meta {
        width: 100%;
        justify-content: space-between;
      }
    }
  }
}
</style> 