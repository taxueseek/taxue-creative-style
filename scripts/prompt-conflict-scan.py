#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""提示词矛盾机械扫描（机械层提醒器，非裁决器）。

语义层的矛盾定级由 optimize-pipeline.md 步骤 1.5 关卡负责；本脚本只做
可枚举的词表配对检测，输出「候选」命中供关卡复核。命中 ≠ 一定严重：
如「赛璐璐×剪纸」在葫芦娃语境是官方混合工艺，不算互斥，词表刻意不放。

机械规则（MECE）：
1. 媒介互斥：互斥媒介词对同时出现在非负向段
2. 色彩超载：非负向段色名计数 > 4
3. 主体-特征互斥：物种词与跨界特征词同时出现
4. 正负互斥：正向指定文字元素，负向无差别禁文字（负向含「除…外」限定不算）
5. 工艺互斥候选：工艺词对同时出现（仅候选，如「哑光×轻微高光」可能共存）
6. 专名堆砌候选：画师/导演/IP 专名 ≥2 并列（吸收自 Viko 逆向分析准入制）
7. 景别互斥：复合景别词（中近景全身）或互斥景别对（特写×全身）并列
8. 比例多处冲突：正文出现 ≥2 个不同画幅比例
9. 正负重叠候选：成像特征词同时出现在正向段与负向段（仅候选，程度限定词可豁免）

用法：
  python3 scripts/prompt-conflict-scan.py "提示词文本"
  python3 scripts/prompt-conflict-scan.py --case all        # 跑内置用例
  python3 scripts/prompt-conflict-scan.py --case c1,c2      # 跑指定用例
退出码：0 = 零命中；1 = 有候选命中（供 CI/回归用）
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = ROOT / "conflict-cases.json"

# ---- 词表（克制原则：只放物理逻辑真正互斥/明确跨界对，宁漏勿误报）----

MEDIA_EXCLUSIVE = [  # (词A, 词B)：物理逻辑相反的媒介
    ("水墨", "丙烯"),
    ("油画", "水彩"),
    ("照片", "插画"),
    ("写实照片", "手绘"),
    ("3d渲染", "手绘"),
    ("3d渲染", "水墨"),
    ("胶片", "矢量"),
]

COLOR_FAMILY = {  # 色名 → 色族（按色族去重计数，黑白灰底+一强调色=4 族内合格）
    "黑": "黑", "墨黑": "黑", "黑白": "黑", "墨": "黑",
    "白": "白", "米白": "白", "钛白": "白", "灰白": "白", "米色": "白",
    "灰": "灰",
    "红": "红", "赤": "红", "朱砂": "红", "朱砂赤": "红", "朱砂红": "红",
    "朱红": "红", "洋红": "红", "胭脂": "红", "朱磦": "红", "赭石": "红",
    "桃色": "红", "樱粉": "红", "藕粉": "红", "绛红": "红",
    "绿": "绿", "青翠": "绿", "藤蔓绿": "绿",
    "蓝": "蓝", "湖蓝": "蓝",
    "青": "青", "石青": "青",
    "黄": "黄", "橙": "橙", "紫": "紫", "金": "金", "银": "银",
}

COLOR_EXCLUDE = ["灰阶", "飞白", "墨色", "水墨", "赤足",  # 技法词/身体状态词，不是色名
                 "留白", "青烟",  # 构图术语/意象词，含色字但非色名（B10）
                 "红利", "金石", "银杏", "红尘",  # 含色字的领域词：金融概念/质感词/树种/佛家词，不是色名
                 "黄昏", "紫禁城",  # 时间词/专有名词，含色字但非色名
                 "旁白"]  # 叙事词（旁白式语气为组装模板高频词），不是色名

POSITION_WORDS = ["左上角", "右上角", "左下角", "右下角", "角落", "四角", "圆角", "一角", "边角", "视角"]  # 位置/观察词，不是特征
NOISE_WORDS = ["角色", "角度", "刀马旦"]  # 含特征字但语义无关（刀马旦=京剧行当）

SPECIES_FEATURE = [  # (物种词, 跨界特征词)：物种自带特征的误配
    ("马", "角"), ("马", "鹿角"), ("牛", "翅膀"), ("鱼", "腿"), ("鱼", "羽毛"),
    ("鸟", "鳞"), ("猫", "角"), ("人", "四条腿"), ("蛇", "腿"),
]

PROCESS_PAIRS = [  # 工艺词对：仅候选，定级交关卡
    ("粗黑描边", "细线勾勒"), ("粗黑描边", "单线勾勒"), ("哑光", "强烈高光"),
    ("平面", "体积光"), ("平面", "立体渲染"),
]

PROPER_NOUNS = [  # 专名词表（保守，宁漏勿误报；命中 ≥2 才报候选）
    "宫崎骏", "新海诚", "细田守", "久石让", "穆夏", "莫奈", "梵高", "达利",
    "埃舍尔", "克里姆特", "吴冠中", "齐白石", "张大千", "韦斯安德森", "韦斯·安德森",
    "王家卫", "诺兰", "是枝裕和", "吉卜力",
]

SHOT_COMPOUND = ["中近景全身", "半身全身", "近景全身", "特写全身", "中景全身"]  # 复合景别词，直接报
SHOT_EXCLUSIVE = [  # 互斥景别对（子串匹配，复合词先剥离再查）
    ("特写", "全身"), ("特写", "远景"), ("特写", "全景"),
    ("近景", "全身"), ("近景", "远景"), ("半身", "全身"),
]

ASPECT_RATIOS = [  # 常见画幅比例白名单（防误捕 f 值/日期）
    "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9",
    "2:1", "1:2", "20:9", "21:9", "5:2", "1:3", "3:1",
]

FEATURE_OVERLAP = ["颗粒", "噪点", "暗角", "虚化", "飞白", "毛边", "纸感"]  # 正负重叠候选词

FEATURE_WORDS = ["角", "翅膀", "腿", "羽毛", "鳞"]
TEXT_POSITIVE = ["logo", "签名", "吊牌", "文字", "标题", "题字"]
TEXT_NEGATIVE_BARE = r"不出现任何文字|无任何文字|不要文字|无文字"
TEXT_NEGATIVE_EXCEPT = r"除[^。；]*?外不出现任何(?:其他)?文字|除指定[^。；]*?外"


NEG_TRIGGERS = ["不要", "避免", "拒绝", "禁止", "不添加", "不加", "勿", "无任何", "无", "不含",
               "严禁", "不出现", "没有", "禁"]


def split_negation(text):
    """把文本切成正向段与负向段：最早负向触发词之后的部分归负向。

    触发词不要求标点前置（B1 修复）：「画面中不出现」类主谓句式的触发词
    前是普通汉字，旧 lookbehind 导致切分失效、负向句落入正向段。
    中文触发词均为独立词，无子串误切风险；误切方向是漏报（更保守），
    符合「机械层是提醒器非裁决器」的定位。
    """
    cut = len(text)
    m = re.search("|".join(NEG_TRIGGERS), text)
    if m:
        cut = m.start()  # 取最早触发点，其后全部归负向
    return text[:cut], text[cut:]


def strip_inline_negation(pos_segment):
    """剥离开入式排除法短语（B2 修复）：「而非X / 而不是X / 并非X」。

    材质排除法是本库自教的句式（prompt-craft 五-2「不是X，不是Y，是Z」），
    「而非油画」中的油画是排除对象不是媒介声明，不剥离会误报媒介互斥。
    剥离上限 10 字，防长句误伤。
    """
    return re.sub(r'(?:而非|而不是|并非)[^\s，。；、：）]{1,10}', "", pos_segment)


def scan(text: str) -> list:
    hits = []
    pos, neg = split_negation(text)
    pos = strip_inline_negation(pos)  # B2: 排除法短语先剥离

    # 1. 媒介互斥（只看正向段；照片→艺术转换源豁免 B7）
    t = pos.lower()
    is_transform = bool(re.search(r"(把|将).{0,12}照片.{0,8}(转|重绘|演绎)|照片(转|重绘|复活)", text))
    for a, b in MEDIA_EXCLUSIVE:
        if a in t and b in t:
            if is_transform and "照片" in (a, b):
                continue  # 照片是转换输入源不是媒介声明（R1 类：把照片重绘成插画）
            hits.append({"rule": "媒介互斥", "pair": f"{a}×{b}",
                         "severity": "严重候选", "detail": "两个物理逻辑相反的媒介并存"})

    # 2. 色彩超载（只看正向段，按色族去重 >4 才报；先剔除技法词与噪声词）
    # B10: 方括号占位符是待填变量（如[光色：暖金/冷白/微蓝]），枚举的是候选不是声明，剥离后再计数
    p2 = re.sub(r"\[[^\]]*\]", "", pos)
    for w in COLOR_EXCLUDE + POSITION_WORDS + NOISE_WORDS:
        p2 = p2.replace(w, "")
    families = set()
    for name, fam in COLOR_FAMILY.items():
        if name in p2:
            families.add(fam)
    if len(families) > 4:
        hits.append({"rule": "色彩超载", "detail": "色族 " + ",".join(sorted(families)) + f" 共 {len(families)} 个 > 4",
                     "severity": "严重候选"})

    # 3. 主体-特征互斥（先剔除位置词与噪声词，如「左上角」「角色」的角）
    p3 = pos
    for w in POSITION_WORDS + NOISE_WORDS:
        p3 = p3.replace(w, "")
    for sp, ft in SPECIES_FEATURE:
        if sp in p3 and ft in p3:
            hits.append({"rule": "主体矛盾", "pair": f"{sp}×{ft}",
                         "severity": "严重候选", "detail": "物种自带特征误配"})

    # 4. 正负互斥：正向要文字，负向无差别禁文字
    pos_for_text = re.sub(r"(?:代替|替代|无需|不靠|不依赖)[^\s，。；]{0,4}文字", "", pos)
    wants_text = any(w in pos_for_text for w in TEXT_POSITIVE)
    if wants_text and re.search(TEXT_NEGATIVE_BARE, text) and not re.search(TEXT_NEGATIVE_EXCEPT, text):
        hits.append({"rule": "正负互斥", "severity": "严重候选",
                     "detail": "正向指定文字元素但负向无差别禁文字（负向未带「除…外」限定）"})

    # 5. 工艺互斥候选
    for a, b in PROCESS_PAIRS:
        if a in text and b in text:
            hits.append({"rule": "工艺互斥", "pair": f"{a}×{b}",
                         "severity": "候选（交关卡定级）", "detail": "技法描述互相否定或共存，需人工判断"})

    # 6. 专名堆砌候选（≥2 个不同专名并列）
    found_names = sorted({n for n in PROPER_NOUNS if n in text})
    if len(found_names) >= 2:
        hits.append({"rule": "专名堆砌", "pair": "×".join(found_names),
                     "severity": "候选（交关卡定级）",
                     "detail": f"{len(found_names)} 个专名并列，模型平均化想象互相拉扯，保留证据最强一个，其余换可观察特征"})

    # 7. 景别互斥（复合词直接报；互斥对在剥离复合词后查）
    p7 = pos
    for w in SHOT_COMPOUND:
        if w in p7:
            hits.append({"rule": "景别互斥", "pair": w,
                         "severity": "严重候选", "detail": "复合景别词自相矛盾，同一主体不能同时占两个景别"})
            p7 = p7.replace(w, "")
    for a, b in SHOT_EXCLUSIVE:
        if a in p7 and b in p7:
            hits.append({"rule": "景别互斥", "pair": f"{a}×{b}",
                         "severity": "严重候选", "detail": "互斥景别并列，取景范围自相矛盾"})

    # 8. 比例多处冲突（白名单比例出现 ≥2 个不同值；数字边界防「13:4」误捕「3:4」）
    ratios = sorted({r for r in ASPECT_RATIOS
                     if re.search(rf"(?<!\d){re.escape(r)}(?!\d)", text)})
    if len(ratios) >= 2:
        hits.append({"rule": "比例多处冲突", "pair": "×".join(ratios),
                     "severity": "严重候选", "detail": "正文出现多个画幅比例，比例必须唯一且与建议比例一致"})

    # 9. 正负重叠候选（同一成像特征词正向负向都出现；程度限定词豁免）
    softeners = ("过重", "过度", "轻微", "太多", "过量")
    for w in FEATURE_OVERLAP:
        if w in pos and w in neg:
            seg = neg
            idx = seg.find(w)
            context = seg[max(0, idx - 6):idx + len(w) + 6]
            if any(s in context for s in softeners):
                continue  # 「避免颗粒过重」是程度限定，合法
            hits.append({"rule": "正负重叠", "pair": w,
                         "severity": "候选（交关卡定级）",
                         "detail": f"特征词「{w}」正向声明负向禁止，自相矛盾候选（程度限定除外）"})

    return hits


def run_case(cid):
    data = json.loads(CASES.read_text(encoding="utf-8"))
    case = next((c for c in data["cases"] if c["id"] == cid), None)
    if case is None:
        print(f"[ERROR] {cid} 不存在，可用：{[c['id'] for c in data['cases']]}")
        return False
    hits = scan(case["prompt"])
    expect = case.get("expect", [])
    if not expect:
        ok = not hits  # 干净用例：任何命中都算 FAIL（B8：旧逻辑 superset 恒真，形同虚设）
    else:
        # 期望非空：命中规则集必须精确等于期望集（B9：superset 会让多余误报静默通过）
        ok = {h["rule"] for h in hits} == set(expect)
    print(f"[{'PASS' if ok else 'FAIL'}] {cid} {case['name']}  期望命中:{expect} 实际:{[h['rule'] for h in hits]}")
    for h in hits:
        print(f"      → {h['severity']}: {h['rule']} {h.get('pair','')} {h.get('detail','')}")
    return ok


def main():
    args = sys.argv[1:]
    if args and args[0] == "--case":
        if not CASES.exists():
            print(f"[ERROR] 用例文件缺失：{CASES}")
            sys.exit(2)
        ids = args[1].split(",") if len(args) > 1 else ["all"]
        data = json.loads(CASES.read_text(encoding="utf-8"))
        ids = [c["id"] for c in data["cases"]] if ids == ["all"] else ids
        results = [run_case(i) for i in ids]
        print(f"\n回归结果: {sum(results)}/{len(results)} 通过")
        sys.exit(0 if all(results) else 1)

    if not args:
        print(__doc__.strip().split("用法：")[1].strip() if "用法：" in (__doc__ or "") else
              '用法：python3 scripts/prompt-conflict-scan.py "提示词文本" | --case all')
        sys.exit(2)

    text = " ".join(args)
    hits = scan(text)
    if not hits:
        print("零命中：未发现机械层矛盾候选")
        sys.exit(0)
    for h in hits:
        print(f"{h['severity']}: {h['rule']} {h.get('pair','')} {h.get('detail','')}")
    sys.exit(1)


if __name__ == "__main__":
    main()
