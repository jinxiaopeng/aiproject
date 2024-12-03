<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-box">
        <div class="register-header">
          <img src="../assets/security.svg" alt="Logo" class="logo">
          <h2>创建账号</h2>
          <p>加入安全学院，开启你的学习之旅</p>
        </div>
        
        <el-form 
          ref="registerForm"
          :model="registerForm"
          :rules="rules"
          class="register-form"
        >
          <el-form-item prop="username">
            <el-input
              v-model="registerForm.username"
              placeholder="用户名"
              prefix-icon="el-icon-user"
            />
          </el-form-item>
          
          <el-form-item prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="邮箱"
              prefix-icon="el-icon-message"
            />
          </el-form-item>
          
          <el-form-item prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="密码"
              prefix-icon="el-icon-lock"
              show-password
            />
          </el-form-item>
          
          <el-form-item prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="确认密码"
              prefix-icon="el-icon-lock"
              show-password
            />
          </el-form-item>
          
          <div class="form-options">
            <el-checkbox v-model="agreeTerms">
              我已阅读并同意
              <el-link type="primary" :underline="false">服务条款</el-link>
              和
              <el-link type="primary" :underline="false">隐私政策</el-link>
            </el-checkbox>
          </div>
          
          <el-button 
            type="primary" 
            class="register-button"
            :loading="loading"
            :disabled="!agreeTerms"
            @click="handleRegister"
          >
            注册
          </el-button>
          
          <div class="divider">
            <span>或</span>
          </div>
          
          <div class="social-register">
            <el-button class="social-button github">
              <i class="fab fa-github"></i>
              GitHub 注册
            </el-button>
            <el-button class="social-button google">
              <i class="fab fa-google"></i>
              Google 注册
            </el-button>
          </div>
        </el-form>
        
        <div class="login-link">
          已有账号？
          <router-link to="/login">立即登录</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const agreeTerms = ref(false)
const loading = ref(false)

const validatePass = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'))
  } else {
    if (registerForm.confirmPassword !== '') {
      if (registerForm.password !== registerForm.confirmPassword) {
        callback(new Error('两次输入密码不一致'))
      }
    }
    callback()
  }
}

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'))
  } else {
    callback()
  }
}

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, validator: validatePass, trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  try {
    loading.value = true
    // TODO: 调用注册 API
    await new Promise(resolve => setTimeout(resolve, 1000)) // 模拟 API 调用
    ElMessage.success('注册成功')
    router.push('/login')
  } catch (error) {
    ElMessage.error('注册失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #1890ff 0%, #1d39c4 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.register-container {
  width: 100%;
  max-width: 440px;
}

.register-box {
  background: #fff;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo {
  width: 64px;
  height: 64px;
  margin-bottom: 24px;
}

.register-header h2 {
  font-size: 28px;
  font-weight: bold;
  color: #1a1a1a;
  margin: 0 0 8px;
}

.register-header p {
  font-size: 16px;
  color: #666;
  margin: 0;
}

.register-form {
  margin-bottom: 24px;
}

.register-form :deep(.el-input__wrapper) {
  background-color: #f5f7fa;
  box-shadow: none !important;
  border-radius: 8px;
  height: 48px;
}

.register-form :deep(.el-input__inner) {
  height: 48px;
  font-size: 16px;
}

.register-form :deep(.el-input__prefix-icon) {
  font-size: 20px;
  color: #999;
}

.form-options {
  margin-bottom: 24px;
}

.form-options :deep(.el-checkbox__label) {
  color: #666;
}

.register-button {
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

.social-register {
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

.login-link {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.login-link a {
  color: #1890ff;
  text-decoration: none;
  margin-left: 4px;
}

.login-link a:hover {
  color: #40a9ff;
}

@media screen and (max-width: 576px) {
  .register-box {
    padding: 30px 20px;
  }
  
  .social-register {
    grid-template-columns: 1fr;
  }
}
</style> 