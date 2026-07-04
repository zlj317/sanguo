import type { Chapter } from '@/types'
import chaptersData from './chapters_content.json'

// 12卷分组
const volumes = [
  { name: '黄巾之乱', range: [1, 2] },
  { name: '董卓之乱', range: [3, 9] },
  { name: '群雄逐鹿', range: [10, 20] },
  { name: '官渡之战', range: [21, 33] },
  { name: '赤壁之战', range: [34, 50] },
  { name: '三气周瑜', range: [51, 57] },
  { name: '西取益州', range: [58, 65] },
  { name: '汉中称王', range: [66, 73] },
  { name: '败走麦城', range: [74, 77] },
  { name: '夷陵之战', range: [78, 85] },
  { name: '六出祁山', range: [86, 105] },
  { name: '三分归晋', range: [106, 120] },
]

const getVolume = (num: number): string => {
  for (const v of volumes) {
    if (num >= v.range[0] && num <= v.range[1]) return v.name
  }
  return ''
}

export const chapters: Chapter[] = Object.entries(chaptersData).map(([num, data]: [string, any]) => {
  const n = parseInt(num)
  return {
    number: n,
    title: data.title,
    content: data.content,
    wordCount: data.content.length,
    volume: getVolume(n),
  }
})

export const getChapterByNumber = (num: number) => chapters.find(c => c.number === num)
export const getChaptersByVolume = (volume: string) => chapters.filter(c => c.volume === volume)
export const volumesList = volumes.map(v => v.name)
