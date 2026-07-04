<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">检索</h1>
      <p class="page-desc">全文检索 · 人物 · 战役 · 地点</p>
    </div>
    <div class="search-box classic-card">
      <el-input v-model="keyword" placeholder="输入关键词搜索..." size="large" clearable @input="search">
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
      <el-radio-group v-model="scope" size="small" @change="search">
        <el-radio-button value="all">全部</el-radio-button>
        <el-radio-button value="persons">人物</el-radio-button>
        <el-radio-button value="battles">战役</el-radio-button>
        <el-radio-button value="locations">地点</el-radio-button>
        <el-radio-button value="chapters">章回</el-radio-button>
      </el-radio-group>
    </div>

    <div class="results" v-if="keyword">
      <div v-if="results.persons.length && (scope==='all'||scope==='persons')" class="result-section">
        <h3>人物 ({{ results.persons.length }})</h3>
        <div class="r-list">
          <div v-for="p in results.persons.slice(0,20)" :key="p.id" class="r-item" @click="router.push(`/persons/${p.id}`)">
            <div class="r-avatar" :style="{borderColor:getFactionColor(p.factionId)}"><span :style="{color:getFactionColor(p.factionId)}">{{p.name.charAt(0)}}</span></div>
            <div class="r-info"><b>{{p.name}}</b> <span class="r-meta">字{{p.courtesyName}} · {{p.role}}</span></div>
          </div>
        </div>
      </div>
      <div v-if="results.battles.length && (scope==='all'||scope==='battles')" class="result-section">
        <h3>战役 ({{ results.battles.length }})</h3>
        <div class="r-list">
          <div v-for="b in results.battles" :key="b.id" class="r-item" @click="router.push(`/battles/${b.id}`)">
            <div class="r-icon" style="background:#a8201a"><el-icon><Flag /></el-icon></div>
            <div class="r-info"><b>{{b.name}}</b> <span class="r-meta">第{{b.chapter}}回 · {{b.date}}</span></div>
          </div>
        </div>
      </div>
      <div v-if="results.locations.length && (scope==='all'||scope==='locations')" class="result-section">
        <h3>地点 ({{ results.locations.length }})</h3>
        <div class="r-list">
          <div v-for="l in results.locations" :key="l.id" class="r-item" @click="router.push('/map')">
            <div class="r-icon" style="background:#3b82f6"><el-icon><Location /></el-icon></div>
            <div class="r-info"><b>{{l.name}}</b> <span class="r-meta">{{l.type}} · 今{{l.modernName}}</span></div>
          </div>
        </div>
      </div>
      <div v-if="results.chapters.length && (scope==='all'||scope==='chapters')" class="result-section">
        <h3>章回 ({{ results.chapters.length }})</h3>
        <div class="r-list">
          <div v-for="c in results.chapters" :key="c.number" class="r-item" @click="router.push(`/reading?chapter=${c.number}`)">
            <div class="r-icon" style="background:#b8860b"><el-icon><Reading /></el-icon></div>
            <div class="r-info"><b>第{{c.number}}回 {{c.title}}</b></div>
          </div>
        </div>
      </div>
      <el-empty v-if="!hasResults" description="未找到相关结果" />
    </div>
    <div v-else class="hot-search classic-card">
      <h3>热门搜索</h3>
      <div class="hot-tags">
        <el-tag v-for="h in hot" :key="h" class="hot-tag" @click="keyword=h;search()">{{ h }}</el-tag>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { Search, Flag, Location, Reading } from '@element-plus/icons-vue'
import { persons } from '@/mock/persons'
import { battles } from '@/mock/battles'
import { locations } from '@/mock/locations'
import { chapters } from '@/mock/chapters'
import { getFactionColor } from '@/mock/factions'

const router = useRouter()
const keyword = ref('')
const scope = ref('all')
const hot = ['诸葛亮','曹操','关羽','赤壁','官渡','夷陵','五丈原','空城计']

const results = reactive({ persons: [] as any[], battles: [] as any[], locations: [] as any[], chapters: [] as any[] })
const hasResults = computed(() => results.persons.length || results.battles.length || results.locations.length || results.chapters.length)

const search = () => {
  const k = keyword.value.trim()
  if (!k) { Object.keys(results).forEach(r => (results as any)[r] = []); return }
  results.persons = persons.filter(p => p.name.includes(k) || p.courtesyName.includes(k) || p.titleName.includes(k) || p.biography.includes(k))
  results.battles = battles.filter(b => b.name.includes(k) || b.alias?.includes(k) || b.description.includes(k) || b.significance.includes(k))
  results.locations = locations.filter(l => l.name.includes(k) || l.alias?.includes(k) || l.modernName.includes(k) || l.description.includes(k))
  results.chapters = chapters.filter(c => c.title.includes(k) || c.content.includes(k))
}
</script>

<style scoped>
.search-box { padding: 20px 24px; margin-bottom: 28px; display: flex; flex-direction: column; gap: 16px; }
.results { display: flex; flex-direction: column; gap: 24px; }
.result-section h3 { font-family: "STKaiti", serif; color: var(--vermilion); margin: 0 0 14px; letter-spacing: 3px; }
.r-list { display: grid; grid-template-columns: repeat(2,1fr); gap: 10px; }
.r-item { display: flex; align-items: center; gap: 12px; padding: 10px 14px; background: linear-gradient(135deg,#fdf6e3,#f5ecd7); border:1px solid var(--line); border-radius: 8px; cursor: pointer; transition: all .2s; }
.r-item:hover { border-color: var(--gold); transform: translateX(4px); }
.r-avatar { width:40px;height:40px;border-radius:50%;border:2px solid;background:linear-gradient(135deg,#ebdfc4,#d9c9a3);display:flex;align-items:center;justify-content:center;font-family:"STKaiti",serif;font-weight:700;font-size:18px; }
.r-icon { width:40px;height:40px;border-radius:8px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:18px; }
.r-info b { font-size: 15px; }
.r-meta { color: var(--ink-soft); font-size: 12px; margin-left: 6px; }
.hot-search { padding: 28px; }
.hot-search h3 { margin: 0 0 16px; font-family: "STKaiti", serif; }
.hot-tags { display: flex; flex-wrap: wrap; gap: 10px; }
.hot-tag { cursor: pointer; }
@media (max-width: 700px) { .r-list { grid-template-columns: 1fr; } }
</style>
