import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  response => response.data,
  error => {
    if (error.response) {
      // 处理服务器返回的错误
      switch (error.response.status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          // 权限不足
          console.error('没有权限访问该资源')
          break
        case 404:
          // 资源不存在
          console.error('请求的资源不存在')
          break
        default:
          console.error('服务器错误:', error.response.data)
      }
    } else if (error.request) {
      // 请求发出但没有收到响应
      console.error('网络错误，请检查您的网络连接')
    } else {
      // 请求配置出错
      console.error('请求配置错误:', error.message)
    }
    return Promise.reject(error)
  }
)

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData extends LoginData {
  email: string
}

export interface UserInfo {
  id: number
  username: string
  email: string
  avatar: string
  role: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

export const login = async (data: LoginData) => {
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('password', data.password)
  
  const response = await api.post<any, LoginResponse>('/auth/login', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  
  // 保存 token
  localStorage.setItem('token', response.access_token)
  
  return response.user
}

export const register = (data: RegisterData) => {
  return api.post<any, UserInfo>('/auth/register', data)
}

export const getUserInfo = () => {
  return api.get<any, UserInfo>('/user/info')
}

export const updateUserInfo = (data: Partial<UserInfo>) => {
  return api.put<any, UserInfo>('/user/info', data)
}

export const uploadAvatar = (file: File) => {
  const formData = new FormData()
  formData.append('avatar', file)
  return api.post<any, { url: string }>('/user/avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export default api 