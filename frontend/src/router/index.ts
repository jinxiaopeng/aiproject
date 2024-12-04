import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'
import { getToken } from '@/utils/auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/login/index.vue'),
    meta: { title: '登录', public: true }
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: { title: '首页', public: true }
  },
  {
    path: '/profile',
    component: Layout,
    redirect: '/profile/index',
    children: [
      {
        path: 'index',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: { title: '个人中心', icon: 'user' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/profile/settings.vue'),
        meta: { title: '账号设置', icon: 'setting' }
      }
    ]
  },
  {
    path: '/dashboard',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', icon: 'dashboard' }
      }
    ]
  },
  {
    path: '/courses',
    component: Layout,
    redirect: '/courses/list',
    meta: { title: '课程管理', icon: 'education' },
    children: [
      {
        path: 'list',
        name: 'CourseList',
        component: () => import('@/views/course/CourseList.vue'),
        meta: { title: '课程列表' }
      },
      {
        path: ':id',
        name: 'CourseDetail',
        component: () => import('@/views/course/CourseDetail.vue'),
        meta: { title: '课程详情' }
      }
    ]
  },
  {
    path: '/labs',
    component: Layout,
    redirect: '/labs/list',
    meta: { title: '实验室', icon: 'experiment' },
    children: [
      {
        path: 'list',
        name: 'LabList',
        component: () => import('@/views/lab/LabList.vue'),
        meta: { title: '实验室列表' }
      },
      {
        path: ':id',
        name: 'LabDetail',
        component: () => import('@/views/lab/LabDetail.vue'),
        meta: { title: '实验详情' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - Web安全智能学习平台`

  console.log('Navigating to:', to.path)
  console.log('Route matched:', to.matched)

  // 检查是否需要登录
  const token = getToken()
  if (!to.meta.public && !token) {
    console.log('No token found, redirecting to login')
    next('/login')
  } else {
    next()
  }
})

export default router 