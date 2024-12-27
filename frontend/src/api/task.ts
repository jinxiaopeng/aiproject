import request from '@/utils/request'

export interface TaskResult {
  success: boolean
  message?: string
  points?: number
}

// 提交flag
export const submitFlag = (challengeId: number, flag: string) => {
  return request.post<TaskResult>(
    `/api/tasks/${challengeId}/flag`,
    { flag }
  )
}

// 验证任务
export const verifyTask = (
  challengeId: number,
  step: number,
  taskIndex: number,
  result: Record<string, any>
) => {
  return request.post<TaskResult>(
    `/api/tasks/${challengeId}/verify`,
    {
      step,
      task_index: taskIndex,
      result
    }
  )
}

// 获取任务提示
export const getTaskHints = (
  challengeId: number,
  step: number,
  taskIndex: number
) => {
  return request.get<string[]>(
    `/api/tasks/${challengeId}/hints`,
    {
      params: {
        step,
        task_index: taskIndex
      }
    }
  )
} 