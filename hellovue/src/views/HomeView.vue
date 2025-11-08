<!-- Home.vue -->
<template>
  <main class="flex-1 ml-60 p-8">

    <!-- 顶部导航栏 -->
    <header class="bg-white shadow-md h-14 flex items-center justify-between px-6 fixed top-0 left-0 right-0 z-10">
      <h1 class="text-xl font-semibold text-gray-700">智能助手系统</h1>
      <div class="flex items-center space-x-4">
        <span class="text-gray-600">👋 {{ userInfo.username || userInfo.nickname }}</span>
        <button
          @click="handleLogout"
          class="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-md text-sm transition"
        >
          退出
        </button>
      </div>
    </header>

    <!-- 左侧菜单栏 -->
    <aside class="w-60 bg-white shadow-md h-[calc(100vh-3.5rem)] fixed left-0 top-14 p-4">
      <nav class="space-y-2">
        <div v-if="loading" class="text-gray-400 text-sm text-center mt-4">加载菜单中...</div>

        <div
          v-for="item in menuItems"
          :key="item.path"
          @click="goTo(item.path)"
          class="cursor-pointer px-3 py-2 rounded-lg hover:bg-blue-100 transition flex items-center gap-2"
          :class="{ 'bg-blue-200 font-semibold text-blue-700': currentPath === item.path }"
        >
          <span class="text-lg">{{ item.icon || '📁' }}</span>
          <span>{{ item.name }}</span>
        </div>
      </nav>
    </aside>

    <!-- 主体内容 -->
    <div class="bg-white p-8 rounded-2xl shadow-md max-w-3xl mx-auto">
      <div class="flex items-center gap-6 mb-8">
        <img
          :src="userInfo.avatar || '/default-avatar.png'"
          alt="用户头像"
          class="w-24 h-24 rounded-full object-cover border shadow"
        />
        <div class="pt-2">
          <h2 class="text-2xl font-bold text-gray-800">{{ userInfo.username || userInfo.nickname }}</h2>
          <p class="text-gray-500 text-sm">注册时间：{{ userInfo.created_at }}</p>
        </div>
      </div>

      <!-- 用户信息块 -->
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 text-gray-700">
        <div>
          <p class="text-sm text-gray-500">用户名</p>
          <p class="text-lg font-medium border border-gray-200 rounded-lg p-2">{{ userInfo.username }}</p>
        </div>

        <div>
          <p class="text-sm text-gray-500">邮箱</p>
          <p class="text-lg font-medium border border-gray-200 rounded-lg p-2">{{ userInfo.email || '未设置' }}</p>
        </div>

        <div>
          <p class="text-sm text-gray-500">手机号</p>
          <p class="text-lg font-medium border border-gray-200 rounded-lg p-2">{{ userInfo.phone_number || '未填写' }}</p>
        </div>

        <div class="col-span-2">
          <p class="text-sm text-gray-500 mb-2">角色</p>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="r in userInfo.roles"
              :key="r.id"
              class="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-medium"
            >
              {{ r.role__name }}
            </span>
          </div>
        </div>

        <div class="col-span-2">
          <p class="text-sm text-gray-500 mb-2">个人简介</p>
          <p class="text-gray-700 text-base leading-relaxed whitespace-pre-wrap border border-gray-200 rounded-lg p-3">
            {{ userInfo.bio || '这个人很神秘，什么都没有写。' }}
          </p>
        </div>
      </div>

      <div class="mt-8 flex justify-end">
        <button
          @click="router.push('/settings')"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
        >
          编辑资料
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const currentPath = ref(route.path)
const userInfo = ref({})
const menuItems = ref([])
const loading = ref(true)

// 获取用户信息
const loadUser = async () => {
  try {
    const res = await axios.get('/api/users/me/', { withCredentials: true })
    userInfo.value = res.data
  } catch (err) {
    console.error('加载用户失败', err)
    router.push('/login')
  }
}

// 获取菜单数据
const loadMenu = async () => {
  try {
    const res = await axios.get('/api/users/menus/', { withCredentials: true })
    menuItems.value = res.data
  } catch (err) {
    console.error('加载菜单失败', err)
  } finally {
    loading.value = false
  }
}

const goTo = (path) => {
  router.push(path)
  currentPath.value = path
}

// 退出登录
const handleLogout = async () => {
  try {
    await api.post('/logout/')
  } catch (err) {
    console.error(err)
  } finally {
    router.push('/login')
  }
}

onMounted(() => {
  loadUser()
  loadMenu()
})
</script>
