import { describe, it, expect, vi, beforeEach } from 'vitest'
import * as api from '../feedback'
import request from '@/utils/request'
import { createFeedbackMock, createFeedbackDetailMock } from '@/test/test-utils'

vi.mock('@/utils/request', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    put: vi.fn(),
    delete: vi.fn()
  }
}))

describe('Feedback API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('createFeedback', () => {
    it('should create feedback successfully', async () => {
      const mockFeedback = createFeedbackMock()
      vi.mocked(request.post).mockResolvedValue({ data: mockFeedback })

      const data = {
        entity_id: 1,
        feedback_type: 'CONTENT',
        content: 'Test feedback',
        rating: 4
      }

      const result = await api.createFeedback(data)
      expect(result).toEqual(mockFeedback)
      expect(request.post).toHaveBeenCalledWith('/api/feedback', data)
    })
  })

  describe('getFeedback', () => {
    it('should get feedback detail successfully', async () => {
      const mockFeedback = createFeedbackDetailMock()
      vi.mocked(request.get).mockResolvedValue({ data: mockFeedback })

      const result = await api.getFeedback(1)
      expect(result).toEqual(mockFeedback)
      expect(request.get).toHaveBeenCalledWith('/api/feedback/1')
    })
  })

  describe('getEntityFeedback', () => {
    it('should get entity feedback list successfully', async () => {
      const mockFeedbackList = [createFeedbackMock()]
      vi.mocked(request.get).mockResolvedValue({ data: mockFeedbackList })

      const params = {
        entity_id: 1,
        feedback_type: 'CONTENT',
        status: 'PENDING'
      }

      const result = await api.getEntityFeedback(params)
      expect(result).toEqual(mockFeedbackList)
      expect(request.get).toHaveBeenCalledWith(`/api/feedback/entity/1`, {
        params: {
          feedback_type: 'CONTENT',
          status: 'PENDING'
        }
      })
    })
  })

  describe('updateFeedback', () => {
    it('should update feedback successfully', async () => {
      const mockFeedback = createFeedbackMock({ status: 'RESOLVED' })
      vi.mocked(request.put).mockResolvedValue({ data: mockFeedback })

      const data = {
        status: 'RESOLVED',
        admin_reply: 'Test reply'
      }

      const result = await api.updateFeedback(1, data)
      expect(result).toEqual(mockFeedback)
      expect(request.put).toHaveBeenCalledWith('/api/feedback/1', data)
    })
  })

  describe('deleteFeedback', () => {
    it('should delete feedback successfully', async () => {
      vi.mocked(request.delete).mockResolvedValue({ data: { success: true } })

      const result = await api.deleteFeedback(1)
      expect(result).toEqual({ success: true })
      expect(request.delete).toHaveBeenCalledWith('/api/feedback/1')
    })
  })

  describe('addComment', () => {
    it('should add comment successfully', async () => {
      const mockComment = {
        id: 1,
        feedback_id: 1,
        user_id: 1,
        content: 'Test comment',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
      }
      vi.mocked(request.post).mockResolvedValue({ data: mockComment })

      const result = await api.addComment(1, 'Test comment')
      expect(result).toEqual(mockComment)
      expect(request.post).toHaveBeenCalledWith('/api/feedback/1/comments', {
        feedback_id: 1,
        content: 'Test comment'
      })
    })
  })

  describe('voteFeedback', () => {
    it('should vote feedback successfully', async () => {
      const mockVote = {
        id: 1,
        feedback_id: 1,
        user_id: 1,
        is_upvote: 1,
        created_at: new Date().toISOString()
      }
      vi.mocked(request.post).mockResolvedValue({ data: mockVote })

      const result = await api.voteFeedback(1, true)
      expect(result).toEqual(mockVote)
      expect(request.post).toHaveBeenCalledWith('/api/feedback/1/vote', {
        feedback_id: 1,
        is_upvote: 1
      })
    })
  })
}) 