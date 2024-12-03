import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/learning',
      name: 'learning',
      component: () => import('@/views/Learning.vue')
    },
    {
      path: '/labs',
      name: 'labs',
      component: () => import('@/views/Labs.vue')
    },
    {
      path: '/knowledge',
      name: 'knowledge',
      component: () => import('@/views/Knowledge.vue')
    }
  ]
})

export default router 