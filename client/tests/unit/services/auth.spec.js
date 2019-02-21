import AuthService from '@/plugins/services/auth.js'
import API from '@/plugins/api.js'

jest.mock('@/plugins/api.js')
const fakeToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNzcxYzA2NzUtMDllMi00ODg1LTlhZGUtZTk4NDNmYTk5NWIyIiwidXNlcm5hbWUiOiJhbmRlcnNvbi5rcnM5NUBnbWFpbC5jb20iLCJleHAiOjE1NDAxMjY5NDIsImVtYWlsIjoiYW5kZXJzb24ua3JzOTVAZ21haWwuY29tIiwib3JpZ19pYXQiOjE1NDAxMjYwNDJ9.xtGQ2cTfd92DHNgmm2l2TZOtvR0Fl3hLu08X9CFb6hQ'

describe('createToken', () => {
  it('calls the correct API endpoint with provided credentials', async () => {
    API.post = jest.fn(() => Promise.resolve())
    const credentials = {
      email: 'john.doe@test.com',
      password: 'john.doe'
    }
    await AuthService.createToken(credentials)

    expect(API.post).toHaveBeenCalledWith('api/auth/jwt/create/', credentials)
  })
})

describe('refreshToken', () => {
  it('calls the API endpoint with provided token and returns the refreshed token when status OK', async () => {
    const newToken = '6640094c-6803-40f6-a219-bb798414d3a6'
    API.post = jest.fn(() => Promise.resolve(
      {
        status: 200,
        data: {
          token: newToken
        }
      }
    ))
    const result = await AuthService.refreshToken(fakeToken)

    expect(result).toEqual(newToken)
    expect(API.post).toHaveBeenCalledWith('api/auth/jwt/refresh/', {
      token: fakeToken
    })
  })

  it('returns an empty string when API returns an error', async () => {
    API.post = jest.fn(() => {
      throw new Error('Bad request')
    })
    const result = await AuthService.refreshToken(fakeToken)

    expect(result).toEqual('')
  })
})

describe('decodedToken', () => {
  it('returns a decoded token correctly', () => {
    const decoded = AuthService.decodedToken(fakeToken)

    expect(decoded).toEqual({
      user_id: '771c0675-09e2-4885-9ade-e9843fa995b2',
      username: 'anderson.krs95@gmail.com',
      exp: 1540126942000,
      email: 'anderson.krs95@gmail.com',
      orig_iat: 1540126042000
    })
  })

  it('returns an empty string if encoded token is empty', () => {
    const decoded = AuthService.decodedToken('')
    expect(decoded).toEqual('')
  })
})

describe('isExpiredToken', () => {
  it('returns true if token is empty', () => {
    expect(AuthService.isExpiredToken('')).toBeTruthy()
  })

  it('returns true if token was created after fifteen minutes', () => {
    global.Date.now = jest.fn(() => {
      return new Date('2018-10-21 10:00:00').getTime()
    })
    AuthService.decodedToken = jest.fn(() => {
      return {
        exp: new Date('2018-10-21 09:00:00').getTime()
      }
    })

    expect(AuthService.isExpiredToken(fakeToken)).toBeTruthy()
  })

  it('returns false if token was created before fifteen minutes', () => {
    global.Date.now = jest.fn(() => {
      return new Date('2018-10-21 10:05:00').getTime()
    })
    AuthService.decodedToken = jest.fn(() => {
      return {
        exp: new Date('2018-10-21 10:15:00').getTime()
      }
    })

    expect(AuthService.isExpiredToken(fakeToken)).toBeFalsy()
  })
})

describe('canRefreshToken', () => {
  it('returns false if token is empty', () => {
    expect(AuthService.canRefreshToken('')).toBeFalsy()
  })

  it('returns false if token is expired', () => {
    AuthService.isExpiredToken = jest.fn(() => true)
    expect(AuthService.canRefreshToken(fakeToken)).toBeFalsy()
  })

  it('returns false if token was created after four hours', () => {
    global.Date.now = jest.fn(() => {
      return new Date('2018-10-21 10:13:30').getTime()
    })
    AuthService.isExpiredToken = jest.fn(() => false)
    AuthService.decodedToken = jest.fn(() => {
      return {
        exp: new Date('2018-10-21 10:15:00').getTime(),
        orig_iat: new Date('2018-10-21 05:00:00').getTime()
      }
    })

    expect(AuthService.canRefreshToken(fakeToken)).toBeFalsy()
  })

  it('returns false if token does not have thirteen minutes', () => {
    global.Date.now = jest.fn(() => {
      return new Date('2018-10-21 10:12:59').getTime()
    })
    AuthService.isExpiredToken = jest.fn(() => false)
    AuthService.decodedToken = jest.fn(() => {
      return {
        exp: new Date('2018-10-21 10:15:00').getTime(),
        orig_iat: new Date('2018-10-21 10:00:00').getTime()
      }
    })

    expect(AuthService.canRefreshToken(fakeToken)).toBeFalsy()
  })

  it('returns true if token was created within four hours and has more than thirteen minutes', () => {
    global.Date.now = jest.fn(() => {
      return new Date('2018-10-21 10:13:01').getTime()
    })
    AuthService.isExpiredToken = jest.fn(() => false)
    AuthService.decodedToken = jest.fn(() => {
      return {
        exp: new Date('2018-10-21 10:15:00').getTime(),
        orig_iat: new Date('2018-10-21 10:00:00').getTime()
      }
    })

    expect(AuthService.canRefreshToken(fakeToken)).toBeTruthy()
  })
})
