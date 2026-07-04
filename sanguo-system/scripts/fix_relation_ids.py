#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据新的persons.ts中的ID映射，更新relations.ts中的人物ID。"""
import re

PERSONS_FILE = '/workspace/sanguo-system/src/mock/persons.ts'
RELATIONS_FILE = '/workspace/sanguo-system/src/mock/relations.ts'
OUT_FILE = '/workspace/sanguo-system/src/mock/relations_new.ts'

def get_name_id_map():
    """从persons.ts中提取 name -> id 映射。"""
    with open(PERSONS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {}
    
    # 找到每个人物块
    pattern = re.compile(r'\{\s*id:\s*(\d+).*?\n\s*\},', re.DOTALL)
    
    for match in pattern.finditer(content):
        block = match.group(0)
        
        id_m = re.search(r'id:\s*(\d+)', block)
        name_m = re.search(r"name:\s*'([^']*)'", block)
        
        if id_m and name_m:
            result[name_m.group(1)] = int(id_m.group(1))
    
    return result

def update_relations():
    name_to_id = get_name_id_map()
    print(f'人物数量: {len(name_to_id)}')
    
    # 读取relations文件
    with open(RELATIONS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 旧ID -> 新ID 映射
    # 我们需要通过描述或其他方式来确定... 不对，让我换个思路
    # 让我从旧的persons.ts提取旧的name->id映射，然后建立 old_id -> new_id 映射
    
    OLD_PERSONS = '/workspace/sanguo-system/src/mock/persons_backup.ts'
    old_name_to_id = {}
    
    with open(OLD_PERSONS, 'r', encoding='utf-8') as f:
        old_content = f.read()
    
    pattern = re.compile(r'\{\s*id:\s*(\d+).*?\n\s*\},', re.DOTALL)
    for match in pattern.finditer(old_content):
        block = match.group(0)
        id_m = re.search(r'id:\s*(\d+)', block)
        name_m = re.search(r"name:\s*'([^']*)'", block)
        if id_m and name_m:
            old_name_to_id[name_m.group(1)] = int(id_m.group(1))
    
    print(f'旧人物数量: {len(old_name_to_id)}')
    
    # 建立 old_id -> new_id 映射（通过名字关联）
    old_id_to_new_id = {}
    for name, old_id in old_name_to_id.items():
        if name in name_to_id:
            old_id_to_new_id[old_id] = name_to_id[name]
    
    print(f'ID映射数量: {len(old_id_to_new_id)}')
    
    # 更新relations.ts中的person1Id和person2Id
    def replace_id(match):
        field = match.group(1)
        old_id = int(match.group(2))
        if old_id in old_id_to_new_id:
            return f'{field}: {old_id_to_new_id[old_id]}'
        return match.group(0)
    
    new_content = re.sub(
        r'(person1Id|person2Id):\s*(\d+)',
        replace_id,
        content
    )
    
    # 写回文件
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # 替换原文件
    import shutil
    shutil.copy(OUT_FILE, RELATIONS_FILE)
    
    print(f'已更新relations.ts中的ID映射')
    
    # 验证几个关键关系
    print('\n验证关羽相关关系:')
    guan_yu_id = name_to_id.get('关羽', 0)
    print(f'关羽新ID: {guan_yu_id}')
    
    # 查找包含关羽ID的关系
    rel_pattern = re.compile(r'\{\s*id:\s*\d+.*?\n\s*\},', re.DOTALL)
    guan_yu_rels = []
    for match in rel_pattern.finditer(new_content):
        block = match.group(0)
        if f'person1Id: {guan_yu_id}' in block or f'person2Id: {guan_yu_id}' in block:
            # 提取关系类型和描述
            type_m = re.search(r"relationType:\s*'([^']*)'", block)
            desc_m = re.search(r"description:\s*'([^']*)'", block)
            if type_m:
                guan_yu_rels.append(f'{type_m.group(1)}: {desc_m.group(1) if desc_m else ""}')
    
    for rel in guan_yu_rels:
        print(f'  - {rel}')

if __name__ == '__main__':
    update_relations()
