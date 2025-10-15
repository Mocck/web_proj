// 定义每个页面的路由

import { createRouter, createWebHistory } from 'vue-router'

const Apps = () => import('@/views/AppsView.vue')
const PingView = () => import('@/views/PingView.vue')
const Graph = () => import('@/views/GraphView.vue')
const Space = () => import('@/views/SpaceView.vue')

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/ping', name: 'ping', component: PingView },
    // 主页重定向到 /apps
    { path: '/', redirect: '/apps' },
    { path: '/apps', name: 'apps', component: Apps },
    { path: '/graph', name: 'graph', component: Graph },
    { path: '/workspace', name: 'workspace', component: Space },
  ],
})
