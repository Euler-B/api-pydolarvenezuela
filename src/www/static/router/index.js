import DashboardView from '@/views/DashboardView.vue'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import PricingView from '@/views/PricingView.vue'
import Cookies from 'js-cookie'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: HomeView,
    },
    {
      path: '/pricing',
      component: PricingView,
    },
    {
      path: '/login',
      component: LoginView,
    },
    {
      path: '/dashboard',
      component: DashboardView,
      children: [
        {
          path: 'usage',
          component: () => import('@/components/dashboard/Usage.vue')
        },
        {
          path: 'profile',
          component: () => import('@/components/dashboard/Profile.vue')
        }
      ],
      beforeEnter: (to, from, next) => {
          if (!Cookies.get('token')) {
              next('/login');
          } else {
              next();
          }
      }
    }
  ],
})

export default router
