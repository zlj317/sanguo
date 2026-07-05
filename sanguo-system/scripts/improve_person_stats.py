#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改进版出场统计：
- 区分"实际出场"（有对话/动作/直接描写）和"仅被提及"
- 实际出场：名字 + (曰/道/大怒/大惊/笑/曰/言/云/谓/问/答 等动词)
- 相关章回只算实际出场的章回
- 同时统计总提及次数（含被提及）
"""
import re, json

TXT = '/workspace/三国演义.txt'
IN_FILE = '/workspace/sanguo-system/src/mock/complete_person_stats.json'
OUT_FILE = '/workspace/sanguo-system/src/mock/complete_person_stats_v2.json'

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

def count_real_appearances(ch_content, name, aliases):
    """
    判断人物在本章是否实际出场（有对话或动作）。
    返回: (实际出场次数, 总提及次数)
    """
    # 实际出场的模式：名字 + 动词/对话/表情
    # 例如：孔明曰、孔明大惊、孔明笑曰、孔明大怒、孔明谓...
    action_verbs = [
        '曰', '言', '云', '道', '谓', '问', '答', '曰', '言', '云',
        '大怒', '大惊', '大笑', '大喝', '骂', '叱', '唤', '召',
        '笑', '哭', '叹', '喜', '怒', '惊', '惧', '恨',
        '乃', '即', '便', '遂', '自', '暗', '默', '私',
        '出', '入', '归', '往', '来', '走', '逃', '降', '败',
        '死', '薨', '卒', '亡', '病', '伤',
        '从', '引', '领', '带', '率', '统', '提', '驱',
        '见', '观', '望', '视', '顾',
        '听', '闻', '知', '觉',
        '曰', '言', '答曰', '对曰', '谏曰', '告曰',
        '起身', '上马', '下马', '拔剑', '掣刀',
        '与', '同', '共', '皆', '俱',
        '之', '命', '令', '使', '遣',
        '是', '乃', '为', '姓', '名',
    ]
    
    real_count = 0
    total_count = 0
    
    for alias in aliases:
        total_count += ch_content.count(alias)
    
    # 实际出场：名字后面紧跟着动作动词或表情
    for alias in aliases:
        for verb in action_verbs:
            pattern = alias + verb
            real_count += ch_content.count(pattern)
        # 名字前面有"是"、"乃"等判断动词
        for prefix in ['是', '乃', '为']:
            pattern = prefix + alias
            real_count += ch_content.count(pattern)
        # "姓名 + 字..." 介绍
        pattern = alias + '字'
        real_count += ch_content.count(pattern)
    
    # 还有一种情况：段落开头直接是人物名字说话
    # 比如 "孔明曰：..." 这种已经被上面的 "曰" 覆盖了
    
    # 如果只是名字在文本中，但没有任何动作/对话动词，则很可能只是被提及
    # 我们用一个阈值：如果实际出场特征 < 总提及的10%，且总提及次数很少，则认为只是被提及
    
    return real_count, total_count

def get_appearance_description(ch_content, name, aliases):
    """从原文中提取人物容貌/外貌描写。"""
    desc_patterns = [
        # 身长...，面...，...
        r'身长[^。]*?',
        r'面如[^。]*?',
        r'形貌[^。]*?',
        r'容貌[^。]*?',
        r'形容[^。]*?',
        r'生得[^。]*?',
        r'为人[^。]*?',
        r'有[^。]*?之貌',
        r'其人身长[^。]*?',
        r'只见[^。]*?',
        r'但见[^。]*?',
        r'头戴[^。]*?',
        r'身披[^。]*?',
        r'手持[^。]*?',
        r'坐下[^。]*?',
        r'骑[^。]*?马',
        r'手使[^。]*?',
    ]
    
    # 找包含人物别名 + 容貌描写特征的句子
    descriptions = []
    
    sentences = re.split(r'[。！？；]', ch_content)
    for sent in sentences:
        # 检查句子中是否有人物名字和容貌描写特征
        has_name = any(a in sent for a in aliases)
        has_desc = any(re.search(p, sent) for p in desc_patterns)
        if has_name and has_desc:
            sent = sent.strip()
            if len(sent) > 5 and len(sent) < 100:
                descriptions.append(sent)
    
    return descriptions

def get_classic_story_hints(ch_content, name, aliases, chapter_num):
    """从回目标题和内容中提取经典故事线索。"""
    stories = []
    # 回目标题通常包含关键事件
    return stories

def main():
    print('读取原文...')
    text = read_text()
    chapters = split_chapters(text)
    print(f'章回数: {len(chapters)}')
    
    with open(IN_FILE, 'r', encoding='utf-8') as f:
        old_stats = json.load(f)
    
    print(f'人物数: {len(old_stats)}')
    
    new_stats = []
    
    for i, s in enumerate(old_stats):
        name = s['name']
        aliases = s['aliases']
        
        real_total = 0
        mention_total = 0
        real_chapters = []
        all_chapters = []
        first_real_chapter = None
        first_mention_chapter = None
        
        # 容貌描写收集
        appearance_descs = set()
        
        for ch in chapters:
            real_c, total_c = count_real_appearances(ch['content'], name, aliases)
            
            if total_c > 0:
                all_chapters.append(ch['number'])
                mention_total += total_c
                if first_mention_chapter is None:
                    first_mention_chapter = ch['number']
            
            if real_c > 0:
                real_chapters.append(ch['number'])
                real_total += real_c
                if first_real_chapter is None:
                    first_real_chapter = ch['number']
                
                # 收集容貌描写
                descs = get_appearance_description(ch['content'], name, aliases)
                for d in descs:
                    if len(d) > 5:
                        appearance_descs.add(d)
        
        new_stats.append({
            'name': name,
            'aliases': aliases,
            'mentionCount': mention_total,        # 总提及次数
            'appearanceCount': len(real_chapters), # 实际出场章回数
            'realActionCount': real_total,        # 实际动作/对话次数
            'firstAppearanceChapter': first_real_chapter or first_mention_chapter,
            'realChapters': real_chapters,        # 实际出场章回
            'allChapters': all_chapters,          # 所有提及章回
            'appearanceDescriptions': list(appearance_descs)[:10],
        })
        
        if (i + 1) % 100 == 0:
            print(f'  已处理 {i+1}/{len(old_stats)}...')
    
    # 按实际出场章回数排序
    new_stats.sort(key=lambda x: -len(x['realChapters']))
    
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_stats, f, ensure_ascii=False, indent=2)
    
    print(f'\n已保存 -> {OUT_FILE}')
    
    # 查看前几名
    print('\n前20名（按实际出场章回数）:')
    for i, s in enumerate(new_stats[:20]):
        print(f"{i+1}. {s['name']}: 出场{len(s['realChapters'])}回, 提及{s['mentionCount']}次, 首出场第{s['firstAppearanceChapter']}回")
    
    # 查看诸葛亮的详细情况
    for s in new_stats:
        if s['name'] == '诸葛亮':
            print(f'\n诸葛亮详情:')
            print(f'  实际出场章回: {len(s["realChapters"])}回')
            print(f'  所有提及章回: {len(s["allChapters"])}回')
            print(f'  实际出场章回列表: {s["realChapters"]}')
            print(f'  死后(103回后)仍提及的章回: {[c for c in s["allChapters"] if c > 103]}')
            print(f'  容貌描写: {s["appearanceDescriptions"][:5]}')
            break

if __name__ == '__main__':
    main()
