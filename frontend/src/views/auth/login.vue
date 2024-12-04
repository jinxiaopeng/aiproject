<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <h2>登录</h2>
        <p>欢迎回来，请登录您的账号</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <div class="form-options">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-button link type="primary" @click="forgotPassword">忘记密码？</el-button>
        </div>
        
        <el-button
          type="primary"
          class="login-button"
          :loading="loading"
          @click="handleLogin"
        >
          登录
        </el-button>
        
        <div class="register-link">
          还没有账号？
          <router-link to="/auth/register">立即注册</router-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { FormInstance } from 'element-plus'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock, User } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { handleApiError } from '@/utils/error'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const loginFormRef = ref<FormInstance>()
const rememberMe = ref(false)

const loginForm = ref({
  username: '',
  password: ''
})

const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    await authStore.login(loginForm.value.username, loginForm.value.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error: any) {
    ElMessage.error(handleApiError(error, '登录失败'))
  } finally {
    loading.value = false
  }
}

const forgotPassword = () => {
  router.push('/auth/forgot-password')
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #0a192f;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(100, 255, 218, 0.1) 0%, transparent 50%);
    animation: rotate 30s linear infinite;
  }
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.login-box {
  width: 400px;
  padding: 40px;
  background: rgba(10, 25, 47, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(100, 255, 218, 0.1);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  position: relative;
  z-index: 1;
}

.login-header {
  text-align: center;
  margin-bottom: 30px;

  h2 {
    font-size: 28px;
    color: #64ffda;
    margin-bottom: 10px;
    font-weight: 600;
  }

  p {
    color: #8892b0;
    font-size: 16px;
  }
}

.login-form {
  :deep(.el-input) {
    --el-input-bg-color: rgba(255, 255, 255, 0.05);
    --el-input-border-color: rgba(100, 255, 218, 0.1);
    --el-input-hover-border-color: rgba(100, 255, 218, 0.3);
    --el-input-focus-border-color: #64ffda;
    
    .el-input__wrapper {
      box-shadow: none !important;
    }
    
    input {
      color: #e6f1ff;
      height: 44px;
      
      &::placeholder {
        color: #8892b0;
      }
    }
    
    .el-input__prefix {
      color: #8892b0;
    }
  }

  :deep(.el-form-item__error) {
    color: #ff4d4f;
  }
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  :deep(.el-checkbox) {
    .el-checkbox__label {
      color: #8892b0;
    }
    
    .el-checkbox__input.is-checked .el-checkbox__inner {
      background-color: #64ffda;
      border-color: #64ffda;
    }
  }

  .el-button {
    color: #64ffda;
    
    &:hover {
      color: #00ff88;
    }
  }
}

.login-button {
  width: 100%;
  height: 44px;
  background: linear-gradient(90deg, #64ffda, #00ff88);
  border: none;
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 20px;
  
  &:hover {
    background: linear-gradient(90deg, #00ff88, #64ffda);
    transform: translateY(-1px);
  }
  
  &:active {
    transform: translateY(0);
  }
}

.register-link {
  text-align: center;
  color: #8892b0;
  
  a {
    color: #64ffda;
    text-decoration: none;
    margin-left: 4px;
    
    &:hover {
      text-decoration: underline;
    }
  }
}
</style> 