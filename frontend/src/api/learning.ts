import monitorService from '@/utils/monitor-request'

// 学习监控API接口
export const learningAPI = {
  // 获取用户学习统计数据
  getUserStats(userId: number, days: number = 7) {
    return monitorService({
      url: `/learning/stats/${userId}`,
      method: 'get',
      params: { days }
    })
  },

  // 更新视频观看进度
  updateVideoProgress(data: {
    user_id: number
    course_id: number
    chapter_id: number
    progress: number
    duration: number
    current_time: number
  }) {
    return monitorService({
      url: '/learning/video/progress',
      method: 'post',
      data
    })
  },

  // 记录学习行为
  recordLearningBehavior(data: {
    user_id: number
    course_id: number
    behavior_type: string
    content_id: number
    duration?: number
  }) {
    return monitorService({
      url: '/learning/behavior',
      method: 'post',
      data
    })
  },

  // 更新实验进度
  updateChallengeProgress(data: {
    user_id: number
    challenge_id: number
    status: string
    attempts?: number
    hints?: number
    score?: number
  }) {
    return monitorService({
      url: '/learning/challenge/progress',
      method: 'post',
      data
    })
  }
} 