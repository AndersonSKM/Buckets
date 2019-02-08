import Vue from 'vue'
import store from './store'
import Router from 'vue-router'

import SignInView from './views/sign-in.vue'
import HomeView from './views/home.vue'
import PasswordResetView from './views/password-reset.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/sign-in',
      name: 'sign-in',
      component: SignInView,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '/password-reset',
      name: 'password-reset',
      component: PasswordResetView,
      meta: {
        requiresAuth: false
      }
    },
    {
      path: '*',
      name: '404',
      component: HomeView,
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
