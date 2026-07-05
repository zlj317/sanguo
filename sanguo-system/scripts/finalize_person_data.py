#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完善人物数据：
1. 手动校准主要人物的死亡回目
2. 从原文中精准提取容貌描写
3. 从回目标题提取经典故事
4. 修正相关章回（截止到死亡回目）
5. 更新 persons.ts
"""
import re, json

TXT = '/workspace/三国演义.txt'
ENHANCED_FILE = '/workspace/sanguo-system/src/mock/person_enhanced_data.json'
PERSONS_FILE = '/workspace/sanguo-system/src/mock/persons.ts'
OUT_FILE = '/workspace/sanguo-system/src/mock/persons_updated.ts'

# 主要人物死亡回目（根据《三国演义》原著校准）
DEATH_CHAPTERS = {
    # 汉末
    '张角': 2, '张宝': 2, '张梁': 2,
    '何进': 3, '董卓': 9, '丁原': 3,
    '孙坚': 7, '孙策': 29,
    '吕布': 19, '陈宫': 19, '高顺': 19,
    '典韦': 16,
    '袁术': 21, '袁绍': 32, '颜良': 26, '文丑': 27,
    '田丰': 31, '沮授': 30,
    '刘表': 40, '刘琦': 52,
    '郭嘉': 33, '太史慈': 53,
    '周瑜': 57, '鲁肃': 69, '吕蒙': 77,
    '庞统': 63, '张松': 62,
    '关羽': 77, '关平': 77, '周仓': 77,
    '曹操': 78, '曹丕': 91,
    '张飞': 81, '刘备': 85, '黄忠': 83,
    '马超': 91, '赵云': 97, '马谡': 96,
    '诸葛亮': 104, '魏延': 105,
    '张郃': 101, '司马懿': 108, '曹真': 100,
    '张辽': 86, '徐晃': 94, '于禁': 79,
    '甘宁': 83, '凌统': 72, '程普': 68,
    '黄盖': 62,
    '李傕': 17, '郭汜': 17,
    '华雄': 5, '潘凤': 5, '祖茂': 5,
    '孔融': 40, '祢衡': 23, '杨修': 72,
    '华佗': 78, '董承': 24,
    '吕布': 19,
    '陶谦': 12,
    '刘焉': 5,
    '马腾': 57, '韩遂': 64,
    '张鲁': 67,
    '夏侯渊': 71,
    '王朗': 93,
    '郝昭': 98,
    '曹爽': 107, '何晏': 107,
    '姜维': 119, '邓艾': 119, '钟会': 119,
    '诸葛恪': 108, '孙峻': 111, '孙綝': 113,
    '孙亮': 113,
    '司马懿': 108, '司马师': 110, '司马昭': 114,
    '司马炎': 120,  # 未死，晋朝建立
    '刘禅': 120,  # 未死，降魏
    '孙皓': 120,  # 未死，降晋
    '曹奂': 120,  # 未死，禅位
}

def read_text():
    with open(TXT, 'r', encoding='gb18030', errors='ignore') as f:
        return f.read()

def split_chapters(text):
    CN = {'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,'十':10,'零':0}
    def cn_to_int(s):
        if not s: return 0
        if s == '十': return 10
        if '百' in s:
            p = s.split('百')
            h = CN.get(p[0],1) if p[0] else 1
            rest = p[1] if len(p)>1 else ''
            if not rest: return h*100
            if rest.startswith('零'):
                rest = rest[1:]
                return h*100 + (cn_to_int(rest) if rest else 0)
            return h*100 + (cn_to_int(rest) if rest else 0)
        if '十' in s:
            p = s.split('十')
            tens = CN.get(p[0],1) if p[0] else 1
            ones = CN.get(p[1],0) if len(p)>1 and p[1] else 0
            return tens*10+ones
        tot=0
        for c in s:
            if c in CN: tot=tot*10+CN[c]
        return tot
    
    marker = re.compile(r'第([一二三四五六七八九十百零]+)回\s*')
    matches = list(marker.finditer(text))
    chapters = []
    for i,m in enumerate(matches):
        num = cn_to_int(m.group(1))
        start = m.end()
        rest = text[start:]
        idx = rest.find('\n')
        if idx == -1:
            title = rest.strip(); body = ''
        else:
            title = rest[:idx].strip()
            body_start = start+idx+1
            body_end = matches[i+1].start() if i+1<len(matches) else len(text)
            body = text[body_start:body_end].strip()
        if 1<=num<=120:
            chapters.append({'number':num,'title':title,'content':body})
    seen=set(); uniq=[]
    for c in chapters:
        if c['number'] not in seen:
            seen.add(c['number']); uniq.append(c)
    uniq.sort(key=lambda x:x['number'])
    return uniq

def extract_appearance_from_first_chapter(chapters, name, aliases, first_ch):
    """从首次出场章节提取容貌描写。"""
    desc_patterns = [
        r'身长[^。！？]{2,30}',
        r'生得[^。！？]{2,40}',
        r'面如[^。！？]{2,20}',
        r'貌若[^。！？]{2,20}',
        r'头戴[^。！？]{2,20}',
        r'身披[^。！？]{2,20}',
        r'手持[^。！？]{2,20}',
        r'坐下[^。！？]{2,20}',
        r'骑[^。！？]{2,15}马',
    ]
    
    descriptions = []
    
    # 在首次出场的前后3回中查找
    start_ch = max(1, first_ch - 2)
    end_ch = min(120, first_ch + 2)
    
    for ch in chapters:
        if ch['number'] < start_ch or ch['number'] > end_ch:
            continue
        
        content = ch['content']
        sentences = re.split(r'[。！？；]', content)
        
        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 10:
                continue
            
            # 必须包含人物名字或别名
            has_name = any(a in sent for a in aliases if len(a) >= 2)
            if not has_name:
                continue
            
            # 必须包含容貌描写关键词
            has_desc = any(re.search(p, sent) for p in desc_patterns)
            if not has_desc:
                continue
            
            # 排除明显是对话的句子
            if any(x in sent for x in ['曰：', '言曰', '问曰', '答曰', '谓曰', '对曰']):
                # 可能是对话中描述别人，也保留
                pass
            
            if 10 < len(sent) < 150:
                descriptions.append(sent)
    
    # 去重
    seen = set()
    unique = []
    for d in descriptions:
        if d not in seen:
            seen.add(d)
            unique.append(d)
    
    return unique[:8]

def extract_classic_stories(chapters, name, aliases):
    """从回目标题提取经典故事。"""
    stories = []
    
    for ch in chapters:
        title = ch['title']
        # 标题中包含人物名字或别名
        has_name = False
        matched_alias = ''
        for a in aliases:
            if len(a) >= 2 and a in title:
                has_name = True
                matched_alias = a
                break
        
        if has_name:
            stories.append({
                'chapter': ch['number'],
                'title': title,
                'matched': matched_alias,
            })
    
    return stories

def get_bio_snippets(chapters, name, aliases, first_ch):
    """从首次出场提取人物简介。"""
    snippets = []
    
    for ch in chapters:
        if ch['number'] < first_ch or ch['number'] > first_ch + 2:
            continue
        
        content = ch['content']
        
        # 找包含人物名 + 字/乃/是/为人/官拜 的句子
        for a in aliases[:3]:
            idx = content.find(a)
            if idx >= 0:
                # 前后扩展
                start = max(0, idx - 30)
                end = min(len(content), idx + 120)
                snippet = content[start:end].replace('\n', ' ').strip()
                
                # 清理到句子边界
                # 向前找句号
                dot_before = snippet.find('。')
                if dot_before >= 0 and dot_before < idx - start:
                    snippet = snippet[dot_before+1:]
                
                # 向后找句号
                dot_after = snippet.rfind('。')
                if dot_after > 0:
                    snippet = snippet[:dot_after+1]
                
                if len(snippet) > 20 and len(snippet) < 200:
                    snippets.append(snippet)
                break
    
    return snippets[:3]

def main():
    print('读取原文...')
    text = read_text()
    chapters = split_chapters(text)
    print(f'章回数: {len(chapters)}')
    
    # 读取当前 persons.ts 中的数据（通过解析）
    print('读取当前人物数据...')
    
    # 用简单方式：读取 enhanced_data 作为基础
    with open(ENHANCED_FILE, 'r', encoding='utf-8') as f:
        enhanced = json.load(f)
    
    # 建立 name -> data 映射
    name_to_data = {e['name']: e for e in enhanced}
    
    # 更新死亡回目（用手动校准的）
    for name, ch in DEATH_CHAPTERS.items():
        if name in name_to_data:
            name_to_data[name]['deathChapter'] = ch
    
    # 重新计算修正后的相关章回
    for name, data in name_to_data.items():
        death_ch = data.get('deathChapter')
        all_chs = data['allChapters']
        if death_ch:
            data['correctedChapters'] = [c for c in all_chs if c <= death_ch]
        else:
            data['correctedChapters'] = all_chs
    
    # 为每个人物提取容貌描写、经典故事
    print('提取容貌描写和经典故事...')
    count = 0
    for name, data in name_to_data.items():
        first_ch = data['firstChapter']
        aliases = data['aliases']
        
        # 提取容貌描写
        apperance = extract_appearance_from_first_chapter(chapters, name, aliases, first_ch)
        data['appearanceDescriptions'] = apperance
        
        # 提取经典故事
        stories = extract_classic_stories(chapters, name, aliases)
        data['classicStories'] = stories
        
        # 提取简介片段
        bio = get_bio_snippets(chapters, name, aliases, first_ch)
        data['bioSnippets'] = bio
        
        count += 1
        if count % 100 == 0:
            print(f'  已处理 {count}/{len(name_to_data)}...')
    
    # 保存更新后的数据
    with open('/workspace/sanguo-system/src/mock/person_final_data.json', 'w', encoding='utf-8') as f:
        json.dump(list(name_to_data.values()), f, ensure_ascii=False, indent=2)
    
    # 打印主要人物结果
    print('\n===== 主要人物数据校准结果 =====')
    top_names = ['诸葛亮', '刘备', '曹操', '关羽', '赵云', '张飞', '吕布', '周瑜', '司马懿', '孙权', '黄忠', '马超', '庞统', '鲁肃', '吕蒙', '陆逊', '袁绍', '刘表', '董卓', '赵云']
    for name in list(dict.fromkeys(top_names)):  # 去重保持顺序
        if name in name_to_data:
            d = name_to_data[name]
            print(f'\n【{name}】')
            print(f'  首出场: 第{d["firstChapter"]}回')
            print(f'  死亡回目: 第{d["deathChapter"]}回' if d.get('deathChapter') else '  死亡回目: 未明确')
            print(f'  原相关章回数: {len(d["allChapters"])}')
            print(f'  修正后章回数: {len(d["correctedChapters"])}')
            print(f'  修正后相关章回: {d["correctedChapters"][:10]}...' if len(d['correctedChapters']) > 10 else f'  修正后相关章回: {d["correctedChapters"]}')
            print(f'  容貌描写: {d["appearanceDescriptions"][:2]}')
            print(f'  经典故事数: {len(d["classicStories"])}')
            if d['classicStories']:
                print(f'  经典故事: {[s["title"] for s in d["classicStories"][:3]]}')
    
    print('\n完成！数据已保存。')

if __name__ == '__main__':
    main()
