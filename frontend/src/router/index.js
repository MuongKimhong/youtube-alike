import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import UploadVideo from '../views/UploadVideo.vue'
import VideoDetail from '../views/VideoDetail.vue'
import SearchResult from '../views/SearchResult.vue'
import store from '../store/index'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/user/:id/upload',
    name: 'UploadVideo',
    component: UploadVideo,
    beforeEnter: (to, from, next) => {
      if (store.state.userInfo.access == null) next({ name: 'Home' })
      else next()
    }
  },
  {
    path: '/search-results',
    name: 'SearchResult',
    component: SearchResult
  },
  {
    path: '/video/:complexId/:id/:slug',
    name: 'VideoDetail',
    component: VideoDetail
  },
  {
    path: '/9278bec8-89fe-4ff8-a676-de76b66fb915/u59MY8U2HWRMCNiucQ11OVVuTOIRAJ/login',
    name: 'Login',
    component: Login,
    beforeEnter: (to, from, next) => {
      if (store.state.userInfo.access != null) next({ name: 'Home' })
      else next()
    }
  },
  {
    path: '/160a519c-9348-4648-ae66-08b07650d4f8/LXUqDmbVTyiJVH7cUFJYb2DrRneiUF/register',
    name: 'Register',
    component: Register,
    beforeEnter: (to, from, next) => {
      if (store.state.userInfo.access != null) next({ name: 'Home' })
      else next()
    }
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

export default router
