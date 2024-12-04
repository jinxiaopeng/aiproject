<template>
  <div class="forgot-password-container">
    <div class="forgot-password-box">
      <div class="forgot-password-header">
        <img src="@/assets/security.svg" alt="Logo" class="logo">
        <h2>重置密码</h2>
      </div>
      
      <el-form
        ref="formRef"
        :model="resetForm"
        :rules="rules"
        class="reset-form"
        size="large"
      >
        <el-form-item prop="email">
          <el-input
            v-model="resetForm.email"
            placeholder="请输入注册邮箱"
            :prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item v-if="step === 2" prop="code">
          <el-input
            v-model="resetForm.code"
            placeholder="请输入验证码"
            :prefix-icon="Key"
            maxlength="6"
          >
            <template #append>
              <el-button
                :disabled="countdown > 0"
                @click="sendCode"
              >
                {{ countdown > 0 ? `${countdown}s` : '获取验证码' }}
              </el-button>
            </template>
          </el-input>
        </el-form-item>
        
        <el-form-item v-if="step === 3" prop="password">
          <el-input
            v-model="resetForm.password"
            type="password"
            placeholder="请输入新密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item v-if="step === 3" prop="confirmPassword">
          <el-input
            v-model="resetForm.confirmPassword"
            type="password"
            placeholder="请确认新密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            class="submit-button"
            :loading="loading"
            @click="handleSubmit"
          >
            {{ submitButtonText }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="back-to-login">
        <router-link to="/login">返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const step = ref(1)
const countdown = ref(0)

const resetForm = ref({
  email: '',
  code: '',
  password: '',
  confirmPassword: ''
})

const validatePass = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (resetForm.value.confirmPassword !== '') {
      if (formRef.value) {
        formRef.value.validateField('confirmPassword', () => null)
      }
    }
    callback()
  }
}

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== resetForm.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const rules: FormRules = {
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  code: [
    { required: true, message: '请输入验证码', trigger: 'blur' },
    { len: 6, message: '验证码长度为6位', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePass, trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

const submitButtonText = computed(() => {
  switch (step.value) {
    case 1:
      return '下一步'
    case 2:
      return '验证'
    case 3:
      return '重置密码'
    default:
      return '提交'
  }
})

const startCountdown = () => {
  countdown.value = 60
  const timer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(timer)
    }
  }, 1000)
}

const sendCode = async () => {
  try {
    // TODO: 调用发送验证码 API
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('验证码已发送')
    startCountdown()
  } catch (error) {
    console.error('Failed to send code:', error)
    ElMessage.error('发送验证码失败，请重试')
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        loading.value = true
        
        switch (step.value) {
          case 1:
            // 验证邮箱是否存在
            // TODO: 调用验证邮箱 API
            await new Promise(resolve => setTimeout(resolve, 1000))
            step.value = 2
            await sendCode()
            break
            
          case 2:
            // 验证验证码
            // TODO: 调用验证码验证 API
            await new Promise(resolve => setTimeout(resolve, 1000))
            step.value = 3
            break
            
          case 3:
            // 重置密码
            // TODO: 调用重置密码 API
            await new Promise(resolve => setTimeout(resolve, 1000))
            ElMessage.success('密码重置成功，请重新登录')
            router.push('/login')
            break
        }
      } catch (error) {
        console.error('Reset password failed:', error)
        ElMessage.error('操作失败，请重试')
      } finally {
        loading.value = false
      }
    }
  })
}
</script>

<style scoped>
.forgot-password-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #1890ff 0%, #36cfc9 100%);
}

.forgot-password-box {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.forgot-password-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
}

.forgot-password-header h2 {
  font-size: 24px;
  color: var(--text-color);
  margin: 0;
}

.reset-form {
  margin-bottom: 24px;
}

.submit-button {
  width: 100%;
}

.back-to-login {
  text-align: center;
  font-size: 14px;
}

.back-to-login a {
  color: var(--primary-color);
}

@media (max-width: 768px) {
  .forgot-password-box {
    margin: 20px;
    padding: 30px;
  }
}
</style> 