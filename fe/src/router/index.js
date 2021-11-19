import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Backtest from '../views/Backtest.vue'

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
    meta: { number: 0 },
  },
  {
    path: "/backtest",
    name: 'backtest',
    component: Backtest,
    mainMenu: true,
    meta: { number: 1 },
  },
]

const router = new VueRouter({
  routes
})

export default router
