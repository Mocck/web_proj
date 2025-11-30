<template>
  <div class="min-h-screen flex bg-gray-100">
    <!-- 左侧菜单 -->
    <aside v-if="showMenu" class="w-64 bg-white shadow-lg flex-shrink-0 p-4">
      <h2 class="text-xl font-bold mb-6 text-center text-gray-700">导航菜单</h2>
      <ul class="space-y-3">
        <li v-for="menu in menuList" :key="menu.id" class="group">
          <!-- 父菜单 -->
          <div
            class="flex items-center justify-between px-3 py-2 rounded-lg hover:bg-blue-50 cursor-pointer transition-colors duration-200"
            @click="toggleMenu(menu)"
          >
            <span class="font-semibold text-gray-700">{{ menu.name }}</span>
            <svg
              v-if="menu.children"
              class="w-4 h-4 text-gray-400 group-hover:text-blue-500 transition-transform duration-200"
              :class="{'rotate-90': menu.expanded}"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
          </div>

          <!-- 子菜单 -->
          <ul v-if="menu.children && menu.expanded" class="ml-4 mt-1 space-y-1">
            <li
              v-for="child in menu.children"
              :key="child.id"
              @click.stop="goTo(child.path)"
              class="px-3 py-2 rounded-lg hover:bg-blue-100 cursor-pointer transition-colors duration-200 text-gray-600"
            >
              {{ child.name }}
            </li>
          </ul>
        </li>
      </ul>
    </aside>

    <!-- 右侧内容区 -->
    <main class="flex-1 p-6">
      <router-view />
    </main>
  </div>
</template>


<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

//它们只是访问那张“路由表”的接口。
const router = useRouter() // 访问路由实例（可以跳转）
const route = useRoute()   // 当前路由信息（可以拿到 path、params 等）

const menuList = ref([])
const loading = ref(false)
const error = ref('')

const hideMenuPaths = ['/login', '/register']
const showMenu = computed(() => !hideMenuPaths.includes(route.path))

const api = axios.create({
  baseURL: '/api/users',
  withCredentials: true  // ⚠️ 关键点！！
})

// ✅ 封装菜单加载函数
const loadMenu = async () => {
  const currentPath = route.path
  if (hideMenuPaths.includes(currentPath)) return

  loading.value = true
  try {
    const res = await api.get('/menus/')
    // 给每个父菜单添加 expanded 字段
    menuList.value = res.data.map(menu => ({ ...menu, expanded: false }))
  } catch (err) {
    console.error(err)
    error.value = '获取菜单失败或未登录'
  } finally {
    loading.value = false
  }
}

// ✅ 页面加载时执行
onMounted(loadMenu)

// ✅ 当路由变化时重新判断是否要加载菜单
watch(
  () => route.path,
  (newPath) => {
    if (!hideMenuPaths.includes(newPath)) {
      loadMenu()
    } else {
      menuList.value = [] // 清空菜单
    }
  },
  { immediate: true } // 加上这个能在初始时自动判断一次
)

/*
这段代码的功能就是：

点击菜单项 → 调用 goTo(child.path)

如果路径有效 → 使用 Vue Router 跳转

如果跳转到当前路由 → 忽略重复导航错误

如果其他错误 → 打印到控制台
*/
const goTo = (path) => {
  if (!path) return
  router.push(path).catch(err => {
    if (err.name !== 'NavigationDuplicated') console.error(err)
  })
}

// 可在点击父菜单时切换展开状态
const toggleMenu = (menu) => {
  menu.expanded = !menu.expanded
}

</script>
