import { describe, it, expect, vi, beforeEach } from 'vitest'
import { ElMessage } from 'element-plus'
import FeedbackList from '../FeedbackList.vue'
import FeedbackDetail from '../FeedbackDetail.vue'
import FeedbackForm from '../FeedbackForm.vue'
import { useFeedbackStore } from '@/stores/feedback'
import { mountComponent, createFeedbackMock, createFeedbackDetailMock } from '@/test/test-utils'

describe('Feedback Components', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('FeedbackForm', () => {
    it('should render correctly', () => {
      const wrapper = mountComponent(FeedbackForm, {
        props: {
          entityId: 1
        }
      })
      
      expect(wrapper.find('.feedback-form').exists()).toBe(true)
      expect(wrapper.find('.el-select').exists()).toBe(true)
      expect(wrapper.find('.el-input').exists()).toBe(true)
      expect(wrapper.find('.el-rate').exists()).toBe(true)
    })

    it('should validate form fields', async () => {
      const wrapper = mountComponent(FeedbackForm, {
        props: {
          entityId: 1
        }
      })

      await wrapper.find('form').trigger('submit')
      
      const errorMessages = wrapper.findAll('.el-form-item__error')
      expect(errorMessages.length).toBeGreaterThan(0)
    })

    it('should submit feedback successfully', async () => {
      const wrapper = mountComponent(FeedbackForm, {
        props: {
          entityId: 1
        }
      })

      const store = useFeedbackStore()
      const createFeedbackSpy = vi.spyOn(store, 'createFeedback').mockResolvedValue(createFeedbackMock())
      
      await wrapper.find('.el-select').setValue('CONTENT')
      await wrapper.find('.el-input').setValue('Test feedback content')
      await wrapper.find('.el-rate').setValue(4)
      await wrapper.find('form').trigger('submit')

      expect(createFeedbackSpy).toHaveBeenCalledWith({
        entity_id: 1,
        feedback_type: 'CONTENT',
        content: 'Test feedback content',
        rating: 4
      })
      expect(ElMessage.success).toHaveBeenCalledWith('反馈提交成功')
    })
  })

  describe('FeedbackList', () => {
    it('should render feedback list correctly', async () => {
      const store = useFeedbackStore()
      store.feedbackList = [createFeedbackMock()]

      const wrapper = mountComponent(FeedbackList, {
        props: {
          entityId: 1
        }
      })

      expect(wrapper.find('.feedback-list').exists()).toBe(true)
      expect(wrapper.findAll('.feedback-item')).toHaveLength(1)
    })

    it('should filter feedback by type', async () => {
      const store = useFeedbackStore()
      store.feedbackList = [
        createFeedbackMock({ feedback_type: 'CONTENT' }),
        createFeedbackMock({ id: 2, feedback_type: 'BUG' })
      ]

      const wrapper = mountComponent(FeedbackList, {
        props: {
          entityId: 1
        }
      })

      await wrapper.find('.el-select').setValue('CONTENT')
      expect(wrapper.findAll('.feedback-item')).toHaveLength(1)
    })
  })

  describe('FeedbackDetail', () => {
    it('should render feedback detail correctly', async () => {
      const store = useFeedbackStore()
      const mockFeedback = createFeedbackDetailMock()
      store.currentFeedback = mockFeedback

      const wrapper = mountComponent(FeedbackDetail, {
        props: {
          feedbackId: 1
        }
      })

      expect(wrapper.find('.feedback-content').text()).toBe(mockFeedback.content)
      expect(wrapper.find('.feedback-rating').exists()).toBe(true)
    })

    it('should handle voting', async () => {
      const store = useFeedbackStore()
      store.currentFeedback = createFeedbackDetailMock()

      const wrapper = mountComponent(FeedbackDetail, {
        props: {
          feedbackId: 1
        }
      })

      const voteFeedbackSpy = vi.spyOn(store, 'voteFeedback').mockResolvedValue(undefined)
      
      await wrapper.find('.vote-button').trigger('click')
      expect(voteFeedbackSpy).toHaveBeenCalledWith(1, true)
      expect(ElMessage.success).toHaveBeenCalledWith('点赞成功')
    })

    it('should handle admin actions', async () => {
      const store = useFeedbackStore()
      store.currentFeedback = createFeedbackDetailMock()

      const wrapper = mountComponent(FeedbackDetail, {
        props: {
          feedbackId: 1
        }
      })

      const updateFeedbackSpy = vi.spyOn(store, 'updateFeedback').mockResolvedValue(undefined)
      
      await wrapper.find('.admin-select').setValue('RESOLVED')
      await wrapper.find('.admin-input').setValue('Admin reply')
      await wrapper.find('.admin-submit').trigger('click')

      expect(updateFeedbackSpy).toHaveBeenCalledWith(1, {
        status: 'RESOLVED',
        admin_reply: 'Admin reply'
      })
      expect(ElMessage.success).toHaveBeenCalledWith('更新成功')
    })
  })
}) 