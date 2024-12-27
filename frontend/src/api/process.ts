import request from '@/utils/request'

export interface ProcessStatus {
  status: string
  pid?: number
  port?: number
  cpu_percent?: number
  memory_percent?: number
  run_time?: number
}

export interface ResourceAlert {
  id: string
  challenge_id: string
  alert_type: string
  severity: string
  message: string
  current_value: number
  limit_value: number
  timestamp: string
}

// 启动靶场进程
export const startChallengeProcess = (challengeId: string) => {
  return request.post<ProcessStatus>(`/api/challenges/${challengeId}/start`)
}

// 停止靶场进程
export const stopChallengeProcess = (challengeId: string) => {
  return request.post<ProcessStatus>(`/api/challenges/${challengeId}/stop`)
}

// 获取进程状态
export const getChallengeProcessStatus = (challengeId: string) => {
  return request.get<ProcessStatus>(`/api/challenges/${challengeId}/status`)
}

// 获取所有运行中的靶场
export const getRunningChallenges = () => {
  return request.get<Record<string, ProcessStatus>>('/api/challenges/running')
}

// 获取靶场告警记录
export const getChallengeAlerts = (challengeId: string, limit: number = 100) => {
  return request.get<ResourceAlert[]>(`/api/challenges/${challengeId}/alerts`, {
    params: { limit }
  })
}

// 获取最近的日志
export const getRecentLogs = (challengeId: string, lines: number = 100) => {
  return request.get<string[]>(`/api/challenges/${challengeId}/logs`, {
    params: { lines }
  })
}