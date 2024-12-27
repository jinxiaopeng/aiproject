import axios, { AxiosInstance } from 'axios'
import { ElMessage } from 'element-plus'

// 创建专门用于监控服务的 axios 实例
const monitorService: AxiosInstance = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 15000
})

// 请求拦截器
monitorService.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    console.error('[Monitor Request Error]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
monitorService.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    console.error('[Monitor Response Error]', error)
    
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 404:
          ElMessage.error('请求的监控数据不存在')
          break
        case 500:
          ElMessage.error('监控服务内部错误，请稍后重试')
          break
        default:
          ElMessage.error(data?.detail || '监控请求失败，请稍后重试')
      }
    } else if (error.code === 'ECONNABORTED') {
      ElMessage.error('监控请求超时，��检查网络连接')
    } else if (error.request) {
      ElMessage.error('无法连接到监控服务，请检查服务是否启动')
    } else {
      ElMessage.error('监控请求配置错误')
    }
    
    return Promise.reject(error)
  }
)

export default monitorService 