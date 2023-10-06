import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/api/v1/profile/',
    name: 'GetUserProfile',
    component: () => import('../views/GetUserProfileView.vue')
  },
  {
    path: '/api/v1/profiles/sajtburesz/',
    name: 'EditUserProfile',
    component: () => import('../views/EditUserProfileView.vue'),
    props: true,
  }
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
