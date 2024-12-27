import { defineStore } from 'pinia'
import type { Challenge, Progress, Achievement } from '@/types/challenge'
import { mockChallenges, mockProgress, mockAchievements } from '@/mock/challengeData'

export const useChallengeStore = defineStore('challenge', {
  state: () => ({
    challenges: [] as Challenge[],
    currentChallenge: null as Challenge | null,
    progress: null as Progress | null,
    achievements: [] as Achievement[],
    isLoading: false,
    error: null as string | null
  }),

  getters: {
    // 获取不同状态的挑战
    completedChallenges: (state) => 
      state.challenges.filter(c => c.status === 'completed'),
    
    inProgressChallenges: (state) =>
      state.challenges.filter(c => c.status === 'in_progress'),
    
    notStartedChallenges: (state) =>
      state.challenges.filter(c => c.status === 'not_started'),

    // 按分类获取挑战
    getChallengesByCategory: (state) => (category: string) =>
      state.challenges.filter(c => c.category === category),

    // 按难度获取挑战
    getChallengesByDifficulty: (state) => (difficulty: string) =>
      state.challenges.filter(c => c.difficulty === difficulty),

    // 获取总进度
    totalProgress: (state): number => {
      if (!state.progress) return 0
      return Math.round((state.progress.completedChallenges / state.progress.totalChallenges) * 100)
    }
  },

  actions: {
    // 初始化数据
    async initialize() {
      this.isLoading = true
      try {
        // 使用模拟数据
        this.challenges = mockChallenges
        this.progress = mockProgress
        this.achievements = mockAchievements
      } catch (error) {
        this.error = error instanceof Error ? error.message : '初始化失败'
      } finally {
        this.isLoading = false
      }
    },

    // 设置当前挑战
    setCurrentChallenge(challenge: Challenge) {
      this.currentChallenge = challenge
    },

    // 开始挑战
    async startChallenge(challengeId: number) {
      const challenge = this.challenges.find(c => c.id === challengeId)
      if (!challenge) return

      challenge.status = 'in_progress'
      challenge.completionRate = 0
      this.currentChallenge = challenge
    },

    // 更新挑战进度
    updateChallengeProgress(challengeId: number, progress: number) {
      const challenge = this.challenges.find(c => c.id === challengeId)
      if (!challenge) return

      challenge.completionRate = progress
      if (progress === 100) {
        challenge.status = 'completed'
      }
    },

    // 提交flag
    async submitFlag(challengeId: number, flag: string) {
      const challenge = this.challenges.find(c => c.id === challengeId)
      if (!challenge) return false

      // 模拟验证过程
      return new Promise((resolve) => {
        setTimeout(() => {
          const isCorrect = Math.random() > 0.5
          if (isCorrect) {
            challenge.status = 'completed'
            challenge.completionRate = 100
            if (this.progress) {
              this.progress.completedChallenges++
              this.progress.totalPoints += challenge.points
            }
          }
          resolve(isCorrect)
        }, 1000)
      })
    },

    // 获取提示
    async getHint(challengeId: number, hintIndex: number) {
      // 模拟获取提示
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            hint: `这是第${hintIndex}个提示`,
            cost: 50
          })
        }, 500)
      })
    },

    // 重置挑战
    async resetChallenge(challengeId: number) {
      const challenge = this.challenges.find(c => c.id === challengeId)
      if (!challenge) return

      challenge.status = 'not_started'
      challenge.completionRate = 0
    },

    // 更新成就
    updateAchievements() {
      // 检查并更新成就
      const completedCount = this.completedChallenges.length
      const inProgressCount = this.inProgressChallenges.length

      // 示例：检查"全能选手"成就
      const allRounderAchievement = this.achievements.find(a => a.name === '全能选手')
      if (allRounderAchievement && !allRounderAchievement.unlocked) {
        const categories = new Set(this.completedChallenges.map(c => c.category))
        if (categories.size >= 5) {
          allRounderAchievement.unlocked = true
          allRounderAchievement.unlockedAt = new Date().toISOString()
        }
      }
    }
  }
}) 