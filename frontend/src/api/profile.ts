import request from '@/utils/request'

export interface UserProfile {
  id: number
  username: string
  email: string
  avatar: string
  nickname: string
  bio: string
  created_at: string
}

export interface UpdateProfileRequest {
  nickname?: string
  bio?: string
}

export interface Activity {
  id: number
  user_id: number
  type: string
  content: string
  created_at: string
}

export interface Stats {
  user_id: number
  study_days: number
  completed_courses: number
  points: number
  total_study_time: number
  created_at: string
  updated_at: string
}

export interface Skill {
  id: number
  user_id: number
  name: string
  level: number
  progress: number
  created_at: string
  updated_at: string
}

// 获取个人信息
export const getProfile = async () => {
  const response = await request.get<UserProfile>('/api/profile/info')
  return response.data
}

// 更新个人信息
export const updateProfile = async (data: UpdateProfileRequest) => {
  const response = await request.put<UserProfile>('/api/profile/info', data)
  return response.data
}

// 上传头像
export const uploadAvatar = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await request.post<{ url: string }>('/api/profile/avatar', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
  return response.data
}

// 获取最近活动
export const getActivities = async () => {
  const response = await request.get<Activity[]>('/api/profile/activities')
  return response.data
}

// 获取统计数据
export const getStats = async () => {
  const response = await request.get<Stats>('/api/profile/stats')
  return response.data
}

// 获取技能数据
export const getSkills = async () => {
  const response = await request.get<Skill[]>('/api/profile/skills')
  return response.data
}

// 修改密码
export const changePassword = async (oldPassword: string, newPassword: string) => {
  const response = await request.post('/api/profile/change-password', {
    old_password: oldPassword,
    new_password: newPassword
  })
  return response.data
}

// 发送邮箱验证码
export const sendEmailCode = async (email: string) => {
  const response = await request.post('/api/profile/change-email/code', { email })
  return response.data
}

// 修改邮箱
export const changeEmail = async (email: string, code: string) => {
  const response = await request.post('/api/profile/change-email', { email, code })
  return response.data
} 