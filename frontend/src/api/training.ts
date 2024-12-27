import request from '@/utils/request'

export interface TrainingProgress {
  id: number
  user_id: number
  challenge_id: number
  current_step: number
  completed_tasks: boolean[]
  unlocked_hints: number[]
  start_time: string
  last_active_time: string
  completed_at?: string
}

export interface HintResponse {
  hint: string
  cost: number
}

// 开始训练
export const startTraining = (challengeId: number) => {
  return request.post<TrainingProgress>(`/api/training/${challengeId}/start`)
}

// 获取训练进度
export const getTrainingProgress = (challengeId: number) => {
  return request.get<TrainingProgress>(`/api/training/${challengeId}/progress`)
}

// 更新训练进度
export const updateTrainingProgress = (
  challengeId: number,
  step: number,
  completedTasks: boolean[]
) => {
  return request.put<TrainingProgress>(
    `/api/training/${challengeId}/progress`,
    { step, completed_tasks: completedTasks }
  )
}

// 解锁提示
export const unlockHint = (challengeId: number, hintIndex: number) => {
  return request.post<HintResponse>(
    `/api/training/${challengeId}/hints/${hintIndex}`
  )
}

// 获取已解锁的提示
export const getUnlockedHints = (challengeId: number) => {
  return request.get<number[]>(`/api/training/${challengeId}/hints`)
} 