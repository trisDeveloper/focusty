import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

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
      component: () => import('../views/CalendarView.vue')
    },
    {
      path: '/signup',
      name: 'sign up',
      component: () => import('../components/user/sign-up.vue')
    },
    {
      path: '/login',
      name: 'log in',
      component: () => import('../components/user/log-in.vue')
    },
    {
      path: '/profile',
      name: 'My profile',
      component: () => import('../components/user/user-profile.vue')
    },

    {
      path: '/pomodoro',
      name: 'Pomodoro',
      component: () => import('../views/pomodoroView.vue')
    },
    {
      path: '/journey',
      name: 'journey',
      // route level code-splitting
      // this generates a separate chunk (about.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../components/user-charts.vue')
    }
  ]
})

export default router
