<template>
  <div class="home-page">
    <!-- 英雄区 -->
    <section class="hero">
      <div class="hero-bg"></div>
      <div class="hero-content">
        <div class="hero-seal">三國演義</div>
        <h1 class="hero-title">三国演义</h1>
        <p class="hero-subtitle">滚滚长江东逝水 · 浪花淘尽英雄</p>
        <p class="hero-desc">基于《三国演义》全书的智能分析系统 · 人物 谱 · 战役志 · 地理图 · 关系网</p>
        <div class="hero-stats">
          <div class="stat-item" v-for="s in stats" :key="s.label">
            <div class="stat-num">{{ s.value }}</div>
            <div class="stat-label">{{ s.label }}</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 势力卡 -->
    <section class="section">
      <h2 class="section-title"><span class="title-deco">◆</span> 三国鼎立 <span class="title-deco">◆</span></h2>
      <div class="faction-grid">
        <div
          v-for="f in factions.slice(0,3)"
          :key="f.id"
          class="faction-card"
          :style="{ '--fc': f.color }"
          @click="router.push(`/persons?faction=${f.id}`)"
        >
          <div class="faction-banner" :style="{ background: `linear-gradient(135deg, ${f.color}, ${f.color}cc)` }">
            <span class="faction-char">{{ f.name.charAt(0) }}</span>
          </div>
          <div class="faction-body">
            <h3>{{ f.name }}</h3>
            <p class="faction-capital">都城 · {{ f.capital }}</p>
            <p class="faction-desc">{{ f.description }}</p>
            <div class="faction-count">{{ personCount(f.id) }} 位人物</div>
          </div>
        </div>
      </div>
    </section>

    <!-- 功能入口 -->
    <section class="section">
      <h2 class="section-title"><span class="title-deco">◆</span> 功能导览 <span class="title-deco">◆</span></h2>
      <div class="feature-grid">
        <div v-for="f in features" :key="f.path" class="feature-card classic-card" @click="router.push(f.path)">
          <el-icon class="feature-icon"><component :is="f.icon" /></el-icon>
          <h3>{{ f.title }}</h3>
          <p>{{ f.desc }}</p>
        </div>
      </div>
    </section>

    <!-- 经典战役 -->
    <section class="section">
      <h2 class="section-title"><span class="title-deco">◆</span> 经典战役 <span class="title-deco">◆</span></h2>
      <div class="battle-strip">
        <div v-for="b in featuredBattles" :key="b.id" class="battle-chip" @click="router.push(`/battles/${b.id}`)">
          <span class="battle-chapter">第{{ b.chapter }}回</span>
          <span class="battle-name">{{ b.name }}</span>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { User, Reading, Flag, Timer, Location, Share, Search } from '@element-plus/icons-vue'
import { persons } from '@/mock/persons'
import { factions } from '@/mock/factions'
import { battles } from '@/mock/battles'
import { chapters } from '@/mock/chapters'

const router = useRouter()

const stats = computed(() => [
  { label: '人物', value: persons.length },
  { label: '章回', value: chapters.length },
  { label: '战役', value: battles.length },
  { label: '势力', value: factions.length },
])

const personCount = (fid: number) => persons.filter(p => p.factionId === fid).length

const features = [
  { path: '/persons', title: '人物谱', desc: '全390位三国人物，含有名无名角色', icon: User },
  { path: '/reading', title: '原文阅读', desc: '120回全本原文，仿古排版', icon: Reading },
  { path: '/battles', title: '战役志', desc: '28场经典战役详解', icon: Flag },
  { path: '/timeline', title: '时间轴', desc: '三国百年大事年表', icon: Timer },
  { path: '/map', title: '地理图', desc: '三国总图·势力分布·战场', icon: Location },
  { path: '/graph', title: '关系图', desc: '人物关系网络可视化', icon: Share },
  { path: '/search', title: '检索', desc: '全文检索人物战役', icon: Search },
]

const featuredBattles = battles.filter(b => [15,10,19,21,22,25,26].includes(b.id))
</script>

<style scoped>
.home-page { padding-bottom: 40px; }

.hero {
  position: relative;
  min-height: 460px;
  display: flex; align-items: center; justify-content: center;
  overflow: hidden;
  border-bottom: 3px solid var(--gold);
}
.hero-bg {
  position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at center, rgba(168,32,26,0.25), rgba(26,8,8,0.95)),
    linear-gradient(135deg, #2a1010, #1a0808);
}
.hero-bg::before {
  content: '三';
  position: absolute;
  font-size: 560px;
  color: rgba(184,134,11,0.06);
  font-family: "STKaiti", serif;
  font-weight: 700;
  top: 50%; left: 50%;
  transform: translate(-50%,-50%);
}
.hero-content { position: relative; text-align: center; color: #f5e6c8; padding: 40px 20px; }
.hero-seal {
  display: inline-block;
  background: var(--vermilion);
  color: #fde9c8;
  padding: 6px 24px;
  font-family: "STKaiti", serif;
  font-size: 18px;
  letter-spacing: 8px;
  border-radius: 4px;
  margin-bottom: 20px;
  box-shadow: 0 4px 16px rgba(168,32,26,0.5);
}
.hero-title {
  font-size: 72px;
  font-family: "STKaiti", "KaiTi", serif;
  letter-spacing: 16px;
  margin: 0 0 12px;
  background: linear-gradient(180deg, #fde9c8, #b8860b);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-subtitle {
  font-size: 18px;
  letter-spacing: 6px;
  color: #d4c4a0;
  margin: 0 0 8px;
}
.hero-desc {
  font-size: 14px;
  color: #8a7a5a;
  letter-spacing: 2px;
  margin: 0 0 32px;
}
.hero-stats { display: flex; gap: 40px; justify-content: center; }
.stat-item { text-align: center; }
.stat-num {
  font-size: 36px; font-weight: 700;
  color: var(--gold-light);
  font-family: "STKaiti", serif;
}
.stat-label { font-size: 13px; color: #8a7a5a; letter-spacing: 3px; margin-top: 4px; }

.section { max-width: 1280px; margin: 48px auto 0; padding: 0 28px; }
.section-title {
  text-align: center;
  font-size: 26px;
  font-family: "STKaiti", serif;
  letter-spacing: 8px;
  color: var(--ink);
  margin: 0 0 28px;
}
.title-deco { color: var(--vermilion); font-size: 16px; }

.faction-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.faction-card {
  background: linear-gradient(135deg, #fdf6e3, #f5ecd7);
  border: 1px solid var(--line);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: var(--shadow);
}
.faction-card:hover { transform: translateY(-5px); box-shadow: var(--shadow-lg); border-color: var(--fc); }
.faction-banner {
  height: 110px;
  display: flex; align-items: center; justify-content: center;
  position: relative;
}
.faction-banner::after {
  content: ''; position: absolute; inset: 8px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 6px;
}
.faction-char {
  font-size: 60px;
  font-family: "STKaiti", serif;
  color: rgba(255,255,255,0.95);
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}
.faction-body { padding: 18px 22px 22px; }
.faction-body h3 { margin: 0 0 6px; font-size: 22px; font-family: "STKaiti", serif; color: var(--fc); }
.faction-capital { font-size: 13px; color: var(--ink-soft); margin: 0 0 10px; }
.faction-desc { font-size: 13px; color: var(--ink-soft); line-height: 1.7; margin: 0 0 12px; }
.faction-count {
  font-size: 13px; color: var(--gold);
  border-top: 1px dashed var(--line);
  padding-top: 10px;
}

.feature-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.feature-card {
  padding: 26px 20px;
  text-align: center;
  cursor: pointer;
}
.feature-icon {
  font-size: 34px; color: var(--vermilion);
  margin-bottom: 12px;
}
.feature-card h3 { margin: 0 0 6px; font-size: 17px; font-family: "STKaiti", serif; }
.feature-card p { margin: 0; font-size: 12px; color: var(--ink-soft); line-height: 1.6; }

.battle-strip {
  display: flex; gap: 12px; flex-wrap: wrap; justify-content: center;
}
.battle-chip {
  background: linear-gradient(135deg, #fdf6e3, #ebdfc4);
  border: 1px solid var(--line);
  border-radius: 24px;
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.25s;
  display: flex; flex-direction: column; align-items: center;
  min-width: 120px;
}
.battle-chip:hover { background: var(--vermilion); color: #fde9c8; transform: scale(1.05); }
.battle-chip:hover .battle-chapter { color: #fde9c8; }
.battle-chapter { font-size: 11px; color: var(--gold); }
.battle-name { font-size: 15px; font-family: "STKaiti", serif; font-weight: 700; }

@media (max-width: 900px) {
  .faction-grid, .feature-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-title { font-size: 48px; }
  .hero-stats { gap: 24px; }
}
</style>
