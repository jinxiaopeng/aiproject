import { RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'

const monitorRoutes: RouteRecordRaw[] = [
  {
    path: '/monitor',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Monitor',
        component: () => import('@/views/monitor/index.vue'),
        meta: {
          title: '监控预警',
          icon: 'monitor',
          auth: true,
          roles: ['admin'] // 只允许管理员访问
        }
      }
    ]
  }
]

export default monitorRoutes 