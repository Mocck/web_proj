<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="w-full max-w-md bg-white p-6 rounded-2xl shadow">
      <h2 class="text-2xl font-bold text-center mb-6">注册账号</h2>

      <!-- 注册表单 -->
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block mb-1 font-medium">用户名</label>
          <input v-model="form.username" type="text" class="input" required />
        </div>

        <div>
          <label class="block mb-1 font-medium">邮箱</label>
          <input v-model="form.email" type="email" class="input" required />
        </div>

        <div>
          <label class="block mb-1 font-medium">手机号</label>
          <input v-model="form.phone_number" type="text" class="input" required />
        </div>

        <div>
          <label class="block mb-1 font-medium">密码</label>
          <input v-model="form.password" type="password" class="input" required />
        </div>

        <div>
          <label class="block mb-1 font-medium">确认密码</label>
          <input v-model="form.confirmpassword" type="password" class="input" required />
        </div>

        <div>
          <label class="block mb-1 font-medium">昵称</label>
          <input v-model="form.nickname" type="text" class="input" />
        </div>

        <div>
          <label class="block mb-1 font-medium">简介</label>
          <textarea v-model="form.bio" class="input"></textarea>
        </div>

        <div>
          <label class="block mb-1 font-medium">头像上传</label>
          <input type="file" @change="onFileChange" accept="image/*" />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-md"
          :disabled="loading"
        >
          {{ loading ? '注册中...' : '注册' }}
        </button>

        <p v-if="error" class="text-red-600 text-center mt-2">{{ error }}</p>
        <p v-if="success" class="text-green-600 text-center mt-2">注册成功！</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmpassword: '',
  nickname: '',
  phone_number: '',
  bio: '',
})

const avatar = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref(false)
const router = useRouter()
const onFileChange = (e) => {
  avatar.value = e.target.files[0]
}

const handleRegister = async () => {
  error.value = ''
  success.value = false

  if (form.value.password !== form.value.confirmpassword) {
    error.value = '两次输入的密码不一致'
    return
  }

  const formData = new FormData()
  for (const key in form.value) {
    if (key !== 'confirmPassword') formData.append(key, form.value[key])
  }
  if (avatar.value) formData.append('avatar', avatar.value)

  loading.value = true
  try {
    const res = await axios.post('/api/users/register/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    console.log('注册成功:', res.data)
    success.value = true

    // 可选：保存 token 到 localStorage
    localStorage.setItem('token', res.data.token?.access || '')

    // 注册成功后可以跳转首页
    router.push('/') // SPA 内部跳转

  } catch (err) {
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else {
      console.error('注册错误:', err) 
      error.value = '注册失败，请检查输入或稍后再试'
    }
  } finally {
    loading.value = false
  }
}
</script>
