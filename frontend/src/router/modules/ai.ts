import { RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'

const aiRoutes: Array<RouteRecordRaw> = [
  {
    path: '/ai',
    component: Layout,
    meta: {
      title: 'AI助手',
      icon: 'ai',
      roles: ['admin', 'user']
    },
    children: [
      {
        path: 'challenge',
        component: () => import('@/views/ai/components/ChallengeGenerator.vue'),
        name: 'AIChallenge',
        meta: {
          title: '靶场题目生成',
          icon: 'challenge',
          roles: ['admin', 'user']
        }
      },
      {
        path: 'learning',
        component: () => import('@/views/ai/components/LearningPathPlanner.vue'),
        name: 'AILearning',
        meta: {
          title: '学习路径规划',
          icon: 'learning',
          roles: ['admin', 'user']
        }
      }
    ]
  }
]

export default aiRoutes 