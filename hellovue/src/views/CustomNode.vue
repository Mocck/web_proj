<template>
  <div class="custom-node border rounded bg-white shadow-md p-2 flex flex-col items-center">
    <Handle type="target" position="top" id="input" class="bg-blue-500 w-3 h-3 rounded-full" />
    <div class="p-2 text-center">{{ data.label }}</div>
    <Handle type="source" position="bottom" id="output" class="bg-green-500 w-3 h-3 rounded-full" />
  </div>
</template>

<script setup>
import { Handle } from '@vue-flow/core'
defineProps({
  data: Object
})
</script>

<style scoped>
.custom-node {
  width: 120px;
  min-height: 60px;
}
</style>
