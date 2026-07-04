import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'home', component: () => import('@/views/home/index.vue'), meta: { title: '首页' } },
  { path: '/persons', name: 'persons', component: () => import('@/views/persons/index.vue'), meta: { title: '人物谱' } },
  { path: '/persons/:id', name: 'personDetail', component: () => import('@/views/persons/detail.vue'), meta: { title: '人物详情' } },
  { path: '/reading', name: 'reading', component: () => import('@/views/reading/index.vue'), meta: { title: '原文阅读' } },
  { path: '/battles', name: 'battles', component: () => import('@/views/battles/index.vue'), meta: { title: '战役志' } },
  { path: '/battles/:id', name: 'battleDetail', component: () => import('@/views/battles/detail.vue'), meta: { title: '战役详情' } },
  { path: '/timeline', name: 'timeline', component: () => import('@/views/timeline/index.vue'), meta: { title: '时间轴' } },
  { path: '/map', name: 'map', component: () => import('@/views/map/index.vue'), meta: { title: '地理图' } },
  { path: '/graph', name: 'graph', component: () => import('@/views/graph/index.vue'), meta: { title: '关系图' } },
  { path: '/search', name: 'search', component: () => import('@/views/search/index.vue'), meta: { title: '检索' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

router.afterEach((to) => {
  document.title = `${to.meta.title || ''} · 三国演义`
})

export default router
