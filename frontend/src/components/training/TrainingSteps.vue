<!-- 训练步骤组件 -->
<template>
  <div class="training-steps">
    <!-- 步骤导航 -->
    <el-steps :active="currentStep" finish-status="success">
      <el-step 
        v-for="(step, index) in steps" 
        :key="index"
        :title="step.title"
        :description="step.description"
      >
        <template #icon>
          <el-icon v-if="isStepCompleted(index)">
            <Check />
          </el-icon>
        </template>
      </el-step>
    </el-steps>

    <!-- 当前步骤内容 -->
    <div v-if="currentStepData" class="step-content">
      <el-card>
        <template #header>
          <div class="step-header">
            <h3>{{ currentStepData.title }}</h3>
            <el-tag 
              :type="isCurrentStepCompleted ? 'success' : ''"
              effect="dark"
            >
              {{ isCurrentStepCompleted ? '已完成' : '进行中' }}
            </el-tag>
          </div>
        </template>

        <!-- 步骤说明 -->
        <div class="step-description">
          {{ currentStepData.description }}
        </div>

        <!-- 提示信息 -->
        <div v-if="currentStepData.tips" class="step-tips">
          <el-collapse>
            <el-collapse-item title="提示信息">
              <ul>
                <li v-for="(tip, index) in currentStepData.tips" :key="index">
                  {{ tip }}
                </li>
              </ul>
            </el-collapse-item>
          </el-collapse>
        </div>

        <!-- 任务列表 -->
        <div v-if="currentStepData.tasks" class="step-tasks">
          <h4>任务清单</h4>
          <el-checkbox-group v-model="completedTasks">
            <el-checkbox 
              v-for="(task, index) in currentStepData.tasks" 
              :key="index"
              :label="index"
            >
              {{ task }}
            </el-checkbox>
          </el-checkbox-group>
        </div>

        <!-- 步骤操作 -->
        <div class="step-actions">
          <el-button 
            v-if="currentStep > 0" 
            @click="prevStep"
          >
            上一步
          </el-button>
          
          <el-button 
            type="primary" 
            @click="nextStep"
            :disabled="!canProceed"
          >
            {{ isLastStep ? '完成训练' : '下一步' }}
          </el-button>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import type { TrainingStep } from '@/types/challenge'
import { getTrainingProgress, updateTrainingProgress } from '@/api/training'

const props = defineProps<{
  challengeId: number
  steps: TrainingStep[]
}>()

const emit = defineEmits<{
  (e: 'complete'): void
}>()

// 状态
const currentStep = ref(0)
const completedTasks = ref<number[]>([])
const stepProgress = ref<boolean[][]>([])

// 计算属性
const currentStepData = computed(() => props.steps[currentStep.value])
const isLastStep = computed(() => currentStep.value === props.steps.length - 1)
const isCurrentStepCompleted = computed(() => 
  stepProgress.value[currentStep.value]?.every(Boolean)
)
const canProceed = computed(() => 
  currentStepData.value.tasks 
    ? completedTasks.value.length === currentStepData.value.tasks.length
    : true
)

// 检查步骤是否完成
const isStepCompleted = (step: number) => 
  stepProgress.value[step]?.every(Boolean)

// 加载训练进度
const loadProgress = async () => {
  try {
    const { data } = await getTrainingProgress(props.challengeId)
    currentStep.value = data.current_step
    stepProgress.value = data.completed_tasks
    if (data.completed_at) {
      emit('complete')
    }
  } catch (error) {
    ElMessage.error('加载训练进度失败')
  }
}

// 保存进度
const saveProgress = async () => {
  try {
    await updateTrainingProgress(
      props.challengeId,
      currentStep.value,
      stepProgress.value[currentStep.value]
    )
  } catch (error) {
    ElMessage.error('保存进度失败')
  }
}

// 上一步
const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
    completedTasks.value = []
  }
}

// 下一步
const nextStep = async () => {
  if (!canProceed.value) return
  
  // 更新当前步骤进度
  stepProgress.value[currentStep.value] = completedTasks.value.map(() => true)
  await saveProgress()
  
  if (isLastStep.value) {
    emit('complete')
  } else {
    currentStep.value++
    completedTasks.value = []
  }
}

// 监听任务完成状态
watch(completedTasks, (newTasks) => {
  stepProgress.value[currentStep.value] = props.steps[currentStep.value].tasks?.map(
    (_, index) => newTasks.includes(index)
  ) || []
})

// 初始化
onMounted(loadProgress)
</script>

<style scoped>
.training-steps {
  padding: 20px;
}

.step-content {
  margin-top: 30px;
}

.step-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.step-header h3 {
  margin: 0;
}

.step-description {
  margin: 20px 0;
  line-height: 1.6;
}

.step-tips {
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.step-tasks {
  margin: 20px 0;
}

.step-tasks h4 {
  margin-bottom: 15px;
}

.step-actions {
  margin-top: 30px;
  text-align: right;
}

.el-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style> 