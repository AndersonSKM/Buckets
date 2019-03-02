import API from '@/plugins/api.js'

class UserService {
  static async sendPasswordResetEmail (email) {
    return API.post('api/accounts/password/reset/', {
      email: email
    })
  }

  static async create ({ name, email, password }) {
    return API.post('api/accounts/users/', {
      name,
      email,
      password
    })
  }
}

export default UserService
