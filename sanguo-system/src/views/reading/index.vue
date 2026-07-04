<template>
  <div class="reading-page">
    <!-- 左侧目录 -->
    <aside class="catalog" :class="{ open: catalogOpen }">
      <div class="catalog-header">
        <h3>目录</h3>
        <el-select v-model="curVolume" placeholder="卷" size="small" filterable @change="onVolume">
          <el-option label="全部" value="" />
          <el-option v-for="v in volumesList" :key="v" :label="v" :value="v" />
        </el-select>
      </div>
      <div class="catalog-list">
        <div
          v-for="c in filteredChapters"
          :key="c.number"
          class="catalog-item"
          :class="{ active: c.number === chapter, read: readChapters.includes(c.number) }"
          @click="selectChapter(c.number)"
        >
          <span class="num">{{ c.number }}</span>
          <span class="title">{{ c.title }}</span>
        </div>
      </div>
    </aside>

    <!-- 阅读区 -->
    <main class="reader">
      <div class="reader-toolbar classic-card">
        <el-button text @click="catalogOpen = !catalogOpen"><el-icon><Menu /></el-icon>目录</el-button>
        <div class="chapter-nav">
          <el-button size="small" :disabled="chapter<=1" @click="selectChapter(chapter-1)">上一回</el-button>
          <span class="cur-ch">第 {{ chapter }} 回</span>
          <el-button size="small" :disabled="chapter>=120" @click="selectChapter(chapter+1)">下一回</el-button>
        </div>
        <div class="font-ctrl">
          <el-button size="small" @click="fontSize--; save()">A-</el-button>
          <span class="fs">{{ fontSize }}</span>
          <el-button size="small" @click="fontSize++; save()">A+</el-button>
          <el-select v-model="fontFamily" size="small" style="width:90px" @change="save">
            <el-option label="宋体" value="STSong, SimSun, serif" />
            <el-option label="楷体" value="STKaiti, KaiTi, serif" />
            <el-option label="黑体" value="Microsoft YaHei, sans-serif" />
          </el-select>
        </div>
      </div>

      <article class="reading-article" v-if="curChapter" :style="{ fontSize: fontSize + 'px', fontFamily }">
        <!-- 章回装饰 -->
        <div class="chapter-illust">
          <svg viewBox="0 0 400 80" class="illust-svg">
            <g fill="none" stroke="var(--gold)" stroke-width="1">
              <path d="M20,40 Q60,10 100,40 T180,40" />
              <path d="M220,40 Q260,70 300,40 T380,40" />
              <circle cx="200" cy="40" r="6" fill="var(--vermilion)" stroke="none" />
              <circle cx="200" cy="40" r="14" />
            </g>
            <text x="200" y="72" text-anchor="middle" fill="var(--gold)" font-size="12" font-family="serif" letter-spacing="6">三国演义</text>
          </svg>
        </div>

        <h1 class="chapter-title">
          <span class="ch-label">第{{ cnNum(chapter) }}回</span>
        </h1>
        <h2 class="chapter-subtitle">{{ curChapter.title }}</h2>
        <div class="chapter-meta">
          <span>{{ curChapter.volume }}</span>
          <span class="sep">·</span>
          <span>{{ curChapter.wordCount }} 字</span>
        </div>

        <div class="chapter-content">
          <p v-for="(para, i) in paragraphs" :key="i" :class="{ 'first-para': i===0 }">{{ para }}</p>
        </div>

        <div class="chapter-illust bottom">
          <svg viewBox="0 0 400 40" class="illust-svg">
            <g fill="none" stroke="var(--gold)" stroke-width="1">
              <path d="M0,20 L160,20" />
              <path d="M240,20 L400,20" />
              <text x="200" y="26" text-anchor="middle" fill="var(--vermilion)" font-size="20" font-family="serif">❋</text>
            </g>
          </svg>
        </div>
      </article>

      <div class="reader-foot">
        <el-button type="primary" plain :disabled="chapter<=1" @click="selectChapter(chapter-1)">上一回</el-button>
        <el-button type="primary" plain :disabled="chapter>=120" @click="selectChapter(chapter+1)">下一回</el-button>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu } from '@element-plus/icons-vue'
import { chapters, getChapterByNumber, volumesList } from '@/mock/chapters'

const route = useRoute()
const router = useRouter()

const chapter = ref(Number(route.query.chapter) || Number(localStorage.getItem('sg_chapter')) || 1)
const fontSize = ref(Number(localStorage.getItem('sg_fs')) || 18)
const fontFamily = ref(localStorage.getItem('sg_ff') || 'STSong, SimSun, serif')
const readChapters = ref<number[]>(JSON.parse(localStorage.getItem('sg_read') || '[]'))
const catalogOpen = ref(false)
const curVolume = ref('')

const curChapter = computed(() => getChapterByNumber(chapter.value))
const filteredChapters = computed(() => curVolume.value ? chapters.filter(c => c.volume === curVolume.value) : chapters)
const paragraphs = computed(() => curChapter.value ? curChapter.value.content.split(/\n+/).filter((s: string) => s.trim()) : [])

const cnNum = (n: number) => {
  const cn = ['零','一','二','三','四','五','六','七','八','九','十']
  if (n <= 10) return cn[n]
  if (n < 20) return '十' + cn[n-10]
  if (n === 20) return '二十'
  if (n < 30) return '二十' + cn[n-20]
  if (n === 30) return '三十'
  if (n < 40) return '三十' + cn[n-30]
  if (n === 40) return '四十'
  if (n < 50) return '四十' + cn[n-40]
  if (n === 50) return '五十'
  if (n < 60) return '五十' + cn[n-50]
  if (n === 60) return '六十'
  if (n < 70) return '六十' + cn[n-60]
  if (n === 70) return '七十'
  if (n < 80) return '七十' + cn[n-70]
  if (n === 80) return '八十'
  if (n < 90) return '八十' + cn[n-80]
  if (n === 90) return '九十'
  if (n < 100) return '九十' + cn[n-90]
  if (n === 100) return '一百'
  if (n < 110) return '一百零' + cn[n-100]
  if (n < 120) return '一百' + cn[n-100].replace('十','十')
  return '一百二十'
}

const selectChapter = (n: number) => {
  if (n < 1 || n > 120) return
  chapter.value = n
  router.replace({ query: { chapter: n } })
  if (!readChapters.value.includes(n)) {
    readChapters.value.push(n)
    localStorage.setItem('sg_read', JSON.stringify(readChapters.value))
  }
  localStorage.setItem('sg_chapter', String(n))
  catalogOpen.value = false
  window.scrollTo(0, 0)
}

const onVolume = () => {}
const save = () => {
  localStorage.setItem('sg_fs', String(fontSize.value))
  localStorage.setItem('sg_ff', fontFamily.value)
}

watch(chapter, () => {
  if (!readChapters.value.includes(chapter.value)) {
    readChapters.value.push(chapter.value)
    localStorage.setItem('sg_read', JSON.stringify(readChapters.value))
  }
})

onMounted(() => {
  if (!readChapters.value.includes(chapter.value)) {
    readChapters.value.push(chapter.value)
    localStorage.setItem('sg_read', JSON.stringify(readChapters.value))
  }
})
</script>

<style scoped>
.reading-page { display: flex; max-width: 1400px; margin: 0 auto; min-height: calc(100vh - 64px); }

.catalog {
  width: 280px; flex-shrink: 0;
  background: linear-gradient(180deg, #fdf6e3, #f0e4cb);
  border-right: 1px solid var(--line);
  position: sticky; top: 64px;
  height: calc(100vh - 64px);
  overflow-y: auto;
  padding: 18px 14px;
}
.catalog-header { margin-bottom: 14px; }
.catalog-header h3 { margin: 0 0 10px; font-family: "STKaiti", serif; letter-spacing: 4px; }
.catalog-list { display: flex; flex-direction: column; gap: 2px; }
.catalog-item {
  display: flex; gap: 8px; align-items: baseline;
  padding: 7px 10px; border-radius: 5px; cursor: pointer;
  font-size: 13px; transition: all 0.2s;
}
.catalog-item:hover { background: rgba(184,134,11,0.12); }
.catalog-item.active { background: var(--vermilion); color: #fde9c8; }
.catalog-item.read .num { color: var(--gold); }
.catalog-item.active .num { color: #fde9c8; }
.catalog-item .num { font-size: 11px; color: var(--gold); min-width: 24px; }
.catalog-item .title { flex: 1; }

.reader { flex: 1; padding: 20px 32px 48px; min-width: 0; }
.reader-toolbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 10px 16px; margin-bottom: 24px;
  position: sticky; top: 72px; z-index: 10;
}
.chapter-nav { display: flex; align-items: center; gap: 12px; }
.cur-ch { font-family: "STKaiti", serif; color: var(--vermilion); font-weight: 700; }
.font-ctrl { display: flex; align-items: center; gap: 6px; }
.fs { font-size: 13px; min-width: 22px; text-align: center; color: var(--gold); }

.reading-article {
  max-width: 760px; margin: 0 auto;
  background: linear-gradient(180deg, #fdf6e3, #f7eed9);
  padding: 40px 56px;
  border: 1px solid var(--line);
  border-radius: 8px;
  box-shadow: var(--shadow);
}
.chapter-illust { text-align: center; margin-bottom: 20px; }
.illust-svg { width: 320px; height: auto; }
.chapter-illust.bottom { margin: 32px 0 0; }
.chapter-title { text-align: center; font-family: "STKaiti", serif; font-size: 28px; color: var(--vermilion); margin: 0 0 8px; letter-spacing: 6px; }
.chapter-subtitle { text-align: center; font-family: "STKaiti", serif; font-size: 22px; color: var(--ink); margin: 0 0 12px; letter-spacing: 3px; }
.chapter-meta { text-align: center; color: var(--gold); font-size: 13px; margin-bottom: 28px; }
.chapter-meta .sep { margin: 0 8px; }
.chapter-content p { text-indent: 2em; line-height: 1.9; margin: 0 0 14px; color: var(--ink-soft); }
.chapter-content p.first-para::first-letter { font-size: 1.8em; color: var(--vermilion); font-weight: 700; }

.reader-foot { display: flex; justify-content: space-between; max-width: 760px; margin: 24px auto 0; }

@media (max-width: 900px) {
  .catalog { position: fixed; left: -300px; z-index: 50; transition: left 0.3s; }
  .catalog.open { left: 0; }
  .reading-article { padding: 24px 20px; }
}
</style>
