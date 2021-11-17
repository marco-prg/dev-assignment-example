const app = {
  state: () => ({
    isLoading: false,
  }),
  mutations: {
    isLoading: (state, isLoading) => {
      state.isLoading = isLoading
    }
  },
  actions: {
    showLoadingScreen({ commit }, isLoading) {
      commit('isLoading', isLoading);
    }
  },
  getters: {
    isLoading: state => state.isLoading
  }
}

export default app