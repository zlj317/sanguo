#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接更新 persons.ts 中所有人物的 relatedChapters 字段。"""
import json, re

STATS_FILE = '/workspace/sanguo-system/src/mock/complete_person_stats.json'
PERSONS_FILE = '/workspace/sanguo-system/src/mock/persons.ts'

def main():
    with open(STATS_FILE, 'r', encoding='utf-8') as f:
        stats = json.load(f)
    
    # 建立 name -> relatedChapters 映射
    name_to_chs = {}
    for s in stats:
        name_to_chs[s['name']] = s['relatedChapters']
    
    print(f'统计人物数: {len(name_to_chs)}')
    
    with open(PERSONS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated = 0
    
    def replace_related_chapters(match):
        nonlocal updated
        block = match.group(0)
        
        # 提取名字
        name_m = re.search(r"name:\s*'([^']*)'", block)
        if name_m and name_m.group(1) in name_to_chs:
            name = name_m.group(1)
            chs = name_to_chs[name]
            chs_str = ', '.join([str(c) for c in chs])
            new_block = re.sub(
                r'relatedChapters:\s*\[[^\]]*\]',
                f'relatedChapters: [{chs_str}]',
                block
            )
            updated += 1
            return new_block
        return block
    
    # 匹配每个人物块
    new_content = re.sub(
        r'\{\s*id:\s*\d+.*?\n\s*\},',
        replace_related_chapters,
        content,
        flags=re.DOTALL
    )
    
    with open(PERSONS_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'已更新 {updated} 个人物的 relatedChapters')
    
    # 验证关羽
    guan_yu_m = re.search(r"name: '关羽'.*?relatedChapters:\s*\[([^\]]*)\]", new_content, re.DOTALL)
    if guan_yu_m:
        print(f'\n关羽的 relatedChapters: [{guan_yu_m.group(1)}]')

if __name__ == '__main__':
    main()
