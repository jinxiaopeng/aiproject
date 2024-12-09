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

interface LoginResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  const login = async (username: string, password: string) => {
    try {
      console.log('Sending login request with:', { username, password })
      
      const formData = new URLSearchParams()
      formData.append('username', username)
      formData.append('password', password)
      
      const response = await request.post<LoginResponse>('/auth/login', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      
      console.log('Login response:', response)
      
      const { data } = response
      setToken(data.access_token)
      token.value = data.access_token
      userInfo.value = data.user
      
      return data
    } catch (error: any) {
      console.error('Login error:', error)
      if (error.response) {
        console.error('Error response:', {
          status: error.response.status,
          data: error.response.data,
          headers: error.response.headers
        })
      }
      throw error
    }
  }

  const logout = () => {
    removeToken()
    token.value = ''
    userInfo.value = null
  }

  const getUserInfo = async () => {
    try {
      const { data } = await request.get<UserInfo>('/auth/user')
      userInfo.value = data
      return data
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