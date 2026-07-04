<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">人物谱</h1>
      <p class="page-desc">三国全书 {{ persons.length }} 位人物 · 含有名有姓与无名称呼</p>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-bar classic-card">
      <div class="filter-row">
        <div class="filter-group">
          <span class="filter-label">势力</span>
          <el-radio-group v-model="filters.faction" size="small" @change="applyFilter">
            <el-radio-button :value="0">全部</el-radio-button>
            <el-radio-button v-for="f in factions" :key="f.id" :value="f.id">{{ f.name }}</el-radio-button>
          </el-radio-group>
        </div>
        <div class="filter-group">
          <span class="filter-label">分类</span>
          <el-radio-group v-model="filters.category" size="small" @change="applyFilter">
            <el-radio-button value="">全部</el-radio-button>
            <el-radio-button value="main">主要</el-radio-button>
            <el-radio-button value="supporting">重要</el-radio-button>
            <el-radio-button value="minor">次要</el-radio-button>
            <el-radio-button value="unnamed">无名</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div class="filter-row">
        <el-input v-model="filters.keyword" placeholder="搜索姓名/字/号..." clearable size="small" style="max-width:280px" @input="applyFilter">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
        <div class="filter-group">
          <span class="filter-label">排序</span>
          <el-select v-model="filters.sortBy" size="small" style="width:110px" @change="applyFilter">
            <el-option label="重要度" value="importance" />
            <el-option label="出场次数" value="appearanceCount" />
            <el-option label="首出场" value="firstAppearanceChapter" />
            <el-option label="姓名" value="name" />
          </el-select>
          <el-radio-group v-model="filters.order" size="small" @change="applyFilter">
            <el-radio-button value="desc">降序</el-radio-button>
            <el-radio-button value="asc">升序</el-radio-button>
          </el-radio-group>
        </div>
        <span class="result-count">共 {{ filtered.length }} 位</span>
      </div>
    </div>

    <!-- 人物网格 -->
    <div class="person-grid" v-loading="loading">
      <div
        v-for="p in paged"
        :key="p.id"
        class="person-card"
        :class="`cat-${p.category}`"
        @click="goDetail(p.id)"
      >
        <div class="card-avatar" :style="{ borderColor: factionColor(p.factionId) }">
          <img v-if="p.avatarUrl" :src="p.avatarUrl" :alt="p.name" />
          <span v-else :style="{ color: factionColor(p.factionId) }">{{ p.name.charAt(0) }}</span>
          <span class="avatar-faction" :style="{ background: factionColor(p.factionId) }">{{ factionName(p.factionId).charAt(0) }}</span>
        </div>
        <div class="card-info">
          <div class="card-name">{{ p.name }}</div>
          <div class="card-meta">
            <span v-if="p.courtesyName">字 {{ p.courtesyName }}</span>
            <span class="dot" v-if="p.courtesyName && p.role">·</span>
            <span v-if="p.role">{{ p.role }}</span>
          </div>
          <div class="card-tags" v-if="p.personalityTags.length">
            <span class="tag-mini" v-for="t in p.personalityTags.slice(0,2)" :key="t">{{ t }}</span>
          </div>
          <div class="card-foot">
            <span class="imp-stars">{{ '★'.repeat(Math.min(5, Math.ceil(p.importance/2))) }}</span>
            <span class="appear">出场 {{ p.appearanceCount }}</span>
          </div>
        </div>
      </div>
    </div>
    <el-empty v-if="!loading && filtered.length===0" description="无匹配人物" />

    <div class="pagination" v-if="filtered.length > pageSize">
      <el-pagination
        background layout="prev, pager, next"
        :total="filtered.length" :page-size="pageSize"
        v-model:current-page="page"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { persons } from '@/mock/persons'
import { factions, getFactionName, getFactionColor } from '@/mock/factions'
import type { Person } from '@/types'

const router = useRouter()
const route = useRoute()
const loading = ref(false)
const pageSize = 36
const page = ref(1)

const filters = reactive({
  faction: Number(route.query.faction) || 0,
  category: '',
  keyword: '',
  sortBy: 'importance',
  order: 'desc' as 'asc' | 'desc',
})

const filtered = ref<Person[]>([])

const applyFilter = () => {
  loading.value = true
  let list = [...persons]
  if (filters.faction) list = list.filter(p => p.factionId === filters.faction)
  if (filters.category) list = list.filter(p => p.category === filters.category)
  if (filters.keyword) {
    const k = filters.keyword
    list = list.filter(p => p.name.includes(k) || p.courtesyName.includes(k) || p.titleName.includes(k))
  }
  const key = filters.sortBy as keyof Person
  const o = filters.order === 'desc' ? -1 : 1
  list.sort((a: any, b: any) => {
    const va = a[key], vb = b[key]
    if (typeof va === 'number' && typeof vb === 'number') return (va - vb) * o
    return String(va||'').localeCompare(String(vb||'')) * o
  })
  filtered.value = list
  page.value = 1
  setTimeout(() => loading.value = false, 200)
}

const paged = computed(() => filtered.value.slice((page.value - 1) * pageSize, page.value * pageSize))

const factionName = (id: number) => getFactionName(id)
const factionColor = (id: number) => getFactionColor(id)
const goDetail = (id: number) => router.push(`/persons/${id}`)

onMounted(() => applyFilter())
</script>

<style scoped>
.filter-bar { padding: 18px 22px; margin-bottom: 24px; display: flex; flex-direction: column; gap: 14px; }
.filter-row { display: flex; align-items: center; gap: 20px; flex-wrap: wrap; }
.filter-group { display: flex; align-items: center; gap: 10px; }
.filter-label { font-size: 13px; color: var(--ink-soft); letter-spacing: 2px; }
.result-count { margin-left: auto; font-size: 13px; color: var(--gold); }

.person-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; }
.person-card {
  background: linear-gradient(135deg, #fdf6e3, #f5ecd7);
  border: 1px solid var(--line);
  border-radius: 10px;
  padding: 16px 12px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex; flex-direction: column; align-items: center;
  text-align: center;
}
.person-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-lg); border-color: var(--gold); }
.person-card.cat-unnamed { opacity: 0.85; background: linear-gradient(135deg, #ede4cf, #ddd0b0); }
.person-card.cat-unnamed .card-name { color: var(--ink-soft); }
.card-avatar {
  width: 72px; height: 72px; border-radius: 50%;
  border: 3px solid var(--gold);
  background: linear-gradient(135deg, #ebdfc4, #d9c9a3);
  display: flex; align-items: center; justify-content: center;
  font-size: 30px; font-family: "STKaiti", serif; font-weight: 700;
  position: relative; overflow: visible;
  margin-bottom: 10px;
}
.card-avatar img { width: 100%; height: 100%; border-radius: 50%; object-fit: cover; }
.avatar-faction {
  position: absolute; bottom: -2px; right: -2px;
  width: 22px; height: 22px; border-radius: 50%;
  color: #fff; font-size: 12px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  border: 2px solid #fdf6e3;
}
.card-name { font-size: 16px; font-weight: 700; font-family: "STKaiti", serif; color: var(--ink); margin-bottom: 4px; }
.card-meta { font-size: 12px; color: var(--ink-soft); margin-bottom: 8px; }
.card-meta .dot { margin: 0 4px; }
.card-tags { display: flex; gap: 4px; flex-wrap: wrap; justify-content: center; margin-bottom: 8px; min-height: 20px; }
.tag-mini { font-size: 10px; background: rgba(168,32,26,0.1); color: var(--vermilion); padding: 1px 6px; border-radius: 8px; }
.card-foot { display: flex; justify-content: space-between; width: 100%; font-size: 11px; color: var(--gold); padding-top: 6px; border-top: 1px dashed var(--line); }
.imp-stars { color: var(--vermilion); letter-spacing: -1px; }
.appear { color: var(--ink-soft); }

.pagination { margin-top: 32px; display: flex; justify-content: center; }

@media (max-width: 1100px) { .person-grid { grid-template-columns: repeat(4, 1fr); } }
@media (max-width: 700px) { .person-grid { grid-template-columns: repeat(2, 1fr); } }
</style>
