import { createStore } from 'vuex';

export default createStore({
  state: {
    isAdmin: false,
    testRuns: []
  },
  mutations: {
    SET_ADMIN_STATUS(state, status) {
      state.isAdmin = status;
    },
    setTestRuns(state, testRuns) {
      state.testRuns = testRuns;
    },
  },
  actions: {
    updateAdminStatus({ commit }, status) {
      commit('SET_ADMIN_STATUS', status);
    },
    setTestRuns(context, testRun) {
      context.commit('setTestRuns', testRun);
    },
  },
  getters: {
    isAdmin: state => state.isAdmin
  }
});
