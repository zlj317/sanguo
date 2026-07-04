import type { PersonRelation } from '@/types'

export const personRelations: PersonRelation[] = [
  // 桃园三兄弟
  { id:1, person1Id:1, person2Id:2, relationType:'结义兄弟', description:'桃园三结义，刘备为兄，关羽为二弟' },
  { id:2, person1Id:1, person2Id:3, relationType:'结义兄弟', description:'桃园三结义，张飞为三弟' },
  { id:3, person1Id:2, person2Id:3, relationType:'结义兄弟', description:'关羽张飞二弟三弟' },
  // 君臣
  { id:4, person1Id:1, person2Id:4, relationType:'君臣', description:'刘备三顾茅庐请诸葛亮' },
  { id:5, person1Id:1, person2Id:5, relationType:'君臣', description:'刘备与赵云' },
  { id:6, person1Id:1, person2Id:6, relationType:'君臣', description:'刘备收马超' },
  { id:7, person1Id:1, person2Id:7, relationType:'君臣', description:'刘备与黄忠' },
  { id:8, person1Id:1, person2Id:8, relationType:'君臣', description:'刘备与魏延' },
  { id:9, person1Id:1, person2Id:9, relationType:'君臣', description:'刘备与庞统' },
  { id:10, person1Id:1, person2Id:10, relationType:'君臣', description:'刘备与法正' },
  { id:11, person1Id:4, person2Id:11, relationType:'师徒', description:'诸葛亮传衣钵于姜维' },
  // 曹魏君臣
  { id:12, person1Id:14, person2Id:22, relationType:'君臣', description:'曹操与郭嘉' },
  { id:13, person1Id:14, person2Id:20, relationType:'君臣', description:'曹操与荀彧' },
  { id:14, person1Id:14, person2Id:21, relationType:'君臣', description:'曹操与荀攸' },
  { id:15, person1Id:14, person2Id:18, relationType:'宗亲', description:'曹操与夏侯惇族兄弟' },
  { id:16, person1Id:14, person2Id:24, relationType:'君臣', description:'曹操与典韦护卫' },
  { id:17, person1Id:14, person2Id:25, relationType:'君臣', description:'曹操与许褚护卫' },
  { id:18, person1Id:14, person2Id:15, relationType:'父子', description:'曹操与吕布（曾欲认父反被杀）' },
  { id:19, person1Id:14, person2Id:17, relationType:'君臣', description:'曹操与司马懿，托孤又忌惮' },
  // 东吴
  { id:20, person1Id:33, person2Id:38, relationType:'君臣', description:'孙权与周瑜' },
  { id:21, person1Id:33, person2Id:39, relationType:'君臣', description:'孙权与鲁肃' },
  { id:22, person1Id:33, person2Id:40, relationType:'君臣', description:'孙权与吕蒙' },
  { id:23, person1Id:33, person2Id:44, relationType:'君臣', description:'孙权与陆逊' },
  { id:24, person1Id:33, person2Id:45, relationType:'君臣', description:'孙权与甘宁' },
  { id:25, person1Id:31, person2Id:32, relationType:'父子', description:'孙坚孙策父子' },
  { id:26, person1Id:32, person2Id:33, relationType:'兄弟', description:'孙策孙权兄弟，兄终弟及' },
  { id:27, person1Id:38, person2Id:39, relationType:'同僚', description:'周瑜鲁肃，东吴战略支柱' },
  // 群雄
  { id:28, person1Id:15, person2Id:100, relationType:'父子', description:'吕布认董卓为义父后杀之' },
  { id:29, person1Id:100, person2Id:107, relationType:'君臣', description:'董卓与王允，被连环计所害' },
  { id:30, person1Id:107, person2Id:16, relationType:'义父女', description:'王允义女貂蝉行连环计' },
  { id:31, person1Id:15, person2Id:36, relationType:'主从', description:'吕布与陈宫，下邳同亡' },
  { id:32, person1Id:108, person2Id:109, relationType:'主从', description:'袁绍与颜良' },
  { id:33, person1Id:108, person2Id:110, relationType:'主从', description:'袁绍与文丑' },
  { id:34, person1Id:108, person2Id:111, relationType:'主从', description:'袁绍与田丰' },
  { id:35, person1Id:108, person2Id:112, relationType:'主从', description:'袁绍与沮授' },
  { id:36, person1Id:108, person2Id:14, relationType:'故交', description:'袁绍曹操少时好友后争霸' },
  // 敌对
  { id:37, person1Id:1, person2Id:14, relationType:'敌对', description:'刘备曹操，天下英雄唯使君与操耳' },
  { id:38, person1Id:4, person2Id:17, relationType:'敌对', description:'诸葛亮司马懿宿命对手' },
  { id:39, person1Id:2, person2Id:41, relationType:'敌对', description:'关羽吕蒙，白衣渡江之仇' },
  { id:40, person1Id:1, person2Id:33, relationType:'盟友', description:'孙刘联盟抗曹' },
  // 夫妻
  { id:41, person1Id:32, person2Id:53, relationType:'夫妻', description:'孙策大乔' },
  { id:42, person1Id:38, person2Id:54, relationType:'夫妻', description:'周瑜小乔' },
  { id:43, person1Id:1, person2Id:48, relationType:'夫妻', description:'刘备孙夫人，赔了夫人又折兵' },
  // 司马氏
  { id:44, person1Id:17, person2Id:18, relationType:'父子', description:'司马懿司马师' },
  { id:45, person1Id:17, person2Id:19, relationType:'父子', description:'司马懿司马昭' },
  { id:46, person1Id:19, person2Id:23, relationType:'父子', description:'司马昭司马炎' },
  // 蜀汉二代
  { id:47, person1Id:2, person2Id:12, relationType:'父子', description:'关羽关平' },
  { id:48, person1Id:2, person2Id:13, relationType:'父子', description:'关羽关兴' },
  { id:49, person1Id:3, person2Id:14, relationType:'父子', description:'张飞张苞' },
  { id:50, person1Id:1, person2Id:37, relationType:'父子', description:'刘备刘禅' },
  // 马家
  { id:51, person1Id:6, person2Id:50, relationType:'父子', description:'马超马岱' },
  // 三顾茅庐
  { id:52, person1Id:1, person2Id:9, relationType:'知遇', description:'刘备庞统' },
  // 蜀汉五虎
  { id:53, person1Id:2, person2Id:6, relationType:'同僚', description:'关羽马超，关羽欲入川比武' },
  { id:54, person1Id:2, person2Id:7, relationType:'同僚', description:'关羽黄忠，长沙之战后同僚' },
  { id:55, person1Id:5, person2Id:6, relationType:'同僚', description:'赵云马超' },
]

export const relationTypeColors: Record<string, string> = {
  '结义兄弟': '#dc2626',
  '君臣': '#f59e0b',
  '父子': '#8b5cf6',
  '兄弟': '#ec4899',
  '夫妻': '#ef4444',
  '师徒': '#10b981',
  '主从': '#3b82f6',
  '敌对': '#7f1d1d',
  '盟友': '#14b8a6',
  '同僚': '#6366f1',
  '宗亲': '#a855f7',
  '故交': '#0891b2',
  '知遇': '#059669',
  '义父女': '#db2777',
}
