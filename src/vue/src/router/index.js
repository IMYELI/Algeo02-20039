import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Ping from '../components/ping.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/image',
    name: 'Ping',
    component: Ping,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
