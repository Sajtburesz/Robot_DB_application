import { createStore } from 'vuex';

export default createStore({
  state: {
    isAdmin: false
  },
  mutations: {
    SET_ADMIN_STATUS(state, status) {
      state.isAdmin = status;
    }
  },
  actions: {
    updateAdminStatus({ commit }, status) {
      commit('SET_ADMIN_STATUS', status);
    }
  },
  getters: {
    isAdmin: state => state.isAdmin
  }
});
