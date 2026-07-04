import { persons } from '@/mock/persons'
import { factions } from '@/mock/factions'
import { locations } from '@/mock/locations'
import { battles } from '@/mock/battles'
import { chapters } from '@/mock/chapters'
import { timelineEvents } from '@/mock/timeline'
import { personRelations } from '@/mock/relations'
import type { Person } from '@/types'

export const api = {
  persons: {
    list: (params?: { factionId?: number; category?: string; hasName?: boolean; keyword?: string; sortBy?: string; sortOrder?: 'asc' | 'desc' }) => {
      let list = [...persons]
      if (params?.factionId) list = list.filter(p => p.factionId === params.factionId)
      if (params?.category) list = list.filter(p => p.category === params.category)
      if (params?.hasName !== undefined) list = list.filter(p => p.hasName === params.hasName)
      if (params?.keyword) {
        const k = params.keyword
        list = list.filter(p => p.name.includes(k) || p.courtesyName.includes(k) || p.titleName.includes(k))
      }
      if (params?.sortBy) {
        const key = params.sortBy as keyof Person
        const order = params.sortOrder === 'desc' ? -1 : 1
        list.sort((a, b) => {
          const va = a[key] as any, vb = b[key] as any
          if (typeof va === 'number' && typeof vb === 'number') return (va - vb) * order
          return String(va).localeCompare(String(vb)) * order
        })
      }
      return Promise.resolve(list)
    },
    getById: (id: number) => Promise.resolve(persons.find(p => p.id === id)),
    stats: () => Promise.resolve({
      total: persons.length,
      byFaction: factions.map(f => ({ id: f.id, name: f.name, count: persons.filter(p => p.factionId === f.id).length })),
      byCategory: ['main', 'supporting', 'minor', 'unnamed'].map(c => ({ category: c, count: persons.filter(p => p.category === c).length })),
    })
  },
  factions: { list: () => Promise.resolve(factions) },
  locations: { list: () => Promise.resolve(locations) },
  battles: { list: () => Promise.resolve(battles), getById: (id: number) => Promise.resolve(battles.find(b => b.id === id)) },
  chapters: { list: () => Promise.resolve(chapters), getByNumber: (n: number) => Promise.resolve(chapters.find(c => c.number === n)) },
  timeline: { list: () => Promise.resolve(timelineEvents) },
  relations: { list: () => Promise.resolve(personRelations) },
}
