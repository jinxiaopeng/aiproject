import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/api/auth'
import * as authApi from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useAuthStore = defineStore('auth', () => {
  // State
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<UserInfo | null>(null)
  const rememberMe = ref<boolean>(localStorage.getItem('rememberMe') === 'true')

  // Getters
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')

  // Actions
  const login = async (username: string, password: string, remember: boolean = false) => {
    try {
      const response = await authApi.login({ username, password })
      token.value = response.access_token
      userInfo.value = response.user
      localStorage.setItem('token', response.access_token)
      rememberMe.value = remember
      localStorage.setItem('rememberMe', remember.toString())
      if (remember) {
        localStorage.setItem('username', username)
      } else {
        localStorage.removeItem('username')
      }
      return true
    } catch (error) {
      console.error('Login failed:', error)
      return false
    }
  }

  const register = async (username: string, email: string, password: string) => {
    try {
      const response = await authApi.register({ username, email, password })
      return true
    } catch (error) {
      console.error('Registration failed:', error)
      return false
    }
  }

  const logout = () => {
    token.value = null
    userInfo.value = null
    localStorage.removeItem('token')
    if (!rememberMe.value) {
      localStorage.removeItem('username')
    }
    localStorage.removeItem('rememberMe')
  }

  const loadUserInfo = async () => {
    try {
      if (token.value) {
        const response = await authApi.getUserInfo()
        userInfo.value = response.data
      }
    } catch (error) {
      console.error('Failed to load user info:', error)
      logout()
    }
  }

  const updateUserInfo = async (data: Partial<UserInfo>) => {
    try {
      const response = await authApi.updateUserInfo(data)
      userInfo.value = response.data
      ElMessage.success('个人信息更新成功')
      return true
    } catch (error) {
      console.error('Failed to update user info:', error)
      ElMessage.error('更新失败，请重试')
      return false
    }
  }

  const updateAvatar = async (file: File) => {
    try {
      const response = await authApi.uploadAvatar(file)
      if (userInfo.value && response.data) {
        userInfo.value.avatar = response.data.url
      }
      ElMessage.success('头像更新成功')
      return true
    } catch (error) {
      console.error('Failed to update avatar:', error)
      ElMessage.error('头像更新失败，请重试')
      return false
    }
  }

  // 初始化时加载用户信息
  if (token.value) {
    loadUserInfo()
  }

  return {
    // State
    token,
    userInfo,
    rememberMe,

    // Getters
    isAuthenticated,
    isAdmin,

    // Actions
    login,
    register,
    logout,
    loadUserInfo,
    updateUserInfo,
    updateAvatar
  }
}) 