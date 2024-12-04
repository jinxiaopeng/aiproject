<template>
  <div class="register-container">
    <div class="register-box">
      <div class="register-header">
        <h2>注册账号</h2>
        <p>加入我们，开启网络安全学习之旅</p>
      </div>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="用户名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input
            v-model="registerForm.email"
            placeholder="邮箱"
            prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="密码"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="确认密码"
            prefix-icon="Key"
            show-password
          />
        </el-form-item>
        
        <div class="form-options">
          <el-checkbox v-model="agreeTerms">
            我已阅读并同意
            <el-button link type="primary" @click="viewTerms">服务条款</el-button>
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
        
        <div class="login-link">
          已有账号？
          <router-link to="/auth/login">立即登录</router-link>
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
import { User, Lock, Message, Key } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { handleApiError } from '@/utils/error'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const registerFormRef = ref<FormInstance>()
const agreeTerms = ref(false)

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const validatePass2 = (rule: any, value: string, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== registerForm.value.password) {
    callback(new Error('两次输入密码不一致!'))
  } else {
    callback()
  }
}

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, validator: validatePass2, trigger: 'blur' }
  ]
}

const handleRegister = async () => {
  if (!registerFormRef.value) return
  
  try {
    await registerFormRef.value.validate()
    loading.value = true
    
    await authStore.register(registerForm.value)
    ElMessage.success('注册成功')
    router.push('/auth/login')
  } catch (error: any) {
    ElMessage.error(handleApiError(error, '注册失败'))
  } finally {
    loading.value = false
  }
}

const viewTerms = () => {
  // 实现查看服务条款功能
}
</script>

<style lang="scss" scoped>
.register-container {
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

.register-box {
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

.register-header {
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

.register-form {
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
    padding: 0 4px;
    color: #64ffda;
    
    &:hover {
      color: #00ff88;
    }
  }
}

.register-button {
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
  
  &:disabled {
    background: linear-gradient(90deg, #64ffda50, #00ff8850);
    cursor: not-allowed;
  }
}

.login-link {
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