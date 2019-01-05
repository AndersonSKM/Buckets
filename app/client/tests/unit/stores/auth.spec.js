import store from '@/stores/auth.js'
import mockAxios from 'axios'

const token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNzcxYzA2NzUtMDllMi00ODg1LTlhZGUtZTk4NDNmYTk5NWIyIiwidXNlcm5hbWUiOiJhbmRlcnNvbi5rcnM5NUBnbWFpbC5jb20iLCJleHAiOjE1NDAxMjY5NDIsImVtYWlsIjoiYW5kZXJzb24ua3JzOTVAZ21haWwuY29tIiwib3JpZ19pYXQiOjE1NDAxMjYwNDJ9.xtGQ2cTfd92DHNgmm2l2TZOtvR0Fl3hLu08X9CFb6hQ'

describe('State', () => {
  describe('initial', () => {
    it('returns the state with all properties blank', () => {
      expect(store.state).toEqual({
        token: '',
        email: '',
        first_name: '',
        last_name: ''
      })
    })
  })
})

describe('Mutations', () => {
  describe('SET_TOKEN', () => {
    it('defines token state correctly', () => {
      store.mutations.SET_TOKEN(store.state, token)
      expect(store.state.token).toEqual(token)
    })
  })
})

describe('Getters', () => {
  describe('decodedToken', () => {
    it('returns a decoded token correctly', () => {
      const state = {
        token: token
      }
      const decoded = store.getters.decodedToken(state)
      expect(decoded).toEqual({
        user_id: '771c0675-09e2-4885-9ade-e9843fa995b2',
        username: 'anderson.krs95@gmail.com',
        exp: 1540126942000,
        email: 'anderson.krs95@gmail.com',
        orig_iat: 1540126042000
      })
    })

    it('returns null if token state is empty', () => {
      const state = {
        token: ''
      }
      const decoded = store.getters.decodedToken(state)
      expect(decoded).toBeNull()
    })
  })

  describe('isExpiredToken', () => {
    it('returns true if token is null', () => {
      const getters = {
        decodedToken: null
      }
      const state = {
        token: null
      }

      expect(store.getters.isExpiredToken(state, getters)).toBeTruthy()
    })

    it('returns true if token was created after fifteen minutes', () => {
      global.Date.now = jest.fn(() => {
        return new Date('2018-10-21 10:00:00').getTime()
      })
      const getters = {
        decodedToken: {
          exp: new Date('2018-10-21 09:00:00').getTime()
        }
      }

      expect(store.getters.isExpiredToken({}, getters)).toBeTruthy()
    })

    it('returns false if token was created before fifteen minutes', () => {
      global.Date.now = jest.fn(() => {
        return new Date('2018-10-21 10:05:00').getTime()
      })
      const getters = {
        decodedToken: {
          exp: new Date('2018-10-21 10:15:00').getTime()
        }
      }

      expect(store.getters.isExpiredToken({}, getters)).toBeFalsy()
    })
  })

  describe('isAuthenticated', () => {
    it('returns false if token is blank', () => {
      const state = {
        token: ''
      }
      const getters = {
        isExpiredToken: false
      }

      expect(store.getters.isAuthenticated(state, getters)).toBeFalsy()
    })

    it('returns false if token is expired', () => {
      const state = {
        token: token
      }
      const getters = {
        isExpiredToken: true
      }

      expect(store.getters.isAuthenticated(state, getters)).toBeFalsy()
    })

    it('returns true with a valid token', () => {
      const state = {
        token: token
      }
      const getters = {
        isExpiredToken: false
      }

      expect(store.getters.isAuthenticated(state, getters)).toBeTruthy()
    })
  })

  describe('canRefreshToken', () => {
    it('returns false if user is not authenticated', () => {
      const getters = {
        isAuthenticated: false
      }
      expect(store.getters.canRefreshToken({}, getters)).toBeFalsy()
    })

    it('returns false if token was created after four hours', () => {
      global.Date.now = jest.fn(() => {
        return new Date('2018-10-21 10:13:30').getTime()
      })
      const getters = {
        isAuthenticated: true,
        decodedToken: {
          exp: new Date('2018-10-21 10:15:00').getTime(),
          orig_iat: new Date('2018-10-21 05:00:00').getTime()
        }
      }

      expect(store.getters.canRefreshToken({}, getters)).toBeFalsy()
    })

    it("returns false if token doesn't have thirteen minutes", () => {
      global.Date.now = jest.fn(() => {
        return new Date('2018-10-21 10:12:59').getTime()
      })
      const getters = {
        isAuthenticated: true,
        decodedToken: {
          exp: new Date('2018-10-21 10:15:00').getTime(),
          orig_iat: new Date('2018-10-21 10:00:00').getTime()
        }
      }

      expect(store.getters.canRefreshToken({}, getters)).toBeFalsy()
    })

    it('returns true if token was created within four hours and has more than thirteen minutes', () => {
      global.Date.now = jest.fn(() => {
        return new Date('2018-10-21 10:13:01').getTime()
      })
      const getters = {
        isAuthenticated: true,
        decodedToken: {
          exp: new Date('2018-10-21 10:15:00').getTime(),
          orig_iat: new Date('2018-10-21 10:00:00').getTime()
        }
      }

      expect(store.getters.canRefreshToken({}, getters)).toBeTruthy()
    })
  })
})

describe('Actions', () => {
  let commit = jest.fn()
  let dispatch = jest.fn()
  let state = {
    token: token
  }

  afterEach(() => {
    commit.mockClear()
    dispatch.mockClear()
  })

  describe('obtainToken', () => {
    it('calls the api with provided credentials and commits the token on state', async () => {
      mockAxios.post.mockImplementation(() => Promise.resolve({
        status: 200,
        data: {
          token: token
        }
      }))
      const credentials = {
        email: 'test@test.com',
        password: 'qwerty'
      }

      await store.actions.obtainToken({ commit }, credentials)

      expect(mockAxios.post).toHaveBeenCalledWith('api/auth/jwt/create/', credentials)
      expect(commit).toHaveBeenCalledWith('SET_TOKEN', token)
    })

    it("doesn't commit the token on state if the api response is invalid", async () => {
      mockAxios.post.mockImplementation(() => Promise.resolve({
        status: 400
      }))

      await store.actions.obtainToken({ commit }, {
        email: 'test@test.com',
        password: 'invalid'
      })

      expect(commit).toHaveBeenCalledTimes(0)
    })
  })

  describe('tryRefreshToken', () => {
    it("doesn't call the refreshToken action if canRefreshToken getter return false", async () => {
      const getters = {
        canRefreshToken: false
      }

      await store.actions.tryRefreshToken({ dispatch, getters })
      expect(dispatch).toHaveBeenCalledTimes(0)
    })

    it('calls the refreshToken acyion if canRefreshToken getter is true', async () => {
      const getters = {
        canRefreshToken: true
      }

      await store.actions.tryRefreshToken({ dispatch, getters })
      expect(dispatch).toHaveBeenCalledWith('refreshToken')
    })
  })

  describe('refreshToken', () => {
    it('calls the api with current token and commit returned token on sucess response', async () => {
      mockAxios.post.mockImplementation(() => Promise.resolve({
        status: 200,
        data: {
          token: 'newToken'
        }
      }))

      await store.actions.refreshToken({ state, commit })
      expect(mockAxios.post).toHaveBeenCalledWith('api/auth/jwt/refresh/', { token: state.token })
      expect(commit).toHaveBeenCalledWith('SET_TOKEN', 'newToken')
    })

    it("ocurrs an error when call the api and doesn't set the token", async () => {
      mockAxios.post.mockImplementation(() => {
        throw new Error('=/')
      })
      global.console = {
        log: jest.fn()
      }

      await store.actions.refreshToken({ state, commit })
      expect(commit).toHaveBeenCalledTimes(0)
      expect(console.log).toHaveBeenCalledWith('Failed to refresh token', Error('=/'))
    })
  })

  describe('destroyToken', () => {
    it('calls the SET_TOKEN mutation with a blank token', () => {
      const commit = jest.fn()

      store.actions.destroyToken({ commit })
      expect(commit).toHaveBeenCalledWith('SET_TOKEN', '')
    })
  })
})
