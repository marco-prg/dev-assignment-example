const app = {
  state: () => ({
    isLoading: true,
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