import API from '@/plugins/api.js'

class UserService {
  async sendPasswordResetEmail (email) {
    return API.post('api/accounts/password/reset/', {
      email: email
    })
  }
}

export default new UserService()
