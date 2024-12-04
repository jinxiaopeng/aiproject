<template>
  <div class="quiz-player">
    <!-- 测验头部 -->
    <div class="quiz-header">
      <h2>{{ quiz.title }}</h2>
      <p class="quiz-description">{{ quiz.description }}</p>
      <el-progress
        :percentage="progress"
        :format="progressFormat"
        class="quiz-progress"
      />
    </div>

    <!-- 测验内容 -->
    <div class="quiz-content" v-if="!completed">
      <div class="question-card">
        <div class="question-header">
          <span class="question-number">
            问题 {{ currentIndex + 1 }}/{{ quiz.questions.length }}
          </span>
          <span class="question-type">
            {{ getQuestionType(currentQuestion.type) }}
          </span>
        </div>

        <div class="question-content">
          <h3>{{ currentQuestion.content }}</h3>
          
          <!-- 单选题 -->
          <template v-if="currentQuestion.type === 'single'">
            <el-radio-group v-model="currentAnswer">
              <el-radio
                v-for="(option, index) in currentQuestion.options"
                :key="index"
                :label="index"
                class="question-option"
              >
                {{ option }}
              </el-radio>
            </el-radio-group>
          </template>

          <!-- 多选题 -->
          <template v-else-if="currentQuestion.type === 'multiple'">
            <el-checkbox-group v-model="currentAnswer">
              <el-checkbox
                v-for="(option, index) in currentQuestion.options"
                :key="index"
                :label="index"
                class="question-option"
              >
                {{ option }}
              </el-checkbox>
            </el-checkbox-group>
          </template>

          <!-- 判断题 -->
          <template v-else-if="currentQuestion.type === 'boolean'">
            <el-radio-group v-model="currentAnswer">
              <el-radio :label="true" class="question-option">正确</el-radio>
              <el-radio :label="false" class="question-option">错误</el-radio>
            </el-radio-group>
          </template>

          <!-- 填空题 -->
          <template v-else-if="currentQuestion.type === 'fill'">
            <el-input
              v-model="currentAnswer"
              type="textarea"
              :rows="3"
              placeholder="请输入你的答案"
            />
          </template>
        </div>

        <!-- 导航按钮 -->
        <div class="question-actions">
          <el-button
            v-if="currentIndex > 0"
            @click="previousQuestion"
          >
            上一题
          </el-button>
          <el-button
            type="primary"
            @click="nextQuestion"
          >
            {{ isLastQuestion ? '提交' : '下一题' }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 测验结果 -->
    <div v-else class="quiz-result">
      <div class="result-card">
        <div class="result-header">
          <el-icon :size="48" :class="scoreClass">
            <component :is="scoreIcon" />
          </el-icon>
          <h2>测验完成</h2>
          <div class="score">得分：{{ score }}分</div>
        </div>

        <el-divider />

        <div class="result-stats">
          <div class="stat-item">
            <div class="stat-value">{{ correctCount }}</div>
            <div class="stat-label">答对题数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ quiz.questions.length }}</div>
            <div class="stat-label">总题数</div>
          </div>
          <div class="stat-item">
            <div class="stat-value">{{ accuracy }}%</div>
            <div class="stat-label">正确率</div>
          </div>
        </div>

        <div class="result-actions">
          <el-button type="primary" @click="reviewQuiz">
            查看解析
          </el-button>
          <el-button @click="retryQuiz">
            重新测试
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import {
  CircleCheck,
  CircleClose,
  Warning
} from '@element-plus/icons-vue'

// 类型定义
interface Question {
  id: number
  type: 'single' | 'multiple' | 'boolean' | 'fill'
  content: string
  options?: string[]
  answer: any
  explanation?: string
}

interface Quiz {
  id: number
  title: string
  description: string
  questions: Question[]
  passingScore: number
}

// Props
const props = defineProps<{
  quizData: string
}>()

// Emits
const emit = defineEmits<{
  (e: 'complete', score: number): void
}>()

// 解析测验数据
const quiz = ref<Quiz>(JSON.parse(props.quizData))

// 状态
const currentIndex = ref(0)
const currentAnswer = ref<any>(null)
const answers = ref<any[]>([])
const completed = ref(false)
const score = ref(0)

// 计算属性
const currentQuestion = computed(() => quiz.value.questions[currentIndex.value])

const isLastQuestion = computed(() => {
  return currentIndex.value === quiz.value.questions.length - 1
})

const progress = computed(() => {
  return ((currentIndex.value + 1) / quiz.value.questions.length) * 100
})

const correctCount = computed(() => {
  return answers.value.filter((answer, index) => {
    const question = quiz.value.questions[index]
    return isAnswerCorrect(answer, question.answer)
  }).length
})

const accuracy = computed(() => {
  return Math.round((correctCount.value / quiz.value.questions.length) * 100)
})

const scoreClass = computed(() => {
  if (score.value >= quiz.value.passingScore) {
    return 'success'
  }
  if (score.value >= quiz.value.passingScore * 0.6) {
    return 'warning'
  }
  return 'danger'
})

const scoreIcon = computed(() => {
  if (score.value >= quiz.value.passingScore) {
    return CircleCheck
  }
  if (score.value >= quiz.value.passingScore * 0.6) {
    return Warning
  }
  return CircleClose
})

// 方法
const progressFormat = (percentage: number) => {
  return `${currentIndex.value + 1}/${quiz.value.questions.length}`
}

const getQuestionType = (type: string) => {
  const types = {
    single: '单选题',
    multiple: '多选题',
    boolean: '判断题',
    fill: '填空题'
  }
  return types[type as keyof typeof types] || type
}

const isAnswerCorrect = (userAnswer: any, correctAnswer: any) => {
  if (Array.isArray(userAnswer) && Array.isArray(correctAnswer)) {
    return (
      userAnswer.length === correctAnswer.length &&
      userAnswer.every(value => correctAnswer.includes(value))
    )
  }
  return userAnswer === correctAnswer
}

const previousQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
    currentAnswer.value = answers.value[currentIndex.value]
  }
}

const nextQuestion = () => {
  // 保存当前答案
  answers.value[currentIndex.value] = currentAnswer.value

  if (isLastQuestion.value) {
    completeQuiz()
  } else {
    currentIndex.value++
    currentAnswer.value = answers.value[currentIndex.value] || null
  }
}

const calculateScore = () => {
  const totalQuestions = quiz.value.questions.length
  const correctAnswers = correctCount.value
  return Math.round((correctAnswers / totalQuestions) * 100)
}

const completeQuiz = () => {
  score.value = calculateScore()
  completed.value = true
  emit('complete', score.value)
}

const reviewQuiz = () => {
  // TODO: 实现答案解析查看功能
}

const retryQuiz = () => {
  currentIndex.value = 0
  currentAnswer.value = null
  answers.value = []
  completed.value = false
  score.value = 0
}
</script>

<style scoped>
.quiz-player {
  max-width: 800px;
  margin: 0 auto;
  padding: 24px;
}

.quiz-header {
  text-align: center;
  margin-bottom: 32px;
}

.quiz-header h2 {
  margin: 0 0 16px;
  font-size: 24px;
}

.quiz-description {
  color: var(--el-text-color-secondary);
  margin-bottom: 24px;
}

.quiz-progress {
  margin-top: 16px;
}

.question-card {
  background-color: var(--el-bg-color);
  border-radius: 8px;
  padding: 24px;
  box-shadow: var(--el-box-shadow-light);
}

.question-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.question-number {
  font-size: 16px;
  font-weight: 500;
}

.question-type {
  color: var(--el-text-color-secondary);
}

.question-content {
  margin-bottom: 32px;
}

.question-content h3 {
  margin: 0 0 24px;
  font-size: 18px;
  line-height: 1.6;
}

.question-option {
  display: block;
  margin-bottom: 16px;
}

.question-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.result-card {
  background-color: var(--el-bg-color);
  border-radius: 8px;
  padding: 32px;
  text-align: center;
  box-shadow: var(--el-box-shadow-light);
}

.result-header {
  margin-bottom: 24px;
}

.result-header h2 {
  margin: 16px 0;
  font-size: 24px;
}

.score {
  font-size: 20px;
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.result-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin: 32px 0;
}

.stat-item {
  text-align: center;
}

.stat-value {
  font-size: 24px;
  font-weight: 500;
  color: var(--el-text-color-primary);
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: var(--el-text-color-secondary);
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-top: 32px;
}

.success {
  color: var(--el-color-success);
}

.warning {
  color: var(--el-color-warning);
}

.danger {
  color: var(--el-color-danger);
}
</style> 