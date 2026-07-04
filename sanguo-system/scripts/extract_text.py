#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从《三国演义》原文提取120回内容和人物列表。原文为gb18030编码。"""
import re, json, os

TXT = '/workspace/三国演义.txt'
OUT_DIR = '/workspace/sanguo-system/src/mock'
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

def read_text():
    with open(TXT,'r',encoding='gb18030',errors='ignore') as f:
        return f.read()

def split_chapters(text):
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

# 核心人物名册
PERSON_NAMES = """刘备 关羽 张飞 诸葛亮 赵云 马超 黄忠 魏延 庞统 法正 姜维 关平 关兴 张苞 马岱 廖化 马良 马谡 简雍 孙乾 糜竺 糜芳 刘封 孟达 严颜 李严 王平 张翼 张嶷 吴懿 费祎 董允 蒋琬 杨仪 邓芝 刘禅 刘琦 刘璋 刘焉 甘夫人 糜夫人 孙夫人 黄月英
曹操 曹丕 曹叡 曹芳 曹髦 曹奂 曹仁 曹洪 曹纯 曹真 曹爽 夏侯惇 夏侯渊 夏侯尚 夏侯玄 荀彧 荀攸 贾诩 郭嘉 程昱 刘晔 满宠 吕虔 毛玠 典韦 许褚 张辽 张郃 徐晃 于禁 乐进 李典 庞德 文聘 曹休 司马懿 司马师 司马昭 司马炎 邓艾 钟会 陈群 钟繇 华歆 王朗 杨修 陈登 孔融 祢衡 董昭 伏皇后 董贵妃 甄氏 蔡琰
孙坚 孙策 孙权 孙亮 孙休 孙皓 程普 黄盖 韩当 祖茂 蒋钦 周泰 陈武 董袭 凌统 甘宁 太史慈 吕蒙 陆逊 周瑜 鲁肃 张昭 张纮 诸葛瑾 步骘 顾雍 张温 陆绩 阚泽 丁奉 徐盛 潘璋 朱然 朱桓 全琮 陆抗 大乔 小乔 吴国太
董卓 吕布 貂蝉 王允 李傕 郭汜 张济 樊稠 李儒 华雄 牛辅 袁绍 袁术 袁谭 袁熙 袁尚 颜良 文丑 高览 淳于琼 田丰 沮授 审配 逢纪 许攸 郭图 辛评 辛毗 陈琳 刘表 刘琮 蔡瑁 张允 蒯越 蒯良 黄祖 张鲁 阎圃 马腾 韩遂 公孙瓒 公孙康 陶谦 张邈 陈宫 张杨 李肃 何进 张让 赵忠 卢植 皇甫嵩 朱儁 丁原 伍琼 周毖 杨彪 士孙瑞 董承 伏完 张角 张宝 张梁 程远志 邓茂""".split()

def extract_persons(chapters):
    stat = {n:{'count':0,'first':None} for n in PERSON_NAMES}
    for ch in chapters:
        c = ch['content']
        for n in PERSON_NAMES:
            cnt = c.count(n)
            if cnt>0:
                stat[n]['count'] += cnt
                if stat[n]['first'] is None:
                    stat[n]['first'] = ch['number']
    result = []
    for n in PERSON_NAMES:
        s = stat[n]
        if s['count']>0:
            result.append({'name':n,'firstChapter':s['first'],'count':s['count']})
    result.sort(key=lambda x:(x['firstChapter'] or 999, -x['count']))
    return result

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    text = read_text()
    chapters = split_chapters(text)
    print(f'章回: {len(chapters)}, 总字数: {sum(len(c["content"]) for c in chapters)}')
    data = {str(c['number']):{'title':c['title'],'content':c['content']} for c in chapters}
    with open(os.path.join(OUT_DIR,'chapters_content.json'),'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    persons = extract_persons(chapters)
    with open(os.path.join(OUT_DIR,'persons_extracted.json'),'w',encoding='utf-8') as f:
        json.dump(persons, f, ensure_ascii=False, indent=2)
    print(f'人物: {len(persons)}')

if __name__=='__main__':
    main()
