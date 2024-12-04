import request from '@/utils/request'

export interface UserInfo {
  id: number
  username: string
  email: string
  avatar?: string
  role: string
}

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData extends LoginData {
  email: string
}

export interface LoginResponse {
  access_token: string
  token_type: string
  user: UserInfo
}

// 登录
export const login = async (data: LoginData) => {
  const response = await request.post<LoginResponse>('/auth/login', data)
  localStorage.setItem('token', response.access_token)
  return response.user
}

// 注册
export const register = (data: RegisterData) => {
  return request.post<UserInfo>('/auth/register', data)
}

// 获取用户信息
export const getUserInfo = () => {
  return request.get<UserInfo>('/user/info')
}

// 更新用户信息
export const updateUserInfo = (data: Partial<UserInfo>) => {
  return request.put<UserInfo>('/user/info', data)
}

// 上传头像
export const uploadAvatar = async (file: File) => {
  const formData = new FormData()
  formData.append('avatar', file)
  return request.post<{ url: string }>('/user/avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
} 