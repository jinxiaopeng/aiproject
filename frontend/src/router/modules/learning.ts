import { RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'

const learningRoutes: RouteRecordRaw[] = [
  {
    path: '/learning-path',
    component: Layout,
    children: [
      {
        path: '',
        name: 'LearningPath',
        component: () => import('@/views/learning-path/index.vue'),
        meta: {
          title: '学习路径',
          requiresAuth: true
        }
      },
      {
        path: 'courses/:courseId',
        name: 'CourseDetail',
        component: () => import('@/views/learning-path/course/index.vue'),
        meta: {
          title: '课程详情',
          requiresAuth: true
        }
      }
    ]
  }
]

export default learningRoutes 