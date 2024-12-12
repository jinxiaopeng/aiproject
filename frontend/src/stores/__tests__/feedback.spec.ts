import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useFeedbackStore } from '../feedback'
import * as api from '@/api/feedback'
import { createFeedbackMock, createFeedbackDetailMock } from '@/test/test-utils'

vi.mock('@/api/feedback')

describe('Feedback Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('Actions', () => {
    describe('createFeedback', () => {
      it('should create feedback successfully', async () => {
        const store = useFeedbackStore()
        const mockFeedback = createFeedbackMock()
        vi.mocked(api.createFeedback).mockResolvedValue(mockFeedback)

        const data = {
          entity_id: 1,
          feedback_type: 'CONTENT',
          content: 'Test feedback',
          rating: 4
        }

        await store.createFeedback(data)
        expect(api.createFeedback).toHaveBeenCalledWith(data)
        expect(store.feedbackList).toContain(mockFeedback)
      })
    })

    describe('getFeedback', () => {
      it('should get feedback detail successfully', async () => {
        const store = useFeedbackStore()
        const mockFeedback = createFeedbackDetailMock()
        vi.mocked(api.getFeedback).mockResolvedValue(mockFeedback)

        await store.getFeedback(1)
        expect(api.getFeedback).toHaveBeenCalledWith(1)
        expect(store.currentFeedback).toEqual(mockFeedback)
      })
    })

    describe('getEntityFeedback', () => {
      it('should get entity feedback list successfully', async () => {
        const store = useFeedbackStore()
        const mockFeedbackList = [createFeedbackMock()]
        vi.mocked(api.getEntityFeedback).mockResolvedValue(mockFeedbackList)

        const params = {
          entity_id: 1,
          feedback_type: 'CONTENT',
          status: 'PENDING'
        }

        await store.getEntityFeedback(params)
        expect(api.getEntityFeedback).toHaveBeenCalledWith(params)
        expect(store.feedbackList).toEqual(mockFeedbackList)
      })
    })

    describe('updateFeedback', () => {
      it('should update feedback successfully', async () => {
        const store = useFeedbackStore()
        const mockFeedback = createFeedbackMock({ status: 'RESOLVED' })
        vi.mocked(api.updateFeedback).mockResolvedValue(mockFeedback)

        const data = {
          status: 'RESOLVED',
          admin_reply: 'Test reply'
        }

        await store.updateFeedback(1, data)
        expect(api.updateFeedback).toHaveBeenCalledWith(1, data)
        expect(store.currentFeedback).toEqual(mockFeedback)
      })
    })

    describe('deleteFeedback', () => {
      it('should delete feedback successfully', async () => {
        const store = useFeedbackStore()
        store.feedbackList = [createFeedbackMock()]
        vi.mocked(api.deleteFeedback).mockResolvedValue({ success: true })

        await store.deleteFeedback(1)
        expect(api.deleteFeedback).toHaveBeenCalledWith(1)
        expect(store.feedbackList).toHaveLength(0)
      })
    })

    describe('addComment', () => {
      it('should add comment successfully', async () => {
        const store = useFeedbackStore()
        store.currentFeedback = createFeedbackDetailMock()
        
        const mockComment = {
          id: 1,
          feedback_id: 1,
          user_id: 1,
          content: 'Test comment',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString()
        }
        vi.mocked(api.addComment).mockResolvedValue(mockComment)

        await store.addComment(1, 'Test comment')
        expect(api.addComment).toHaveBeenCalledWith(1, 'Test comment')
        expect(store.currentFeedback?.comments).toContain(mockComment)
      })
    })

    describe('voteFeedback', () => {
      it('should vote feedback successfully', async () => {
        const store = useFeedbackStore()
        store.currentFeedback = createFeedbackDetailMock()
        
        const mockVote = {
          id: 1,
          feedback_id: 1,
          user_id: 1,
          is_upvote: 1,
          created_at: new Date().toISOString()
        }
        vi.mocked(api.voteFeedback).mockResolvedValue(mockVote)

        await store.voteFeedback(1, true)
        expect(api.voteFeedback).toHaveBeenCalledWith(1, true)
        expect(store.currentFeedback?.votes).toContain(mockVote)
      })
    })
  })

  describe('Getters', () => {
    describe('feedbackStats', () => {
      it('should calculate feedback statistics correctly', () => {
        const store = useFeedbackStore()
        store.feedbackList = [
          createFeedbackMock({ feedback_type: 'CONTENT', rating: 4 }),
          createFeedbackMock({ id: 2, feedback_type: 'BUG', rating: 5 }),
          createFeedbackMock({ id: 3, feedback_type: 'CONTENT', rating: 3 })
        ]

        const stats = store.feedbackStats
        expect(stats.total).toBe(3)
        expect(stats.averageRating).toBe(4)
        expect(stats.byType.CONTENT).toBe(2)
        expect(stats.byType.BUG).toBe(1)
      })
    })
  })
}) 