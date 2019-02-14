import UserService from '@/plugins/services/user.js'
import API from '@/plugins/api.js'

jest.mock('@/plugins/api.js')

describe('sendPasswordResetEmail', () => {
  it('calls the correct API endpoint with provided email', async () => {
    const email = 'john.doe@test.com'
    API.post = jest.fn(() => Promise.resolve())
    await UserService.sendPasswordResetEmail(email)

    expect(API.post).toHaveBeenCalledWith('api/accounts/password/reset/', { email: email })
  })
})
