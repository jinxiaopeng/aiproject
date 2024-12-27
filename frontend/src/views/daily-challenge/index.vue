# 将原来的 DailyChallenge.vue 的内容复制到这里
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
import { ElMessage, ElMessageBox } from 'element-plus'
import { Calendar, Trophy, Star, Medal, Timer } from '@element-plus/icons-vue'
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
    '简单': 'success',
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

在这个挑战中，你需要找到并利用一个XSS漏洞。目标网站使用了不安全的模板渲染方式。

### 环境信息
- 目标URL: \`http://challenge-server.example/profile?name=test\`
- 后端框架: Express.js + EJS模板引擎

### 目标
1. 找到XSS注入点
2. 构造Payload获取cookie
3. 提交获取到的flag

### 提示
- 检查URL参数的处理方式
- 观察服务器的响应头
- Cookie中可能包含敏感信息

### 提交格式
请提交flag，格式为：flag{xxxxx}
      `,
      hints: [
        '尝试在URL参数中注入JavaScript代码',
        '使用BurpSuite观察响应头',
        'document.cookie可能会有帮助'
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
    ElMessage.warning('请输入flag')
    return
  }
  
  try {
    loading.value = true
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟API请求
    
    // 检查flag格式
    const flagRegex = /^flag{[a-zA-Z0-9_]+}$/
    const isValidFormat = flagRegex.test(userAnswer.value.trim())
    
    if (!isValidFormat) {
      ElMessage.error('flag格式不正确，请使用格式：flag{xxxxx}')
      return
    }
    
    // 模拟验证flag
    const correctFlag = 'flag{xss_detected_123}'
    const isCorrect = userAnswer.value.trim() === correctFlag
    
    // 生成反馈
    const result = isCorrect ? {
      correct: true,
      score: 100,
      feedback: [
        '恭喜你成功完成挑战！',
        '你已经掌握了：',
        '1. XSS漏洞的发现方法',
        '2. Payload的构造技巧',
        '3. 漏洞利用与信息获取'
      ],
      rewards: {
        points: 100,
        exp: 50,
        streak: 1
      }
    } : {
      correct: false,
      score: 0,
      feedback: [
        'flag不正确，请继续尝试：',
        '1. 检查注入点是否正确',
        '2. 确认payload是否成功执行',
        '3. 验证cookie信息是否完整获取'
      ],
      rewards: {
        points: 0,
        exp: 5,
        streak: 0
      }
    }

    // 显示结果对话框
    ElMessageBox.alert(
      `<div class="challenge-result">
        <div class="result-header ${result.correct ? 'success' : 'fail'}">
          <el-icon>${result.correct ? '<CircleCheckFilled />' : '<CircleCloseFilled />'}</el-icon>
          <h3>${result.correct ? '恭喜通过！' : '再接再厉！'}</h3>
        </div>
        <div class="result-feedback">
          ${result.feedback.map(item => `<p>${item}</p>`).join('')}
        </div>
        <div class="result-rewards">
          <div class="reward-item">
            <el-icon><Trophy /></el-icon>
            <span>积分 ${result.rewards.points > 0 ? '+' + result.rewards.points : 0}</span>
          </div>
          <div class="reward-item">
            <el-icon><Star /></el-icon>
            <span>经验 +${result.rewards.exp}</span>
          </div>
          ${result.correct ? `
          <div class="reward-item">
            <el-icon><Timer /></el-icon>
            <span>连续打卡 +${result.rewards.streak}</span>
          </div>` : ''}
        </div>
        ${!result.correct ? `
        <div class="result-actions">
          <el-button type="primary" @click="retryChallenge">重新尝试</el-button>
          <el-button @click="showHints">查看提示</el-button>
        </div>` : ''}
      </div>`,
      '挑战结果',
      {
        dangerouslyUseHTMLString: true,
        confirmButtonText: result.correct ? '太棒了' : '知道了',
        customClass: 'challenge-result-dialog',
        showClose: true
      }
    )

    // 只有答对时才更新状态
    if (result.correct) {
      isCompleted.value = true
      stats.value.totalPoints += result.rewards.points
      stats.value.streak += result.rewards.streak
      
      // 添加系统评论
      comments.value.unshift({
        id: Date.now(),
        username: '系统',
        userAvatar: 'https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png',
        content: `恭喜完成今日挑战！获得 ${result.rewards.points} 积分奖励`,
        createTime: new Date().toISOString()
      })
    }

  } catch (error) {
    ElMessage.error('提交失败')
    console.error('提交答案失败:', error)
  } finally {
    loading.value = false
  }
}

// 重试挑战
const retryChallenge = () => {
  userAnswer.value = ''
  ElMessageBox.close()
}

// 显示提示
const showHints = () => {
  ElMessageBox.close()
  // 自动展开提示折叠面板
  const hintCollapse = document.querySelector('.challenge-hints .el-collapse')
  if (hintCollapse) {
    // 这里需要通过Vue的方式来控制折叠面板的展开状态
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
    ElMessage.error('评论发表失败')
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
  background: var(--bg-light, #f5f7fa);
  min-height: 100vh;

  .page-header {
    margin-bottom: 24px;

    .title {
      font-size: 28px;
      margin-bottom: 24px;
      color: var(--text-primary, #2c3e50);
    }

    .stats {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 24px;

      .stat-card {
        background: var(--bg-white, #ffffff);
        border: 1px solid rgba(0, 0, 0, 0.1);
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);

        .card-header {
          display: flex;
          align-items: center;
          gap: 8px;
          color: var(--text-secondary, #606266);
          font-size: 14px;

          .el-icon {
            font-size: 16px;
            color: var(--accent, #409eff);
          }
        }

        .stat-value {
          font-size: 24px;
          font-weight: bold;
          color: var(--text-primary, #2c3e50);
          text-align: center;
          padding: 12px 0;
        }
      }
    }
  }

  .challenge-content {
    display: grid;
    gap: 24px;

    .challenge-card, .discussion-card {
      background: var(--bg-white, #ffffff);
      border: 1px solid rgba(0, 0, 0, 0.1);
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);

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
            color: var(--text-primary, #2c3e50);
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
            color: var(--text-secondary, #606266);
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
          color: var(--text-primary, #2c3e50);
          line-height: 1.6;

          :deep(h2) {
            font-size: 20px;
            margin: 24px 0 16px;
            color: var(--accent, #409eff);
          }

          :deep(h3) {
            font-size: 18px;
            margin: 20px 0 12px;
            color: var(--text-primary, #2c3e50);
          }

          :deep(p) {
            margin: 12px 0;
            color: var(--text-regular, #606266);
          }

          :deep(ul) {
            padding-left: 24px;
            margin: 12px 0;
            color: var(--text-regular, #606266);
          }

          :deep(code) {
            background: rgba(64, 158, 255, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            color: #409eff;
          }

          :deep(pre) {
            background: #f8f9fa;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;

            code {
              background: none;
              padding: 0;
              color: #2c3e50;
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
          color: var(--text-primary, #2c3e50);
        }
      }
    }

    .discussion-card {
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        h3 {
          margin: 0;
          font-size: 18px;
          color: var(--text-primary, #2c3e50);
        }
      }

      .comments-list {
        .no-comments {
          text-align: center;
          color: var(--text-secondary, #909399);
          padding: 24px;
        }

        .comment-item {
          padding: 16px 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.1);

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
                color: var(--text-primary, #2c3e50);
              }
            }

            .comment-time {
              font-size: 12px;
              color: var(--text-secondary, #909399);
            }
          }

          .comment-content {
            color: var(--text-regular, #606266);
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

:deep(.challenge-result-dialog) {
  .el-message-box__content {
    padding: 0;
  }
  
  .challenge-result {
    .result-header {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 20px;
      
      &.success {
        background: rgba(103, 194, 58, 0.1);
        color: #67c23a;
      }
      
      &.fail {
        background: rgba(245, 108, 108, 0.1);
        color: #f56c6c;
      }
      
      .el-icon {
        font-size: 24px;
      }
      
      h3 {
        margin: 0;
        font-size: 18px;
      }
    }
    
    .result-feedback {
      padding: 20px;
      border-bottom: 1px solid #ebeef5;
      
      p {
        margin: 8px 0;
        color: #606266;
        line-height: 1.6;
      }
    }
    
    .result-rewards {
      padding: 20px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 16px;
      
      .reward-item {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #409eff;
        
        .el-icon {
          font-size: 20px;
        }
      }
    }

    .result-actions {
      padding: 20px;
      display: flex;
      justify-content: center;
      gap: 16px;
      border-top: 1px solid #ebeef5;
    }
  }
}
</style> 