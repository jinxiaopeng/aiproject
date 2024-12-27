import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { 
  AnalysisData, 
  LearningMetrics, 
  AISuggestion, 
  SkillData,
  KnowledgePoint 
} from '@/types/analysis'

export const useAnalysisStore = defineStore('analysis', () => {
  // 状态
  const analysisData = ref<AnalysisData>({
    metrics: {
      efficiency: 75,
      mastery: 68,
      engagement: 82
    },
    suggestions: [
      {
        id: 1,
        type: 'success',
        color: '#67C23A',
        hollow: true,
        timestamp: '今日',
        title: '学习方法建议',
        content: '你的学习效率较高，建议继续保持当前的学习节奏。可以尝试在完成课程后做知识总结，加深理解。'
      },
      {
        id: 2,
        type: 'warning',
        color: '#E6A23C',
        hollow: true,
        timestamp: '今日',
        title: '知识巩固建议',
        content: '在Web安全基础模块中，建议重点复习CSRF和XSS相关内容，这些是你的薄弱环节。'
      },
      {
        id: 3,
        type: 'info',
        color: '#909399',
        hollow: true,
        timestamp: '今日',
        title: '技能提升建议',
        content: '可以尝试参与更多实战练习，提高渗透测试的实践能力。推荐完成"Web漏洞挖掘"进阶课程。'
      }
    ],
    skills: [
      { category: 'Web安全', value: 80, max: 100 },
      { category: '系统安全', value: 65, max: 100 },
      { category: '网络安全', value: 70, max: 100 },
      { category: '密码学', value: 60, max: 100 },
      { category: '安全开发', value: 75, max: 100 }
    ],
    lastUpdated: new Date().toISOString()
  })

  const knowledgePoints = ref<KnowledgePoint[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // 计算属性
  const averageSkillLevel = computed(() => {
    const skills = analysisData.value.skills
    const total = skills.reduce((sum, skill) => sum + skill.value, 0)
    return Math.round(total / skills.length)
  })

  const weakestSkills = computed(() => {
    return analysisData.value.skills
      .filter(skill => skill.value < 70)
      .sort((a, b) => a.value - b.value)
  })

  const strongestSkills = computed(() => {
    return analysisData.value.skills
      .filter(skill => skill.value >= 80)
      .sort((a, b) => b.value - a.value)
  })

  // 方法
  const fetchAnalysisData = async () => {
    loading.value = true
    error.value = null
    try {
      // TODO: 调用后端API获取分析数据
      await new Promise(resolve => setTimeout(resolve, 1000))
      // 模拟数据更新
      analysisData.value = {
        ...analysisData.value,
        metrics: {
          efficiency: Math.floor(Math.random() * 30) + 60,
          mastery: Math.floor(Math.random() * 30) + 60,
          engagement: Math.floor(Math.random() * 30) + 60
        },
        lastUpdated: new Date().toISOString()
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取分析数据失败'
      console.error('获取分析数据失败:', err)
    } finally {
      loading.value = false
    }
  }

  const updateKnowledgePoints = async () => {
    try {
      // TODO: 调用后端API更新知识点数据
      await new Promise(resolve => setTimeout(resolve, 1000))
      // 模拟数据更新
      knowledgePoints.value = [
        {
          id: '1',
          name: 'SQL注入',
          category: 'Web安全',
          mastery: 85,
          lastReviewed: new Date().toISOString(),
          relatedCourses: [1, 2, 3]
        },
        {
          id: '2',
          name: 'XSS攻击',
          category: 'Web安全',
          mastery: 75,
          lastReviewed: new Date().toISOString(),
          relatedCourses: [1, 4]
        }
      ]
    } catch (err) {
      console.error('更新知识点数据失败:', err)
    }
  }

  const generateSuggestions = () => {
    const suggestions: AISuggestion[] = []
    
    // 基于学习效率生成建议
    if (analysisData.value.metrics.efficiency < 60) {
      suggestions.push({
        id: Date.now(),
        type: 'warning',
        color: '#E6A23C',
        hollow: true,
        timestamp: '今日',
        title: '学习效率提升建议',
        content: '建议制定合理的学习计划，将学习任务分解为小目标，逐步完成。'
      })
    }

    // 基于薄弱技能生成建议
    const weak = weakestSkills.value
    if (weak.length > 0) {
      suggestions.push({
        id: Date.now() + 1,
        type: 'info',
        color: '#909399',
        hollow: true,
        timestamp: '今日',
        title: '技能提升建议',
        content: `建议加强 ${weak[0].category} 相关知识的学习，当前掌握度较低。`
      })
    }

    analysisData.value.suggestions = suggestions
  }

  return {
    analysisData,
    knowledgePoints,
    loading,
    error,
    averageSkillLevel,
    weakestSkills,
    strongestSkills,
    fetchAnalysisData,
    updateKnowledgePoints,
    generateSuggestions
  }
}) 