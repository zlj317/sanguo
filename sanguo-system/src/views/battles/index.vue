<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">战役志</h1>
      <p class="page-desc">三国 {{ battles.length }} 场经典战役 · 铁马金戈 · 烽火连天</p>
    </div>
    <div class="battle-grid">
      <div v-for="b in battles" :key="b.id" class="battle-card classic-card" @click="router.push(`/battles/${b.id}`)">
        <div class="battle-top" :style="{ background: `linear-gradient(135deg, ${importanceColor(b.significance)}, ${importanceColor(b.significance)}cc)` }">
          <span class="b-chapter">第 {{ b.chapter }} 回</span>
          <span class="b-date">{{ b.date }}</span>
        </div>
        <div class="battle-body">
          <h3>{{ b.name }}</h3>
          <p class="b-alias" v-if="b.alias">「{{ b.alias }}」</p>
          <p class="b-loc"><el-icon><Location /></el-icon>{{ b.location }}</p>
          <p class="b-result" :style="{ color: resultColor(b.result) }">结果：{{ b.result }}</p>
          <p class="b-sig">{{ b.significance }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Location } from '@element-plus/icons-vue'
import { battles } from '@/mock/battles'

const router = useRouter()
const importanceColor = (s: string) => {
  if (s.includes('奠定') || s.includes('一统') || s.includes('灭亡')) return '#a8201a'
  if (s.includes('名扬') || s.includes('扬名') || s.includes('威震')) return '#b8860b'
  return '#6b7280'
}
const resultColor = (r: string) => r.includes('胜') ? '#2e7d52' : r.includes('相持') ? '#b8860b' : '#a8201a'
</script>

<style scoped>
.battle-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.battle-card { cursor: pointer; overflow: hidden; }
.battle-top {
  padding: 10px 18px; color: #fff;
  display: flex; justify-content: space-between; font-size: 12px;
}
.battle-body { padding: 18px 20px; }
.battle-body h3 { margin: 0 0 4px; font-size: 19px; font-family: "STKaiti", serif; color: var(--ink); }
.b-alias { margin: 0 0 8px; font-size: 12px; color: var(--gold); }
.b-loc { margin: 0 0 6px; font-size: 13px; color: var(--ink-soft); display: flex; align-items: center; gap: 4px; }
.b-result { margin: 0 0 8px; font-size: 13px; font-weight: 700; }
.b-sig { margin: 0; font-size: 12px; color: var(--ink-soft); line-height: 1.6; }
@media (max-width: 900px) { .battle-grid { grid-template-columns: 1fr; } }
</style>
