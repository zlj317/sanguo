#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从《三国演义》原文中提取尽可能多的人物名字。
方法：
1. 基于常见姓氏的模式匹配
2. 基于上下文模式（如"某曰"、"某大怒"、"姓某名某"等）
3. 基于官职/称谓前缀 + 名字的模式
"""
import re, json, os

TXT = '/workspace/三国演义.txt'
OUT = '/workspace/sanguo-system/src/mock/extracted_names.json'

# 常见中文姓氏（百家姓+三国常见姓氏）
SURNAMES = set("""
赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜
戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐
费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄
和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁
杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍
虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚
程嵇邢滑裴陆荣翁荀羊于惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓
牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙
叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴郁胥能苍双
闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍却璩桑桂濮牛寿通边扈燕冀郏浦尚农
温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘
匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空
曾毋沙乜养鞠须丰巢关蒯相查后荆红游竺权逯盖益桓公
万俟司马上官欧阳夏侯诸葛闻人东方赫连皇甫尉迟公羊澹台公冶宗政濮阳
淳于单于太叔申屠公孙仲孙轩辕令狐钟离宇文长孙慕容鲜于闾丘司徒司空
亓官司寇仉督子车颛孙端木巫马公西漆雕乐正壤驷公良拓跋夹谷宰父谷梁
晋楚闫法汝鄢涂钦段干百里东郭南门呼延归海羊舌微生岳帅缑亢况后有琴
梁丘左丘东门西门商牟佘佴伯赏南宫墨哈谯笪年爱阳佟第五言福
""".strip())

SURNAMES_LIST = sorted(SURNAMES, key=lambda x: -len(x))

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

def extract_by_surname(text):
    """基于姓氏+1~2个名字字的模式提取候选人名。"""
    candidates = set()
    
    # 姓氏 + 1~2个汉字（双字名或单字名）
    for surname in SURNAMES_LIST:
        if len(surname) == 1:
            # 单姓 + 双字名
            pattern = re.compile(rf'{re.escape(surname)}[\u4e00-\u9fa5]{{2}}')
            for m in pattern.finditer(text):
                candidates.add(m.group())
            # 单姓 + 单字名（需上下文验证，先收集）
            pattern2 = re.compile(rf'{re.escape(surname)}[\u4e00-\u9fa5]{{1}}')
            for m in pattern2.finditer(text):
                candidates.add(m.group())
        else:
            # 复姓 + 1~2个汉字
            pattern = re.compile(rf'{re.escape(surname)}[\u4e00-\u9fa5]{{1,2}}')
            for m in pattern.finditer(text):
                candidates.add(m.group())
    
    return candidates

def extract_by_context(text):
    """基于上下文模式提取人名。"""
    candidates = set()
    
    # 模式1: 曰/道/大怒/大惊 等动词前的人名
    patterns = [
        r'([\u4e00-\u9fa5]{2,4})(?:曰|道|大怒|大惊|大喜|大喝|问|答|曰|言|云)',
        r'(?:遣|使|命|令|差|遣)([\u4e00-\u9fa5]{2,4})(?:曰|往|去|来)',
        r'(?:斩|杀|擒|捉|取)([\u4e000-\u9fa5]{2,4})',
    ]
    for pat in patterns:
        for m in re.finditer(pat, text):
            name = m.group(1)
            if 2 <= len(name) <= 4:
                candidates.add(name)
    
    # 模式2: 姓某名某的介绍
    for m in re.finditer(r'姓(\w+)名(\w+)字(\w+)', text):
        full = m.group(1) + m.group(2)
        candidates.add(full)
    
    # 模式3: 某（人）引/某（人）曰 等
    for m in re.finditer(r'([\u4e00-\u9fa5]{2,3})引(?:兵|军|马|众)', text):
        candidates.add(m.group(1))
    
    return candidates

def filter_names(candidates, text):
    """过滤掉明显不是人名的候选。"""
    # 排除词表（常见的非人名词汇）
    exclude_words = set("""
今日 明日 昨日 今日 此时 彼时 是时 时 此 彼 其 之 而 也 矣 乎 哉 焉 耳
天下 国家 朝廷 官府 百姓 军士 兵马 粮草 城池 关隘 山寨 村庄 州县 府郡
左右 前后 上下 东西 南北 中间 内外 大小 多少 长短 高低 远近 深浅 轻重
先生 大人 老爷 小人 奴家 贫僧 贫道 在下 区区 不才 贤弟 仁兄 父老 乡亲
将军 丞相 太守 刺史 县令 校尉 都督 军师 大夫 尚书 侍郎 中郎 郎中 令史
主公 明公 恩相 恩公 贤侄 贤婿 令尊 令堂 令郎 令爱 贵府 贵庄 贵县 贵乡
贫道 贫僧 贫尼 小道 小僧 老衲 老叟 老丈 老儿 小子 后生 晚辈 晚生
不知 不敢 不可 不能 不得 不用 不要 不必 不妨 不须 岂非 岂不 岂敢
如何 奈何 若何 何如 何故 何为 何以 何所 何足 何足道
因此 是以 所以 于是 遂 乃 即 便 就 方 才 却 倒 反 转
忽然 突然 猛然 勃然 哗然 悚然 凛然 昂然 慨然 愤然 黯然
一二人 三五人 数十人 数百人 数千人 数万 数十万 几百万
三军 众将 诸将 军士 士卒 马步 水军 陆军 精兵 强兵 弱兵
洛阳 长安 许昌 建业 成都 荆州 徐州 兖州 冀州 幽州 并州 青州
司隶 豫州 凉州 益州 交州 扬州 广州 交州 汉中 南阳 汝南 颍川
陈留 东郡 济北 渤海 平原 北海 下邳 广陵 庐江 会稽 吴郡 丹阳
豫章 长沙 桂阳 零陵 武陵 江夏 南郡 襄阳 樊城 麦城 白帝城
虎牢关 汜水关 函谷关 潼关 剑阁 阳平关 葭萌关 绵竹 雒城 成都
赤壁 官渡 夷陵 猇亭 长坂坡 当阳 华容道 葫芦谷 上方谷 五丈原
祁山 街亭 陈仓 散关 斜谷 骆谷 子午谷 阴平 江油 涪城 绵竹
青龙 白虎 朱雀 玄武 麒麟 凤凰 鸾凤 鸳鸯 龙虎 熊罴 豺狼
天地 日月 星辰 风云 雨雪 雷电 山川 河流 湖海 草木 花鸟
龙凤 麟凤 龟鹤 貔貅 虎豹 鹰犬 牛马 羊猪 鸡犬 鱼雁
金银 铜铁 玉石 珠宝 绸缎 绫罗 锦缎 纱罗 绢帛
琴棋 书画 诗酒 歌舞 礼乐 射御 书数 孝悌 忠信 仁义 道德
春秋 战国 秦汉 三国 魏晋 南北朝 隋唐 五代 宋辽金元 明清
黄帝 炎帝 尧舜 禹汤 文武 周公 孔子 孟子 老子 庄子 墨子
孙子 吴子 荀子 韩非子 屈原 宋玉 司马相如 司马迁 班固
曹操 刘备 孙权 关羽 张飞 诸葛亮 赵云 马超 黄忠 魏延
司马懿 司马师 司马昭 司马炎 曹丕 曹叡 曹芳 曹髦 曹奂
孙坚 孙策 孙亮 孙休 孙皓 周瑜 鲁肃 吕蒙 陆逊 张昭
吕布 董卓 袁绍 袁术 刘表 刘璋 张鲁 马腾 韩遂 公孙瓒
陶谦 孔融 祢衡 杨修 华佗 左慈 于吉 管辂
大汉 皇叔 丞相 武侯 武圣 关帝 武侯 卧龙 凤雏 水镜
先锋 大将 上将 副将 偏将 牙将 裨将 参将 统领 统领
太守 刺史 州牧 县令 县官 县尉 县丞 主簿 功曹 别驾
长史 司马 参军 祭酒 从事 中郎 郎中 令史 记室 书吏
尚书 侍郎 侍中 御史 大夫 太常 光禄勋 卫尉 太仆 廷尉
大鸿胪 宗正 大司农 少府 执金吾 将作大匠 大长秋 太子太傅
中常侍 小黄门 黄门 宦官 太监 内侍 内监
太师 太傅 太保 太尉 司徒 司空 大将军 骠骑将军 车骑将军
卫将军 前后左右将军 征东 征西 征南 征北 镇东 镇西 镇南 镇北
安东 安西 安南 安北 平东 平西 平南 平北 翊军 军师 领军 护军
监军 督军校尉 骑都尉 奉车都尉 驸马都尉 光禄大夫 太中大夫
中散大夫 谏议大夫 议郎 中郎 郎中 侍郎 尚书郎 著作郎
秘书郎 校书郎 侍御史 监察御史 殿中侍御史 御史中丞
司隶校尉 城门校尉 屯骑校尉 越骑校尉 步兵校尉 长水校尉 射声校尉
中领军 中护军 武卫将军 奋武将军 扬武将军 建武将军 昭武将军
武威将军 广武将军 安远将军 镇远将军 平远将军 辅国将军 辅汉将军
镇军将军 抚军将军 征虏将军 讨虏将军 破虏将军 荡寇将军 讨逆将军
征南将军 镇南将军 安南将军 平南将军 征西将军 镇西将军 安西将军
平西将军 征北将军 镇北将军 安北将军 平北将军
前将军 后将军 左将军 右将军 偏将军 裨将军 牙门将军 偏将军
裨将军 中郎将 校尉 都尉 司马 参军 功曹 主簿 记室 书佐
从事 别驾 治中 长史 郎中 令史 掾属 佐吏 小吏 胥吏
士卒 兵士 军士 步卒 骑兵 弓手 弩手 刀手 枪手 盾手
水军 步军 马军 马步军 马步水兵 三军 众军 诸军 大军 小军
精兵 强兵 弱兵 老弱 疲兵 骄兵 惰归 哀兵 义兵 奇兵 正兵
伏兵 疑兵 援兵 救兵 援军 追兵 退军 撤军 班师 回军 还军
进军 进兵 出兵 起兵 举兵 兴兵 动兵 用兵 交兵 合兵 会战
决战 死战 力战 苦战 速战 持久战 游击战 运动战 阵地战
攻坚战 防御战 阻击战 遭遇战 伏击战 袭击战 夜袭 偷袭
劫寨 劫营 劫粮 劫道 打援 围点打援 声东击西 围魏救赵
空城计 苦肉计 连环计 反间计 离间计 美人计 走为上计
三十六计 孙子兵法 吴子兵法 六韬 三略 尉缭子 司马法
将苑 便宜十六策 军令 军法 军纪 军规 军制 军礼 军乐
军威 军容 军阵 军势 军情 军机 军务 军政 军饷 军粮
军械 军装 军马 军犬 军鸽 军旗 军鼓 军号 军乐 军礼
兵器 武器 甲胄 盔甲 铠甲 头盔 盾牌 刀枪 剑戟 斧钺
钩叉 鞭锏 锤抓 镗镰 槊棒 拐子 流星 弓弩 箭簇 火箭
火炮 火铳 投石机 云梯 冲车 楼车 巢车 轒辒 木牛流马
连弩 诸葛弩 元戎弩 霹雳车 发石车 撞车 钩车 火车
""".strip().split())
    
    filtered = set()
    for name in candidates:
        # 长度过滤
        if len(name) < 2 or len(name) > 4:
            continue
        # 排除纯虚词组合
        if all(c in '之乎者也矣焉哉耳而但其之于以若如则所为何不岂那这此彼' for c in name):
            continue
        # 排除常见词
        if name in exclude_words:
            continue
        # 排除数字相关
        if re.search(r'[一二三四五六七八九十百千万]', name) and name not in candidates:
            continue
        # 至少出现一定次数才认为可能是人名
        count = text.count(name)
        if count < 3:
            continue
        filtered.add((name, count))
    
    return filtered

def main():
    print('读取原文...')
    text = read_text()
    print(f'总字数: {len(text)}')
    
    print('分割章回...')
    chapters = split_chapters(text)
    print(f'章回数: {len(chapters)}')
    
    # 合并所有内容
    all_content = '\n'.join(c['content'] for c in chapters)
    
    print('基于姓氏提取候选...')
    candidates1 = extract_by_surname(all_content)
    print(f'  候选数: {len(candidates1)}')
    
    print('基于上下文提取候选...')
    candidates2 = extract_by_context(all_content)
    print(f'  候选数: {len(candidates2)}')
    
    all_candidates = candidates1 | candidates2
    print(f'总候选数: {len(all_candidates)}')
    
    print('过滤非人名...')
    filtered = filter_names(all_candidates, all_content)
    print(f'过滤后: {len(filtered)}')
    
    # 按出现次数排序
    sorted_names = sorted(filtered, key=lambda x: -x[1])
    
    # 保存结果
    result = [{'name': n, 'count': c} for n, c in sorted_names]
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f'\n已保存到 {OUT}')
    print(f'\n前100名:')
    for i, (name, count) in enumerate(sorted_names[:100]):
        print(f'{i+1}. {name}: {count}次')

if __name__ == '__main__':
    main()
