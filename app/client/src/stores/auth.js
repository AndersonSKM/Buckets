import api from '@/plugins/api'
import jwt from 'jsonwebtoken'

const state = {
  token: '',
  email: '',
  first_name: '',
  last_name: ''
}

const mutations = {
  SET_TOKEN (state, token) {
    state.token = token
  }
}

const getters = {
  isAuthenticated: (state, getters) => {
    return (state.token !== '') && !getters.isExpiredToken
  },
  isExpiredToken: (state, getters) => {
    const token = getters.decodedToken
    if (!token) {
      return true
    }

    return Date.now() > token.exp
  },
  decodedToken: (state) => {
    if (!state.token) {
      return null
    }

    const token = jwt.decode(state.token)
    return {
      ...token,
      orig_iat: token.orig_iat * 1000,
      exp: token.exp * 1000
    }
  },
  canRefreshToken: (state, getters) => {
    const token = getters.decodedToken
    if (!token) {
      return false
    }

    const oneMinuteInMiliseconds = 60000
    const oneHourInMiliseconds = 36e5

    const tokenWasCreatedWithinFourHours = (Math.abs(Date.now() - token.orig_iat) / oneHourInMiliseconds) <= 4
    const tokenHasMoreThanThirteenMinutes = (Math.abs(Date.now() - token.orig_iat) / oneMinuteInMiliseconds) >= 13
    return tokenWasCreatedWithinFourHours && tokenHasMoreThanThirteenMinutes
  }
}

const actions = {
  async obtainToken ({ commit }, credentials) {
    const response = await api.post('api/auth/jwt/create/', credentials)

    if (response.status === 200) {
      commit('SET_TOKEN', response.data.token)
    }
  },
  async tryRefreshToken ({ getters, dispatch }) {
    if (!getters.canRefreshToken) {
      return
    }

    await dispatch('refreshToken')
  },
  async refreshToken ({ state, commit }) {
    try {
      const response = await api.post('api/auth/jwt/refresh/', { token: state.token })

      if (response.status === 200) {
        commit('SET_TOKEN', response.data.token)
      }
    } catch (error) {
      console.log('Failed to refresh token', error)
    }
  },
  destroyToken ({ commit }) {
    commit('SET_TOKEN', '')
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  getters,
  actions
}
