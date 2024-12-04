import axios from 'axios'

export interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  role: string
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface ResetPasswordRequest {
  email: string
  code: string
  password: string
}

export interface UpdateUserInfoRequest {
  username?: string
  email?: string
  avatar?: string
}

// 登录
export const login = async (data: LoginRequest) => {
  const response = await axios.post<UserInfo>('/api/auth/login', data)
  return response.data
}

// 注册
export const register = async (data: RegisterRequest) => {
  const response = await axios.post<UserInfo>('/api/auth/register', data)
  return response.data
}

// 获取用户信息
export const getUserInfo = async () => {
  const response = await axios.get<UserInfo>('/api/auth/user')
  return response.data
}

// 更新用户信息
export const updateUserInfo = async (data: UpdateUserInfoRequest) => {
  const response = await axios.put<UserInfo>('/api/auth/user', data)
  return response.data
}

// 上传头像
export const uploadAvatar = async (file: File) => {
  const formData = new FormData()
  formData.append('avatar', file)
  const response = await axios.post<{ url: string }>('/api/auth/avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

// 发送重置密码验证码
export const sendResetCode = async (email: string) => {
  const response = await axios.post('/api/auth/reset-code', { email })
  return response.data
}

// 验证重置密码验证码
export const verifyResetCode = async (email: string, code: string) => {
  const response = await axios.post('/api/auth/verify-code', { email, code })
  return response.data
}

// 重置密码
export const resetPassword = async (data: ResetPasswordRequest) => {
  const response = await axios.post('/api/auth/reset-password', data)
  return response.data
}

// 修改密码
export const changePassword = async (oldPassword: string, newPassword: string) => {
  const response = await axios.post('/api/auth/change-password', {
    oldPassword,
    newPassword
  })
  return response.data
}

// 登出
export const logout = async () => {
  const response = await axios.post('/api/auth/logout')
  return response.data
} 