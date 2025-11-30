<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="w-11/12 sm:w-full max-w-md bg-white p-8 rounded-2xl shadow-lg">
      <h2 class="text-2xl font-bold text-center mb-6">用户登录</h2>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block mb-1 font-medium">用户名或者邮箱</label>
          <input
            v-model="form.username_or_email"
            type="text"
            placeholder="请输入用户名或者邮箱"
            class="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <div>
          <label class="block mb-1 font-medium">密码</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            class="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-md"
          :disabled="loading"
        >
          {{ loading ? '登录中...' : '登录' }}
        </button>

        <p v-if="error" class="text-red-600 text-center mt-2">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const form = ref({
  username_or_email: '',
  password: ''
})

const loading = ref(false)
const error = ref('')
const router = useRouter()   // ✅ 必须加上这行

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    const res = await axios.post('/api/users/login/', form.value)
    
    // 假设返回 { user: {...}, token: "xxx" }
    console.log('登录成功', res.data)

    // 保存 token 到 localStorage
    localStorage.setItem('token', res.data.token?.access || '')

    // 登录成功后可以跳转首页
    router.push('/') // SPA 内部跳转
    
  } catch (err) {
    if (err.response) {
      // 有响应 -> 说明后端正常返回错误
      if (err.response.data?.detail) {
        error.value = err.response.data.detail
      } else {
        error.value = '登录失败，请检查用户名或密码'
      }
    } else if (err.request) {
      // 有请求但没响应 -> 服务器没启动 / 网络问题
      error.value = '服务器无法连接，请稍后再试'
    } else {
      // 其他未知错误
      error.value = '发生未知错误'
    }
  } finally {
    loading.value = false
  }
}
</script>
