import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

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
]

const router = createRouter({
  history: createWebHistory("/"),
  routes
})

export default router
