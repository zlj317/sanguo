<template>
  <div class="page" v-if="person">
    <div class="back-bar">
      <el-button text @click="router.back()"><el-icon><ArrowLeft /></el-icon> 返回</el-button>
    </div>

    <div class="detail-hero classic-card" :style="{ borderTopColor: factionColor, borderTopWidth: '4px' }">
      <div class="hero-left">
        <div class="big-avatar" :style="{ borderColor: factionColor }">
          <img v-if="person.avatarUrl" :src="person.avatarUrl" :alt="person.name" />
          <span v-else :style="{ color: factionColor }">{{ person.name.charAt(0) }}</span>
        </div>
      </div>
      <div class="hero-right">
        <div class="name-row">
          <h1>{{ person.name }}</h1>
          <span class="seal" :style="{ background: factionColor }">{{ factionName }}</span>
        </div>
        <div class="subtitle-row">
          <span v-if="person.courtesyName">字 <b>{{ person.courtesyName }}</b></span>
          <span v-if="person.titleName">· {{ person.titleName }}</span>
        </div>
        <div class="bio">{{ person.biography }}</div>
        <div class="tag-row" v-if="person.personalityTags.length">
          <el-tag v-for="t in person.personalityTags" :key="t" size="small" effect="light" round>{{ t }}</el-tag>
        </div>
      </div>
    </div>

    <div class="detail-grid">
      <div class="info-card classic-card">
        <h3 class="card-h"><span class="seal">籍</span> 基本信息</h3>
        <el-descriptions :column="2" border size="small">
          <el-descriptions-item label="生卒">{{ person.birthYear }} - {{ person.deathYear }}</el-descriptions-item>
          <el-descriptions-item label="籍贯">{{ person.hometown }}</el-descriptions-item>
          <el-descriptions-item label="身份">{{ person.role }}</el-descriptions-item>
          <el-descriptions-item label="势力">{{ factionName }}</el-descriptions-item>
          <el-descriptions-item label="武器">{{ person.weapon || '—' }}</el-descriptions-item>
          <el-descriptions-item label="坐骑">{{ person.mount || '—' }}</el-descriptions-item>
          <el-descriptions-item label="首出场">第 {{ person.firstAppearanceChapter || '—' }} 回</el-descriptions-item>
          <el-descriptions-item label="出场次数">{{ person.appearanceCount }} 次</el-descriptions-item>
          <el-descriptions-item label="重要度" :span="2">
            <el-rate :model-value="person.importance/2" disabled show-score />
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <div class="info-card classic-card" v-if="person.appearance">
        <h3 class="card-h"><span class="seal">貌</span> 容貌</h3>
        <p class="content-text">{{ person.appearance }}</p>
      </div>

      <div class="info-card classic-card" v-if="person.classicStories.length">
        <h3 class="card-h"><span class="seal">事</span> 经典故事</h3>
        <div class="story-list">
          <div v-for="s in person.classicStories" :key="s" class="story-item">
            <el-icon><Star /></el-icon>{{ s }}
          </div>
        </div>
      </div>

      <div class="info-card classic-card" v-if="person.relatedChapters.length">
        <h3 class="card-h"><span class="seal">章</span> 相关章回</h3>
        <div class="chapter-tags">
          <el-tag v-for="c in person.relatedChapters" :key="c" type="info" effect="plain" size="small" class="ch-tag" @click="router.push(`/reading?chapter=${c}`)">第{{ c }}回</el-tag>
        </div>
      </div>

      <div class="info-card classic-card" v-if="relations.length">
        <h3 class="card-h"><span class="seal">关</span> 人际关系</h3>
        <div class="rel-list">
          <div v-for="r in relations" :key="r.id" class="rel-item" @click="router.push(`/persons/${r.otherId}`)">
            <span class="rel-type" :style="{ background: relColor(r.relationType) }">{{ r.relationType }}</span>
            <div class="rel-avatar" :style="{ borderColor: r.otherFactionColor }">
              <img v-if="r.otherAvatar" :src="r.otherAvatar" :alt="r.otherName" />
              <span v-else :style="{ color: r.otherFactionColor }">{{ r.otherName.charAt(0) }}</span>
            </div>
            <div class="rel-info">
              <span class="rel-name">{{ r.otherName }}</span>
              <span class="rel-desc" v-if="r.description">{{ r.description }}</span>
            </div>
            <el-icon class="rel-arrow"><ArrowRight /></el-icon>
          </div>
        </div>
      </div>
    </div>
  </div>
  <el-empty v-else description="人物不存在" />
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, ArrowRight, Star } from '@element-plus/icons-vue'
import { persons, getPersonById } from '@/mock/persons'
import { personRelations, relationTypeColors } from '@/mock/relations'
import { getFactionName, getFactionColor } from '@/mock/factions'

const router = useRouter()
const route = useRoute()
const id = Number(route.params.id)
const person = getPersonById(id)

const factionName = computed(() => person ? getFactionName(person.factionId) : '')
const factionColor = computed(() => person ? getFactionColor(person.factionId) : '')

const relations = computed(() => {
  if (!person) return []
  return personRelations
    .filter(r => r.person1Id === person.id || r.person2Id === person.id)
    .map(r => {
      const otherId = r.person1Id === person.id ? r.person2Id : r.person1Id
      const other = getPersonById(otherId)
      return {
        id: r.id,
        otherId,
        otherName: other?.name || '未知',
        otherAvatar: other?.avatarUrl || '',
        otherFactionColor: other ? getFactionColor(other.factionId) : '#6b7280',
        relationType: r.relationType,
        description: r.description
      }
    })
})

const relColor = (t: string) => relationTypeColors[t] || '#6b7280'
</script>

<style scoped>
.back-bar { margin-bottom: 16px; }

.detail-hero { display: flex; gap: 32px; padding: 28px; margin-bottom: 24px; }
.hero-left { flex-shrink: 0; }
.big-avatar {
  width: 160px; height: 160px; border-radius: 50%;
  border: 4px solid var(--gold);
  background: linear-gradient(135deg, #ebdfc4, #d9c9a3);
  display: flex; align-items: center; justify-content: center;
  font-size: 64px; font-family: "STKaiti", serif; font-weight: 700;
  overflow: hidden;
}
.big-avatar img { width: 100%; height: 100%; object-fit: cover; }
.hero-right { flex: 1; }
.name-row { display: flex; align-items: center; gap: 14px; margin-bottom: 8px; }
.name-row h1 { margin: 0; font-size: 38px; font-family: "STKaiti", serif; letter-spacing: 4px; }
.subtitle-row { color: var(--ink-soft); margin-bottom: 16px; font-size: 15px; }
.subtitle-row b { color: var(--vermilion); }
.bio { line-height: 1.9; color: var(--ink-soft); margin-bottom: 16px; text-indent: 2em; }
.tag-row { display: flex; gap: 8px; flex-wrap: wrap; }

.detail-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.info-card { padding: 22px; }
.card-h { display: flex; align-items: center; gap: 10px; margin: 0 0 16px; font-size: 18px; font-family: "STKaiti", serif; }
.content-text { line-height: 1.9; color: var(--ink-soft); margin: 0; text-indent: 2em; }
.story-list { display: flex; flex-direction: column; gap: 10px; }
.story-item { display: flex; align-items: center; gap: 8px; color: var(--ink); font-size: 14px; }
.story-item .el-icon { color: var(--vermilion); }
.chapter-tags { display: flex; flex-wrap: wrap; gap: 8px; }
.ch-tag { cursor: pointer; }
.rel-list { display: flex; flex-direction: column; gap: 10px; }
.rel-item { display: flex; align-items: center; gap: 12px; padding: 10px 12px; background: rgba(184,134,11,0.06); border-radius: 6px; cursor: pointer; transition: all 0.2s; }
.rel-item:hover { background: rgba(168,32,26,0.1); transform: translateX(4px); }
.rel-type { color: #fff; font-size: 12px; padding: 3px 10px; border-radius: 4px; white-space: nowrap; flex-shrink: 0; }
.rel-avatar { width: 40px; height: 40px; border-radius: 50%; border: 2px solid var(--gold); background: linear-gradient(135deg, #ebdfc4, #d9c9a3); display: flex; align-items: center; justify-content: center; font-size: 18px; font-family: "STKaiti", serif; font-weight: 700; overflow: hidden; flex-shrink: 0; }
.rel-avatar img { width: 100%; height: 100%; object-fit: cover; }
.rel-info { display: flex; flex-direction: column; gap: 2px; flex: 1; min-width: 0; }
.rel-name { font-weight: 700; font-size: 15px; }
.rel-desc { color: var(--ink-soft); font-size: 12px; }
.rel-arrow { color: var(--ink-soft); font-size: 14px; }

@media (max-width: 800px) {
  .detail-hero { flex-direction: column; align-items: center; text-align: center; }
  .detail-grid { grid-template-columns: 1fr; }
}
</style>
