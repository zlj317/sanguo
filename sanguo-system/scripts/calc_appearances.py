import re, json

with open('/workspace/三国演义.txt', 'r', encoding='gb18030', errors='ignore') as f:
    text = f.read()

chapter_pattern = re.compile(r'第[一二三四五六七八九十百零\d]+回')
chapter_matches = list(chapter_pattern.finditer(text))
chapters = []
for i, m in enumerate(chapter_matches):
    start = m.start()
    end = chapter_matches[i+1].start() if i+1 < len(chapter_matches) else len(text)
    chapters.append(text[start:end])

print(f'共 {len(chapters)} 回')

persons_ts_path = '/workspace/sanguo-system/src/mock/persons.ts'
with open(persons_ts_path, 'r') as f:
    content = f.read()

blocks = re.findall(r'\{([^{}]+)\}', content)
persons = []
for b in blocks:
    pid_m = re.search(r'id:\s*(\d+)', b)
    name_m = re.search(r"name:\s*'([^']+)'", b)
    courtesy_m = re.search(r"courtesyName:\s*'([^']*)'", b)
    title_m = re.search(r"titleName:\s*'([^']*)'", b)
    faction_m = re.search(r'factionId:\s*(\d+)', b)
    cat_m = re.search(r"category:\s*'(\w+)'", b)
    hasname_m = re.search(r'hasName:\s*(true|false)', b)
    imp_m = re.search(r'importance:\s*(\d+)', b)
    avatar_m = re.search(r"avatarUrl:\s*'([^']*)'", b)
    if pid_m and name_m:
        persons.append({
            'id': int(pid_m.group(1)),
            'name': name_m.group(1),
            'courtesyName': courtesy_m.group(1) if courtesy_m else '',
            'titleName': title_m.group(1) if title_m else '',
            'factionId': int(faction_m.group(1)) if faction_m else 4,
            'category': cat_m.group(1) if cat_m else 'minor',
            'hasName': hasname_m.group(1) == 'true' if hasname_m else True,
            'importance': int(imp_m.group(1)) if imp_m else 3,
            'avatarUrl': avatar_m.group(1) if avatar_m else '',
        })

print(f'解析到 {len(persons)} 个人物')
for p in persons[:8]:
    print(f"  id={p['id']:3d}  name={p['name']:6s}  字={p['courtesyName']:6s}  势力={p['factionId']}")

name_to_id = {p['name']: p['id'] for p in persons}
id_to_person = {p['id']: p for p in persons}

special_aliases = {
    '刘备': ['刘备', '玄德', '刘皇叔', '使君', '先主', '刘玄德'],
    '关羽': ['关羽', '云长', '关公', '关云长', '美髯公'],
    '张飞': ['张飞', '翼德', '张翼德'],
    '诸葛亮': ['诸葛亮', '孔明', '卧龙', '诸葛孔明', '丞相'],
    '曹操': ['曹操', '孟德', '曹孟德', '曹公', '魏公', '魏王', '阿瞒'],
    '赵云': ['赵云', '子龙', '赵子龙', '常山赵子龙'],
    '吕布': ['吕布', '奉先', '吕奉先', '温侯'],
    '司马懿': ['司马懿', '仲达', '司马仲达', '宣王'],
    '孙权': ['孙权', '仲谋', '孙仲谋', '吴侯', '吴王'],
    '周瑜': ['周瑜', '公瑾', '周公瑾', '周郎'],
    '马超': ['马超', '孟起', '马孟起', '锦马超'],
    '黄忠': ['黄忠', '汉升', '黄汉升'],
    '魏延': ['魏延', '文长', '魏文长'],
    '庞统': ['庞统', '士元', '凤雏', '庞士元'],
    '姜维': ['姜维', '伯约', '姜伯约'],
    '孙策': ['孙策', '伯符', '孙伯符', '小霸王'],
    '孙坚': ['孙坚', '文台', '孙文台'],
    '董卓': ['董卓', '仲颖', '董太师', '董相国'],
    '袁绍': ['袁绍', '本初', '袁本初'],
    '袁术': ['袁术', '公路', '袁公路'],
    '刘表': ['刘表', '景升', '刘景升'],
    '郭嘉': ['郭嘉', '奉孝', '郭奉孝'],
    '荀彧': ['荀彧', '文若', '荀文若'],
    '鲁肃': ['鲁肃', '子敬', '鲁子敬'],
    '吕蒙': ['吕蒙', '子明', '吕子明'],
    '陆逊': ['陆逊', '伯言', '陆伯言'],
    '张辽': ['张辽', '文远', '张文远'],
    '许褚': ['许褚', '仲康', '虎痴'],
    '典韦': ['典韦'],
    '夏侯惇': ['夏侯惇', '元让', '夏侯元让'],
    '夏侯渊': ['夏侯渊', '妙才', '夏侯妙才'],
    '徐晃': ['徐晃', '公明', '徐公明'],
    '张郃': ['张郃', '俊乂', '儁乂'],
    '于禁': ['于禁', '文则'],
    '乐进': ['乐进', '文谦'],
    '李典': ['李典', '曼成'],
    '貂蝉': ['貂蝉'],
    '大乔': ['大乔'],
    '小乔': ['小乔'],
    '孙尚香': ['孙夫人', '孙尚香'],
    '刘禅': ['刘禅', '阿斗', '后主'],
    '曹植': ['曹植', '子建', '曹子建'],
    '曹丕': ['曹丕', '子桓', '魏文帝'],
    '司马昭': ['司马昭', '子上'],
    '司马师': ['司马师', '子元'],
    '邓艾': ['邓艾', '士载'],
    '钟会': ['钟会', '士季'],
    '甘宁': ['甘宁', '兴霸'],
    '太史慈': ['太史慈', '子义'],
    '凌统': ['凌统', '公绩'],
    '周泰': ['周泰', '幼平'],
    '徐盛': ['徐盛', '文向'],
    '丁奉': ['丁奉', '承渊'],
    '黄盖': ['黄盖', '公覆'],
    '程普': ['程普', '德谋'],
    '韩当': ['韩当', '义公'],
    '贾诩': ['贾诩', '文和'],
    '程昱': ['程昱', '仲德'],
    '法正': ['法正', '孝直'],
    '马谡': ['马谡', '幼常'],
    '马良': ['马良', '季常'],
    '廖化': ['廖化', '元俭'],
    '王平': ['王平', '子均'],
    '关平': ['关平'],
    '关兴': ['关兴', '安国'],
    '张苞': ['张苞'],
    '关索': ['关索'],
}

stop_short = ['将军', '丞相', '太守', '刺史', '都督', '主公', '陛下', '天子', '皇帝', '皇叔',
              '大王', '公子', '先生', '大夫', '尚书', '太尉', '司徒', '司空', '军师',
              '大汉', '黄巾', '贼人', '贼兵', '军士', '士兵', '百姓', '众人', '左右',
              '老人', '妇人', '女子', '庄客', '庄主', '县令', '县尉', '督邮', '刺史',
              '使者', '校尉', '郎中', '参军', '主簿', '从事', '别驾', '治中', '功曹']

person_stats = {}
for p in persons:
    name = p['name']
    als = []
    
    if name in special_aliases:
        als = special_aliases[name][:]
    else:
        als = [name]
        if p['courtesyName'] and p['hasName'] and len(p['courtesyName']) >= 2:
            als.append(p['courtesyName'])
        if p['titleName']:
            for t in re.split(r'[、·]', p['titleName']):
                t = t.strip()
                if t and len(t) >= 2 and t not in stop_short and t != name:
                    als.append(t)
    
    als = [a for a in als if a and len(a) >= 2 and a not in stop_short]
    
    total_count = 0
    first_chapter = None
    related_chapters = []
    
    for i, ch in enumerate(chapters):
        ch_count = 0
        for a in als:
            ch_count += ch.count(a)
        if ch_count > 0:
            total_count += ch_count
            related_chapters.append(i + 1)
            if first_chapter is None:
                first_chapter = i + 1
    
    person_stats[p['id']] = {
        'name': name,
        'aliases': als,
        'count': total_count,
        'firstChapter': first_chapter if first_chapter else 1,
        'relatedChapters': related_chapters[:20],
    }

top20 = sorted(person_stats.items(), key=lambda x: x[1]['count'], reverse=True)[:20]
print('\n出场次数Top 20:')
for pid, s in top20:
    print(f"  {s['name']:6s} (id={pid:3d}): {s['count']:4d}次, 首出场第{s['firstChapter']}回")

if 15 in person_stats:
    print(f'\n关羽(id=15): {person_stats[15]["count"]}次, 首出场第{person_stats[15]["firstChapter"]}回')
if 3 in person_stats:
    print(f'刘备(id=3): {person_stats[3]["count"]}次, 首出场第{person_stats[3]["firstChapter"]}回')
if 1 in person_stats:
    print(f'曹操(id=1): {person_stats[1]["count"]}次, 首出场第{person_stats[1]["firstChapter"]}回')

with open('/workspace/sanguo-system/src/mock/person_stats.json', 'w', encoding='utf-8') as f:
    json.dump(person_stats, f, ensure_ascii=False, indent=2)

print('\n统计数据已保存')
