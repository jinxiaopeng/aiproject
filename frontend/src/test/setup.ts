import { config } from '@vue/test-utils'
import { vi } from 'vitest'

// Mock Element Plus
vi.mock('element-plus', async () => {
  return {
    default: {
      install: vi.fn()
    },
    ElMessage: {
      success: vi.fn(),
      error: vi.fn(),
      warning: vi.fn()
    }
  }
})

// Mock Element Plus icons
vi.mock('@element-plus/icons-vue', () => ({
  ThumbUp: vi.fn(),
  ThumbDown: vi.fn(),
  ChatRound: vi.fn()
}))

// Mock router
vi.mock('vue-router', () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn()
  }),
  useRoute: () => ({
    params: {},
    query: {}
  })
})) 