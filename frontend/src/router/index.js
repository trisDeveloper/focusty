import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
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
      component: () => import('../components/sign-up.vue')
    },
    {
      path: '/login',
      name: 'log in',
      component: () => import('../components/log-in.vue')
    },
    {
      path: '/profile',
      name: 'My profile',
      component: () => import('../components/user-profile.vue')
    } /*,

  {
    path: "/habits",
    name: "habits",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/HabitView.vue"),
  } 
  {
    path: "/journey",
    name: "journey",
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import("../views/JourneyView.vue"),
  },*/
  ]
})

export default router
