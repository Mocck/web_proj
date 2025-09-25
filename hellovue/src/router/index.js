import { createRouter, createWebHistory } from 'vue-router'

const Apps = () => import('@/views/AppsView.vue')
const PingView = () => import('@/views/PingView.vue')

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/ping', name: 'ping', component: PingView },
    { path: '/', redirect: '/apps' },
    { path: '/apps', name: 'apps', component: Apps },
  ],
})
