import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    tweetsFile: null
  },
  getters: {
    file: state => {
      return state.tweetsFile
    }
  },
  mutations: {
    updateFile (state, payload) {
      state.tweetsFile = payload
      console.log(payload)
    },
    removeFile (state, payload) {
      if (payload === true) {
        state.tweetsFile = null
      }
    }
  },
  actions: {}
})
