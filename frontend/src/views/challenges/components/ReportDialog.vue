<template>
  <el-dialog
    v-model="dialogVisible"
    title="提交实验报告"
    width="60%"
    :before-close="handleClose"
  >
    <el-form
      ref="reportForm"
      :model="form"
      :rules="rules"
      label-width="100px"
    >
      <el-form-item label="实验过程" prop="process">
        <el-input
          v-model="form.process"
          type="textarea"
          :rows="6"
          placeholder="请详细描述你的实验过程，包括使用的工具、方法和步骤"
        />
      </el-form-item>

      <el-form-item label="实验结果" prop="result">
        <el-input
          v-model="form.result"
          type="textarea"
          :rows="4"
          placeholder="请描述你获得的实验结果，包括发现的漏洞、获取的信息等"
        />
      </el-form-item>

      <el-form-item label="实验总结" prop="summary">
        <el-input
          v-model="form.summary"
          type="textarea"
          :rows="4"
          placeholder="请总结本次实验的收获和体会，以及可能的改进建议"
        />
      </el-form-item>

      <el-form-item label="截图附件" prop="screenshots">
        <el-upload
          v-model:file-list="fileList"
          action="/api/upload"
          list-type="picture-card"
          :on-preview="handlePictureCardPreview"
          :on-remove="handleRemove"
          :before-upload="beforeUpload"
        >
          <el-icon><Plus /></el-icon>
        </el-upload>

        <el-dialog v-model="dialogImageVisible">
          <img w-full :src="dialogImageUrl" alt="Preview Image" />
        </el-dialog>
      </el-form-item>
    </el-form>

    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          提交报告
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules, UploadProps, UploadUserFile } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { submitReport } from '@/api/challenge'

const props = defineProps<{
  challengeId: number
  visible: boolean
}>()

const emit = defineEmits(['update:visible', 'submitted'])

const dialogVisible = computed({
  get: () => props.visible,
  set: (value) => emit('update:visible', value)
})

const reportForm = ref<FormInstance>()
const submitting = ref(false)
const fileList = ref<UploadUserFile[]>([])
const dialogImageUrl = ref('')
const dialogImageVisible = ref(false)

const form = ref({
  process: '',
  result: '',
  summary: '',
  screenshots: [] as string[]
})

const rules: FormRules = {
  process: [
    { required: true, message: '请描述实验过程', trigger: 'blur' },
    { min: 100, message: '描述不能少于100字', trigger: 'blur' }
  ],
  result: [
    { required: true, message: '请描述实验结果', trigger: 'blur' },
    { min: 50, message: '描述不能少于50字', trigger: 'blur' }
  ],
  summary: [
    { required: true, message: '请总结实验心得', trigger: 'blur' },
    { min: 50, message: '总结不能少于50字', trigger: 'blur' }
  ]
}

// 图片上传相关
const handleRemove: UploadProps['onRemove'] = (uploadFile) => {
  const index = form.value.screenshots.indexOf(uploadFile.url as string)
  if (index > -1) {
    form.value.screenshots.splice(index, 1)
  }
}

const handlePictureCardPreview: UploadProps['onPreview'] = (uploadFile) => {
  dialogImageUrl.value = uploadFile.url!
  dialogImageVisible.value = true
}

const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB!')
    return false
  }
  return true
}

// 关闭对话框
const handleClose = () => {
  dialogVisible.value = false
  reportForm.value?.resetFields()
  fileList.value = []
}

// 提交报告
const handleSubmit = async () => {
  if (!reportForm.value) return
  
  await reportForm.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        submitting.value = true
        
        await submitReport({
          challengeId: props.challengeId,
          ...form.value
        })
        
        ElMessage.success('报告提交成功')
        emit('submitted')
        handleClose()
      } catch (error) {
        ElMessage.error('提交失败，请重试')
      } finally {
        submitting.value = false
      }
    }
  })
}
</script>

<style scoped>
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

:deep(.el-upload--picture-card) {
  --el-upload-picture-card-size: 100px;
}

:deep(.el-dialog__body) {
  padding: 20px;
}
</style> 