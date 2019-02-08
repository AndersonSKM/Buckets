import store from '@/stores/auth.js'
import AuthService from '@/plugins/services/auth.js'

jest.mock('@/plugins/services/auth.js')
const fakeToken = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiNzcxYzA2NzUtMDllMi00ODg1LTlhZGUtZTk4NDNmYTk5NWIyIiwidXNlcm5hbWUiOiJhbmRlcnNvbi5rcnM5NUBnbWFpbC5jb20iLCJleHAiOjE1NDAxMjY5NDIsImVtYWlsIjoiYW5kZXJzb24ua3JzOTVAZ21haWwuY29tIiwib3JpZ19pYXQiOjE1NDAxMjYwNDJ9.xtGQ2cTfd92DHNgmm2l2TZOtvR0Fl3hLu08X9CFb6hQ'

describe('State', () => {
  describe('initial', () => {
    it('returns the state with all properties blank', () => {
      expect(store.state).toEqual({
        token: ''
      })
    })
  })
})

describe('Mutations', () => {
  describe('SET_TOKEN', () => {
    it('defines token state correctly', () => {
      store.mutations.SET_TOKEN(store.state, fakeToken)
      expect(store.state.token).toEqual(fakeToken)
    })
  })
})

describe('Getters', () => {
  describe('isAuthenticated', () => {
    it('returns false if token is blank', () => {
      const state = {
        token: ''
      }

      expect(store.getters.isAuthenticated(state)).toBeFalsy()
    })

    it('returns false if token is expired', () => {
      const state = {
        token: fakeToken
      }
      AuthService.isExpiredToken = jest.fn((token) => true)

      expect(store.getters.isAuthenticated(state)).toBeFalsy()
    })

    it('returns true with a valid token', () => {
      const state = {
        token: fakeToken
      }
      AuthService.isExpiredToken = jest.fn((token) => false)

      expect(store.getters.isAuthenticated(state)).toBeTruthy()
    })
  })
})

describe('Actions', () => {
  let commit = jest.fn()
  let dispatch = jest.fn()

  afterEach(() => {
    commit.mockClear()
    dispatch.mockClear()
  })

  describe('obtainToken', () => {
    it('calls the auth service with provided credentials and commits the token on state', async () => {
      const response = {
        status: 200,
        data: {
          token: fakeToken
        }
      }
      AuthService.createToken = jest.fn(() => Promise.resolve(response))

      const credentials = {
        email: 'john.doe@test.com',
        password: 'john.doe'
      }
      expect(await store.actions.obtainToken({ commit }, credentials)).toEqual(response)

      expect(AuthService.createToken).toHaveBeenCalledWith(credentials)
      expect(commit).toHaveBeenCalledWith('SET_TOKEN', fakeToken)
    })

    it("doesn't commit the token on state if the api response is invalid", async () => {
      AuthService.createToken = jest.fn(() => {
        return Promise.resolve({
          status: 303
        })
      })
      await store.actions.obtainToken({ commit }, 'test@test.com', 'invalid')

      expect(commit).toHaveBeenCalledTimes(0)
    })
  })

  describe('tryRefreshToken', () => {
    it("doesn't call the refreshToken action if canRefreshToken getter return false", async () => {
      AuthService.canRefreshToken = jest.fn((token) => false)
      const state = {
        token: fakeToken
      }
      await store.actions.tryRefreshToken({ commit, state })

      expect(AuthService.canRefreshToken).toHaveBeenCalledWith(fakeToken)
      expect(commit).toHaveBeenCalledTimes(0)
    })

    it('calls the refreshToken if canRefreshToken returns true', async () => {
      const newToken = 'b3ee9fbb-f81e-4bfc-a4ac-44c93008134f'

      AuthService.canRefreshToken = jest.fn((token) => true)
      AuthService.refreshToken = jest.fn(() => newToken)
      const state = {
        token: fakeToken
      }
      await store.actions.tryRefreshToken({ commit, state })

      expect(AuthService.refreshToken).toHaveBeenCalledWith(fakeToken)
      expect(commit).toHaveBeenCalledWith('SET_TOKEN', newToken)
    })
  })

  describe('destroyToken', () => {
    it('calls the SET_TOKEN mutation with a blank token', () => {
      store.actions.destroyToken({ commit })
      expect(commit).toHaveBeenCalledWith('SET_TOKEN', '')
    })
  })
})
