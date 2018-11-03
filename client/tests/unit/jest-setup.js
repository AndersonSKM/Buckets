import Vue from 'vue'
import Vuetify from 'vuetify'
import VeeValidate from 'vee-validate'
import Vuex from 'vuex'

Vue.use(Vuetify)
Vue.use(VeeValidate)
Vue.use(Vuex)

Vue.config.productionTip = false

const { getComputedStyle } = window
window.getComputedStyle = (node) => {
  return Object.assign(getComputedStyle(node), {
    transitionDelay: '',
    animationDelay: '',
    transitionDuration: '',
    animationDuration: ''
  })
}
