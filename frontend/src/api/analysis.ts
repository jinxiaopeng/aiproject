import request from '@/utils/request'
import type { AnalysisData, KnowledgePoint } from '@/types/analysis'

export const analysisApi = {
  // 获取学习分析数据
  getAnalysisData: async () => {
    const response = await request.get<AnalysisData>('/api/analysis/data')
    return response.data
  },

  // 获取知识点掌握度
  getKnowledgePoints: async () => {
    const response = await request.get<KnowledgePoint[]>('/api/analysis/knowledge-points')
    return response.data
  },

  // 更新学习行为
  updateLearningBehavior: async (data: {
    courseId: number;
    type: string;
    duration?: number;
    progress?: number;
  }) => {
    const response = await request.post('/api/analysis/learning-behavior', data)
    return response.data
  },

  // 获取技能分析
  getSkillAnalysis: async () => {
    const response = await request.get('/api/analysis/skills')
    return response.data
  },

  // 获取学习建议
  getLearningAdvice: async () => {
    const response = await request.get('/api/analysis/advice')
    return response.data
  },

  // 获取学习效率分析
  getEfficiencyAnalysis: async (timeRange: string) => {
    const response = await request.get('/api/analysis/efficiency', {
      params: { timeRange }
    })
    return response.data
  }
} 