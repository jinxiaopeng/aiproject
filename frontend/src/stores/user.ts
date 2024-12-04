import { defineStore } from 'pinia'
import { userApi } from '@/api'

interface UserInfo {
  id: number
  username: string
  email: string
  role: 'user' | 'admin'
  avatar?: string
  created_at?: string
  updated_at?: string
}

interface UserState {
  user: UserInfo | null
  token: string | null
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    user: null,
    token: localStorage.getItem('token')
  }),

  getters: {
    isAuthenticated: (state): boolean => !!state.token,
    userInfo: (state): UserInfo => state.user || {
      id: 0,
      username: '',
      email: '',
      role: 'user',
      avatar: ''
    },
    isAdmin: (state): boolean => state.user?.role === 'admin'
  },

  actions: {
    async login(username: string, password: string) {
      try {
        const response = await userApi.login(username, password)
        this.token = response.access_token
        this.user = response.user
        localStorage.setItem('token', response.access_token)
        return response
      } catch (error) {
        throw error
      }
    },

    async logout() {
      try {
        await userApi.logout()
      } finally {
        this.token = null
        this.user = null
        localStorage.removeItem('token')
      }
    },

    async fetchUserInfo() {
      try {
        const user = await userApi.getCurrentUser()
        this.user = user
        return user
      } catch (error) {
        throw error
      }
    }
  }
}) 