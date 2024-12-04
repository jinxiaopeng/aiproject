import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
      meta: {
        title: '首页'
      }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/Login.vue'),
      meta: {
        title: '登录',
        guest: true
      }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/Register.vue'),
      meta: {
        title: '注册',
        guest: true
      }
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/views/ForgotPassword.vue'),
      meta: {
        title: '忘记密码',
        guest: true
      }
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('@/views/Terms.vue'),
      meta: {
        title: '服务条款'
      }
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('@/views/Privacy.vue'),
      meta: {
        title: '隐私政策'
      }
    },
    {
      path: '/404',
      name: 'not-found',
      component: () => import('@/views/NotFound.vue'),
      meta: {
        title: '页面未找到'
      }
    },
    {
      path: '/403',
      name: 'forbidden',
      component: () => import('@/views/Forbidden.vue'),
      meta: {
        title: '无权访问'
      }
    },
    {
      path: '/:pathMatch(.*)*',
      redirect: '/404'
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 设置页面标题
  document.title = `${to.meta.title} - CyberLabs`
  
  // 未登录用户只能访问 guest 页面和公共页面
  if (!to.meta.guest && !['terms', 'privacy'].includes(to.name as string) && !authStore.isAuthenticated) {
    next('/login')
    return
  }
  
  // 已登录用户不能访问 guest 页面
  if (to.meta.guest && authStore.isAuthenticated) {
    next('/')
    return
  }
  
  next()
})

export default router 