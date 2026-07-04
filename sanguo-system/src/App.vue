<template>
  <div class="app-layout">
    <header class="app-header">
      <div class="header-inner">
        <div class="brand" @click="router.push('/')">
          <span class="brand-seal">三</span>
          <div class="brand-text">
            <h1>三国演义</h1>
            <p>智能分析系统</p>
          </div>
        </div>
        <nav class="nav-menu">
          <router-link
            v-for="item in menu"
            :key="item.path"
            :to="item.path"
            class="nav-item"
            :class="{ active: isActive(item.path) }"
          >
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </router-link>
        </nav>
      </div>
    </header>
    <main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <footer class="app-footer">
      <p>滚滚长江东逝水 · 浪花淘尽英雄 · 三国演义智能分析系统</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router'
import { Home, User, Reading, Flag, Timer, Location, Share, Search } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const menu = [
  { path: '/', label: '首页', icon: Home },
  { path: '/persons', label: '人物谱', icon: User },
  { path: '/reading', label: '原文', icon: Reading },
  { path: '/battles', label: '战役志', icon: Flag },
  { path: '/timeline', label: '时间轴', icon: Timer },
  { path: '/map', label: '地理图', icon: Location },
  { path: '/graph', label: '关系图', icon: Share },
  { path: '/search', label: '检索', icon: Search },
]

const isActive = (path: string) => {
  if (path === '/') return route.path === '/'
  return route.path.startsWith(path)
}
</script>

<style scoped>
.app-layout { min-height: 100vh; display: flex; flex-direction: column; }

.app-header {
  background: linear-gradient(180deg, #2a1010 0%, #1a0808 100%);
  border-bottom: 3px solid var(--gold);
  box-shadow: 0 2px 16px rgba(0,0,0,0.3);
  position: sticky; top: 0; z-index: 100;
}
.header-inner {
  max-width: 1320px; margin: 0 auto;
  padding: 0 28px;
  display: flex; align-items: center; justify-content: space-between;
  height: 64px;
}
.brand { display: flex; align-items: center; gap: 12px; cursor: pointer; }
.brand-seal {
  width: 42px; height: 42px;
  background: var(--vermilion);
  color: #fde9c8;
  font-family: "STKaiti", serif;
  font-size: 28px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(168,32,26,0.5);
}
.brand-text h1 {
  margin: 0; font-size: 20px; color: #f5e6c8;
  font-family: "STKaiti", serif; letter-spacing: 3px;
}
.brand-text p {
  margin: 0; font-size: 11px; color: #b8860b; letter-spacing: 2px;
}
.nav-menu { display: flex; gap: 4px; }
.nav-item {
  display: flex; align-items: center; gap: 5px;
  padding: 8px 14px;
  color: #d4c4a0;
  font-size: 14px;
  border-radius: 6px;
  transition: all 0.25s;
  letter-spacing: 1px;
}
.nav-item:hover { color: #fde9c8; background: rgba(184,134,11,0.15); }
.nav-item.active {
  color: #fde9c8; background: var(--vermilion);
  box-shadow: 0 2px 8px rgba(168,32,26,0.4);
}
.nav-item .el-icon { font-size: 16px; }

.app-main { flex: 1; }

.app-footer {
  background: #1a0808;
  border-top: 3px solid var(--gold);
  text-align: center;
  padding: 16px;
  color: #8a7a5a;
  font-size: 13px;
  letter-spacing: 2px;
}

.fade-enter-active, .fade-leave-active { transition: opacity 0.25s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

@media (max-width: 900px) {
  .nav-menu { gap: 0; }
  .nav-item span { display: none; }
  .nav-item { padding: 8px 10px; }
}
</style>
