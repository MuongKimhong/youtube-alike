import Vue from 'vue'
import Vuex from 'vuex'
import VuexPersistence from 'vuex-persist'

const vuexLocal = new VuexPersistence({
  storage: window.localStorage
})

Vue.use(Vuex)

export default new Vuex.Store({
  plugins: [vuexLocal.plugin],
  state: {
    userInfo: {
      id      : null,
      access  : null,
      refresh : null,
      username: null
    },
    currentUrl: null,
    showLogin: true
  },
  mutations: {
    getUserInfo: function (state, info) {
      state.userInfo = info
    },
    deleteUserInfo: function (state) {
      for (var key in state.userInfo) {
        state.userInfo[key] = null
      }
    },
    getCurrentUrl: function (state, url) {
      state.currentUrl = url
    },
    deleteCurrentUrl: function (state) {
      state.currentUrl = null
    },
    changeShowLogin: function (state, value) {
      state.showLogin = value
    }
  },
  actions: {
  },
  modules: {
  }
})
