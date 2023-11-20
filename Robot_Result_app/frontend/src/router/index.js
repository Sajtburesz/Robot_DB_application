import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import store from '../store/index.js'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
    {
    path: '/my-profile/',
    name: 'RetreiveUpdateDestroyeProfileView',
    component: () => import('../views/RetreiveUpdateDestroyProfileView.vue'),
  },
  {
    path: '/teams/list/',
    name: 'ListTeamsView',
    component: () => import('../views/ListTeamsView.vue'),
  },
  {
    path: '/teams/creat-team/',
    name: 'CreateTeamView',
    component: () => import('../views/CreateTeamView.vue'),
  },
  {
    path: '/manage-team/:teamId/',
    name: 'RetreiveUpdateDestroyTeamView',
    component: () => import('../views/RetreiveUpdateDestroyTeamView.vue'),
    props: true,
  },
  {
    path: '/test-runs/create/',
    name: 'CreateTestRunView',
    component: () => import('../views/CreateTestRunView.vue'),
  },
  {
    path: '/test-runs/list/',
    name: 'ListTestRunsView',
    component: () => import('../views/ListTestRunsView.vue'),
  },
  {
    path: '/test-runs/:teamId/:testRunId',
    name: 'TestRunView',
    component: () => import('../views/TestRunView.vue'),
  },
  {
    path: '/test-runs/compare/',
    name: 'CompareTestRunView',
    component: () => import('../views/CompareTestRunsView.vue'),
  },
  {
    path: '/admin_page/attributes/',
    name: 'ManageAttributesView',
    meta: { requiresAdmin: true },
    component: () => import('../views/ManageAttributesAdminView.vue'),
  },
  {
    path: '/admin_page/users/',
    name: 'ManageUsersView',
    meta: { requiresAdmin: true },
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
    if (store.state.isAdmin) {
      next();
    } else {
      next({ path: '/' }); // Redirect to a different route
    }
  } else {
    next();
  }
});


export default router
