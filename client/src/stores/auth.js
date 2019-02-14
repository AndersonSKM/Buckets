import AuthService from '@/plugins/services/auth.js'

const state = {
  token: ''
}

const mutations = {
  SET_TOKEN (state, token) {
    state.token = token
  }
}

const getters = {
  isAuthenticated: (state) => {
    return (state.token !== '') && !AuthService.isExpiredToken(state.token)
  }
}

const actions = {
  async obtainToken ({ commit }, credentials) {
    const response = await AuthService.createToken(credentials)
    if (response.status === 200) {
      commit('SET_TOKEN', response.data.token)
    }
    return response
  },

  async tryRefreshToken ({ commit, state }) {
    if (!AuthService.canRefreshToken(state.token)) {
      return
    }

    const newToken = await AuthService.refreshToken(state.token)
    if (newToken !== '') {
      commit('SET_TOKEN', newToken)
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
