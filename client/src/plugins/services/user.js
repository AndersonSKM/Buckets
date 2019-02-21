import API from '@/plugins/api.js'

class UserService {
  async sendPasswordResetEmail (email) {
    return API.post('api/accounts/password/reset/', {
      email: email
    })
  }

  async create ({ name, email, password }) {
    return API.post('api/accounts/users/', {
      name,
      email,
      password
    })
  }
}

export default new UserService()
