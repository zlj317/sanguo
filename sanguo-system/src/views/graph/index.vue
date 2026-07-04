<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">关系图</h1>
      <p class="page-desc">三国人物关系网络 · 君臣父子 · 兄弟敌对</p>
    </div>
    <div class="graph-wrap">
      <div class="control-panel classic-card">
        <h4>势力筛选</h4>
        <el-checkbox-group v-model="selFactions">
          <el-checkbox v-for="f in factions" :key="f.id" :value="f.id">
            <span class="fc-dot" :style="{background:f.color}"></span>{{ f.name }}
          </el-checkbox>
        </el-checkbox-group>
        <el-divider />
        <h4>关系类型</h4>
        <el-checkbox-group v-model="selTypes">
          <el-checkbox v-for="(c, t) in relationTypeColors" :key="t" :value="t">
            <span class="rt-line" :style="{background:c}"></span>{{ t }}
          </el-checkbox>
        </el-checkbox-group>
        <el-divider />
        <el-button type="primary" plain size="small" @click="reset" style="width:100%">重置视图</el-button>
      </div>
      <div ref="cyRef" class="cy-container"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import cytoscape from 'cytoscape'
import { persons, getPersonById } from '@/mock/persons'
import { personRelations, relationTypeColors } from '@/mock/relations'
import { factions, getFactionColor } from '@/mock/factions'

const cyRef = ref<HTMLElement | null>(null)
const selFactions = ref<number[]>(factions.map(f => f.id))
const selTypes = ref<string[]>(Object.keys(relationTypeColors))
let cy: any = null

const buildGraph = () => {
  const validIds = new Set(persons.filter(p => selFactions.value.includes(p.factionId)).map(p => p.id))
  const nodes = persons
    .filter(p => validIds.has(p.id) && p.importance >= 5)
    .map(p => ({
      data: { id: String(p.id), name: p.name, faction: p.factionId, color: getFactionColor(p.factionId), size: 20 + p.importance * 3 }
    }))
  const nodeIds = new Set(nodes.map(n => n.data.id))
  const edges = personRelations
    .filter(r => selTypes.value.includes(r.relationType)
      && nodeIds.has(String(r.person1Id)) && nodeIds.has(String(r.person2Id)))
    .map(r => ({
      data: { id: `e${r.id}`, source: String(r.person1Id), target: String(r.person2Id), type: r.relationType, color: relationTypeColors[r.relationType] }
    }))
  return { nodes, edges }
}

const render = () => {
  const { nodes, edges } = buildGraph()
  if (cy) cy.destroy()
  cy = cytoscape({
    container: cyRef.value,
    elements: [...nodes, ...edges],
    style: [
      { selector: 'node', style: {
        'background-color': 'data(color)', 'width': 'data(size)', 'height': 'data(size)',
        'label': 'data(name)', 'color': '#1a1410', 'font-size': '11px',
        'text-valign': 'bottom', 'text-margin-y': 4, 'border-width': 2, 'border-color': '#fff',
      }},
      { selector: 'edge', style: {
        'width': 2, 'line-color': 'data(color)', 'target-arrow-color': 'data(color)',
        'target-arrow-shape': 'triangle', 'curve-style': 'bezier', 'opacity': 0.7,
      }},
      { selector: ':selected', style: { 'border-width': 4, 'border-color': '#a8201a' } }
    ],
    layout: { name: 'cose', animate: true, nodeRepulsion: 8000, idealEdgeLength: 100 } as any
  })
  cy.on('tap', 'node', (evt: any) => {
    const id = Number(evt.target.id())
    const p = getPersonById(id)
    if (p) alert(`${p.name}（字${p.courtesyName||'—'}）· ${p.role}`)
  })
}

const reset = () => { cy?.fit(undefined, 40) }
watch([selFactions, selTypes], () => render())
onMounted(() => render())
onBeforeUnmount(() => cy?.destroy())
</script>

<style scoped>
.graph-wrap { display: flex; gap: 20px; height: 75vh; min-height: 540px; }
.control-panel { width: 220px; padding: 18px; overflow-y: auto; flex-shrink: 0; }
.control-panel h4 { margin: 0 0 12px; font-family: "STKaiti", serif; }
.fc-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 4px; }
.rt-line { display: inline-block; width: 16px; height: 3px; margin-right: 4px; vertical-align: middle; }
.cy-container { flex: 1; background: linear-gradient(135deg, #fdf6e3, #f0e4cb); border: 1px solid var(--line); border-radius: 10px; }
@media (max-width: 800px) { .graph-wrap { flex-direction: column; height: auto; } .control-panel { width: 100%; } .cy-container { height: 500px; } }
</style>
