import Vue from 'vue'
import Router from 'vue-router'

import store from '@/store.js'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/home.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/sign-in',
      name: 'sign-in',
      component: () => import('@/views/sign-in.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/password-reset',
      name: 'password-reset',
      component: () => import('@/views/password-reset.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/sign-up',
      name: 'sign-up',
      component: () => import('@/views/sign-up.vue'),
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '*',
      name: '404',
      component: () => import('@/views/home.vue'),
      meta: {
        requiresAuth: true
      }
    }
  ]
})

router.beforeEach(
  (to, from, next) => {
    if (to.matched.some(record => !record.meta.requiresAuth) && store.getters['auth/isAuthenticated']) {
      next({
        path: '/'
      })
    } else if (to.matched.some(record => record.meta.requiresAuth) && !store.getters['auth/isAuthenticated']) {
      next({
        path: '/sign-in'
      })
    } else {
      store.dispatch('auth/tryRefreshToken')
      next()
    }
  }
)

export default router
