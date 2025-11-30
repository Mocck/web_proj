<template>
  <div class="max-w-2xl mx-auto mt-10 p-6 bg-white rounded-lg shadow-md">
    <h2 class="text-2xl font-bold mb-6">创建团队</h2>

    <form @submit.prevent="handleCreateTeam" class="space-y-4">
      <!-- 团队名称 -->
      <div>
        <label class="block font-medium mb-1">团队名称</label>
        <input
          v-model="form.name"
          type="text"
          placeholder="请输入团队名称"
          class="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- 是否公开 -->
      <div class="flex items-center space-x-4">
        <label class="font-medium">是否公开</label>
        <select v-model="form.is_public" class="border rounded-md px-2 py-1">
          <option :value="true">公开</option>
          <option :value="false">私密</option>
        </select>
      </div>

      <!-- 加入策略 -->
      <div class="flex items-center space-x-4">
        <label class="font-medium">加入策略</label>
        <select v-model="form.join_policy" class="border rounded-md px-2 py-1">
          <option value="open">开放加入</option>
          <option value="approval">需要审批</option>
          <option value="invite">仅邀请</option>
        </select>
      </div>

      <!-- 最大成员数 -->
      <div>
        <label class="block font-medium mb-1">最大成员数</label>
        <input
          v-model.number="form.max_members"
          type="number"
          min="1"
          placeholder="请输入最大成员数"
          class="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <!-- 简介 -->
      <div>
        <label class="block font-medium mb-1">团队简介</label>
        <textarea
          v-model="form.description"
          placeholder="团队简介"
          class="w-full border rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
        ></textarea>
      </div>

      <!-- 团队头像 -->
      <div>
        <label class="block font-medium mb-1">团队头像</label>
        <input type="file" @change="handleFileChange" accept="image/*" />
      </div>

      <!-- 提交按钮 -->
      <div>
        <button
          type="submit"
          :disabled="loading"
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md"
        >
          {{ loading ? '创建中...' : '创建团队' }}
        </button>
      </div>

      <!-- 错误提示 -->
      <p v-if="error" class="text-red-500 mt-2">{{ error }}</p>
      <p v-if="success" class="text-green-500 mt-2">{{ success }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

// 表单数据
const form = ref({
  name: '',
  is_public: true,
  join_policy: 'open',
  max_members: 10,
  description: '',
  avatar: null,
})

const loading = ref(false)
const error = ref('')
const success = ref('')

// 处理头像文件
const handleFileChange = (e) => {
  form.value.avatar = e.target.files[0] || null
}

// 提交表单
const handleCreateTeam = async () => {
  loading.value = true
  error.value = ''
  success.value = ''

  try {
    const formData = new FormData()
    formData.append('name', form.value.name)
    formData.append('is_public', form.value.is_public)
    formData.append('join_policy', form.value.join_policy)
    formData.append('max_members', form.value.max_members)
    formData.append('description', form.value.description || '')
    if (form.value.avatar) {
      formData.append('avatar', form.value.avatar)
    }

    const res = await axios.post('/api/users/teams/', formData, {
      withCredentials: true, // 如果后端用 cookie 认证
      headers: { 'Content-Type': 'multipart/form-data' },
    })

    success.value = res.data.message || '团队创建成功'
    console.log('返回团队数据', res.data.team)

    // 可跳转到团队详情页或刷新菜单
    // router.push(`/teams/${res.data.team.id}`)
  } catch (err) {
    console.error(err)
    if (err.response?.data?.detail) {
      error.value = err.response.data.detail
    } else if (err.response?.data?.message) {
      error.value = err.response.data.message
    } else {
      error.value = '创建团队失败'
    }
  } finally {
    loading.value = false
  }
}
</script>
