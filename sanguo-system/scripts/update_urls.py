#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""将persons.ts中avatarUrl: ''替换为/avatars/person_{id}.png"""
import re
P='/workspace/sanguo-system/src/mock/persons.ts'
with open(P,'r',encoding='utf-8') as f: c=f.read()
pat=re.compile(r"(\{\s*id:\s*(\d+),.*?avatarUrl:\s*)'[^']*'(,)",re.DOTALL)
n=0
def r(m):
    global n; n+=1
    return f"{m.group(1)}'/avatars/person_{m.group(2)}.png'{m.group(3)}"
with open(P,'w',encoding='utf-8') as f: f.write(pat.sub(r,c))
print(f'更新 {n} 个 avatarUrl')
