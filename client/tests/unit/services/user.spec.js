import UserService from '@/plugins/services/user.js'
import API from '@/plugins/api.js'

jest.mock('@/plugins/api.js')

describe('UserService', () => {
  describe('sendPasswordResetEmail', () => {
    it('calls the correct API endpoint with provided email', async () => {
      const email = 'john.doe@test.com'
      API.post = jest.fn(() => Promise.resolve())
      await UserService.sendPasswordResetEmail(email)

      expect(API.post).toHaveBeenCalledWith('api/accounts/password/reset/', { email: email })
    })
  })

  describe('create', () => {
    it('calls the correct API endpoint with provided user data', async () => {
      const name = 'John Doe'
      const email = 'john.doe@test.com'
      const password = 'MySecretPa$$'
      API.post = jest.fn(() => Promise.resolve())
      await UserService.create({ name, email, password })

      expect(API.post).toHaveBeenCalledWith('api/accounts/users/', {
        name: name,
        email: email,
        password: password
      })
    })
  })
})
