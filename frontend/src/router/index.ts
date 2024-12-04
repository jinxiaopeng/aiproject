import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'
import { getToken } from '@/utils/auth'
import { useAuthStore } from '@/stores/auth'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Home',
        component: () => import('@/views/home/index.vue'),
        meta: { title: '首页', auth: false }
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', icon: 'dashboard', auth: true }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: { title: '个人中心', icon: 'user', auth: true }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/profile/settings.vue'),
        meta: { title: '账号设置', icon: 'setting' }
      },
      {
        path: 'courses',
        name: 'Courses',
        component: () => import('@/views/course/CourseList.vue'),
        meta: { title: '课程列表' }
      },
      {
        path: 'courses/:id',
        name: 'CourseDetail',
        component: () => import('@/views/course/CourseDetail.vue'),
        meta: { title: '课程详情' }
      },
      {
        path: 'labs',
        name: 'Labs',
        component: () => import('@/views/lab/LabList.vue'),
        meta: { title: '实验室列表' }
      },
      {
        path: 'labs/:id',
        name: 'LabDetail',
        component: () => import('@/views/lab/LabDetail.vue'),
        meta: { title: '实验详情' }
      }
    ]
  },
  {
    path: '/auth',
    component: () => import('@/layout/auth.vue'),
    children: [
      {
        path: 'login',
        name: 'Login',
        component: () => import('@/views/auth/login.vue'),
        meta: { title: '登录', auth: false }
      },
      {
        path: 'register',
        name: 'Register',
        component: () => import('@/views/auth/register.vue'),
        meta: { title: '注册', auth: false }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  document.title = `${to.meta.title} - Web安全智能学习平台`

  const token = getToken()
  const authStore = useAuthStore()

  // 未登录用户
  if (!token) {
    if (to.meta.auth === false) {
      // 允许访问不需要认证的页面（首页、登录、注册）
      next()
    } else {
      // 需要认证的页面重定向到登录
      next('/auth/login')
    }
    return
  }

  // 已登录用户
  if (to.path === '/auth/login' || to.path === '/auth/register') {
    // 已登录用户访问登录或注册页面，重定向到仪表盘
    next('/dashboard')
    return
  }

  // 获取用户信息
  if (!authStore.userInfo) {
    try {
      await authStore.getUserInfo()
    } catch (error) {
      // token失效，清除登录状态
      authStore.logout()
      next('/auth/login')
      return
    }
  }

  next()
})

export default router 