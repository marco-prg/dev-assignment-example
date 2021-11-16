import Vue from 'vue'
import Vuex from 'vuex'
import app from './modules/app';
import notification from './modules/notification';

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {    
  },
  modules: {
    app, 
    notification
  }
})

export default store