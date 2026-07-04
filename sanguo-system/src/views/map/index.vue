<template>
  <div class="map-page">
    <div class="map-header">
      <div class="header-left">
        <h1 class="page-title">地理图</h1>
        <p class="page-desc">三国疆域 · 势力分布 · 古战场</p>
      </div>
      <el-radio-group v-model="layer" size="default">
        <el-radio-button value="all">三国总图</el-radio-button>
        <el-radio-button value="faction">势力分布</el-radio-button>
        <el-radio-button value="battle">战场路线</el-radio-button>
      </el-radio-group>
    </div>
    <div class="map-wrap">
      <div ref="mapRef" class="leaflet-map"></div>
      <div class="legend classic-card">
        <h4>图例</h4>
        <template v-if="layer==='all'">
          <div v-for="t in typeLegend" :key="t.name" class="lg-item"><span class="lg-dot" :style="{background:t.color}"></span>{{ t.name }}</div>
        </template>
        <template v-else-if="layer==='faction'">
          <div v-for="f in factions.slice(0,3)" :key="f.id" class="lg-item"><span class="lg-rect" :style="{background:f.color+'66',borderColor:f.color}"></span>{{ f.name }}疆域</div>
        </template>
        <template v-else>
          <div class="lg-item"><span class="lg-diamond" style="background:#ec4899"></span>战役发生地</div>
          <div class="lg-item"><span class="lg-line" style="background:#a8201a"></span>进攻路线</div>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import { locations } from '@/mock/locations'
import { factions } from '@/mock/factions'
import { battles } from '@/mock/battles'

const mapRef = ref<HTMLElement | null>(null)
const layer = ref<'all' | 'faction' | 'battle'>('all')
let map: L.Map | null = null
let markers: L.Layer[] = []
let polygons: L.Layer[] = []
let lines: L.Layer[] = []

const typeLegend = [
  { name: '都城', color: '#ef4444' },
  { name: '城池', color: '#f59e0b' },
  { name: '关隘', color: '#8b5cf6' },
  { name: '地点', color: '#22c55e' },
  { name: '州郡', color: '#3b82f6' },
]
const typeColor = (t: string) => typeLegend.find(x => x.name === t)?.color || '#6b7280'

const clearAll = () => {
  markers.forEach(m => map?.removeLayer(m))
  polygons.forEach(p => map?.removeLayer(p))
  lines.forEach(l => map?.removeLayer(l))
  markers = []; polygons = []; lines = []
}

const renderAll = () => {
  clearAll()
  locations.forEach(loc => {
    const m = L.marker(loc.coordinates).addTo(map!)
    m.bindPopup(`<b>${loc.name}</b><br/>${loc.type} · ${loc.modernName}<br/>${loc.description}`)
    const icon = L.divIcon({ html: `<div style="width:14px;height:14px;border-radius:50%;background:${typeColor(loc.type)};border:2px solid #fff;box-shadow:0 0 4px rgba(0,0,0,.5)"></div>`, className: '', iconSize: [14,14] })
    m.setIcon(icon)
    markers.push(m)
  })
}

const renderFaction = () => {
  clearAll()
  factions.slice(0,3).forEach(f => {
    f.territory.forEach(t => {
      const poly = L.polygon(t.points, { color: f.color, weight: 2, fillColor: f.color, fillOpacity: 0.25 }).addTo(map!)
      poly.bindPopup(`<b>${f.name} · ${t.name}</b>`)
      polygons.push(poly)
    })
    const cap = locations.find(l => l.name === f.capital)
    if (cap) {
      const m = L.marker(cap.coordinates).addTo(map!)
      m.bindPopup(`<b>${f.name}都城 · ${f.capital}</b>`)
      markers.push(m)
    }
  })
}

const renderBattle = () => {
  clearAll()
  battles.filter(b => b.coordinates).forEach(b => {
    const m = L.marker(b.coordinates!).addTo(map!)
    m.bindPopup(`<b>${b.name}</b><br/>第${b.chapter}回 · ${b.date}<br/>结果：${b.result}`)
    const icon = L.divIcon({ html: `<div style="width:16px;height:16px;background:#ec4899;transform:rotate(45deg);border:2px solid #fff;box-shadow:0 0 4px rgba(0,0,0,.5)"></div>`, className: '', iconSize: [16,16] })
    m.setIcon(icon)
    markers.push(m)
  })
  // 几条经典战役路线
  const routes = [
    { name: '赤壁之战', color: '#a8201a', pts: [[34.26,117.19],[30.82,111.79],[29.72,113.90]] },
    { name: '夷陵之战', color: '#a8201a', pts: [[30.67,104.07],[31.05,109.54],[30.70,111.27]] },
    { name: '灭蜀之战', color: '#a8201a', pts: [[33.07,107.03],[32.28,105.45],[30.67,104.07]] },
  ]
  routes.forEach(r => {
    const line = L.polyline(r.pts, { color: r.color, weight: 3, opacity: 0.7, dashArray: '8,6' }).addTo(map!)
    line.bindPopup(r.name)
    lines.push(line)
  })
}

watch(layer, () => {
  if (layer.value === 'all') renderAll()
  else if (layer.value === 'faction') renderFaction()
  else renderBattle()
})

onMounted(() => {
  map = L.map(mapRef.value!, { zoomControl: true, attributionControl: false }).setView([33, 110], 4)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    subdomains: 'abcd', maxZoom: 18
  }).addTo(map)
  renderAll()
})

onBeforeUnmount(() => { map?.remove() })
</script>

<style scoped>
.map-page { padding: 24px 28px; }
.map-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px; max-width:1320px; margin-left:auto; margin-right:auto; }
.page-title { font-size: 30px; font-family: "STKaiti", serif; letter-spacing: 6px; margin: 0 0 6px; }
.page-desc { font-size: 14px; color: var(--ink-soft); margin: 0; }
.map-wrap { max-width: 1320px; margin: 0 auto; position: relative; }
.leaflet-map { height: 70vh; min-height: 500px; border: 1px solid var(--line); border-radius: 10px; filter: sepia(0.2); }
.legend { position: absolute; right: 16px; top: 16px; padding: 14px 18px; z-index: 500; }
.legend h4 { margin: 0 0 10px; font-family: "STKaiti", serif; }
.lg-item { display: flex; align-items: center; gap: 8px; font-size: 13px; margin-bottom: 6px; }
.lg-dot { width: 12px; height: 12px; border-radius: 50%; }
.lg-rect { width: 14px; height: 14px; border: 1px solid; }
.lg-diamond { width: 12px; height: 12px; transform: rotate(45deg); }
.lg-line { width: 18px; height: 3px; }
</style>
