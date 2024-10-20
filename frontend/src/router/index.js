import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/home-view.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/calendar',
      name: 'calendar',
      component: () => import('../views/calendar-view.vue')
    },
    {
      path: '/signup',
      name: 'sign up',
      component: () => import('../views/user/sign-up.vue')
    },
    {
      path: '/login',
      name: 'log in',
      component: () => import('../views/user/log-in.vue')
    },
    {
      path: '/profile',
      name: 'My profile',
      component: () => import('../views/user/user-profile.vue')
    },

    {
      path: '/pomodoro',
      name: 'Pomodoro',
      component: () => import('../views/pomodoro-view.vue')
    },
    {
      path: '/journey',
      name: 'journey',
      component: () => import('../views/journey-view.vue')
    }
  ]
})

export default router
