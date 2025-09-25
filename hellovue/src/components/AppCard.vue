<script setup>
import { computed, onMounted} from 'vue'
import { Download, ChatDotSquare } from '@element-plus/icons-vue'


const props = defineProps({ item: { type: Object, required: true } })
const isFree = computed(() => Number(props.item.price) === 0)
const priceLabel = computed(() => isFree.value ? '免费' : `¥${Number(props.item.price).toLocaleString()}`)
</script>

<template>
  <article
    class="group rounded-2xl border border-slate-200 bg-white p-5 shadow-[0_1px_0_rgba(0,0,0,0.02)]
           hover:shadow-md hover:-translate-y-0.5 transition-all duration-200 focus-within:shadow-md"
    role="button" tabindex="0" :aria-label="item.name"
  >
    <div class="flex items-start gap-4">
      <img :src="item.avatar" :alt="item.name" loading="lazy"
           class="size-14 rounded-xl object-cover ring-1 ring-slate-100" />

      <div class="min-w-0 flex-1">
        <div class="flex items-center justify-between gap-2">
          <h3 class="font-semibold truncate pr-2 text-slate-900">{{ item.name }}</h3>
          <span
            class="text-xs px-2 py-0.5 rounded-full ring-1"
            :class="isFree
              ? 'bg-emerald-50 text-emerald-700 ring-emerald-100'
              : 'bg-amber-50 text-amber-700 ring-amber-100'"
          >
            {{ priceLabel }}
          </span>
        </div>

        <p class="mt-1 text-sm text-slate-600 line-clamp-2">{{ item.description }}</p>

        <div class="mt-3 flex flex-wrap items-center gap-3">
          <el-rate :model-value="item.rating" disabled show-score score-template="{value}" class="!text-yellow-400" />
          <div class="text-xs text-slate-500 flex items-center gap-1" aria-label="下载量">
            <el-icon><Download /></el-icon>{{ item.downloads }}
          </div>
          <div class="text-xs text-slate-500 flex items-center gap-1" aria-label="评价数">
            <el-icon><ChatDotSquare /></el-icon>{{ item.reviews }}
          </div>
        </div>

        <div class="mt-3 flex flex-wrap gap-2">
          <el-tag v-for="t in item.tags" :key="t" size="small" effect="plain" type="info" round>{{ t }}</el-tag>
        </div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.line-clamp-2 { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; }
</style>
