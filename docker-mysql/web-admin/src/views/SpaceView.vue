<script setup>
import { onMounted, computed } from 'vue'
import { ref } from 'vue'
import AppCard from '@/components/AppCard.vue'
import { getSpace } from '@/data/getSpace'

const list = ref([])
const loading = ref(false)
const error = ref('')


onMounted(async () => {
  loading.value = true
  try {
    list.value = await getSpace()
  } catch (e) {
    error.value = e?.message || '加载失败'
  } finally {
    loading.value = false
  }
})
</script>


<template>
  <section class="min-h-dvh bg-slate-50 text-slate-800 antialiased">
    <div class="mx-auto max-w-screen-xl px-4 py-6 space-y-5">
      <header class="space-y-1">
        <h2 class="text-lg font-medium text-slate-900">工作空间列表</h2>
        <p class="text-sm text-slate-500">轻量卡片栅格，移动优先，自适应多端。</p>
      </header>

      <!-- 加载态 -->
      <el-skeleton v-if="loading" animated :count="6">
        <template #template>
          <div class="grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
            <div class="rounded-2xl border border-slate-200 bg-white p-5">
              <el-skeleton-item variant="image" style="width:56px;height:56px;border-radius:12px" />
              <el-skeleton-item variant="h1" style="width:60%;margin-top:12px" />
              <el-skeleton-item variant="text" />
              <el-skeleton-item variant="text" style="width:80%" />
            </div>
          </div>
        </template>
      </el-skeleton>

      <!-- 错误态 -->
      <el-alert v-else-if="error" type="error" :title="error" show-icon />

      <!-- 空态 -->
      <el-empty v-else-if="!list.length" description="暂无" />

      <!-- 数据态 -->
      <div v-else class="grid gap-5 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
        <AppCard v-for="item in list" :key="item.id" :item="item" />
      </div>
    </div>
  </section>
</template>
