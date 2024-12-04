import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

// 路由配置
const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页'
    }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录',
      guest: true
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: {
      title: '注册',
      guest: true
    }
  },
  {
    path: '/courses',
    name: 'Courses',
    component: () => import('@/views/courses/CourseList.vue'),
    meta: {
      title: '课程中心'
    }
  },
  {
    path: '/course/:id',
    name: 'CourseDetail',
    component: () => import('@/views/courses/CourseDetail.vue'),
    meta: {
      title: '课程详情'
    }
  },
  {
    path: '/labs',
    name: 'Labs',
    component: () => import('@/views/labs/LabList.vue'),
    meta: {
      title: '在线实验'
    }
  },
  {
    path: '/lab/:id',
    name: 'LabDetail',
    component: () => import('@/views/labs/LabDetail.vue'),
    meta: {
      title: '实验详情',
      requiresAuth: true
    }
  },
  {
    path: '/knowledge',
    name: 'Knowledge',
    component: () => import('@/views/Knowledge.vue'),
    meta: {
      title: '知识库'
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/Profile.vue'),
    meta: {
      title: '个人资料',
      requiresAuth: true
    }
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: {
      title: '系统设置',
      requiresAuth: true
    }
  },
  // 管理员路由
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/Layout.vue'),
    meta: {
      title: '管理后台',
      requiresAuth: true,
      requiresAdmin: true
    },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: {
          title: '仪表盘'
        }
      },
      {
        path: 'users',
        name: 'UserManagement',
        component: () => import('@/views/admin/UserManagement.vue'),
        meta: {
          title: '用户管理'
        }
      },
      {
        path: 'lessons',
        name: 'LessonManagement',
        component: () => import('@/views/admin/LessonManagement.vue'),
        meta: {
          title: '课时管理'
        }
      }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '404'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 开始加载进度条
  NProgress.start()
  
  // 设置页面标题
  document.title = `${to.meta.title} - ${import.meta.env.VITE_APP_TITLE}`
  
  const userStore = useUserStore()
  const isAuthenticated = !!userStore.token
  const isAdmin = userStore.userInfo?.role === 'admin'
  
  // 如果用户已登录但没有用户信息，尝试获取用户信息
  if (isAuthenticated && !userStore.userInfo) {
    try {
      await userStore.loadUserInfo()
    } catch (error) {
      // 如果获取用户信息失败，可能是token过期，清除登录状态
      userStore.logout()
      next('/login')
      return
    }
  }
  
  // 检查是否需要登录权限
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }
  
  // 检查是否需要管理员权限
  if (to.meta.requiresAdmin && !isAdmin) {
    next('/')
    return
  }
  
  // 已登录用户不能访问游客页面
  if (to.meta.guest && isAuthenticated) {
    next('/')
    return
  }
  
  next()
})

router.afterEach(() => {
  // 结束加载进度条
  NProgress.done()
})

export default router 