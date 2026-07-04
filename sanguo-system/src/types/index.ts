export interface Person {
  id: number
  name: string
  courtesyName: string
  titleName: string
  birthYear: string
  deathYear: string
  hometown: string
  appearance: string
  weapon: string
  mount: string
  factionId: number
  role: string
  importance: number
  appearanceCount: number
  biography: string
  personalityTags: string[]
  avatarUrl: string
  classicStories: string[]
  relatedChapters: number[]
  hasName: boolean
  category: 'main' | 'supporting' | 'minor' | 'unnamed'
  firstAppearanceChapter?: number
}

export interface Faction {
  id: number
  name: string
  founderId: number
  capital: string
  description: string
  color: string
  territory: { name: string; points: [number, number][] }[]
}

export interface Location {
  id: number
  name: string
  alias?: string
  type: '都城' | '城池' | '关隘' | '地点' | '州郡'
  modernName: string
  coordinates: [number, number]
  factionId: number
  description: string
  appearanceCount: number
  relatedChapters?: number[]
}

export interface Battle {
  id: number
  name: string
  alias?: string
  date: string
  chapter: number
  factions: number[]
  commanders: number[]
  location: string
  coordinates?: [number, number]
  result: string
  significance: string
  description: string
  keyFigures?: number[]
}

export interface Chapter {
  number: number
  title: string
  content: string
  wordCount: number
  volume?: string
  keyPersons?: number[]
  keyBattles?: number[]
}

export interface PersonRelation {
  id: number
  person1Id: number
  person2Id: number
  relationType: string
  description?: string
}

export interface TimelineEvent {
  id: number
  year: string
  title: string
  description: string
  chapter: number
  type: '政治' | '军事' | '人物' | '外交' | '其他'
  relatedPersons?: number[]
  relatedBattles?: number[]
  importance: number
}

export interface MapLayer {
  id: string
  name: string
  type: 'faction' | 'battle' | 'location'
  visible: boolean
}
