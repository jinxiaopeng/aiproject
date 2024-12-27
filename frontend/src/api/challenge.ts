import request from '@/utils/request'
import type { Challenge, ChallengeConfig, ChallengeStatus } from '@/types/challenge'

// 获取靶场列表
export const getChallenges = () => {
  return request.get<Challenge[]>('/api/challenges')
}

// 获取靶场详情
export const getChallenge = (id: number) => {
  return request.get<Challenge>(`/api/challenges/${id}`)
}

// 更新靶场配置
export const updateChallengeConfig = (id: number, config: Partial<ChallengeConfig>) => {
  return request.patch<Challenge>(`/api/challenges/${id}/config`, config)
}

// 获取靶场状态
export const getChallengeStatus = (id: number) => {
  return request.get<ChallengeStatus>(`/api/challenges/${id}/status`)
}

// 提交flag
export const submitFlag = (id: number, flag: string) => {
  return request.post<{correct: boolean, points?: number}>(`/api/tasks/${id}/flag`, { flag })
}

// 获取提示
export const getHint = (id: number, hintIndex: number) => {
  return request.get<{hint: string, cost: number}>(`/api/challenges/${id}/hints/${hintIndex}`)
}

// 创建靶场
export const createChallenge = (data: Partial<Challenge>) => {
  return request.post<Challenge>('/api/challenges', data)
}

// 更新靶场
export const updateChallenge = (id: number, data: Partial<Challenge>) => {
  return request.put<Challenge>(`/api/challenges/${id}`, data)
}

// 删除靶场
export const deleteChallenge = (id: number) => {
  return request.delete(`/api/challenges/${id}`)
}

// 启动靶场实例
export const startChallenge = (id: number) => {
  return request.post<ChallengeStatus>(`/api/challenges/${id}/start`)
}

// 停止靶场实例
export const stopChallenge = (id: number) => {
  return request.post<ChallengeStatus>(`/api/challenges/${id}/stop`)
}

// 重启靶场实例
export const restartChallenge = (id: number) => {
  return request.post<ChallengeStatus>(`/api/challenges/${id}/restart`)
}

// 获取靶场日志
export const getChallengeLogs = (id: number, lines: number = 100) => {
  return request.get<string[]>(`/api/challenges/${id}/logs`, { params: { lines } })
}

// 获取靶场资源使用情况
export const getChallengeResources = (id: number) => {
  return request.get<ChallengeStatus>(`/api/challenges/${id}/resources`)
}