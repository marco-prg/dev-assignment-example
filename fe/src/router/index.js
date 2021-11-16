import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

export const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/home",
    name: 'home',
    component: Home,
    mainMenu: true,
  },
]

const router = new VueRouter({
  routes
})

export default router
