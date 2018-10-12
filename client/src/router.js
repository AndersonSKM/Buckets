import Vue from 'vue'
import store from './store'
import Router from 'vue-router'
import SignIn from './views/sign-in.vue'
import Home from './views/home.vue'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/sign-in',
      name: 'sign-in',
      component: SignIn,
      meta: { requiresAuth: false }
    },
    {
      path: '/home',
      name: 'home',
      component: Home,
      meta: { requiresAuth: true }
    },
    { // Always leave this as last one
      path: '*',
      name: '404',
      component: Home,
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
