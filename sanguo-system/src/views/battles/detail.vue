<template>
  <div class="page" v-if="battle">
    <div class="back-bar"><el-button text @click="router.back()"><el-icon><ArrowLeft /></el-icon> 返回</el-button></div>

    <div class="b-hero classic-card">
      <div class="b-hero-top">
        <span class="seal big">第{{ battle.chapter }}回</span>
        <h1>{{ battle.name }}</h1>
        <p class="alias" v-if="battle.alias">「{{ battle.alias }}」</p>
      </div>
      <div class="b-meta">
        <span><el-icon><Timer /></el-icon> {{ battle.date }}</span>
        <span><el-icon><Location /></el-icon> {{ battle.location }}</span>
      </div>
    </div>

    <div class="b-grid">
      <div class="info-card classic-card">
        <h3 class="card-h"><span class="seal">战</span> 战役概述</h3>
        <p class="content">{{ battle.description }}</p>
      </div>
      <div class="info-card classic-card">
        <h3 class="card-h"><span class="seal">果</span> 结果与意义</h3>
        <p class="result" :style="{ color: battle.result.includes('胜') ? '#2e7d52' : '#a8201a' }">{{ battle.result }}</p>
        <p class="sig">{{ battle.significance }}</p>
      </div>
      <div class="info-card classic-card">
        <h3 class="card-h"><span class="seal">帅</span> 参战势力与主帅</h3>
        <div class="faction-list">
          <div v-for="fid in battle.factions" :key="fid" class="faction-block" :style="{ borderLeftColor: getFactionColor(fid) }">
            <div class="fb-name" :style="{ color: getFactionColor(fid) }">{{ getFactionName(fid) }}</div>
            <div class="fb-cmds">
              <span v-for="cid in battle.commanders.filter(c => getPersonById(c)?.factionId === fid)" :key="cid" class="cmd-chip" @click="router.push(`/persons/${cid}`)">
                {{ getPersonName(cid) }}
              </span>
            </div>
          </div>
        </div>
      </div>
      <div class="info-card classic-card" v-if="battle.keyFigures?.length">
        <h3 class="card-h"><span class="seal">杰</span> 关键人物</h3>
        <div class="figure-grid">
          <div v-for="fid in battle.keyFigures" :key="fid" class="figure-chip" @click="router.push(`/persons/${fid}`)">
            <div class="fig-avatar" :style="{ borderColor: getFactionColor(getPersonById(fid)?.factionId||4) }">
              <span :style="{ color: getFactionColor(getPersonById(fid)?.factionId||4) }">{{ getPersonName(fid).charAt(0) }}</span>
            </div>
            <span>{{ getPersonName(fid) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft, Timer, Location } from '@element-plus/icons-vue'
import { battles, getBattleById } from '@/mock/battles'
import { getPersonById, getPersonName } from '@/mock/persons'
import { getFactionName, getFactionColor } from '@/mock/factions'

const router = useRouter()
const route = useRoute()
const battle = getBattleById(Number(route.params.id))
</script>

<style scoped>
.back-bar { margin-bottom: 16px; }
.b-hero { padding: 32px; text-align: center; margin-bottom: 24px; }
.b-hero-top { margin-bottom: 16px; }
.b-hero-top h1 { margin: 12px 0 6px; font-size: 36px; font-family: "STKaiti", serif; letter-spacing: 6px; }
.seal.big { font-size: 14px; padding: 4px 14px; }
.alias { color: var(--gold); margin: 0; }
.b-meta { display: flex; gap: 24px; justify-content: center; color: var(--ink-soft); font-size: 14px; }
.b-meta span { display: flex; align-items: center; gap: 4px; }
.b-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.info-card { padding: 22px; }
.card-h { display: flex; align-items: center; gap: 10px; margin: 0 0 14px; font-size: 18px; font-family: "STKaiti", serif; }
.content { line-height: 1.9; color: var(--ink-soft); margin: 0; text-indent: 2em; }
.result { font-size: 16px; font-weight: 700; margin: 0 0 10px; }
.sig { color: var(--ink-soft); margin: 0; }
.faction-list { display: flex; flex-direction: column; gap: 12px; }
.faction-block { padding: 10px 14px; background: rgba(184,134,11,0.06); border-left: 4px solid; border-radius: 4px; }
.fb-name { font-weight: 700; font-family: "STKaiti", serif; margin-bottom: 6px; }
.fb-cmds { display: flex; gap: 8px; flex-wrap: wrap; }
.cmd-chip { background: #fff; border: 1px solid var(--line); padding: 3px 12px; border-radius: 12px; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.cmd-chip:hover { background: var(--vermilion); color: #fde9c8; border-color: var(--vermilion); }
.figure-grid { display: flex; gap: 14px; flex-wrap: wrap; }
.figure-chip { display: flex; flex-direction: column; align-items: center; gap: 6px; cursor: pointer; font-size: 13px; }
.fig-avatar { width: 48px; height: 48px; border-radius: 50%; border: 2px solid; background: linear-gradient(135deg, #ebdfc4, #d9c9a3); display: flex; align-items: center; justify-content: center; font-family: "STKaiti", serif; font-weight: 700; font-size: 20px; }
.figure-chip:hover .fig-avatar { box-shadow: 0 0 0 3px rgba(184,134,11,0.3); }
@media (max-width: 800px) { .b-grid { grid-template-columns: 1fr; } }
</style>
