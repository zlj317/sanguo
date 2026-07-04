#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复头像URL映射，确保有头像的人物保持正确的头像。"""
import re

OLD_FILE = '/workspace/sanguo-system/src/mock/persons_backup.ts'
NEW_FILE = '/workspace/sanguo-system/src/mock/persons.ts'

def extract_name_avatar_map(file_path):
    """从文件中提取 name -> avatarUrl 映射。"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    result = {}
    
    # 找到每个人物块
    pattern = re.compile(r'\{\s*id:\s*\d+.*?\n\s*\},', re.DOTALL)
    
    for match in pattern.finditer(content):
        block = match.group(0)
        
        # 提取名字
        name_m = re.search(r"name:\s*'([^']*)'", block)
        avatar_m = re.search(r"avatarUrl:\s*'([^']*)'", block)
        
        if name_m and avatar_m and avatar_m.group(1):
            result[name_m.group(1)] = avatar_m.group(1)
    
    return result

def update_avatar_urls():
    # 从旧文件提取名字-头像映射
    old_map = extract_name_avatar_map(OLD_FILE)
    print(f'旧头像映射数: {len(old_map)}')
    
    # 读取新文件
    with open(NEW_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 找到每个人物块并更新头像
    updated = 0
    
    def replace_avatar(match):
        nonlocal updated
        block = match.group(0)
        
        name_m = re.search(r"name:\s*'([^']*)'", block)
        if name_m and name_m.group(1) in old_map:
            name = name_m.group(1)
            new_avatar = old_map[name]
            new_block = re.sub(
                r"avatarUrl:\s*'[^']*'",
                f"avatarUrl: '{new_avatar}'",
                block
            )
            updated += 1
            return new_block
        return block
    
    new_content = re.sub(
        r'\{\s*id:\s*\d+.*?\n\s*\},',
        replace_avatar,
        content,
        flags=re.DOTALL
    )
    
    # 写回文件
    with open(NEW_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'已更新 {updated} 个人物的头像URL')

if __name__ == '__main__':
    update_avatar_urls()
