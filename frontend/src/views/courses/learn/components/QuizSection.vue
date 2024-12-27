<template>
  <div class="quiz-section">
    <div class="section-title">
      <span>课后测试</span>
      <el-tag v-if="completed" type="success" size="small">已完成</el-tag>
    </div>
    
    <div v-if="currentQuiz" class="quiz-content">
      <div class="quiz-question">{{ currentQuiz.question }}</div>
      
      <el-radio-group v-model="selectedAnswer" class="options-list">
        <el-radio 
          v-for="option in currentQuiz.options" 
          :key="option.value" 
          :label="option.value"
          :disabled="submitted"
        >
          {{ option.text }}
        </el-radio>
      </el-radio-group>

      <div class="quiz-actions">
        <el-button 
          type="primary" 
          @click="submitAnswer"
          :disabled="!selectedAnswer || submitted"
        >
          提交答案
        </el-button>
      </div>

      <div v-if="submitted" class="feedback" :class="{ correct: isCorrect }">
        <i :class="isCorrect ? 'el-icon-check' : 'el-icon-close'"></i>
        {{ feedbackMessage }}
      </div>
    </div>

    <div v-else class="no-quiz">
      <el-empty description="完成视频后解锁测试题" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface QuizOption {
  value: string
  text: string
}

interface Quiz {
  id: number
  chapterId: number
  question: string
  options: QuizOption[]
  correctAnswer: string
  explanation: string
}

const props = defineProps<{
  chapterId: number
  videoProgress: number
}>()

const selectedAnswer = ref('')
const submitted = ref(false)
const completed = ref(false)
const isCorrect = ref(false)

// 模拟测试题数据
const quizzes: Quiz[] = [
  {
    id: 1,
    chapterId: 1,
    question: '以下哪个不是Web安全的主要威胁？',
    options: [
      { value: 'A', text: 'SQL注入攻击' },
      { value: 'B', text: '跨站脚本攻击(XSS)' },
      { value: 'C', text: '系统重启' },
      { value: 'D', text: '跨站请求伪造(CSRF)' }
    ],
    correctAnswer: 'C',
    explanation: '系统重启是系统维护操作，不属于Web安全威胁。'
  },
  {
    id: 2,
    chapterId: 2,
    question: 'SQL注入攻击的主要目的是什么？',
    options: [
      { value: 'A', text: '获取数据库中的敏感信息' },
      { value: 'B', text: '使服务器崩溃' },
      { value: 'C', text: '修改网页内容' },
      { value: 'D', text: '窃取用户cookie' }
    ],
    correctAnswer: 'A',
    explanation: 'SQL注入攻击主要是通过构造特殊的SQL语句来获取或操作数据库中的数据。'
  }
]

const currentQuiz = computed(() => {
  return quizzes.find(quiz => quiz.chapterId === props.chapterId)
})

const feedbackMessage = computed(() => {
  if (!submitted.value) return ''
  if (isCorrect.value) {
    return '回答正确！' + currentQuiz.value?.explanation
  }
  return '回答错误，请重试。'
})

const submitAnswer = () => {
  if (!currentQuiz.value || !selectedAnswer.value) return
  
  submitted.value = true
  isCorrect.value = selectedAnswer.value === currentQuiz.value.correctAnswer
  
  if (isCorrect.value) {
    completed.value = true
  }
}

watch(() => props.chapterId, () => {
  selectedAnswer.value = ''
  submitted.value = false
  completed.value = false
})
</script>

<style lang="scss" scoped>
.quiz-section {
  padding: 16px;

  .section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 16px;
  }

  .quiz-content {
    .quiz-question {
      font-size: 14px;
      margin-bottom: 16px;
      color: var(--el-text-color-primary);
    }

    .options-list {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 20px;
    }

    .quiz-actions {
      margin-top: 16px;
      text-align: center;
    }

    .feedback {
      margin-top: 16px;
      padding: 12px;
      border-radius: 4px;
      background-color: var(--el-color-danger-light-9);
      color: var(--el-color-danger);

      &.correct {
        background-color: var(--el-color-success-light-9);
        color: var(--el-color-success);
      }
    }
  }

  .no-quiz {
    padding: 20px;
    text-align: center;
  }
}
</style> 