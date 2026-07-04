<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">时间轴</h1>
      <p class="page-desc">三国百年 · 风云变幻 · 大事年表</p>
    </div>
    <div class="filter-bar classic-card">
      <el-radio-group v-model="filterType" size="small">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button value="政治">政治</el-radio-button>
        <el-radio-button value="军事">军事</el-radio-button>
        <el-radio-button value="人物">人物</el-radio-button>
      </el-radio-group>
    </div>
    <div class="timeline">
      <div class="timeline-line"></div>
      <div v-for="(e, i) in filtered" :key="e.id" class="tl-item" :class="{ left: i % 2 === 0 }">
        <div class="tl-dot" :style="{ background: typeColor(e.type) }"></div>
        <div class="tl-card classic-card">
          <div class="tl-year" :style="{ color: typeColor(e.type) }">{{ e.year }}</div>
          <h3 class="tl-title">{{ e.title }}</h3>
          <p class="tl-desc">{{ e.description }}</p>
          <div class="tl-meta">
            <span class="tl-type" :style="{ background: typeColor(e.type) }">{{ e.type }}</span>
            <span class="tl-ch">第{{ e.chapter }}回</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { timelineEvents } from '@/mock/timeline'

const filterType = ref('')
const filtered = computed(() => filterType.value ? timelineEvents.filter(e => e.type === filterType.value) : timelineEvents)
const typeColor = (t: string) => ({ '政治': '#3b82f6', '军事': '#a8201a', '人物': '#b8860b', '外交': '#2e7d52', '其他': '#6b7280' }[t] || '#6b7280')
</script>

<style scoped>
.filter-bar { padding: 14px 22px; margin-bottom: 32px; }
.timeline { position: relative; max-width: 900px; margin: 0 auto; padding: 20px 0; }
.timeline-line { position: absolute; left: 50%; top: 0; bottom: 0; width: 3px; background: linear-gradient(180deg, var(--gold), var(--vermilion), var(--gold)); transform: translateX(-50%); }
.tl-item { position: relative; width: 50%; padding: 12px 28px; margin-bottom: 16px; }
.tl-item.left { left: 0; text-align: right; }
.tl-item:not(.left) { left: 50%; }
.tl-dot { position: absolute; top: 24px; width: 16px; height: 16px; border-radius: 50%; border: 3px solid var(--paper); box-shadow: 0 0 0 2px var(--gold); z-index: 2; }
.tl-item.left .tl-dot { right: -8px; }
.tl-item:not(.left) .tl-dot { left: -8px; }
.tl-card { padding: 16px 20px; }
.tl-year { font-size: 18px; font-weight: 700; font-family: "STKaiti", serif; }
.tl-title { margin: 6px 0 8px; font-size: 17px; font-family: "STKaiti", serif; }
.tl-desc { margin: 0 0 10px; font-size: 13px; color: var(--ink-soft); line-height: 1.7; }
.tl-meta { display: flex; gap: 8px; font-size: 12px; align-items: center; }
.tl-item.left .tl-meta { justify-content: flex-end; }
.tl-type { color: #fff; padding: 1px 8px; border-radius: 3px; }
.tl-ch { color: var(--gold); }
@media (max-width: 700px) {
  .timeline-line { left: 12px; }
  .tl-item, .tl-item.left { width: 100%; left: 0; text-align: left; padding-left: 36px; padding-right: 12px; }
  .tl-item .tl-dot, .tl-item.left .tl-dot { left: 4px; right: auto; }
  .tl-item.left .tl-meta { justify-content: flex-start; }
}
</style>
