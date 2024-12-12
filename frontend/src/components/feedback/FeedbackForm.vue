<template>
  <div class="feedback-form">
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="80px"
      @submit.prevent="handleSubmit"
    >
      <el-form-item label="类型" prop="feedback_type">
        <el-select v-model="form.feedback_type" placeholder="请选择反馈类型">
          <el-option label="内容相关" value="CONTENT" />
          <el-option label="难度相关" value="DIFFICULTY" />
          <el-option label="建议" value="SUGGESTION" />
          <el-option label="问题反馈" value="BUG" />
          <el-option label="其他" value="OTHER" />
        </el-select>
      </el-form-item>

      <el-form-item label="内容" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="4"
          placeholder="请详细描述您的反馈内容"
        />
      </el-form-item>

      <el-form-item label="评分" prop="rating">
        <el-rate
          v-model="form.rating"
          show-score
          :max="5"
          :texts="['很差', '较差', '一般', '较好', '很好']"
        />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="feedbackStore.submitting">
          提交反馈
        </el-button>
        <el-button @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInstance, FormRules } from 'element-plus'
import { ElMessage } from 'element-plus'
import { useFeedbackStore } from '@/stores/feedback'
import { isEmpty } from '@/utils/validate'

const props = defineProps<{
  entityId: number
}>()

const emit = defineEmits<{
  (e: 'success'): void
  (e: 'cancel'): void
}>()

const feedbackStore = useFeedbackStore()
const formRef = ref<FormInstance>()

const form = ref({
  feedback_type: '',
  content: '',
  rating: 0
})

const rules: FormRules = {
  feedback_type: [
    { required: true, message: '请选择反馈类型', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入反馈内容', trigger: 'blur' },
    { min: 10, message: '反馈内容至少10个字符', trigger: 'blur' }
  ],
  rating: [
    { 
      validator: (rule, value, callback) => {
        if (isEmpty(value)) {
          callback(new Error('请选择评分'))
        } else {
          callback()
        }
      },
      trigger: 'change'
    }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    
    await feedbackStore.createFeedback({
      entity_id: props.entityId,
      feedback_type: form.value.feedback_type,
      content: form.value.content,
      rating: form.value.rating
    })
    
    ElMessage.success('反馈提交成功')
    emit('success')
    handleReset()
  } catch (error) {
    // 表单验证错误或API错误已在store中处理
  }
}

const handleReset = () => {
  if (formRef.value) {
    formRef.value.resetFields()
  }
  emit('cancel')
}
</script>

<style scoped>
.feedback-form {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}
</style> 