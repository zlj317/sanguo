#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成完整的 persons.ts 文件，包含1085位人物。"""
import json, os

STATS_FILE = '/workspace/sanguo-system/src/mock/complete_person_stats.json'
OLD_PERSONS_FILE = '/workspace/sanguo-system/src/mock/persons.ts'
OUT_FILE = '/workspace/sanguo-system/src/mock/persons_new.ts'

def load_stats():
    with open(STATS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def read_old_file():
    with open(OLD_PERSONS_FILE, 'r', encoding='utf-8') as f:
        return f.read()

def extract_person_by_name(old_content, name):
    """从旧文件中提取指定名字的人物数据块。"""
    # 找到 name: 'xxx' 的位置
    import re
    pattern = re.compile(rf"name:\s*'{name}',", re.IGNORECASE)
    match = pattern.search(old_content)
    if not match:
        return None
    
    # 向前找到最近的 {
    start = match.start()
    while start > 0 and old_content[start] != '{':
        start -= 1
    
    # 向后找到匹配的 },
    depth = 0
    end = start
    for i in range(start, len(old_content)):
        if old_content[i] == '{':
            depth += 1
        elif old_content[i] == '}':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    
    return old_content[start:end]

def get_faction(name, aliases):
    """根据人物名字判断所属势力。"""
    shu = set([
        '刘备', '刘禅', '刘永', '刘理', '刘谌', '关羽', '关平', '关兴', '关索', '关彝',
        '张飞', '张苞', '张绍', '诸葛亮', '诸葛瞻', '诸葛尚', '诸葛均',
        '赵云', '赵统', '赵广', '马超', '马岱', '黄忠',
        '魏延', '庞统', '法正', '许靖', '麋竺', '麋芳', '孙乾', '简雍',
        '伊籍', '秦宓', '董和', '董允', '董厥', '刘巴', '廖立', '李严',
        '李丰', '向朗', '向宠', '张裔', '杨洪', '费诗', '王连', '杜微',
        '周群', '杜琼', '许慈', '孟光', '来敏', '尹默', '谯周', '郤正',
        '费祎', '蒋琬', '郭攸之', '陈震', '陈式', '陈到', '廖化', '宗预',
        '张翼', '张嶷', '王平', '马忠', '张南', '冯习', '傅肜', '程畿',
        '沙摩柯', '霍峻', '霍弋', '罗宪', '黄权', '黄崇', '李恢',
        '吕凯', '马良', '马谡', '王甫', '赵累', '周仓', '关定', '关宁',
        '刘封', '刘琦', '刘泌', '孟获', '祝融夫人', '孟优', '朵思大王',
        '木鹿大王', '兀突骨', '带来洞主', '金环三结', '董荼那', '阿会喃',
        '忙牙长', '雍闿', '高定', '朱褒', '鄂焕', '糜竺', '糜芳', '糜夫人',
        '甘夫人', '鲍三娘', '诸葛果', '杨仪', '蒋斌', '蒋显', '柳隐',
        '胡济', '阎宇', '张表', '陈祗', '黄皓', '诸葛乔',
    ])
    wei = set([
        '曹操', '曹丕', '曹植', '曹彰', '曹熊', '曹昂', '曹安民', '曹睿',
        '曹芳', '曹髦', '曹奂', '曹仁', '曹洪', '曹纯', '曹休', '曹真',
        '曹爽', '曹羲', '曹训', '曹彦', '夏侯渊', '夏侯惇', '夏侯霸',
        '夏侯威', '夏侯惠', '夏侯和', '夏侯尚', '夏侯玄', '夏侯茂',
        '司马懿', '司马师', '司马昭', '司马炎', '司马孚', '司马望',
        '张辽', '张郃', '徐晃', '于禁', '乐进', '李典', '典韦', '许褚',
        '庞德', '文聘', '臧霸', '吕虔', '满宠', '毛玠', '郭嘉', '荀彧',
        '荀攸', '贾诩', '程昱', '刘晔', '陈群', '陈琳', '王粲',
        '蔡邕', '蔡琰', '钟繇', '钟会', '华歆',
        '王朗', '王肃', '王基', '王经', '邓艾', '邓忠', '钟毓', '陈泰',
        '郭淮', '孙礼', '郝昭', '王双', '郭奕', '荀顗', '羊祜', '杜预',
        '王濬', '王浑', '王戎', '张华', '贾充', '裴秀', '何曾', '山涛',
        '向秀', '刘伶', '阮籍', '阮咸', '傅玄', '荀勖', '石苞', '陈骞',
        '卫瓘', '卫觊', '曹节', '曹腾', '曹嵩', '曹德', '曹豹', '曹性',
        '曹永', '曹遵', '曹宇', '曹据', '曹霖', '曹文叔',
        '卞氏', '甄氏', '郭皇后', '毛氏', '张皇后', '何太后', '董太后',
        '伏皇后', '董贵妃', '曹贵妃', '韩福', '孟坦', '孔秀',
        '卞喜', '王植', '秦琪', '蔡阳', '车胄', '刘岱', '王忠',
        '朱灵', '路昭', '史涣', '韩浩', '史迹', '夏侯兰', '夏侯恩',
        '夏侯杰', '夏侯德', '夏侯存', '夏侯咸', '侯成',
        '宋宪', '魏续', '高顺', '陈宫', '李儒', '李肃', '华雄',
        '胡车儿', '胡赤儿', '牛辅', '徐荣', '李傕', '郭汜', '张济',
        '樊稠', '杨奉', '韩暹', '李乐', '李封', '李蒙', '王方',
        '淳于琼', '淳于导', '淳于丹', '高览', '高干', '颜良', '文丑',
        '田丰', '沮授', '审配', '郭图', '许攸', '逢纪', '辛评', '辛毗',
        '辛宪英', '沮鹄', '高柔', '郭常', '郭奕',
        '郭恩', '郭永', '王美人', '何进', '何顒', '何苗',
        '何晏', '何曾', '何氏', '何植', '王允', '王匡', '王颀',
        '王昌', '王邑', '王立', '王则', '王垕', '王楷', '王子服',
        '王修', '王琰', '王威', '王累', '王必', '王谋', '王伉',
        '王连', '王建', '王观', '王夫人', '王昶', '王韬', '王敦',
        '王真', '王含', '王沈', '王业', '王瓘', '王买', '王祥',
        '王氏', '汪昭', '吴匡', '吴景', '吴敦', '吴子兰', '吴硕',
        '吴臣', '吴懿', '吴兰', '吴班', '吴质', '吴氏', '吴押狱',
        '吴妻', '吴纲', '伍琼', '伍孚', '伍习', '伍延',
        '吾彦', '吾粲', '卫弘', '卫凯', '卫仲道', '卫演',
        '文钦', '文淑', '文虎', '魏邈', '魏平', '韦康', '韦晃',
        '万政', '万彧', '武安国', '毋丘俭', '毋丘甸', '乐就', '乐綝',
        '司马朗', '司马防', '司马隽', '司马攸', '司马伷',
        '曹据', '曹霖', '曹髦', '曹奂', '曹芳', '曹睿',
        '徐晃', '张郃', '张辽', '于禁', '乐进', '李典',
    ])
    wu = set([
        '孙坚', '孙策', '孙权', '孙翊', '孙匡', '孙朗', '孙仁', '孙韶',
        '孙静', '孙端', '孙观', '孙高', '孙瑜', '孙皎', '孙桓',
        '孙河', '孙礼', '孙资', '孙登', '孙谦', '孙和', '孙亮', '孙峻',
        '孙恭', '孙綝', '孙据', '孙恩', '孙干', '孙闿', '孙楷', '孙休',
        '孙皓', '孙异', '孙冀', '孙歆', '孙秀', '周瑜', '鲁肃', '吕蒙',
        '陆逊', '张昭', '张纮', '顾雍', '步骘', '阚泽', '严畯', '程秉',
        '薛综', '薛悌', '薛则', '薛乔', '薛珝', '薛莹', '诸葛瑾',
        '诸葛恪', '诸葛靓', '太史慈', '太史亨', '甘宁', '凌统',
        '凌操', '周泰', '蒋钦', '陈武', '潘璋', '董袭',
        '黄盖', '韩当', '丁奉', '徐盛', '马忠',
        '全琮', '全端', '全怿', '全祎', '全纪', '全尚', '全后',
        '朱然', '朱桓', '朱治', '朱光', '朱褒', '朱赞',
        '朱恩', '朱芳', '朱异', '朱太后', '周鲂', '周旨', '周循',
        '周胤', '周善', '周群', '周平', '周舫', '陆抗', '陆凯',
        '陆景', '陆康', '陆绩', '陆纡', '陆骏', '骆统',
        '吕范', '吕岱', '吕据', '吕凯', '吕霸', '吕建', '吕常',
        '吕义', '吕通', '吕威璜', '吕旷', '吕翔', '留赞', '留略',
        '留平', '滕胤', '滕循', '濮阳兴', '左咸', '陶濬', '沈莹',
        '张悌', '张尚', '张象', '张布', '张约', '张特', '张当',
        '张弥', '张茂', '张承', '张休', '张普', '张韬', '张达',
        '大乔', '小乔', '吴国太',
    ])
    
    if name in shu:
        return 1
    elif name in wei:
        return 2
    elif name in wu:
        return 3
    else:
        return 4

def get_role(name, faction_id):
    """判断人物角色。"""
    monarchs = set(['刘备', '刘禅', '曹操', '曹丕', '曹睿', '曹芳', '曹髦', '曹奂',
                    '孙权', '孙亮', '孙休', '孙皓', '孙策', '孙坚',
                    '董卓', '吕布', '袁绍', '袁术', '刘表', '刘璋', '张鲁',
                    '马腾', '韩遂', '公孙瓒', '陶谦', '孔融', '张角'])
    advisors = set(['诸葛亮', '庞统', '法正', '郭嘉', '荀彧', '荀攸', '贾诩',
                    '程昱', '刘晔', '司马懿', '鲁肃', '张昭', '张纮',
                    '顾雍', '步骘', '诸葛瑾', '姜维', '蒋琬', '费祎', '董允',
                    '田丰', '沮授', '审配', '郭图', '许攸', '陈宫', '李儒',
                    '谯周', '郤正', '向朗', '杨仪', '陈群', '钟繇', '华歆',
                    '王朗', '贾充', '羊祜', '杜预'])
    generals = set(['关羽', '张飞', '赵云', '马超', '黄忠', '魏延', '姜维',
                    '张辽', '张郃', '徐晃', '于禁', '乐进', '李典', '典韦',
                    '许褚', '庞德', '文聘', '夏侯惇', '夏侯渊', '曹仁',
                    '曹洪', '曹休', '曹真', '邓艾', '钟会', '郭淮', '孙礼',
                    '周瑜', '吕蒙', '陆逊', '甘宁', '太史慈', '凌统',
                    '周泰', '黄盖', '韩当', '程普', '丁奉', '徐盛', '潘璋',
                    '马岱', '关平', '关兴', '张苞', '张翼', '张嶷', '王平',
                    '马忠', '廖化', '宗预', '霍峻', '罗宪',
                    '吕布', '高顺', '颜良', '文丑', '高览',
                    '华雄', '徐荣', '李傕', '郭汜', '张济', '樊稠',
                    '公孙瓒', '严颜', '张任', '严白虎'])
    
    if name in monarchs:
        return '君主'
    elif name in advisors:
        return '谋士'
    elif name in generals:
        return '武将'
    else:
        return '其他'

def get_importance(appearance_count):
    """根据出场次数判断重要性。"""
    if appearance_count >= 500:
        return 10
    elif appearance_count >= 200:
        return 9
    elif appearance_count >= 100:
        return 8
    elif appearance_count >= 50:
        return 7
    elif appearance_count >= 20:
        return 6
    elif appearance_count >= 10:
        return 5
    elif appearance_count >= 5:
        return 4
    elif appearance_count >= 3:
        return 3
    elif appearance_count >= 2:
        return 2
    else:
        return 1

def get_category(appearance_count, has_detailed_info):
    """判断人物分类。"""
    if appearance_count >= 100 or has_detailed_info:
        return 'main'
    elif appearance_count >= 20:
        return 'supporting'
    elif appearance_count >= 3:
        return 'minor'
    else:
        return 'unnamed'

def generate_person_obj(name, count, first_chapter, related_chapters, aliases, old_block=None):
    """生成一个人物对象的TS代码。"""
    if old_block:
        # 从旧数据块中更新字段
        import re
        # 更新 appearanceCount
        old_block = re.sub(r'appearanceCount:\s*\d+', f'appearanceCount: {count}', old_block)
        # 更新 firstAppearanceChapter
        old_block = re.sub(r'firstAppearanceChapter:\s*\d+', f'firstAppearanceChapter: {first_chapter}', old_block)
        # 更新 relatedChapters
        chs_str = ', '.join([str(c) for c in related_chapters])
        old_block = re.sub(r'relatedChapters:\s*\[[^\]]*\]', f'relatedChapters: [{chs_str}]', old_block)
        # 确保有逗号
        if not old_block.strip().endswith(','):
            old_block = old_block.rstrip() + ','
        return old_block
    
    # 生成新对象
    faction_id = get_faction(name, aliases)
    role = get_role(name, faction_id)
    importance = get_importance(count)
    category = get_category(count, False)
    
    # 提取字
    courtesy_name = ''
    for alias in aliases[1:]:
        if len(alias) == 2 and alias != name:
            courtesy_name = alias
            break
    
    has_name = len(name) >= 2
    
    bio = f'{name}，《三国演义》人物，共出场{count}次，首出场于第{first_chapter}回。'
    
    lines = []
    lines.append(f'  {{')
    lines.append(f'    id: 0,')  # 后面重新分配
    lines.append(f"    name: '{name}',")
    lines.append(f"    courtesyName: '{courtesy_name}',")
    lines.append(f"    titleName: '',")
    lines.append(f"    birthYear: '?',")
    lines.append(f"    deathYear: '?',")
    lines.append(f"    hometown: '',")
    lines.append(f"    appearance: '',")
    lines.append(f"    weapon: '',")
    lines.append(f"    mount: '',")
    lines.append(f'    factionId: {faction_id},')
    lines.append(f"    role: '{role}',")
    lines.append(f'    importance: {importance},')
    lines.append(f'    appearanceCount: {count},')
    lines.append(f"    biography: '{bio}',")
    lines.append(f'    personalityTags: [],')
    lines.append(f"    avatarUrl: '',")
    lines.append(f'    classicStories: [],')
    chs_str = ', '.join([str(c) for c in related_chapters])
    lines.append(f'    relatedChapters: [{chs_str}],')
    lines.append(f'    hasName: {str(has_name).lower()},')
    lines.append(f"    category: '{category}',")
    lines.append(f'    firstAppearanceChapter: {first_chapter},')
    lines.append(f'  }},')
    return '\n'.join(lines)

def main():
    stats = load_stats()
    old_content = read_old_file()
    
    print(f'新统计人物数: {len(stats)}')
    
    # 生成人物对象列表
    person_blocks = []
    has_old = 0
    new_count = 0
    
    for s in stats:
        name = s['name']
        old_block = extract_person_by_name(old_content, name)
        
        if old_block:
            has_old += 1
        else:
            new_count += 1
        
        block = generate_person_obj(
            name,
            s['count'],
            s['firstChapter'],
            s['relatedChapters'],
            s['aliases'],
            old_block
        )
        person_blocks.append(block)
    
    print(f'有详细信息: {has_old}')
    print(f'新增人物: {new_count}')
    
    # 现在需要重新分配ID。让我用一个更简单的方法：
    # 先生成完整的TS文件，然后重新编号。
    # 实际上，由于旧数据中已有ID，我们需要统一处理。
    
    # 让我换个方式：把所有人物数据解析成字典列表，重新分配ID，再写回
    
    # 读取所有人物数据到内存
    import re
    
    persons_data = []
    
    for s in stats:
        name = s['name']
        old_block = extract_person_by_name(old_content, name)
        
        if old_block:
            # 从旧块提取数据
            def field_val(block, field):
                m = re.search(rf'{field}:\s*(.+?)(?:,\n|\n  \}})', block, re.DOTALL)
                if m:
                    return m.group(1).strip()
                return None
            
            def str_field(block, field):
                m = re.search(rf"{field}:\s*'([^']*)'", block)
                if m:
                    return m.group(1)
                return ''
            
            def int_field(block, field):
                m = re.search(rf'{field}:\s*(\d+)', block)
                if m:
                    return int(m.group(1))
                return 0
            
            def bool_field(block, field):
                m = re.search(rf'{field}:\s*(true|false)', block)
                if m:
                    return m.group(1) == 'true'
                return True
            
            def arr_field(block, field):
                m = re.search(rf'{field}:\s*\[([^\]]*)\]', block)
                if m:
                    items = re.findall(r"'([^']*)'", m.group(1))
                    if items:
                        return items
                    # 数字数组
                    nums = re.findall(r'\d+', m.group(1))
                    return [int(n) for n in nums]
                return []
            
            p = {
                'name': str_field(old_block, 'name'),
                'courtesyName': str_field(old_block, 'courtesyName'),
                'titleName': str_field(old_block, 'titleName'),
                'birthYear': str_field(old_block, 'birthYear') or '?',
                'deathYear': str_field(old_block, 'deathYear') or '?',
                'hometown': str_field(old_block, 'hometown'),
                'appearance': str_field(old_block, 'appearance'),
                'weapon': str_field(old_block, 'weapon'),
                'mount': str_field(old_block, 'mount'),
                'factionId': int_field(old_block, 'factionId'),
                'role': str_field(old_block, 'role'),
                'importance': int_field(old_block, 'importance'),
                'appearanceCount': s['count'],  # 更新为新的统计值
                'biography': str_field(old_block, 'biography'),
                'personalityTags': arr_field(old_block, 'personalityTags'),
                'avatarUrl': str_field(old_block, 'avatarUrl'),
                'classicStories': arr_field(old_block, 'classicStories'),
                'relatedChapters': s['relatedChapters'],  # 更新
                'hasName': bool_field(old_block, 'hasName'),
                'category': str_field(old_block, 'category') or 'main',
                'firstAppearanceChapter': s['firstChapter'],  # 更新
            }
            persons_data.append(p)
        else:
            # 新增人物
            faction_id = get_faction(name, s['aliases'])
            role = get_role(name, faction_id)
            importance = get_importance(s['count'])
            category = get_category(s['count'], False)
            
            courtesy_name = ''
            for alias in s['aliases'][1:]:
                if len(alias) == 2 and alias != name:
                    courtesy_name = alias
                    break
            
            p = {
                'name': name,
                'courtesyName': courtesy_name,
                'titleName': '',
                'birthYear': '?',
                'deathYear': '?',
                'hometown': '',
                'appearance': '',
                'weapon': '',
                'mount': '',
                'factionId': faction_id,
                'role': role,
                'importance': importance,
                'appearanceCount': s['count'],
                'biography': f'{name}，《三国演义》人物，共出场{s["count"]}次，首出场于第{s["firstChapter"]}回。',
                'personalityTags': [],
                'avatarUrl': '',
                'classicStories': [],
                'relatedChapters': s['relatedChapters'],
                'hasName': len(name) >= 2,
                'category': category,
                'firstAppearanceChapter': s['firstChapter'],
            }
            persons_data.append(p)
    
    # 按出场次数排序
    persons_data.sort(key=lambda x: -x['appearanceCount'])
    
    # 重新分配ID
    for i, p in enumerate(persons_data):
        p['id'] = i + 1
    
    # 生成TS文件
    lines = []
    lines.append("import type { Person } from '@/types'")
    lines.append("")
    lines.append("export const persons: Person[] = [")
    
    for p in persons_data:
        lines.append(f'  {{')
        lines.append(f'    id: {p["id"]},')
        lines.append(f"    name: '{p['name']}',")
        lines.append(f"    courtesyName: '{p['courtesyName']}',")
        lines.append(f"    titleName: '{p['titleName']}',")
        lines.append(f"    birthYear: '{p['birthYear']}',")
        lines.append(f"    deathYear: '{p['deathYear']}',")
        lines.append(f"    hometown: '{p['hometown']}',")
        lines.append(f"    appearance: '{p['appearance']}',")
        lines.append(f"    weapon: '{p['weapon']}',")
        lines.append(f"    mount: '{p['mount']}',")
        lines.append(f'    factionId: {p["factionId"]},')
        lines.append(f"    role: '{p['role']}',")
        lines.append(f'    importance: {p["importance"]},')
        lines.append(f'    appearanceCount: {p["appearanceCount"]},')
        lines.append(f"    biography: '{p['biography']}',")
        
        # personalityTags
        tags = p['personalityTags']
        if isinstance(tags, list) and tags:
            tags_str = ', '.join([f"'{t}'" for t in tags])
            lines.append(f'    personalityTags: [{tags_str}],')
        else:
            lines.append(f'    personalityTags: [],')
        
        lines.append(f"    avatarUrl: '{p['avatarUrl']}',")
        
        # classicStories
        stories = p['classicStories']
        if isinstance(stories, list) and stories and all(isinstance(s, str) for s in stories):
            stories_str = ', '.join([f"'{s}'" for s in stories])
            lines.append(f'    classicStories: [{stories_str}],')
        else:
            lines.append(f'    classicStories: [],')
        
        # relatedChapters
        chs = p['relatedChapters']
        chs_str = ', '.join([str(c) for c in chs[:20]])
        lines.append(f'    relatedChapters: [{chs_str}],')
        lines.append(f'    hasName: {str(p["hasName"]).lower()},')
        lines.append(f"    category: '{p['category']}',")
        lines.append(f'    firstAppearanceChapter: {p["firstAppearanceChapter"]},')
        lines.append(f'  }},')
    
    lines.append(']')
    
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f'\n已生成新的persons.ts -> {OUT_FILE}')
    print(f'总人物数: {len(persons_data)}')
    
    # 分类统计
    cats = {}
    factions = {}
    for p in persons_data:
        cats[p['category']] = cats.get(p['category'], 0) + 1
        factions[p['factionId']] = factions.get(p['factionId'], 0) + 1
    
    print(f'\n分类统计:')
    for k, v in sorted(cats.items()):
        print(f'  {k}: {v}')
    
    print(f'\n势力统计:')
    faction_names = {1: '蜀汉', 2: '曹魏', 3: '东吴', 4: '群雄/其他'}
    for k, v in sorted(factions.items()):
        print(f'  {faction_names.get(k, k)}: {v}')
    
    print()
    print('前20名:')
    for i, p in enumerate(persons_data[:20]):
        fnames = {1: '蜀', 2: '魏', 3: '吴', 4: '群'}
        print(f'{i+1}. {p["name"]}: {p["appearanceCount"]}次 ({fnames.get(p["factionId"], "?")}{p["role"]}, 重要度{p["importance"]})')

if __name__ == '__main__':
    main()
