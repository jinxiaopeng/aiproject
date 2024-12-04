<template>
  <div class="login-container">
    <dynamic-background />
    
    <div class="login-box">
      <div class="login-header">
        <h2 class="title">CYBER-EDU</h2>
        <p class="subtitle">Web安全智能学习平台</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @keyup.enter="handleLogin"
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
            show-password
          />
        </el-form-item>

        <div class="form-actions">
          <el-checkbox v-model="rememberMe">记住我</el-checkbox>
          <el-link type="primary" @click="forgotPassword">忘记密码？</el-link>
        </div>

        <el-button
          :loading="loading"
          type="primary"
          class="login-button"
          @click="handleLogin"
        >
          登录
        </el-button>

        <div class="register-link">
          还没有账号？
          <el-link type="primary" @click="$router.push('/register')">立即注册</el-link>
        </div>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import DynamicBackground from '@/components/DynamicBackground.vue'

const router = useRouter()
const userStore = useUserStore()
const loginFormRef = ref()

const loginForm = reactive({
  username: '',
  password: ''
})

const loginRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const loading = ref(false)
const rememberMe = ref(false)

const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    await loginFormRef.value.validate()
    loading.value = true

    await userStore.login(loginForm.username, loginForm.password)
    
    ElMessage({
      message: '登录成功',
      type: 'success'
    })

    // 如果记住我，保存用户名
    if (rememberMe.value) {
      localStorage.setItem('rememberedUsername', loginForm.username)
    } else {
      localStorage.removeItem('rememberedUsername')
    }

    // 跳转到首页或之前的页面
    const redirect = router.currentRoute.value.query.redirect as string
    router.push(redirect || '/')

  } catch (error: any) {
    ElMessage({
      message: error.message || '登录失败',
      type: 'error'
    })
  } finally {
    loading.value = false
  }
}

const forgotPassword = () => {
  router.push('/forgot-password')
}

// 初始化时检查是否有记住的用户名
const initRememberedUsername = () => {
  const rememberedUsername = localStorage.getItem('rememberedUsername')
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    rememberMe.value = true
  }
}

initRememberedUsername()
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 32px;
  font-weight: bold;
  margin: 0;
  background: linear-gradient(120deg, #bd34fe 30%, #47caff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  letter-spacing: 2px;
}

.subtitle {
  margin: 10px 0 0;
  color: rgba(255, 255, 255, 0.8);
  font-size: 16px;
}

.login-form {
  margin-top: 20px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.login-button {
  width: 100%;
  height: 40px;
  font-size: 16px;
  background: linear-gradient(120deg, #bd34fe, #47caff);
  border: none;
}

.login-button:hover {
  background: linear-gradient(120deg, #47caff, #bd34fe);
}

.register-link {
  margin-top: 16px;
  text-align: center;
  color: rgba(255, 255, 255, 0.8);
}

:deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.1);
  box-shadow: none;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

:deep(.el-input__wrapper:hover) {
  box-shadow: none;
  border-color: rgba(255, 255, 255, 0.2);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: none;
  border-color: #bd34fe;
}

:deep(.el-input__inner) {
  color: #ffffff;
  height: 40px;
}

:deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.5);
}

:deep(.el-checkbox__label) {
  color: rgba(255, 255, 255, 0.8);
}

@media (max-width: 768px) {
  .login-box {
    width: 90%;
    max-width: 400px;
    padding: 30px 20px;
  }

  .title {
    font-size: 28px;
  }

  .subtitle {
    font-size: 14px;
  }
}
</style> 