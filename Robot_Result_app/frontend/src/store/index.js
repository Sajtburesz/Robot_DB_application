import { createStore } from 'vuex';

export default createStore({
  state: {
    isAdmin: false,
    testRuns: [],
    wayOfAccess: []
  },
  mutations: {
    SET_ADMIN_STATUS(state, status) {
      state.isAdmin = status;
    },
    setTestRuns(state, testRuns) {
      state.testRuns = testRuns;
    },
    setWayOfAccess(state, id) {
      state.wayOfAccess = id;
    },
  },
  actions: {
    updateAdminStatus({ commit }, status) {
      commit('SET_ADMIN_STATUS', status);
    },
    setTestRuns(context, testRun) {
      context.commit('setTestRuns', testRun);
    },
    setWayOfAccess(context, id) {
      context.commit('setWayOfAccess', id);
    },
  },
  getters: {
    isAdmin: state => state.isAdmin
  }
});
