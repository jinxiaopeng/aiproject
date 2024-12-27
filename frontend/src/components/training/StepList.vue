<!-- 训练步骤列表组件 -->
<template>
  <div class="step-list">
    <el-steps :active="activeStep" finish-status="success" :process-status="trainingStatus">
      <el-step 
        v-for="step in steps" 
        :key="step.id" 
        :title="step.name"
        :description="step.description"
      >
        <template #icon>
          <el-icon v-if="step.completed">
            <Check />
          </el-icon>
        </template>
      </el-step>
    </el-steps>

    <!-- 当前步骤详情 -->
    <div class="step-detail" v-if="currentStep">
      <h3>{{ currentStep.name }}</h3>
      <p>{{ currentStep.description }}</p>
      
      <!-- 步骤操作区 -->
      <div class="step-actions">
        <el-button 
          type="primary" 
          @click="submitStep"
          :loading="submitting"
          :disabled="!canSubmit"
        >
          完成步骤
        </el-button>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Check } from '@element-plus/icons-vue'
import type { TrainingStep } from '@/api/training'
import { submitTrainingStep } from '@/api/training'

const props = defineProps<{
  trainingId: string
  steps: TrainingStep[]
  activeStep: number
}>()

const emit = defineEmits<{
  (e: 'step-completed', step: TrainingStep): void
}>()

const submitting = ref(false)

// 当前步骤
const currentStep = computed(() => 
  props.steps[props.activeStep - 1]
)

// 是否可以提交
const canSubmit = computed(() => 
  currentStep.value && !currentStep.value.completed
)

// 训练状态
const trainingStatus = computed(() => 
  submitting.value ? 'wait' : 'process'
)

// 提交步骤
async function submitStep() {
  if (!currentStep.value || submitting.value) return
  
  submitting.value = true
  try {
    const result = await submitTrainingStep(
      props.trainingId,
      currentStep.value.step_number,
      { completed: true }
    )
    ElMessage.success('步骤完成')
    emit('step-completed', currentStep.value)
  } catch (error) {
    ElMessage.error('提交失败，请重试')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.step-list {
  padding: 20px;
}

.step-detail {
  margin-top: 30px;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 4px;
}

.step-actions {
  margin-top: 20px;
  text-align: right;
}
</style>