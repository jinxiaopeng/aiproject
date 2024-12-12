import request from '@/utils/request'
import type { AxiosResponse } from 'axios'

// API 响应类型定义
interface Lab {
  id: number
  title: string
  description: string
  category: string
  difficulty: 'easy' | 'medium' | 'hard'
  points: number
  status: 'not_started' | 'created' | 'running' | 'stopped' | 'completed' | 'error'
  completionRate: number
  solvedCount: number
  created_at: string | null
  hints: string[]
  docker_image: string
  port_mapping: string
  resource_limits: {
    cpu: string
    memory: string
  }
}

interface UserStats {
  totalHours: number
  completedCount: number
  points: number
  rank: number
}

interface SkillRadarData {
  categories: string[]
  scores: number[]
}

interface ProgressTrendData {
  dates: string[]
  counts: number[]
}

interface LabStatus {
  status: 'not_started' | 'created' | 'running' | 'stopped' | 'completed' | 'error'
  instance_url?: string
}

interface LabResponse {
  status: string
  message: string
  instance_id?: number
}

interface FlagSubmission {
  correct: boolean
  message: string
}

// API 请求函数
export const labApi = {
  // 获取靶场列表
  getList(): Promise<AxiosResponse<Lab[]>> {
    return request({
      url: '/api/practice/labs',
      method: 'get'
    })
  },

  // 获取靶场详情
  getLabDetail(id: number): Promise<AxiosResponse<Lab>> {
    return request({
      url: `/api/practice/labs/${id}`,
      method: 'get'
    })
  },

  // 启动靶场
  startLab(id: number): Promise<AxiosResponse<LabResponse>> {
    return request({
      url: `/api/practice/labs/${id}/start`,
      method: 'post'
    })
  },

  // 停止靶场
  stopLab(id: number): Promise<AxiosResponse<LabResponse>> {
    return request({
      url: `/api/practice/labs/${id}/stop`,
      method: 'post'
    })
  },

  // 提交Flag
  submit(id: number, flag: string): Promise<AxiosResponse<FlagSubmission>> {
    return request({
      url: `/api/practice/labs/${id}/submit`,
      method: 'post',
      data: { flag }
    })
  },

  // 获取靶场状态
  getStatus(id: number): Promise<AxiosResponse<LabStatus>> {
    return request({
      url: `/api/practice/labs/${id}/status`,
      method: 'get'
    })
  },

  // 获取用户统计数据
  getUserStats(): Promise<AxiosResponse<UserStats>> {
    return request({
      url: '/api/practice/stats',
      method: 'get'
    })
  },

  // 获取技能雷达图数据
  getSkillRadarData(): Promise<AxiosResponse<SkillRadarData>> {
    return request({
      url: '/api/practice/stats/skill-radar',
      method: 'get'
    })
  },

  // 获取进度趋势数据
  getProgressTrend(days: number = 30): Promise<AxiosResponse<ProgressTrendData>> {
    return request({
      url: '/api/practice/stats/progress-trend',
      method: 'get',
      params: { days }
    })
  }
} 