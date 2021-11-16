const HIDE_TIMEOUT = 5000;
let timeout = null;

const notifications = {
  state: () => ({
    text: null,
    error: null,
  }),
  mutations: {
    showNotification: (state, { text, error = null }) => {
      state.text = text;
      state.error = error;
    },
    hideNotification: (state) => {
      state.text = null;
      state.error = false;
    }
  },
  actions: {
    showNotification({ commit }, data) {
      timeout && clearTimeout(timeout);
      commit('hideNotification');

      setTimeout(() => {
        commit('showNotification', data);

        timeout = setTimeout(() => {
          commit('hideNotification');
        }, HIDE_TIMEOUT);
      }, 10);

    },
    hideNotification({ commit }) {
      timeout && clearTimeout(timeout);
      commit('hideNotification');
    }
  },
  getters: {
    notificationState: state => state
  }
}

export default notifications;