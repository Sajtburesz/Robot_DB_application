import { createStore } from 'vuex';
import { axios } from "@/common/api.service.js";

export default createStore({
  state: {
    isAdmin: false,
    isSuperUser: false,
    testRuns: [],
    wayOfAccess: [],
    avatar: "",
  },
  mutations: {
    SET_ADMIN_STATUS(state, status) {
      state.isAdmin = status;
    },
    SET_SUPERUSER_STATUS(state, status) {
      state.isSuperUser = status;
    },
    setTestRuns(state, testRuns) {
      state.testRuns = testRuns;
    },
    setWayOfAccess(state, id) {
      state.wayOfAccess = id;
    },
    updateAvatar(state, avatar) {
      state.avatar = avatar;
    }
  },
  actions: {
    updateAdminStatus({ commit }, status) {
      commit('SET_ADMIN_STATUS', status);
    },
    updateSuperuserStatus({ commit }, status) {
      commit('SET_SUPERUSER_STATUS', status);
    },
    setTestRuns(context, testRun) {
      context.commit('setTestRuns', testRun);
    },
    setWayOfAccess(context, id) {
      context.commit('setWayOfAccess', id);
    },
    setAvatar(context, avatar) {
      context.commit('updateAvatar', avatar);
    },
    async fetchAdminStatus(context) {
      try {
        const response = await axios.get('/api/v1/check-admin-status/');

        let isAdmin = false;
        let is_superuser = false;
        if(response.data.is_superuser){
          isAdmin = true;
          is_superuser = true;
        }else if (response.data.is_staff) {
          isAdmin = true;
        }
        context.commit('SET_ADMIN_STATUS', isAdmin);
        context.commit('SET_SUPERUSER_STATUS', is_superuser);
      } catch (error) {
        console.error("Error fetching admin status:", error);
      }
    }
  },
  getters: {
    isAdmin: state => state.isAdmin
  }
});
