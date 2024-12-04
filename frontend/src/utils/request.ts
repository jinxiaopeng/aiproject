import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          ElMessage.error(data.message || '请求参数错误')
          break
          
        case 401:
          // 未授权或 token 过期
          ElMessage.error('登录已过期，请重新登录')
          const authStore = useAuthStore()
          authStore.logout()
          router.push('/login')
          break
          
        case 403:
          ElMessage.error('没有权限访问')
          router.push('/403')
          break
          
        case 404:
          ElMessage.error('请求的资源不存在')
          router.push('/404')
          break
          
        case 500:
          ElMessage.error('服务器错误，请稍后重试')
          break
          
        default:
          ElMessage.error(data.message || '未知错误')
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      ElMessage.error('网络错误，请检查您的网络连接')
    } else {
      // 请求配置出错
      ElMessage.error('请求配置错误: ' + error.message)
    }
    
    return Promise.reject(error)
  }
)

export default request 