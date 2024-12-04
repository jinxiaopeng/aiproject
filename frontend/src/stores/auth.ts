import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  nickname?: string
  bio?: string
}

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)

  const login = async (username: string, password: string) => {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)
    
    const response = await axios.post('/api/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    
    const { token: newToken, user: userData } = response.data
    
    localStorage.setItem('token', newToken)
    token.value = newToken
    userInfo.value = userData
    
    axios.defaults.headers.common['Authorization'] = `Bearer ${newToken}`
    
    return response.data
  }

  const logout = () => {
    localStorage.removeItem('token')
    token.value = ''
    userInfo.value = null
    delete axios.defaults.headers.common['Authorization']
  }

  const getUserInfo = async () => {
    const response = await axios.get('/api/auth/user')
    userInfo.value = response.data
    return response.data
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