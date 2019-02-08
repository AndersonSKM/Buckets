import AuthService from '@/plugins/services/auth.js'
import UserService from '@/plugins/services/user.js'

const Services = {
  install (Vue, options) {
    Vue.prototype.$services = {
      auth: AuthService,
      user: UserService
    }
  }
}

export default Services
