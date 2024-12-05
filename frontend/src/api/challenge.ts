import request from '@/utils/request'

export interface Challenge {
  id: number
  title: string
  description: string
  category: string
  difficulty: string
  points: number
  is_solved: boolean
  solved_count: number
  docker_image?: string
}

export interface ChallengeInstance {
  id: number
  challenge_id: number
  instance_url: string
  created_at: string
  expires_at: string
  is_active: boolean
}

// 获取题目分类
export const getCategories = () => {
  return request.get('/api/challenges/categories')
}

// 获取题目列表
export const getChallenges = (params?: { category?: string; difficulty?: string }) => {
  return request.get('/api/challenges', { params })
}

// 获取题目详情
export const getChallenge = (id: number) => {
  return request.get(`/api/challenges/${id}`)
}

// 提交flag
export const submitFlag = (challengeId: number, flag: string) => {
  return request.post(`/api/challenges/${challengeId}/submit`, { flag })
}

// 启动题目实例
export const createInstance = (challengeId: number) => {
  return request.post(`/api/challenges/${challengeId}/instance`)
}

// 停止题目实例
export const stopInstance = (challengeId: number) => {
  return request.delete(`/api/challenges/${challengeId}/instance`)
} 