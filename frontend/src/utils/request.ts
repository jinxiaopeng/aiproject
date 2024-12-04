import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'
import { useAuthStore } from '@/stores/auth'

// 创建 axios 实例
const request = axios.create({
  baseURL: '',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token && !config.url?.includes('/auth/login')) {  // 登录请求不需要token
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 添加缓存控制头
    config.headers['Cache-Control'] = 'no-cache'
    config.headers['Pragma'] = 'no-cache'
    
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
    // 如果响应包含token，保存它
    const token = response.headers['authorization'] || response.data?.access_token
    if (token) {
      localStorage.setItem('token', token)
    }
    return response
  },
  error => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 400:
          ElMessage.error(data.detail || '请求参数错误')  // 使用 detail 字段
          break
          
        case 401:
          // 未授权或 token 过期
          ElMessage.error(data.detail || '登录已过期，请重新登录')  // 使用 detail 字段
          const authStore = useAuthStore()
          authStore.logout()
          router.push('/login')
          break
          
        case 403:
          ElMessage.error(data.detail || '没有权限访问')  // 使用 detail 字段
          router.push('/403')
          break
          
        case 404:
          ElMessage.error(data.detail || '请求的资源不存在')  // 使用 detail 字段
          router.push('/404')
          break
          
        case 500:
          ElMessage.error(data.detail || '服务器错误，请稍后重试')  // 使用 detail 字段
          break
          
        default:
          ElMessage.error(data.detail || '未知错误')  // 使用 detail 字段
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