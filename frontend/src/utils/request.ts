import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import { getToken } from '@/utils/auth'
import router from '@/router'

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 15000,
  withCredentials: true
})

// 请求重试配置
const retryDelay = 1000
const maxRetryCount = 2

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 打印请求信息
    console.log('[Request]', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data
    })

    // 添加 token
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 处理不同的请求类型
    if (config.url?.includes('/auth/login')) {
      config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
      // 转换登录请求数据为 URLSearchParams
      if (!(config.data instanceof URLSearchParams)) {
        const formData = new URLSearchParams()
        Object.entries(config.data).forEach(([key, value]) => {
          formData.append(key, String(value))
        })
        config.data = formData
      }
    } else if (config.headers['Content-Type'] === 'multipart/form-data') {
      // 对于文件上传，保持原有的 FormData
      if (!(config.data instanceof FormData)) {
        const formData = new FormData()
        Object.entries(config.data).forEach(([key, value]) => {
          formData.append(key, value)
        })
        config.data = formData
      }
    } else {
      // 默认使用 JSON
      config.headers['Content-Type'] = 'application/json'
    }

    // 添加重试配置
    config.retryCount = 0
    
    return config
  },
  (error) => {
    console.error('[Request Error]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    console.log('[Response]', {
      url: response.config.url,
      status: response.status,
      data: response.data
    })
    return response
  },
  async (error) => {
    console.error('[Response Error]', {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data
    })

    const config = error.config

    // 只对网络错误或 500 错误进行重试
    if (config && config.retryCount < maxRetryCount && 
        (!error.response || error.response.status >= 500)) {
      config.retryCount++
      
      return new Promise(resolve => {
        setTimeout(() => {
          console.log(`Retrying request (${config.retryCount}/${maxRetryCount})...`)
          resolve(service(config))
        }, retryDelay)
      })
    }

    if (error?.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          if (router.currentRoute.value.path !== '/auth/login') {
            router.push('/auth/login')
          }
          break
        case 403:
          ElMessage.error('没有权限进行此操作')
          break
        case 404:
          ElMessage.error(data?.detail || '请求的资源不存在')
          break
        case 500:
          ElMessage.error(data?.detail || '服务器内部错误，请稍后重试')
          break
        default:
          ElMessage.error(data?.detail || '请求失败，请稍后重试')
      }
    } else if (error?.code === 'ECONNABORTED') {
      ElMessage.error('请求超时，请检查网络连接')
    } else if (error?.request) {
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      ElMessage.error('请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default service 