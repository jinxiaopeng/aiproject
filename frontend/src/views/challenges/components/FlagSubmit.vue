<template>
  <div class="flag-submit">
    <el-form @submit.prevent="handleSubmit">
      <el-form-item>
        <el-input
          v-model="flag"
          placeholder="输入找到的flag"
          class="flag-input"
        >
          <template #append>
            <el-button type="primary" @click="handleSubmit" :loading="loading">
              提交
            </el-button>
          </template>
        </el-input>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { submitFlag } from '@/api/challenge'

const props = defineProps<{
  challengeId: number
}>()

const emit = defineEmits<{
  (e: 'success'): void
}>()

const flag = ref('')
const loading = ref(false)

const handleSubmit = async () => {
  if (!flag.value) {
    ElMessage.warning('请输入flag')
    return
  }

  try {
    loading.value = true
    const { correct, message } = await submitFlag(props.challengeId, flag.value)
    
    if (correct) {
      ElMessage.success(message)
      emit('success')
      flag.value = ''
    } else {
      ElMessage.error(message)
    }
  } catch (error) {
    ElMessage.error('提交失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.flag-submit {
  margin-top: 16px;
  padding: 16px;
  background: rgba(30, 35, 40, 0.95);
  border: 1px solid rgba(65, 184, 131, 0.1);
  border-radius: 4px;
}

.flag-input :deep(.el-input__wrapper) {
  background: #1e1e1e;
}

.flag-input :deep(.el-input-group__append) {
  background: #1e1e1e;
  border-color: rgba(65, 184, 131, 0.1);
}
</style> 