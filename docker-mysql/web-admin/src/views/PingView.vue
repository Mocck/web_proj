<script setup>
import { ref, onMounted } from 'vue'
import { ping } from '@/api'

const pingResult = ref(null)

onMounted(async () => {
  const res = await ping()
  pingResult.value = res.data
})
</script>


<template>
  <div>
    <h1>Ping 接口返回结果</h1>
    <pre>{{ JSON.stringify(pingResult, null, 2) }}</pre>
  </div>
</template>