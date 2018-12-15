import Vue from 'vue'
import store from './store'
import Router from 'vue-router'

import SignInView from './views/sign-in.vue'
import PasswordForgotView from './views/password-forgot.vue'
import HomeView from './views/home.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/sign-in',
      name: 'sign-in',
      component: SignInView,
      meta: { requiresAuth: false }
    },
    {
      path: '/password-forgot',
      name: 'password-forgot',
      component: PasswordForgotView,
      meta: { requiresAuth: false }
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '*',
      name: '404',
      component: HomeView,
      meta: { requiresAuth: true }
    }
  ]
})

router.beforeEach(
  (to, from, next) => {
    if (to.matched.some(record => !record.meta.requiresAuth) && store.getters['auth/isAuthenticated']) {
      next({
        path: '/home'
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
