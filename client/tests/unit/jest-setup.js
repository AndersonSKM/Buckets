import Vue from 'vue'
import Vuetify from 'vuetify'
import VeeValidate from 'vee-validate'
import Vuex from 'vuex'
import VueTestUtils from '@vue/test-utils'

Vue.config.productionTip = false
Vue.use(Vuetify)
Vue.use(Vuex)
Vue.use(VeeValidate, {
  events: ''
})

VueTestUtils.config.mocks['$t'] = (msg) => msg
VueTestUtils.config.mocks['$router'] = {
  push: jest.fn()
}
VueTestUtils.config.mocks['$services'] = jest.fn()
VueTestUtils.config.mocks['$store'] = {
  dispatch: jest.fn(() => Promise.resolve())
}

const { getComputedStyle } = window
window.getComputedStyle = (node) => {
  return Object.assign(getComputedStyle(node), {
    transitionDelay: '',
    animationDelay: '',
    transitionDuration: '',
    animationDuration: ''
  })
}
