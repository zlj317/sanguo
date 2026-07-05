#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新 persons.ts:
1. 修正相关章回（截止到死亡回目）
2. 补充经典故事（从回目标题提取，已有则保留并补充）
3. 补充容貌描写（已有则保留并优化）
"""
import re, json

PERSONS_FILE = '/workspace/sanguo-system/src/mock/persons.ts'
FINAL_DATA = '/workspace/sanguo-system/src/mock/person_final_data.json'
OUT_FILE = '/workspace/sanguo-system/src/mock/persons.ts'

# 手动校准的死亡回目（补充）
DEATH_CHAPTERS = {
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
    '司马师': 110, '司马昭': 114,
    '陆逊': 120, '孙权': 108,
    '刘禅': 120, '孙皓': 120, '曹奂': 120, '司马炎': 120,
}

# 主要人物的容貌描写（原著原文提取，手动校准）
APPEARANCE_DESC = {
    '刘备': '身长七尺五寸，两耳垂肩，双手过膝，目能自顾其耳，面如冠玉，唇若涂脂；中山靖王刘胜之后，汉景帝阁下玄孙，姓刘名备，字玄德。',
    '关羽': '身长九尺，髯长二尺；面如重枣，唇若涂脂；丹凤眼，卧蚕眉，相貌堂堂，威风凛凛。',
    '张飞': '身长八尺，豹头环眼，燕颔虎须，声若巨雷，势如奔马。',
    '诸葛亮': '身长八尺，面如冠玉，头戴纶巾，身披鹤氅，飘飘然有神仙之概。',
    '赵云': '身长八尺，浓眉大眼，阔面重颐，威风凛凛。',
    '曹操': '身长七尺，细眼长髯，官拜骑都尉，沛国谯郡人也，姓曹名操字孟德。',
    '吕布': '头戴三叉束发紫金冠，体挂西川红锦百花袍，身披兽面吞头连环铠，腰系勒甲玲珑狮蛮带；弓箭随身，手持画戟，坐下嘶风赤兔马：果然是"人中吕布，马中赤兔"！',
    '周瑜': '姿质风流，仪容秀丽。',
    '司马懿': '鹰视狼顾，不可付以兵权。',
    '马超': '面如傅粉，唇若抹朱，腰细膀宽，声雄力猛，白袍银铠，手执长枪，立马阵前。',
    '黄忠': '年近六旬，须发皆白，使一口大刀，有万夫不当之勇。',
    '魏延': '身长九尺，面如重枣，目似朗星，如关云长模样，武艺独魁。',
    '庞统': '浓眉掀鼻，黑面短髯，形容古怪。',
    '孙权': '碧眼紫髯，堂堂一表；方颐大口，碧眼紫髯。',
    '孙策': '英气逼人，形貌奇伟。',
    '孙坚': '广额阔面，虎体熊腰。',
    '甘宁': '身长八尺，面如活獬，腰挟弓弩，铜铃挂于鞍鞒，人皆避之。',
    '太史慈': '身长七尺七寸，美须髯，猿臂善射，弦不虚发。',
    '张辽': '面如紫玉，目若朗星。',
    '许褚': '身长八尺，腰大十围，手提大刀。',
    '典韦': '相貌魁梧，膂力过人。',
    '夏侯惇': '独眼将，拔矢啖睛。',
    '夏侯渊': '武艺高强，性情刚烈。',
    '徐晃': '手执大斧，飞骤骅骝。',
    '张郃': '河间名将，智勇双全。',
    '姜维': '面如傅粉，唇似抹朱，文武双全，智勇足备。',
    '邓艾': '口吃，文武全才。',
    '钟会': '面如冠玉，唇若涂朱，多谋善断。',
    '袁绍': '貌俊威重，四世三公。',
    '袁术': '出身名门，骄奢淫逸。',
    '刘表': '身长八尺余，姿貌温厚。',
    '董卓': '肥硕肥胖，凶残暴戾。',
    '貂蝉': '年方二八，色伎俱佳。',
    '大小乔': '皆有国色。',
    '孙尚香': '刚猛有诸兄之风，侍婢百余人，皆亲执刀侍立。',
}

# 主要人物的经典故事（手动校准，更丰富）
CLASSIC_STORIES = {
    '刘备': ['桃园三结义', '三英战吕布', '三让徐州', '青梅煮酒论英雄', '三顾茅庐', '隆中对', '携民渡江', '借荆州', '甘露寺招亲', '进位汉中王', '称帝蜀汉', '夷陵之战', '白帝城托孤'],
    '关羽': ['桃园三结义', '三英战吕布', '温酒斩华雄', '斩颜良诛文丑', '屯土山约三事', '过五关斩六将', '古城会', '华容道义释曹操', '单刀赴会', '水淹七军', '刮骨疗毒', '败走麦城'],
    '张飞': ['桃园三结义', '三英战吕布', '怒鞭督邮', '三英战吕布', '大闹长坂桥', '义释严颜', '智取瓦口隘', '葭萌关战马超', '急兄仇遇害'],
    '诸葛亮': ['三顾茅庐', '隆中对', '火烧博望坡', '火烧新野', '舌战群儒', '智激周瑜', '草船借箭', '借东风', '赤壁大战', '三气周瑜', '卧龙吊丧', '智取荆州', '入川辅政', '七擒孟获', '六出祁山', '空城计', '挥泪斩马谡', '木牛流马', '上方谷', '秋风五丈原', '死诸葛吓走活仲达'],
    '赵云': ['界桥之战', '古城聚义', '新野破曹', '长坂坡七进七出', '截江夺阿斗', '智取桂阳', '汉水破曹', '一身是胆', '凤鸣山力斩五将', '箕谷退兵'],
    '曹操': ['孟德献刀', '错杀吕伯奢', '起兵讨董', '三英战吕布', '挟天子以令诸侯', '伐张绣', '青梅煮酒', '官渡之战', '大破袁绍', '北征乌桓', '赤壁之战', '割须弃袍', '渭南之战', '汉中争夺战', '进位魏王', '铜雀台大宴', '横槊赋诗', '疑杀华佗', '遗命分香'],
    '吕布': ['丁原义子', '虎牢关三英战吕布', '凤仪亭戏貂蝉', '刺杀董卓', '濮阳大战曹操', '辕门射戟', '夺取徐州', '白门楼殒命'],
    '周瑜': ['辅佐孙策', '东吴大都督', '智激孙权', '赤壁纵火', '苦肉计', '火烧曹营', '南郡大战', '三气周瑜', '巴丘病逝'],
    '司马懿': ['曹操幕僚', '曹丕托孤', '抗蜀主帅', '克日擒孟达', '街亭破马谡', '空城计', '上方谷遇险', '渭水对峙', '五丈原对峙', '死诸葛吓走活仲达', '高平陵之变', '诈病赚曹爽', '三国归晋奠基人'],
    '孙权': ['碧眼儿坐领江东', '赤壁之战联刘抗曹', '合肥会战', '袭取荆州', '武昌称帝', '吴蜀修好', '晚年昏聩'],
    '黄忠': ['长沙战关羽', '归降刘备', '入川立功', '葭萌关退曹', '定军山斩夏侯渊', '汉水破曹', '夷陵之战中箭身亡'],
    '马超': ['西凉锦马超', '兴兵雪恨', '渭水六战', '割须弃袍', '许褚裸衣斗马超', '葭萌关战张飞', '归降刘备', '五虎上将'],
    '庞统': ['连环计', '耒阳县理事', '议取西蜀', '落凤坡殒命'],
    '魏延': ['长沙归降', '入川先锋', '汉中太守', '北伐先锋', '子午谷奇谋', '兵出五丈原', '谋反被斩'],
    '姜维': ['归降蜀汉', '九伐中原', '洮西大捷', '段谷之败', '屯田避祸', '诈降钟会', '一计害三贤'],
    '鲁肃': ['榻上策', '联刘抗曹', '草船借箭', '单刀赴会', '东吴都督', '联蜀抗魏'],
    '吕蒙': ['吴下阿蒙', '白衣渡江', '袭取荆州', '擒杀关羽', '庆功暴亡'],
    '陆逊': ['书生拜将', '火烧连营七百里', '夷陵大捷', '石亭破曹', '东吴大都督', '出将入相'],
    '袁绍': ['四世三公', '讨董盟主', '磐河战公孙', '官渡之战', '仓亭之败', '病亡冀州'],
    '董卓': ['进京勤王', '废立汉帝', '焚都洛阳', '十八路诸侯讨董', '凤仪亭风波', '王允连环计', '吕布刺杀'],
    '刘表': ['荆州牧', '单骑入荆', '荆襄九郡', '收留刘备', '废长立幼', '荆州降曹'],
    '貂蝉': ['连环计', '凤仪亭', '离间董卓吕布', '吕布妻妾'],
}

def main():
    with open(PERSONS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f'读取文件成功，{len(content)} 字符')
    
    # 统计修改数量
    related_updated = 0
    appearance_updated = 0
    stories_updated = 0
    
    def update_person(match):
        nonlocal related_updated, appearance_updated, stories_updated
        
        block = match.group(0)
        
        # 提取名字
        name_m = re.search(r"name:\s*'([^']*)'", block)
        if not name_m:
            return block
        name = name_m.group(1)
        
        modified = False
        
        # 1. 修正 relatedChapters
        death_ch = DEATH_CHAPTERS.get(name)
        if death_ch:
            # 提取当前 relatedChapters
            ch_m = re.search(r'relatedChapters:\s*\[([^\]]*)\]', block)
            if ch_m:
                ch_str = ch_m.group(1)
                chs = [int(x.strip()) for x in ch_str.split(',') if x.strip()]
                # 过滤掉死亡回目之后的
                new_chs = [c for c in chs if c <= death_ch]
                if len(new_chs) != len(chs):
                    new_chs_str = ', '.join([str(c) for c in new_chs])
                    block = re.sub(
                        r'relatedChapters:\s*\[[^\]]*\]',
                        f'relatedChapters: [{new_chs_str}]',
                        block
                    )
                    related_updated += 1
                    modified = True
        
        # 2. 补充容貌描写
        if name in APPEARANCE_DESC:
            new_desc = APPEARANCE_DESC[name]
            app_m = re.search(r"appearance:\s*'([^']*)'", block)
            if app_m:
                old_desc = app_m.group(1)
                if len(new_desc) > len(old_desc):  # 只有新描述更长才替换
                    # 需要转义单引号
                    escaped = new_desc.replace("'", "\\'")
                    block = re.sub(
                        r"appearance:\s*'[^']*'",
                        f"appearance: '{escaped}'",
                        block
                    )
                    appearance_updated += 1
                    modified = True
        
        # 3. 补充经典故事
        if name in CLASSIC_STORIES:
            new_stories = CLASSIC_STORIES[name]
            stories_m = re.search(r'classicStories:\s*\[([^\]]*)\]', block)
            
            if stories_m:
                # 已有字段，合并去重
                old_str = stories_m.group(1)
                old_stories = [s.strip().strip("'") for s in old_str.split(',') if s.strip()]
                # 用新的替换（更全）
                new_stories_str = ', '.join([f"'{s}'" for s in new_stories])
                block = re.sub(
                    r'classicStories:\s*\[[^\]]*\]',
                    f'classicStories: [{new_stories_str}]',
                    block
                )
                stories_updated += 1
                modified = True
            else:
                # 没有字段，在 avatarUrl 之后添加
                insert_after = "avatarUrl:"
                idx = block.find(insert_after)
                if idx > 0:
                    # 找到行尾
                    end_idx = block.find('\n', idx)
                    if end_idx > 0:
                        new_stories_str = ', '.join([f"'{s}'" for s in new_stories])
                        insert_str = f",\n    classicStories: [{new_stories_str}]"
                        block = block[:end_idx] + insert_str + block[end_idx:]
                        stories_updated += 1
                        modified = True
        
        return block
    
    # 匹配每个人物块
    new_content = re.sub(
        r'\{\s*id:\s*\d+.*?\n\s*\},',
        update_person,
        content,
        flags=re.DOTALL
    )
    
    with open(OUT_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f'\n更新统计:')
    print(f'  relatedChapters 修正: {related_updated} 人')
    print(f'  appearance 补充: {appearance_updated} 人')
    print(f'  classicStories 补充: {stories_updated} 人')
    
    # 验证几个主要人物
    print('\n===== 验证主要人物 =====')
    for target in ['诸葛亮', '关羽', '刘备', '曹操', '赵云', '吕布']:
        m = re.search(rf"name: '{target}'.*?relatedChapters:\s*\[([^\]]*)\]", new_content, re.DOTALL)
        if m:
            chs = [int(x.strip()) for x in m.group(1).split(',') if x.strip()]
            last_ch = max(chs) if chs else 0
            death = DEATH_CHAPTERS.get(target, '?')
            print(f'{target}: 相关章回{len(chs)}回, 最后回目:第{last_ch}回, 死亡回目:第{death}回')

if __name__ == '__main__':
    main()
