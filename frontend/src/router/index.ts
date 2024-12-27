import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import Layout from '@/layout/index.vue'
import { getToken } from '@/utils/auth'
import { useAuthStore } from '@/stores/auth'
import learningRoutes from './modules/learning'
import monitorRoutes from './modules/monitor'
import aiRoutes from './modules/ai'

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
        path: 'profile',
        name: 'Profile',
        component: () => import('@/views/profile/index.vue'),
        meta: { title: '个人中心', icon: 'user', auth: true }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/profile/settings.vue'),
        meta: { title: '账号设置', icon: 'setting', auth: true }
      },
      {
        path: 'courses',
        name: 'Courses',
        component: () => import('@/views/courses/index.vue'),
        meta: { title: '课程学习', icon: 'reading', auth: false }
      },
      {
        path: 'courses/:id',
        name: 'CourseDetail',
        component: () => import('@/views/courses/detail.vue'),
        meta: { title: '课程详情', auth: false }
      },
      {
        path: 'courses/:courseId/learn',
        name: 'CourseLearn',
        component: () => import('@/views/courses/learn/index.vue'),
        meta: { title: '课程学习', auth: false }
      },
      {
        path: 'labs',
        name: 'Labs',
        component: () => import('@/views/lab/LabList.vue'),
        meta: { title: '实验室', icon: 'monitor', auth: true }
      },
      {
        path: 'labs/:id',
        name: 'LabDetail',
        component: () => import('@/views/lab/LabDetail.vue'),
        meta: { title: '实验详情', auth: true }
      },
      {
        path: 'knowledge',
        name: 'Knowledge',
        component: () => import('@/views/knowledge/index.vue'),
        meta: { title: '知识图谱', icon: 'knowledge', auth: true }
      },
      {
        path: 'challenge',
        component: () => import('@/views/challenge/index.vue'),
        meta: { title: '靶场训练', icon: 'target', auth: true },
        alias: '/practice'
      },
      {
        path: 'daily-challenge',
        name: 'DailyChallenge',
        component: () => import('@/views/daily-challenge/index.vue'),
        meta: { title: '每日挑战', auth: true }
      },
      {
        path: 'challenge/stats',
        name: 'ChallengeStats',
        component: () => import('@/views/challenge/Stats.vue'),
        meta: { title: '训练统计', auth: true },
        alias: '/practice/stats'
      },
      {
        path: 'challenge/:id',
        name: 'ChallengeDetail',
        component: () => import('@/views/challenge/ChallengeDetail.vue'),
        meta: { title: '靶场详情', auth: true },
        alias: '/practice/:id'
      },
      {
        path: 'challenge/add',
        name: 'AddChallenge',
        component: () => import('@/views/challenge/AddChallenge.vue'),
        meta: { title: '添加题库', auth: true }
      },
      {
        path: 'achievements',
        name: 'Achievements',
        component: () => import('@/views/achievements/index.vue'),
        meta: { 
          title: '成就徽章', 
          icon: 'medal',
          auth: true 
        }
      },
      {
        path: 'monitor',
        name: 'Monitor',
        component: () => import('@/views/monitor/LearningMonitor.vue'),
        meta: { title: '系统监控', icon: 'monitor', auth: true }
      },
      {
        path: '/monitor',
        name: 'LearningMonitor',
        component: () => import('@/views/monitor/LearningMonitor.vue'),
        meta: {
          title: '学习监控',
          requiresAuth: true
        }
      },
      {
        path: '/challenge',
        name: 'challenge',
        component: () => import('@/views/challenge/index.vue')
      },
      {
        path: '/universe',
        name: 'Universe',
        component: () => import('@/views/universe/index.vue'),
        meta: {
          title: '知识宇宙',
          requiresAuth: true
        }
      },
      {
        path: 'learning/ai-assistant',
        name: 'AILearningAssistant',
        component: () => import('@/views/ai/AiAssistant.vue'),
        meta: { 
          title: 'AI学习助手', 
          icon: 'ai',
          auth: true 
        }
      },
      {
        path: 'practice/ai-assistant',
        name: 'AIPracticeAssistant',
        component: () => import('@/views/ai/AiAssistant.vue'),
        meta: { 
          title: 'AI靶场助手', 
          icon: 'ai',
          auth: true 
        }
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
  },
  ...learningRoutes,
  ...monitorRoutes,
  ...aiRoutes
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
    if (to.meta.auth === true) {
      // 需要认证的页面重定向到登录
      next({ path: '/auth/login', query: { redirect: to.fullPath } })
    } else {
      // 不需要认证的页面直接访问
      next()
    }
    return
  }

  // 已登录用户
  if (to.path === '/auth/login' || to.path === '/auth/register') {
    // 已登录用户访问登录或注册页面，重定向到首页
    next('/')
    return
  }

  // 获取用户信息
  if (!authStore.userInfo) {
    try {
      await authStore.getUserInfo()
      next()
    } catch (error) {
      // token失效，除登录状态
      authStore.logout()
      next({ path: '/auth/login', query: { redirect: to.fullPath } })
    }
  } else {
    next()
  }
})

export default router