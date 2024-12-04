import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/api/auth'
import * as authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo | null>(null)

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')

  const login = async (username: string, password: string) => {
    try {
      const user = await authApi.login({ username, password })
      userInfo.value = user
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  const register = async (username: string, email: string, password: string) => {
    try {
      const user = await authApi.register({ username, email, password })
      return true
    } catch (error) {
      console.error('Registration failed:', error)
      return false
    }
  }

  const logout = async () => {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('token')
  }

  const updateUserInfo = async (data: Partial<UserInfo>) => {
    try {
      const updatedUser = await authApi.updateUserInfo(data)
      userInfo.value = updatedUser
      return true
    } catch (error) {
      console.error('Update user info failed:', error)
      return false
    }
  }

  const updateAvatar = async (file: File) => {
    try {
      const result = await authApi.uploadAvatar(file)
      if (userInfo.value) {
        userInfo.value.avatar = result.url
      }
      return true
    } catch (error) {
      console.error('Update avatar failed:', error)
      return false
    }
  }

  return {
    token,
    userInfo,
    isAuthenticated,
    isAdmin,
    login,
    register,
    logout,
    updateUserInfo,
    updateAvatar
  }
}) 