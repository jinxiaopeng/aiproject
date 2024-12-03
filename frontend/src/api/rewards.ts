import request from '@/utils/request'

export interface AchievementType {
  id: number
  name: string
  description?: string
  icon?: string
  points: number
  createdAt: string
}

export interface UserAchievement {
  id: number
  userId: number
  achievementTypeId: number
  progress: number
  completed: boolean
  completedAt?: string
  createdAt: string
  updatedAt: string
  achievementType: AchievementType
}

export interface PointHistory {
  id: number
  userId: number
  points: number
  type: string
  description?: string
  referenceId?: number
  referenceType?: string
  createdAt: string
}

export interface LevelRule {
  id: number
  level: number
  pointsRequired: number
  title: string
  icon?: string
  rewards?: Record<string, any>
  createdAt: string
}

export interface UserLevel {
  id: number
  userId: number
  level: number
  currentPoints: number
  nextLevelPoints: number
  createdAt: string
  updatedAt: string
}

export default {
  // 获取所有成就类型
  getAchievementTypes() {
    return request.get<AchievementType[]>('/api/rewards/achievements/types')
  },

  // 获取用户成就
  getUserAchievements() {
    return request.get<UserAchievement[]>('/api/rewards/achievements')
  },

  // 检查并更新用户成就
  checkAchievements() {
    return request.post<UserAchievement[]>('/api/rewards/achievements/check')
  },

  // 获取积分历史
  getPointHistory(limit = 10) {
    return request.get<PointHistory[]>(`/api/rewards/points/history?limit=${limit}`)
  },

  // 获取等级规则
  getLevelRules() {
    return request.get<LevelRule[]>('/api/rewards/levels/rules')
  },

  // 获取用户当前等级
  getUserLevel() {
    return request.get<UserLevel>('/api/rewards/levels/current')
  }
} 