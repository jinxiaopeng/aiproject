import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  role: string
}

export const useUserStore = defineStore('user', () => {
  const userInfo = ref<UserInfo | null>(null)
  const token = ref<string | null>(null)

  // 检查认证状态
  const checkAuth = async () => {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      token.value = storedToken
      try {
        const response = await axios.get('/api/user/info', {
          headers: { Authorization: `Bearer ${storedToken}` }
        })
        userInfo.value = response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
        logout()
      }
    }
  }

  // 登录
  const login = async (email: string, password: string) => {
    try {
      const response = await axios.post('/api/auth/login', { email, password })
      const { token: newToken, user } = response.data
      token.value = newToken
      userInfo.value = user
      localStorage.setItem('token', newToken)
      ElMessage.success('登录成功')
      return true
    } catch (error) {
      console.error('登录失败:', error)
      ElMessage.error('登录失败，请检查邮箱和密码')
      return false
    }
  }

  // 注册
  const register = async (username: string, email: string, password: string) => {
    try {
      const response = await axios.post('/api/auth/register', {
        username,
        email,
        password
      })
      ElMessage.success('注册成功，请登录')
      return true
    } catch (error) {
      console.error('注册失败:', error)
      ElMessage.error('注册失败，请稍后重试')
      return false
    }
  }

  // 登出
  const logout = () => {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('token')
    ElMessage.success('已退出登录')
  }

  // 更新用户信息
  const updateUserInfo = async (data: Partial<UserInfo>) => {
    try {
      const response = await axios.put('/api/user/info', data, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      userInfo.value = { ...userInfo.value, ...response.data }
      ElMessage.success('更新成功')
      return true
    } catch (error) {
      console.error('更新用户信息失败:', error)
      ElMessage.error('更新失败，请稍后重试')
      return false
    }
  }

  // 更新头像
  const updateAvatar = async (avatarUrl: string) => {
    try {
      const response = await axios.put('/api/user/avatar', { avatar: avatarUrl }, {
        headers: { Authorization: `Bearer ${token.value}` }
      })
      userInfo.value = { ...userInfo.value, avatar: response.data.avatar }
      ElMessage.success('头像更新成功')
      return true
    } catch (error) {
      console.error('更新头像失败:', error)
      ElMessage.error('更新头像失败，请稍后重试')
      return false
    }
  }

  return {
    userInfo,
    token,
    checkAuth,
    login,
    register,
    logout,
    updateUserInfo,
    updateAvatar
  }
})

export default {
  useUserStore
} 