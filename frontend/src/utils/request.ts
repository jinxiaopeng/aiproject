import axios, { AxiosInstance, InternalAxiosRequestConfig, AxiosResponse } from 'axios'
import { ElMessage } from 'element-plus'
import { getToken } from '@/utils/auth'
import router from '@/router'

// 创建 axios 实例
const service: AxiosInstance = axios.create({
  baseURL: '',  // 不设置默认的 baseURL，由拦截器处理
  timeout: 30000,
  withCredentials: false
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 统一处理 API 路径
    if (!config.url?.startsWith('/api/')) {
      config.url = `/api${config.url}`
    }
    
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
  (error) => {
    console.error('[Response Error]', {
      url: error.config?.url,
      status: error.response?.status,
      data: error.response?.data
    })

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