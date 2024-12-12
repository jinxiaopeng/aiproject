import { RouteRecordRaw } from 'vue-router'

const practiceRoutes: RouteRecordRaw = {
  path: '/practice',
  name: 'Practice',
  component: () => import('@/layout/index.vue'),
  meta: {
    title: '靶场训练',
    icon: 'target',
    requiresAuth: true
  },
  children: [
    {
      path: '',
      name: 'PracticeList',
      component: () => import('@/views/practice/index.vue'),
      meta: {
        title: '靶场列表'
      }
    },
    {
      path: ':id',
      name: 'PracticeDetail',
      component: () => import('@/views/practice/detail.vue'),
      meta: {
        title: '靶场详情'
      }
    },
    {
      path: 'stats',
      name: 'PracticeStats',
      component: () => import('@/views/practice/stats.vue'),
      meta: {
        title: '训练统计'
      }
    }
  ]
}

export default practiceRoutes 