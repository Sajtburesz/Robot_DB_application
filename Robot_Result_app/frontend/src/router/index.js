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
  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = createRouter({
  history: createWebHistory("/"),
  routes
})

export default router
