import re, json

with open('/workspace/sanguo-system/src/mock/persons.ts', 'r') as f:
    content = f.read()

with open('/workspace/sanguo-system/src/mock/person_stats.json', 'r', encoding='utf-8') as f:
    stats = json.load(f)

def update_person(match):
    block = match.group(0)
    pid_m = re.search(r'id:\s*(\d+)', block)
    if not pid_m:
        return block
    pid = pid_m.group(1)
    if pid not in stats:
        return block
    s = stats[pid]
    
    block = re.sub(
        r"appearanceCount:\s*\d+",
        f"appearanceCount: {s['count']}",
        block
    )
    block = re.sub(
        r"firstAppearanceChapter:\s*\d+",
        f"firstAppearanceChapter: {s['firstChapter']}",
        block
    )
    ch_list = str(s['relatedChapters'][:15])
    block = re.sub(
        r"relatedChapters:\s*\[[^\]]*\]",
        f"relatedChapters: {ch_list}",
        block
    )
    return block

pattern = re.compile(r'\{[^}]*id:\s*\d+[^}]*\}', re.DOTALL)
new_content = pattern.sub(update_person, content)

with open('/workspace/sanguo-system/src/mock/persons.ts', 'w') as f:
    f.write(new_content)

print('persons.ts 已更新出场次数、首出场章节、相关章回')

# 验证
with open('/workspace/sanguo-system/src/mock/persons.ts', 'r') as f:
    verify = f.read()

for name in ['曹操', '刘备', '关羽', '张飞', '诸葛亮']:
    m = re.search(r"name:\s*'" + name + r"'[^}]*appearanceCount:\s*(\d+)", verify, re.DOTALL)
    if m:
        print(f'  {name}: {m.group(1)}次')
