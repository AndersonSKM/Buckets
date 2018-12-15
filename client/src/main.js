import '@babel/polyfill'
import Vue from 'vue'
import './plugins/vuetify'
import App from './App.vue'
import router from './router'
import store from './store'
import './registerServiceWorker'
import i18n from './i18n'
import VeeValidate from 'vee-validate'

Vue.config.productionTip = false

Vue.use(VeeValidate, {
  events: ''
})

new Vue({
  router,
  store,
  i18n,
  render: h => h(App)
}).$mount('#app')
