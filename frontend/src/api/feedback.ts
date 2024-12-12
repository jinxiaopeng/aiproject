import request from '@/utils/request'

export interface FeedbackType {
  CONTENT: 'content'
  DIFFICULTY: 'difficulty'
  SUGGESTION: 'suggestion'
  BUG: 'bug'
  OTHER: 'other'
}

export interface FeedbackStatus {
  PENDING: 'pending'
  PROCESSING: 'processing'
  RESOLVED: 'resolved'
  REJECTED: 'rejected'
}

export interface Feedback {
  id: number
  user_id: number
  entity_id: number
  feedback_type: keyof FeedbackType
  content: string
  rating?: number
  status: keyof FeedbackStatus
  admin_reply?: string
  created_at: string
  updated_at: string
}

export interface FeedbackComment {
  id: number
  feedback_id: number
  user_id: number
  content: string
  created_at: string
  updated_at: string
}

export interface FeedbackVote {
  id: number
  feedback_id: number
  user_id: number
  is_upvote: number
  created_at: string
}

export interface FeedbackDetail extends Feedback {
  comments: FeedbackComment[]
  votes: FeedbackVote[]
  upvotes: number
  downvotes: number
}

export interface FeedbackStats {
  total_feedback: number
  pending_feedback: number
  resolved_feedback: number
  average_rating?: number
  feedback_by_type: Record<keyof FeedbackType, number>
  feedback_by_status: Record<keyof FeedbackStatus, number>
}

// 创建反馈
export const createFeedback = async (data: {
  entity_id: number
  feedback_type: keyof FeedbackType
  content: string
  rating?: number
}) => {
  const response = await request.post<Feedback>('/api/feedback', data)
  return response.data
}

// 获取反馈详情
export const getFeedback = async (id: number) => {
  const response = await request.get<FeedbackDetail>(`/api/feedback/${id}`)
  return response.data
}

// 获取实体的反馈列表
export const getEntityFeedback = async (params: {
  entity_id: number
  feedback_type?: keyof FeedbackType
  status?: keyof FeedbackStatus
  skip?: number
  limit?: number
}) => {
  const response = await request.get<Feedback[]>(`/api/feedback/entity/${params.entity_id}`, {
    params: {
      feedback_type: params.feedback_type,
      status: params.status,
      skip: params.skip,
      limit: params.limit
    }
  })
  return response.data
}

// 更新反馈
export const updateFeedback = async (id: number, data: {
  feedback_type?: keyof FeedbackType
  content?: string
  rating?: number
  status?: keyof FeedbackStatus
  admin_reply?: string
}) => {
  const response = await request.put<Feedback>(`/api/feedback/${id}`, data)
  return response.data
}

// 删除反馈
export const deleteFeedback = async (id: number) => {
  const response = await request.delete(`/api/feedback/${id}`)
  return response.data
}

// 添加评论
export const addComment = async (feedback_id: number, content: string) => {
  const response = await request.post<FeedbackComment>(`/api/feedback/${feedback_id}/comments`, {
    feedback_id,
    content
  })
  return response.data
}

// 获取评论列表
export const getComments = async (feedback_id: number, params?: {
  skip?: number
  limit?: number
}) => {
  const response = await request.get<FeedbackComment[]>(`/api/feedback/${feedback_id}/comments`, {
    params
  })
  return response.data
}

// 投票
export const voteFeedback = async (feedback_id: number, is_upvote: boolean) => {
  const response = await request.post<FeedbackVote>(`/api/feedback/${feedback_id}/vote`, {
    feedback_id,
    is_upvote: is_upvote ? 1 : -1
  })
  return response.data
}

// 获取反馈统计
export const getFeedbackStats = async (entity_id: number) => {
  const response = await request.get<FeedbackStats>(`/api/feedback/stats/${entity_id}`)
  return response.data
} 