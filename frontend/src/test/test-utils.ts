import { mount, type VueWrapper } from '@vue/test-utils'
import { createPinia, type Pinia } from 'pinia'
import ElementPlus from 'element-plus'
import type { Component } from 'vue'

interface MountOptions {
  props?: Record<string, any>
  global?: Record<string, any>
}

export const createTestingPinia = (): Pinia => {
  return createPinia()
}

export const mountComponent = (
  component: Component,
  options: MountOptions = {}
): VueWrapper => {
  const pinia = createTestingPinia()
  
  return mount(component, {
    props: options.props || {},
    global: {
      plugins: [pinia, ElementPlus],
      ...options.global
    }
  })
}

export const createFeedbackMock = (override = {}) => ({
  id: 1,
  user_id: 1,
  entity_id: 1,
  feedback_type: 'CONTENT',
  content: 'Test feedback content',
  rating: 4,
  status: 'PENDING',
  admin_reply: null,
  created_at: new Date().toISOString(),
  updated_at: new Date().toISOString(),
  ...override
})

export const createFeedbackDetailMock = (override = {}) => ({
  ...createFeedbackMock(),
  comments: [],
  votes: [],
  upvotes: 0,
  downvotes: 0,
  ...override
}) 