import { defineStore } from 'pinia'
import request from '@/utils/request'
import { ref } from 'vue'

export interface Challenge {
  title: string
  description: string
  difficulty: string
  category: string
  hints: string[]
  resources?: Array<{
    name: string
    type: string
    url?: string
  }>
}

export interface LearningPath {
  estimatedTime: string
  stages: Array<{
    title: string
    description: string
    duration: string
    status: 'completed' | 'in_progress' | 'pending'
    skills: string[]
    resources?: Array<{
      name: string
      type: string
      difficulty: string
      url?: string
    }>
  }>
  progress?: {
    percentage: number
    completedCourses: number
    totalHours: number
    points: number
  }
}

export const useAiStore = defineStore('ai', () => {
  const loading = ref(false)
  const context = ref<Array<{role: string, content: string}>>([])

  const chat = async (message: string) => {
    try {
      const { data } = await request.post('/ai/chat', {
        message,
        context: context.value
      })
      context.value = data.context
      return data
    } catch (error) {
      console.error('AI对话失败:', error)
      throw error
    }
  }

  const analyzeCode = async (code: string, language: string) => {
    try {
      const { data } = await request.post('/ai/analyze_code', {
        code,
        language
      })
      return data
    } catch (error) {
      console.error('代码分析失败:', error)
      throw error
    }
  }

  const explainVulnerability = async (vulnerabilityType: string) => {
    try {
      const { data } = await request.post('/ai/explain_vulnerability', {
        vulnerability_type: vulnerabilityType
      })
      return data
    } catch (error) {
      console.error('漏洞解释失败:', error)
      throw error
    }
  }

  const generateChallenge = async (
    difficulty: string,
    category: string,
    skills?: string[]
  ): Promise<Challenge> => {
    try {
      const { data } = await request.post('/ai/generate_challenge', {
        difficulty,
        category,
        skills
      })
      return data
    } catch (error) {
      console.error('题目生成失败:', error)
      throw error
    }
  }

  const generateLearningPath = async (
    targetSkill: string,
    currentLevel: string,
    timeCommitment: string
  ): Promise<LearningPath> => {
    try {
      const { data } = await request.post('/ai/learning_path', {
        target_skill: targetSkill,
        current_level: currentLevel,
        time_commitment: timeCommitment
      })
      return data
    } catch (error) {
      console.error('学习路径生成失败:', error)
      throw error
    }
  }

  const clearContext = () => {
    context.value = []
  }

  return {
    loading,
    context,
    chat,
    analyzeCode,
    explainVulnerability,
    generateChallenge,
    generateLearningPath,
    clearContext
  }
}) 