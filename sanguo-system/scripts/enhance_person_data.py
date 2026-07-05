#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从《三国演义》原文中系统提取人物信息：
1. 首出场回目和容貌描写
2. 死亡/退场回目
3. 经典故事（从回目标题提取）
4. 修正相关章回（截止到死亡/退场回目）
"""
import re, json

TXT = '/workspace/三国演义.txt'
IN_STATS = '/workspace/sanguo-system/src/mock/complete_person_stats.json'
OUT_FILE = '/workspace/sanguo-system/src/mock/person_enhanced_data.json'

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

def get_appearance_desc(chapters, name, aliases):
    """从原著中提取人物容貌描写。
    主要从首次出场的章节中提取。
    """
    # 容貌描写关键词
    desc_keywords = [
        '身长', '生得', '面如', '貌若', '形容', '形貌', '容貌',
        '头戴', '身披', '手持', '坐下', '骑', '手使',
        '丹凤眼', '卧蚕眉', '豹头', '环眼', '美髯',
        '面如冠玉', '唇若涂脂', '声若巨雷', '势如奔马',
        '细眼长髯', '方颐大口', '碧眼紫髯',
        '身长八尺', '身长九尺', '身长七尺', '身长一丈',
        '浓眉大眼', '阔面重颐',
    ]
    
    descriptions = []
    
    for ch in chapters:
        content = ch['content']
        sentences = re.split(r'[。！？；\n]', content)
        
        for sent in sentences:
            sent = sent.strip()
            if not sent or len(sent) < 10:
                continue
            
            # 句子中包含人物名字和容貌关键词
            has_name = any(a in sent for a in aliases)
            has_desc_kw = any(kw in sent for kw in desc_keywords)
            
            if has_name and has_desc_kw:
                # 过滤掉明显不是容貌描写的
                if any(x in sent for x in ['乃', '是', '曰', '言', '问', '答']):
                    # 如果是对话，跳过
                    if '曰' in sent or '言' in sent or '问' in sent or '答' in sent:
                        continue
                if len(sent) < 150:  # 不要太长的句子
                    descriptions.append(sent)
    
    # 去重并按出场顺序排序
    seen = set()
    unique = []
    for d in descriptions:
        if d not in seen and len(d) > 10:
            seen.add(d)
            unique.append(d)
    
    return unique[:10]

def find_death_chapter(chapters, name, aliases):
    """查找人物死亡/退场回目。
    基于死亡相关关键词。
    """
    death_keywords = [
        '死', '薨', '卒', '亡', '病逝', '病死', '气死', '吓死',
        '被杀', '被斩', '遇害', '身亡', '丧命', '殒命', '归天',
        '逝世', '去世', '身故', '绝命', '自刎', '自缢', '自裁',
        '中毒', '箭伤', '重伤', '死于', '死于', '战死', '阵亡',
        '关公败走麦城', '武侯归天', '陨大星', '五丈原',
    ]
    
    # 更精确的模式：人物名 + 死/薨/卒/亡/被杀/被斩/身亡 等
    death_patterns = []
    for a in aliases:
        death_patterns.extend([
            a + '死', a + '薨', a + '卒', a + '亡',
            a + '被杀', a + '被斩', a + '遇害', a + '身亡',
            a + '丧命', a + '归天', a + '病逝', a + '病死',
            '杀' + a, '斩' + a, '刺' + a, '诛' + a,
        ])
    
    death_chapter = None
    death_desc = ''
    
    for ch in chapters:
        content = ch['content']
        
        # 检查回目标题是否暗示人物死亡
        title = ch['title']
        title_death_kw = ['归天', '殒命', '被杀', '被斩', '死', '薨', '卒', '亡', '陨大星']
        title_has_death = any(kw in title for kw in title_death_kw)
        
        # 检查内容中是否有死亡描述
        has_death = False
        death_sentence = ''
        
        for pat in death_patterns:
            if pat in content:
                has_death = True
                # 找到包含这个模式的句子
                idx = content.find(pat)
                # 向前向后找句子
                start = max(0, idx - 50)
                end = min(len(content), idx + 50)
                death_sentence = content[start:end].replace('\n', ' ')
                break
        
        if has_death or (title_has_death and any(a in content for a in aliases)):
            # 确认这是死亡而不是一般提及
            # 简单的确认：名字后面跟着死亡相关词汇
            confirmed = False
            for a in aliases:
                for dw in ['死', '薨', '卒', '亡', '被杀', '被斩', '遇害', '身亡', '丧命', '归天', '病逝']:
                    if a + dw in content or a + '之死' in content:
                        confirmed = True
                        break
                if confirmed:
                    break
            
            # 或者回目标题明确且人物在本章出现
            if title_has_death and any(a in content for a in aliases):
                confirmed = True
            
            if confirmed:
                death_chapter = ch['number']
                death_desc = death_sentence if death_sentence else title
                # 继续找后面的，因为可能前面的是提及而不是真正死亡
                # 但通常第一次出现死亡就是真的死亡
    
    return death_chapter, death_desc

def extract_classic_stories(chapters, name, aliases):
    """从回目标题和内容中提取经典故事。"""
    stories = []
    
    # 检查回目标题中是否包含人物名字（或别名）
    for ch in chapters:
        title = ch['title']
        has_name = any(a in title for a in aliases if len(a) >= 2)
        
        if has_name:
            # 这一回的标题有人物，说明是重要回目
            stories.append({
                'chapter': ch['number'],
                'title': title,
            })
    
    return stories

def get_biography(chapters, name, aliases):
    """从原著中提取人物简介相关内容。"""
    # 找首次出场时的介绍
    intro_patterns = [
        '字', '乃', '是', '为人', '生得', '身长',
        '官至', '封为', '拜为',
    ]
    
    intros = []
    
    for ch in chapters[:30]:  # 主要人物一般在前30回出场
        content = ch['content']
        for a in aliases:
            idx = content.find(a)
            if idx >= 0:
                # 提取上下文
                start = max(0, idx - 20)
                end = min(len(content), idx + 100)
                context = content[start:end].replace('\n', ' ').strip()
                if len(context) > 20:
                    intros.append({'chapter': ch['number'], 'text': context})
                break
    
    return intros[:3]

def main():
    print('读取原文...')
    text = read_text()
    chapters = split_chapters(text)
    print(f'章回数: {len(chapters)}')
    
    with open(IN_STATS, 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    print(f'人物数: {len(stats)}')
    
    enhanced = []
    
    for i, s in enumerate(stats):
        name = s['name']
        aliases = s['aliases']
        all_chapters = s['relatedChapters']
        
        # 提取容貌描写
        appearance_descs = get_appearance_desc(chapters, name, aliases)
        
        # 查找死亡回目
        death_chapter, death_desc = find_death_chapter(chapters, name, aliases)
        
        # 提取经典故事
        classic_stories = extract_classic_stories(chapters, name, aliases)
        
        # 修正相关章回：如果有死亡回目，截止到死亡回目
        if death_chapter:
            corrected_chapters = [c for c in all_chapters if c <= death_chapter]
        else:
            corrected_chapters = all_chapters
        
        enhanced.append({
            'name': name,
            'aliases': aliases,
            'mentionCount': s['count'],
            'firstChapter': s['firstChapter'],
            'allChapters': all_chapters,
            'deathChapter': death_chapter,
            'deathDesc': death_desc,
            'correctedChapters': corrected_chapters,  # 截止到死亡回目
            'appearanceDescriptions': appearance_descs,
            'classicStories': classic_stories,
        })
        
        if (i + 1) % 100 == 0:
            print(f'  已处理 {i+1}/{len(stats)}...')
    
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(enhanced, f, ensure_ascii=False, indent=2)
    
    print(f'\n已保存 -> {OUT_FILE}')
    
    # 查看几个主要人物
    for target in ['诸葛亮', '关羽', '曹操', '刘备', '张飞', '赵云', '周瑜', '吕布', '司马懿', '鲁肃']:
        for e in enhanced:
            if e['name'] == target:
                print(f'\n{e["name"]}:')
                print(f'  首出场: 第{e["firstChapter"]}回')
                print(f'  死亡回目: 第{e["deathChapter"]}回' if e['deathChapter'] else '  死亡回目: 未明确')
                print(f'  所有提及章回数: {len(e["allChapters"])}')
                print(f'  修正后章回数: {len(e["correctedChapters"])}')
                print(f'  容貌描写: {e["appearanceDescriptions"][:3]}')
                print(f'  经典故事数: {len(e["classicStories"])}')
                if e['classicStories']:
                    print(f'  经典故事: {[s["title"] for s in e["classicStories"][:5]]}')
                break

if __name__ == '__main__':
    main()
