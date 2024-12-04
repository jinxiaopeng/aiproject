<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box">
        <div class="login-header">
          <img src="../assets/security.svg" alt="Logo" class="logo">
          <h2>欢迎回来</h2>
          <p>登录你的安全学院账号</p>
        </div>
        
        <el-form 
          ref="formRef"
          :model="loginForm"
          :rules="rules"
          class="login-form"
        >
          <el-form-item prop="username">
            <el-input
              v-model="loginForm.username"
              placeholder="用户名/邮箱"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="密码"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>
          
          <div class="form-options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <el-link type="primary" :underline="false" @click="handleForgotPassword">忘记密码？</el-link>
          </div>
          
          <el-button 
            type="primary" 
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
          
          <div class="divider">
            <span>或</span>
          </div>
          
          <div class="social-login">
            <el-button class="social-button github">
              <i class="fab fa-github"></i>
              GitHub 登录
            </el-button>
            <el-button class="social-button google">
              <i class="fab fa-google"></i>
              Google 登录
            </el-button>
          </div>
        </el-form>
        
        <div class="register-link">
          还没有账号？
          <router-link to="/register">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, FormRules } from 'element-plus'

const router = useRouter()
const authStore = useAuthStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const rememberMe = ref(authStore.rememberMe)

const loginForm = ref({
  username: localStorage.getItem('username') || '',
  password: ''
})

const rules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid, fields) => {
    if (valid) {
      try {
        loading.value = true
        const success = await authStore.login(
          loginForm.value.username,
          loginForm.value.password,
          rememberMe.value
        )
        
        if (success) {
          ElMessage.success('登录成功')
          router.push('/')
        }
      } catch (error) {
        console.error('Login failed:', error)
        ElMessage.error('登录失败，请检查用户名和密码')
      } finally {
        loading.value = false
      }
    }
  })
}

const handleForgotPassword = () => {
  router.push('/forgot-password')
}

// 如果启用了记住密码，自动填充用户名
onMounted(() => {
  if (authStore.rememberMe) {
    const savedUsername = localStorage.getItem('username')
    if (savedUsername) {
      loginForm.value.username = savedUsername
    }
  }
})
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #1890ff 0%, #1d39c4 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.login-container {
  width: 100%;
  max-width: 440px;
}

.login-box {
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  width: 64px;
  height: 64px;
  margin-bottom: 24px;
}

.login-header h2 {
  font-size: 28px;
  font-weight: bold;
  color: #1a1a1a;
  margin: 0 0 8px;
}

.login-header p {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.login-form {
  margin-bottom: 24px;
}

.login-form :deep(.el-input__wrapper) {
  background-color: #f5f7fa;
  box-shadow: none !important;
  border-radius: 8px;
  height: 48px;
}

.login-form :deep(.el-input__inner) {
  height: 48px;
  font-size: 16px;
}

.login-form :deep(.el-input__prefix-icon) {
  font-size: 20px;
  color: #999;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  border-radius: 8px;
  margin-bottom: 24px;
}

.divider {
  position: relative;
  text-align: center;
  margin: 24px 0;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: calc(50% - 24px);
  height: 1px;
  background: #e8e8e8;
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.divider span {
  background: #fff;
  padding: 0 12px;
  color: #999;
  font-size: 14px;
}

.social-login {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.social-button {
  height: 44px;
  border-radius: 8px;
  font-size: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.social-button i {
  font-size: 18px;
}

.social-button.github {
  background: #24292e;
  color: #fff;
  border: none;
}

.social-button.github:hover {
  background: #2f363d;
  transform: translateY(-2px);
}

.social-button.google {
  background: #fff;
  color: #666;
  border: 1px solid #ddd;
}

.social-button.google:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.register-link {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.register-link a {
  color: #1890ff;
  text-decoration: none;
  margin-left: 4px;
}

.register-link a:hover {
  color: #40a9ff;
}

@media screen and (max-width: 576px) {
  .login-box {
    padding: 30px 20px;
  }
  
  .social-login {
    grid-template-columns: 1fr;
  }
}
</style> 