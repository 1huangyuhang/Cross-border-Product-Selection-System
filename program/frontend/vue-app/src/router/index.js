import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import Products from '../views/Products.vue'
import Crawler from '../views/Crawler.vue'
import Analysis from '../views/Analysis.vue'
import Recommend from '../views/Recommend.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard'
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard
  },
  {
    path: '/products',
    name: 'products',
    component: Products
  },
  {
    path: '/crawler',
    name: 'crawler',
    component: Crawler
  },
  {
    path: '/analysis',
    name: 'analysis',
    component: Analysis
  },
  {
    path: '/recommend',
    name: 'recommend',
    component: Recommend
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
