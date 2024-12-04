import { defineStore } from 'pinia'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/request'
import { getToken, setToken, removeToken } from '@/utils/auth'

export const useAuthStore = defineStore('auth', () => {
  const router = useRouter()
  const token = ref<string | null>(getToken())
  const userInfo = ref<any>(null)
  const loading = ref(false)

  // 登录
  async function login(username: string, password: string) {
    try {
      loading.value = true
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      
      const res = await request.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      const { access_token, user } = res
      token.value = access_token
      userInfo.value = user
      setToken(access_token)
      
      ElMessage.success('登录成功')
      router.push('/')
    } catch (error: any) {
      ElMessage.error(error.message || '登录失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 登出
  async function logout() {
    try {
      await request.post('/auth/logout')
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      userInfo.value = null
      removeToken()
      router.push('/login')
    }
  }

  // 获取用户信息
  async function getUserInfo() {
    try {
      const res = await request.get('/auth/user')
      userInfo.value = res
      return res
    } catch (error) {
      console.error('Get user info error:', error)
      throw error
    }
  }

  return {
    token,
    userInfo,
    loading,
    login,
    logout,
    getUserInfo
  }
}) 