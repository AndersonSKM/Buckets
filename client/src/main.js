import '@babel/polyfill'
import '@/plugins/vuetify'
import Vue from 'vue'
import VeeValidate from 'vee-validate'
import App from '@/App.vue'
import router from '@/router.js'
import store from '@/store.js'
import i18n from '@/i18n.js'
import Services from '@/plugins/services/index.js'

Vue.config.productionTip = false

Vue.use(VeeValidate, {
  events: ''
})

Vue.use(Services, {
})

new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
