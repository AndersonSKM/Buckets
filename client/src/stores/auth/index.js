import api from '@/plugins/api'
import jwt from 'jsonwebtoken'

const Auth = {
  namespaced: true,
  state: {
    token: '',
    email: '',
    first_name: '',
    last_name: ''
  },
  mutations: {
    setToken (state, token) {
      state.token = token
    }
  },
  getters: {
    isAuthenticated: (state, getters) => {
      return (state.token !== '') && getters.isExpiredToken()
    },
    isExpiredToken: (state, getters) => {
      const fiveteenMinutesInSeconds = 900
      const decodedToken = getters.decodedToken()

      return (decodedToken.exp - (Date.now() / 1000)) < fiveteenMinutesInSeconds
    },
    decodedToken: (state) => {
      return jwt.decode(state.token)
    },
    canRefreshToken: (state, getters) => {
      const twoDaysInSeconds = 172800
      const decodedToken = getters.decodedToken

      return ((Date.now() / 1000) - decodedToken.orig_iat) < twoDaysInSeconds
    }
  },
  actions: {
    async obtainToken ({ commit }, credentials) {
      console.log(process.env)
      const response = await api.post('tokens/', credentials)
      if (response.status === 200) {
        commit('setToken', response.data.token)
      }

      return response
    },
    tryRefreshToken ({ getters, actions }) {
      console.log('tryRefreshToken')
      if (!getters.canRefreshToken()) {
        return
      }

      actions.refreshToken()
    },
    async refreshToken ({ state, commit }) {
      try {
        const response = await api.post('tokens/refresh/', { token: state.token })

        if (response.status === 200) {
          commit('setToken', response.data.token)
        }
      } catch (error) {
        console.log(error)
      }
    },
    destroyToken ({ commit }) {
      commit('setToken', '')
    }
  }
}

export default Auth
