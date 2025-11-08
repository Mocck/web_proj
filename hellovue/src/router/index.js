// 定义每个页面的路由

import { createRouter, createWebHistory } from 'vue-router'

const Apps = () => import('@/views/AppsView.vue')
const PingView = () => import('@/views/PingView.vue')
const Graph = () => import('@/views/GraphView.vue')
const Space = () => import('@/views/SpaceView.vue')
const Register = () => import('@/views/RegisterView.vue') 
const Login = () => import('@/views/LoginView.vue') 
const Home = () => import('@/views/HomeView.vue')
const DefaultLayout = () => import('@/layouts/Defaultlayout.vue')
const Team = () => import('@/views/TeamView.vue')
const Chat = () => import('@/views/ChatView.vue')


const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/ping', name: 'ping', component: PingView },

    // 主页等使用 DefaultLayout 的页面, 只有在 DefaultLayout 中写了 <router-view> 才能显示子路由
    {  path: '/', 
      component: DefaultLayout,
      children: [
        { path: '', name: 'home', component: Home },
        { path: 'home', name: 'homePage', component: Home } // ✅ 显式匹配 /home
      ]
    },

    // 应用市场
    { path: '/apps', name: 'apps', component: Apps },
    { path: '/graph', name: 'graph', component: Graph },
    { path: '/workspace', name: 'workspace', component: Space },

    // ai 对话
    { path: '/chat', name: 'chat', component: Chat },

    // 这些不使用 DefaultLayout
    { path: '/register', name: 'register', component: Register, meta: { requiresAuth: false }},
    { path: '/login', component: Login , meta: { requiresAuth: false }},

     // 受保护页面
    { path: '/create_team', component: Team , meta: { requiresAuth: true }},
    
    //{ path: '/menu', component: Menu, meta: { requiresAuth: true } },
  ],
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    // 页面需要登录但没有 token，跳回登录页
    next('/login')
  } else {
    next()
  }
})

export default router