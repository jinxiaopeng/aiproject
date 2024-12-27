// 挑战分类类型
export interface Category {
  id: number
  name: string
  icon: string
  color: string
}

// 难度等级类型
export interface DifficultyLevel {
  id: number
  name: string
  value: string
  color: string
}

// 挑战状态类型
export interface ChallengeStatus {
  id: number
  name: string
  value: string
  color: string
}

// 挑战类型
export interface Challenge {
  id: number
  title: string
  description: string
  category: string
  difficulty: string
  points: number
  status: 'not_started' | 'running' | 'completed'
  completionRate: number
  tags: string[]
  estimatedTime: string
  prerequisites: string[]
  tools: string[]
  createTime: string
  updateTime: string
  targetUrl?: string
  targetPort?: number
  targetHost?: string
  containerStatus?: 'starting' | 'running' | 'stopped' | 'error'
  remainingTime?: number
}

// 进度类型
export interface Progress {
  totalChallenges: number
  completedChallenges: number
  inProgressChallenges: number
  totalPoints: number
  weeklyProgress: WeeklyProgress[]
  categoryProgress: CategoryProgress[]
}

export interface WeeklyProgress {
  day: string
  completed: number
}

export interface CategoryProgress {
  name: string
  completed: number
  total: number
}

// 成就类型
export interface Achievement {
  id: number
  name: string
  description: string
  icon: string
  unlocked: boolean
  unlockedAt?: string
}

// 挑战配置类型
export interface ChallengeConfig {
  dockerImage: string
  ports: number[]
  memory: string
  cpu: string
  timeout: number
  flag: string
} 