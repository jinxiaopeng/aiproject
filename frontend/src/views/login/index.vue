<template>
  <div class="login-container">
    <DynamicBackground />
    
    <div class="login-box">
      <div class="login-title">
        <h2>Web安全智能学习平台</h2>
        <p>登录您的账号</p>
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
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            :prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-checkbox v-model="loginForm.remember">记住我</el-checkbox>
          <el-link type="primary" class="forget-pwd">忘记密码？</el-link>
        </el-form-item>
        
        <el-form-item>
          <el-button
            :loading="loading"
            type="primary"
            class="login-button"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/stores/auth'
import DynamicBackground from '@/components/DynamicBackground.vue'

const authStore = useAuthStore()
const loading = ref(false)
const loginFormRef = ref()

const loginForm = reactive({
  username: '',
  password: '',
  remember: false
})

const loginRules = {
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
  if (!loginFormRef.value) return
  
  try {
    await loginFormRef.value.validate()
    loading.value = true
    
    await authStore.login(loginForm.username, loginForm.password)
    
    if (loginForm.remember) {
      localStorage.setItem('username', loginForm.username)
    } else {
      localStorage.removeItem('username')
    }
    
  } catch (error: any) {
    console.error('Login error:', error)
    ElMessage.error(error.message || '登录失败，请重试')
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: transparent;
}

.login-box {
  width: 400px;
  padding: 40px;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  
  .login-title {
    text-align: center;
    margin-bottom: 30px;
    
    h2 {
      color: #fff;
      font-size: 24px;
      margin-bottom: 10px;
    }
    
    p {
      color: rgba(255, 255, 255, 0.7);
      font-size: 16px;
    }
  }
}

.login-form {
  .el-input {
    background: transparent;
    
    :deep(.el-input__wrapper) {
      background: rgba(255, 255, 255, 0.1);
      box-shadow: none;
      border: 1px solid rgba(255, 255, 255, 0.2);
      
      &.is-focus {
        border-color: #409EFF;
      }
      
      .el-input__inner {
        color: #fff;
        
        &::placeholder {
          color: rgba(255, 255, 255, 0.5);
        }
      }
    }
  }
  
  .el-checkbox {
    color: #fff;
  }
  
  .forget-pwd {
    float: right;
  }
  
  .login-button {
    width: 100%;
    height: 40px;
    border-radius: 20px;
    background: linear-gradient(45deg, #409EFF, #36D1DC);
    border: none;
    
    &:hover {
      background: linear-gradient(45deg, #36D1DC, #409EFF);
    }
  }
}
</style> 