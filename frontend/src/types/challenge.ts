export interface Challenge {
  id: number
  title: string
  description: string
  difficulty: string
  category: string
  points: number
  createdAt: Date
  completions: number
  passRate: number
  hints: string[]
}

export interface Discussion {
  id: number
  userId: number
  username: string
  avatar: string
  content: string
  createdAt: Date
  likes: number
  isLiked: boolean
}

export interface Report {
  id: number
  userId: number
  username: string
  process: string
  result: string
  summary: string
  screenshots: string[]
  createdAt: Date
  status: 'pending' | 'approved' | 'rejected'
  feedback?: string
} 