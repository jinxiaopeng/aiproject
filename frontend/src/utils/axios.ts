import axios from 'axios'

// 设置基础URL - 确保这个路径与后端服务匹配
axios.defaults.baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// 请求拦截器
axios.interceptors.request.use(
  config => {
    console.log('Request config:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data
    })
    
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
axios.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message)
    
    if (error.response?.status === 401) {
      // token过期或无效
      localStorage.removeItem('token')
      window.location.href = '/login'
    } else if (error.response?.status === 422) {
      // 表单验证错误
      console.error('Validation error:', error.response.data)
    } else if (error.response?.status === 500) {
      // 服务器错误
      console.error('Server error:', error.response.data)
    }
    
    console.error('API Error Details:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      config: {
        url: error.config?.url,
        method: error.config?.method,
        headers: error.config?.headers,
        data: error.config?.data
      }
    })
    
    if (error.response?.status === 500) {
      // 服务器错误
      console.error('Server error details:', error.response.data)
    }
    
    return Promise.reject(error)
  }
)

export default axios 