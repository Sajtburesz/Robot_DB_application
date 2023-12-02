import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import store from '../store/index.js'
import { axios } from "@/common/api.service.js";

const routes = [
  {
    path: '/',
    name: 'home',
    meta: {requiresAuth: true},
    component: HomeView
  },
    {
    path: '/my-profile/',
    name: 'RetreiveUpdateDestroyeProfileView',
    meta: {requiresAuth: true},
    component: () => import('../views/RetreiveUpdateDestroyProfileView.vue'),
  },
  {
    path: '/teams/list/',
    name: 'ListTeamsView',
    meta: {requiresAuth: true},
    component: () => import('../views/ListTeamsView.vue'),
  },
  {
    path: '/teams/create-team/',
    name: 'CreateTeamView',
    meta: {requiresAuth: true},
    component: () => import('../views/CreateTeamView.vue'),
  },
  {
    path: '/manage-team/:teamId/',
    name: 'RetreiveUpdateDestroyTeamView',
    meta: {requiresAuth: true},
    component: () => import('../views/RetreiveUpdateDestroyTeamView.vue'),
    props: true,
  },
  {
    path: '/test-runs/create/',
    name: 'CreateTestRunView',
    meta: {requiresAuth: true},
    component: () => import('../views/CreateTestRunView.vue'),
  },
  {
    path: '/test-runs/list/',
    name: 'ListTestRunsView',
    meta: {requiresAuth: true},
    component: () => import('../views/ListTestRunsView.vue'),
  },
  {
    path: '/test-runs/:teamId/:testRunId',
    name: 'TestRunView',
    meta: {requiresAuth: true},
    component: () => import('../views/TestRunView.vue'),
  },
  {
    path: '/test-runs/compare/',
    name: 'CompareTestRunView',
    meta: {requiresAuth: true},
    component: () => import('../views/CompareTestRunsView.vue'),
  },
  {
    path: '/admin_page/attributes/',
    name: 'ManageAttributesView',
    meta: { requiresAdmin: true, requiresAuth: true },
    component: () => import('../views/ManageAttributesAdminView.vue'),
  },
  {
    path: '/admin_page/users/',
    name: 'ManageUsersView',
    meta: { requiresAdmin: true, requiresAuth: true },
    component: () => import('../views/ManageUsersAdminView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory("/"),
  routes
})

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    await store.dispatch('fetchAdminStatus');
    axios.get('/api/check_session/')
    if (store.state.isAdmin) {
      next();
    } else {
      next({ path: '/' });
    }
  } else {
    next();
  }
});

router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    await axios.get('/api/v1/check-session/')
      .then(response => {
        if (response.data.isAuthenticated) {
          next();
        } else {
          window.location.href = '/accounts/login/';
        }
      })
      .catch(() => {
        window.location.href = '/accounts/login/';
      });
  } else {
    next(); 
  }
});

export default router
