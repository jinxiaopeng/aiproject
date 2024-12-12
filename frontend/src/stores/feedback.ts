import { defineStore } from 'pinia'
import type { Feedback, FeedbackDetail, FeedbackStats } from '@/api/feedback'
import * as feedbackApi from '@/api/feedback'
import { handleError } from '@/utils/error'

interface FeedbackState {
  feedbackList: Feedback[]
  currentFeedback: FeedbackDetail | null
  feedbackStats: FeedbackStats | null
  loading: boolean
  submitting: boolean
}

export const useFeedbackStore = defineStore('feedback', {
  state: (): FeedbackState => ({
    feedbackList: [],
    currentFeedback: null,
    feedbackStats: null,
    loading: false,
    submitting: false
  }),

  getters: {
    getFeedbackById: (state) => (id: number) => {
      return state.feedbackList.find(feedback => feedback.id === id)
    },
    
    getPendingFeedback: (state) => {
      return state.feedbackList.filter(feedback => feedback.status === 'PENDING')
    },
    
    getResolvedFeedback: (state) => {
      return state.feedbackList.filter(feedback => feedback.status === 'RESOLVED')
    }
  },

  actions: {
    async fetchEntityFeedback(entityId: number, params?: {
      feedback_type?: string
      status?: string
      skip?: number
      limit?: number
    }) {
      try {
        this.loading = true
        const data = await feedbackApi.getEntityFeedback({
          entity_id: entityId,
          ...params
        })
        this.feedbackList = data
      } catch (error) {
        handleError(error)
      } finally {
        this.loading = false
      }
    },

    async fetchFeedbackDetail(id: number) {
      try {
        this.loading = true
        const data = await feedbackApi.getFeedback(id)
        this.currentFeedback = data
      } catch (error) {
        handleError(error)
      } finally {
        this.loading = false
      }
    },

    async fetchFeedbackStats(entityId: number) {
      try {
        this.loading = true
        const data = await feedbackApi.getFeedbackStats(entityId)
        this.feedbackStats = data
      } catch (error) {
        handleError(error)
      } finally {
        this.loading = false
      }
    },

    async createFeedback(data: {
      entity_id: number
      feedback_type: string
      content: string
      rating?: number
    }) {
      try {
        this.submitting = true
        const feedback = await feedbackApi.createFeedback(data)
        this.feedbackList.unshift(feedback)
        return feedback
      } catch (error) {
        handleError(error)
        throw error
      } finally {
        this.submitting = false
      }
    },

    async updateFeedback(id: number, data: {
      feedback_type?: string
      content?: string
      rating?: number
      status?: string
      admin_reply?: string
    }) {
      try {
        this.submitting = true
        const feedback = await feedbackApi.updateFeedback(id, data)
        const index = this.feedbackList.findIndex(f => f.id === id)
        if (index !== -1) {
          this.feedbackList[index] = feedback
        }
        if (this.currentFeedback?.id === id) {
          this.currentFeedback = {
            ...this.currentFeedback,
            ...feedback
          }
        }
        return feedback
      } catch (error) {
        handleError(error)
        throw error
      } finally {
        this.submitting = false
      }
    },

    async deleteFeedback(id: number) {
      try {
        this.submitting = true
        await feedbackApi.deleteFeedback(id)
        this.feedbackList = this.feedbackList.filter(f => f.id !== id)
        if (this.currentFeedback?.id === id) {
          this.currentFeedback = null
        }
      } catch (error) {
        handleError(error)
        throw error
      } finally {
        this.submitting = false
      }
    },

    async addComment(feedbackId: number, content: string) {
      try {
        this.submitting = true
        const comment = await feedbackApi.addComment(feedbackId, content)
        if (this.currentFeedback?.id === feedbackId) {
          this.currentFeedback.comments.push(comment)
        }
        return comment
      } catch (error) {
        handleError(error)
        throw error
      } finally {
        this.submitting = false
      }
    },

    async voteFeedback(feedbackId: number, isUpvote: boolean) {
      try {
        this.submitting = true
        const vote = await feedbackApi.voteFeedback(feedbackId, isUpvote)
        if (this.currentFeedback?.id === feedbackId) {
          if (isUpvote) {
            this.currentFeedback.upvotes++
          } else {
            this.currentFeedback.downvotes++
          }
        }
        return vote
      } catch (error) {
        handleError(error)
        throw error
      } finally {
        this.submitting = false
      }
    }
  }
}) 