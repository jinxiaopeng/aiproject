<template>
  <div class="add-challenge-container">
    <el-card class="form-card">
      <template #header>
        <div class="card-header">
          <h2>添加题库</h2>
          <el-button 
            type="text" 
            class="close-button"
            @click="handleClose"
          >
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="120px"
        class="challenge-form"
      >
        <el-form-item label="题目名称" prop="title">
          <el-input v-model="form.title" placeholder="请输入题目名称" />
        </el-form-item>

        <el-form-item label="题目描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="4"
            placeholder="请输入题目描述"
          />
        </el-form-item>

        <el-form-item label="难度等级" prop="difficulty">
          <el-select v-model="form.difficulty" placeholder="请选择难度等级">
            <el-option label="入门" value="beginner" />
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
            <el-option label="专家" value="expert" />
          </el-select>
        </el-form-item>

        <el-form-item label="分值" prop="points">
          <el-input-number v-model="form.points" :min="1" :max="1000" />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类">
            <el-option label="Web安全" value="web" />
            <el-option label="系统安全" value="system" />
            <el-option label="密码学" value="crypto" />
            <el-option label="逆向工程" value="reverse" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>

        <el-form-item label="标签" prop="tags">
          <el-select
            v-model="form.tags"
            multiple
            filterable
            allow-create
            placeholder="请选择或输入标签"
          >
            <el-option
              v-for="tag in commonTags"
              :key="tag"
              :label="tag"
              :value="tag"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="环境配置">
          <el-form-item label="环境类型" prop="environment.type">
            <el-select v-model="form.environment.type" placeholder="请选择环境类型">
              <el-option label="Docker" value="Docker" />
              <el-option label="Kubernetes" value="Kubernetes" />
              <el-option label="虚拟机" value="VM" />
            </el-select>
          </el-form-item>
          <el-form-item label="访问地址" prop="environment.url">
            <el-input 
              v-model="form.environment.url" 
              placeholder="环境访问地址"
              :value="generateAccessUrl(form.environment.port)"
              disabled
            />
          </el-form-item>
          <el-form-item label="端口" prop="environment.port">
            <el-input-number 
              v-model="form.environment.port" 
              :min="1" 
              :max="65535"
              @change="updateAccessUrl" 
            />
          </el-form-item>
          
          <el-form-item label="题目文件">
            <el-upload
              class="challenge-upload"
              action="/api/challenges/upload"
              :headers="{
                'Accept': 'application/json',
              }"
              name="files"
              :multiple="true"
              :on-preview="handlePreview"
              :on-remove="handleRemove"
              :before-remove="beforeRemove"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :before-upload="beforeUpload"
              :limit="5"
              :on-exceed="handleExceed"
              :file-list="fileList"
            >
              <el-button type="primary">上传题目文件</el-button>
              <template #tip>
                <div class="el-upload__tip">
                  可上传 Dockerfile、docker-compose.yml、源代码等文件，单个文件不超过10MB
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useStore } from '../../stores/challenge'
import { 
  Connection,
  Monitor,
  Setting,
  VideoPlay,
  Close,
  Check
} from '@element-plus/icons-vue'

// 定义表单数据类型
interface UploadFile {
  name: string
  size: number
  status?: string
  uid?: number
  url?: string
}

interface ChallengeForm {
  title: string
  description: string
  difficulty: 'beginner' | 'easy' | 'medium' | 'hard' | 'expert'
  points: number
  category: string
  tags: string[]
  environment: {
    type: string
    url: string
    port: number
  }
  status: 'not_started'
  completionRate: number
  files?: UploadFile[]
  challengeId?: string
}

const router = useRouter()
const store = useStore()
const formRef = ref<FormInstance>()

// 表单数据
const form = reactive<ChallengeForm>({
  title: '',
  description: '',
  difficulty: 'easy',  // 设置默认值
  points: 100,
  category: '',
  tags: [],
  environment: {
    type: '',
    url: '',
    port: 80
  },
  status: 'not_started',
  completionRate: 0
})

// 常用标签
const commonTags = [
  'SQL注入',
  'XSS',
  'CSRF',
  'RCE',
  '文件上传',
  '权限提升',
  '缓冲区溢出',
  '密码破解'
]

// 表单验证规则
const rules = reactive<FormRules>({
  title: [
    { required: true, message: '请输入题目名称', trigger: 'blur' },
    { min: 3, max: 50, message: '长度��� 3 到 50 个字符', trigger: 'blur' }
  ],
  description: [
    { required: true, message: '请输入题目描述', trigger: 'blur' },
    { min: 10, max: 500, message: '长度在 10 到 500 个字符', trigger: 'blur' }
  ],
  difficulty: [
    { required: true, message: '请选择难度等级', trigger: 'change' }
  ],
  points: [
    { required: true, message: '请输入分值', trigger: 'change' }
  ],
  category: [
    { required: true, message: '请选择分类', trigger: 'change' }
  ],
  'environment.type': [
    { required: true, message: '请选择环境类型', trigger: 'change' }
  ],
  'environment.port': [
    { required: true, message: '请设置端口号', trigger: 'change' }
  ]
})

// 文件上传相关方法
const handleRemove = (file: any, fileList: any[]) => {
  console.log(file, fileList)
}

const handlePreview = (file: any) => {
  console.log(file)
}

const handleExceed = (files: any[], fileList: any[]) => {
  ElMessage.warning(
    `当前限制选择 5 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`
  )
}

const beforeRemove = (file: any) => {
  return ElMessageBox.confirm(
    `确定移除 ${file.name}？`
  ).then(
    () => true,
    () => false
  )
}

const fileList = ref<UploadFile[]>([])

// 生成访问地址
const generateAccessUrl = (port: number) => {
  return `http://localhost:${port}`
}

// 更新访问地址
const updateAccessUrl = (port: number) => {
  form.environment.url = generateAccessUrl(port)
}

// 检测是否包含 Docker 相关文件
const checkDockerFiles = (files: any[]) => {
  const dockerFiles = files.some(file => 
    file.name.toLowerCase() === 'dockerfile' || 
    file.name.toLowerCase() === 'docker-compose.yml'
  )
  if (dockerFiles) {
    form.environment.type = 'Docker'
    // 如果是 Docker 文件，设置默认端口并更新访问地址
    if (!form.environment.port) {
      form.environment.port = 8080
      updateAccessUrl(8080)
    }
  }
}

// 修改文件上传成功处理函数
const handleUploadSuccess = (response: any, uploadFile: any, uploadFiles: any[]) => {
  console.log('Upload success:', response)
  form.files = response.files
  form.challengeId = response.challenge_id
  fileList.value = uploadFiles
  
  // 检查是否包含 Docker 文件并更新环境类型
  checkDockerFiles(uploadFiles)
  
  ElMessage.success('文件上传成功')
}

const handleUploadError = (error: any, uploadFile: any, uploadFiles: any[]) => {
  console.error('Upload error:', error)
  ElMessage.error('文件上传失败：' + (error.message || '未知错误'))
}

const beforeUpload = (file: File) => {
  // 检查文件大小
  const isLt10M = file.size / 1024 / 1024 < 10
  if (!isLt10M) {
    ElMessage.error('文件大小不能超过 10MB!')
    return false
  }
  return true
}

// 提交表单
const submitForm = async () => {
  if (!formRef.value) return
  
  // 检查是否上传了文件
  if (!form.files || form.files.length === 0) {
    ElMessage.warning('请上传题目相关文件')
    return
  }
  
  await formRef.value.validate((valid, fields) => {
    if (valid) {
      try {
        // 创建新的Challenge对象
        const newChallenge = {
          id: Date.now(),
          ...form,
          solvedCount: 0,
          totalAttempts: 0,
          files: form.files || [],
          challengeId: form.challengeId,
          environment: {
            ...form.environment,
            url: generateAccessUrl(form.environment.port)
          }
        }
        
        console.log('Submitting challenge:', newChallenge)
        
        // 添加到store
        store.addChallenge(newChallenge)
        
        // 显示成功动画和通知
        showSuccessEffect()
        
        // 2秒后返回列表页面
        setTimeout(() => {
          router.push('/challenge')
        }, 2000)
      } catch (err) {
        const error = err as Error
        console.error('Submit error:', error)
        ElMessage.error('添加题库失败：' + error.message)
      }
    } else {
      console.log('Validation failed:', fields)
      ElMessage.error('请填写所有必填字段')
    }
  })
}

// 显示成功效果
const showSuccessEffect = () => {
  // 显示大号成功通知
  ElNotification({
    title: '提交成功',
    message: '题目已成功添加到题库',
    type: 'success',
    duration: 3000,
    position: 'top-right',
    icon: Check,
    customClass: 'success-notification'
  })
  
  // 显示中央成功消息
  ElMessage({
    message: '题目添加成功！即将返回题目列表...',
    type: 'success',
    duration: 2000,
    showClose: true,
    center: true,
    customClass: 'success-message'
  })
}

// 重置表单
const resetForm = () => {
  if (!formRef.value) return
  formRef.value.resetFields()
}

// 处理关闭
const handleClose = () => {
  ElMessageBox.confirm(
    '确定要关闭吗？未保存的内容将会丢失',
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    router.push('/challenge')
  }).catch(() => {
    // 用户取消关闭
  })
}
</script>

<style scoped>
.add-challenge-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

.form-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.challenge-form {
  margin-top: 20px;
}

:deep(.el-form-item__content) {
  flex-wrap: wrap;
}

.challenge-upload {
  margin-top: 16px;
}

.el-upload__tip {
  color: #666;
  font-size: 12px;
  margin-top: 8px;
}

.close-button {
  padding: 8px;
  font-size: 20px;
}

.close-button:hover {
  color: var(--el-color-primary);
}

:deep(.success-notification) {
  background-color: #f0f9eb;
  border-color: #67c23a;
  padding: 20px;
  
  .el-notification__title {
    font-size: 18px;
    color: #67c23a;
  }
  
  .el-notification__content {
    font-size: 16px;
  }
  
  .el-icon {
    font-size: 24px;
    color: #67c23a;
  }
}

:deep(.success-message) {
  min-width: 300px;
  padding: 15px 20px;
  
  .el-message__content {
    font-size: 16px;
  }
}

@keyframes success-pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
  }
}

.success-animation {
  animation: success-pulse 0.5s ease-in-out;
}
</style> 