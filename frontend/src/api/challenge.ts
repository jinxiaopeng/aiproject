import request from '@/utils/request'

export interface Challenge {
  id: number
  title: string
  description: string
  category: string
  difficulty: string
  points: number
  docker_image?: string
  is_solved: boolean
  solved_count: number
}

export interface ChallengeInstance {
  id: number
  challenge_id: number
  instance_url: string
  created_at: string
  expires_at: string
  is_active: boolean
}

export interface ChallengeSubmission {
  id: number
  challenge_id: number
  user_id: number
  submitted_flag: string
  is_correct: boolean
  points_awarded: number
  submitted_at: string
}

// 获取题目分类
export const getCategories = () => {
  return request.get('/challenges/categories')
}

// 获取题目列表
export const getChallenges = (params?: { category?: string; difficulty?: string }) => {
  return request.get('/challenges', { params })
}

// 获取题目详情
export const getChallenge = (id: number) => {
  return request.get(`/challenges/${id}`)
}

// 提交flag
export const submitFlag = (challengeId: number, flag: string) => {
  return request.post(`/challenges/${challengeId}/submit`, { flag })
}

// 启动题目实例
export const createInstance = (challengeId: number) => {
  return request.post(`/challenges/${challengeId}/instance`)
}

// 停止题目实例
export const stopInstance = (challengeId: number) => {
  return request.delete(`/challenges/${challengeId}/instance`)
}

// 获取提交记录
export const getSubmissions = (challengeId: number) => {
  return request.get(`/challenges/${challengeId}/submissions`)
} 