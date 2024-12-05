import { defineStore } from 'pinia'
import { ref } from 'vue'
import request from '@/utils/request'
import { setToken, removeToken } from '@/utils/auth'

interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  nickname?: string
  bio?: string
  role?: string
  status?: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  const login = async (username: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('grant_type', 'password')
    formData.append('username', username)
    formData.append('password', password)
    formData.append('scope', '')
    
    const response = await request.post('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    const { access_token, user } = response
    
    setToken(access_token)
    token.value = access_token
    userInfo.value = user
    
    return response
  }

  const logout = () => {
    removeToken()
    token.value = ''
    userInfo.value = null
  }

  const getUserInfo = async () => {
    try {
      const response = await request.get('/auth/user')
      userInfo.value = response
      return response
    } catch (error) {
      console.error('Failed to get user info:', error)
      throw error
    }
  }

  const updateUserInfo = (data: Partial<UserInfo>) => {
    if (userInfo.value) {
      userInfo.value = { ...userInfo.value, ...data }
    }
  }

  return {
    token,
    userInfo,
    login,
    logout,
    getUserInfo,
    updateUserInfo
  }
}) 