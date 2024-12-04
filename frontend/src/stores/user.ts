import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { UserInfo } from '@/api/auth'
import { login as loginApi, getUserInfo } from '@/api/auth'
import router from '@/router'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref<UserInfo | null>(null)
  const loading = ref(false)

  const setToken = (newToken: string) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
  }

  const login = async (username: string, password: string) => {
    try {
      loading.value = true
      const user = await loginApi({ username, password })
      setUserInfo(user)
      router.push('/')
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    router.push('/login')
  }

  const loadUserInfo = async () => {
    if (!token.value) return
    
    try {
      loading.value = true
      const user = await getUserInfo()
      setUserInfo(user)
    } catch (error) {
      console.error('Failed to load user info:', error)
      logout()
    } finally {
      loading.value = false
    }
  }

  return {
    token,
    userInfo,
    loading,
    login,
    logout,
    loadUserInfo
  }
}) 