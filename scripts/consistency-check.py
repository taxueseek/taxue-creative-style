#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""taxue-creative-style 一致性检查（只读，不改文件）。

检查项：
1. SKILL.md §1 速查表 9 家族变体清单
2. 各家族文件「变体索引」表与速查表是否一致（含状态图标）
3. References 表声称的变体数与速查表是否一致
4. verification-ledger.md 台账行数是否等于速查表变体总数
5. 规范矛盾回归（canary：留白一刀切 / 色数双标准 / scenario 门控（11 个实验·测试
   变体不得进场景包表）/ 归档路径缺失 / 比例真源缺 5:2 / 交付完整性计数同步 /
   家族层 L2 参数数值 / 家族层 ≤5 色 / 文字纯净句病句）
6. 正文状态行同步（✅/⚠️/🔶 变体的正文小节须含同一状态图标）

用法：python3 scripts/consistency-check.py
退出码：0 = 全部一致；1 = 存在漂移（按 memory-protocol.md 三处同步修复）。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")

FAMILY_FILES = {
    "F1": "F1-ink-wash.md",
    "F2": "F2-blank-poster.md",
    "F3": "F3-city.md",
    "F4": "F4-healing.md",
    "F5": "F5-oriental.md",
    "F6": "F6-atmosphere.md",
    "F7": "F7-photography.md",
    "F8": "F8-concept-poster.md",
    "F9": "F9-photo-art.md",
}
STATUS = {"✅": "✅", "⚠️": "⚠️", "🔶": "🔶"}


def speed_table():
    """返回 {家族: [(变体, 状态文本), ...]}，按 SKILL §1 速查表解析。"""
    m = re.search(r"\| 家族 \| 适用主题 \| 变体 \| 默认比例 \| 文件 \|(.*?)\*\*编号纪律\*\*", SKILL, re.S)
    if m is None:
        raise SystemExit("FAIL: SKILL.md 速查表锚点失配（表格或「编号纪律」标题被改动），无法解析")
    rows = {}
    for line in m.group(1).splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not cells[0].startswith("F"):
            continue
        fam_full, vs = cells[0], cells[2]
        fam = fam_full.split()[0]
        if not fam.startswith("F"):
            continue
        out = []
        for token in vs.split("、"):
            token = token.strip()
            state = ""
            for s in ("✅", "⚠️", "🔶"):
                if token.endswith(s):
                    state, token = s, token[: -len(s)]
                    break
            out.append((token.strip(), state))
        rows[fam] = out
    return rows


def family_index_table(fam):
    path = ROOT / "references" / "style-library" / FAMILY_FILES[fam]
    text = path.read_text(encoding="utf-8")
    if "**变体索引**" not in text:
        raise SystemExit(f"FAIL: {path.name} 缺「**变体索引**」锚点，无法解析")
    idx = text.index("**变体索引**")
    out = []
    for line in text[idx:].splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] == "变体" or re.fullmatch(r"-+", cells[0]):
            continue
        token, state = cells[0], cells[-1]
        for s in STATUS:
            if token.endswith(s):
                state, token = s, token[: -len(s)]
                break
        state = "✅" if "✅" in state else ("⚠️" if "⚠️" in state else ("🔶" if "🔶" in state else ""))
        out.append((token.strip(), state))
    return out


def reference_names(text):
    """把 References 名单文本解析为变体代号列表：
    - 区间展开：R1-R5 → R1,R2,R3,R4,R5
    - 剥状态后缀：V8 已验证 → V8；F2-K（实验）→ F2-K
    """
    tokens = []
    for raw in re.split(r"[、，,/\s]+", text.strip()):
        raw = raw.strip()
        if not raw:
            continue
        m = re.fullmatch(r"([A-Z]+\d+)-([A-Z]+\d+)", raw)
        if m:
            a, b = m.group(1), m.group(2)
            pa, pb = re.fullmatch(r"([A-Z]+)(\d+)", a), re.fullmatch(r"([A-Z]+)(\d+)", b)
            if pa and pb and pa.group(1) == pb.group(1):
                for n in range(int(pa.group(2)), int(pb.group(2)) + 1):
                    tokens.append(f"{pa.group(1)}{n}")
                continue
        # 剥「（实验）/（已验证）/ 已验证」等状态后缀
        raw = re.sub(r"[（(][^）)]*[）)]$", "", raw).strip()
        raw = re.sub(r"\s*(已验证|默认|实验|测试中)$", "", raw).strip()
        if raw:
            tokens.append(raw)
    return tokens


def references_counts():
    """返回 {家族: (声明计数, [变体代号...])}，按 References 表解析。
    历史教训：只比计数会漏「计数对、名单漏」漂移（F5 曾 13 个变体、表里只写 11 个名字，
    计数却写 11 对得上，名单少于速查表）。"""
    out = {}
    for line in SKILL.splitlines():
        m = re.match(r"\| `references/style-library/(F\d)-[\w-]+\.md` \| (F\d)[^|]*?(\d+) 变体[（(](.*?)[）)]", line)
        if m:
            fam, count, names = m.group(2), int(m.group(3)), m.group(4)
            out[fam] = (count, reference_names(names))
    return out


def skill_summary_numbers():
    """叙述性数字断言（防「标题写 62 实际 61」类漂移）：
    1. SKILL §1 标题「N 个变体」= 速查表实际总数
    2. SKILL References 表中每个家族「N 变体（名单）」：计数 = 名单长度 = 速查表长度，名单 = 速查表清单（顺序忽略）
    3. SKILL References 表 gallery 行所称「N 张」= 实际 jpg 数
    4. verification-ledger 各家族标题「（N）」= 该族实际行数（F1 曾写 15 实际 14）"""
    errors = []
    speed = speed_table()
    total = sum(len(v) for v in speed.values())

    m = re.search(r"^## 1\. 风格库（9 家族，(\d+) 个变体）", SKILL, re.M)
    if not m:
        errors.append("SKILL §1 标题锚点失配（「风格库（9 家族，N 个变体）」被改动）")
    elif int(m.group(1)) != total:
        errors.append(f"SKILL §1 标题称 {int(m.group(1))} 个变体，速查表实际 {total}")

    refs = references_counts()
    for fam, vs in speed.items():
        flat = [v for v, _ in vs]
        if fam not in refs:
            errors.append(f"References 表缺少 F{fam[1:]} 行")
            continue
        count, tokens = refs[fam]
        if count != len(flat):
            errors.append(f"References 表 {fam} 声称计数 {count}，速查表实际 {len(flat)}")
        if len(tokens) != len(flat) or sorted(tokens) != sorted(flat):
            errors.append(f"References 表 {fam} 变体名单与速查表不一致: 表={tokens} vs 速查表={flat}")

    gt = re.search(r"`references/gallery/` \| [^|]*?（(\d+) 张", SKILL)
    if gt:
        jpgs = len(list((ROOT / "references" / "gallery").glob("*.jpg")))
        if int(gt.group(1)) != jpgs:
            errors.append(f"SKILL References 表 gallery 行称 {int(gt.group(1))} 张，实际 {jpgs} 张")
    return errors


def ledger_header_counts(speed):
    """verification-ledger 各家族标题「（N）」= 该族台账行数；台账「用途」行 N = 速查表总数。
    历史教训：F1 曾标题写（15）实际 14 行；用途行写 62 实际 61。"""
    errors = []
    ledger = (ROOT / "references" / "verification-ledger.md").read_text(encoding="utf-8")
    fam_of = {"F1": "F1 笔意水墨", "F2": "F2 留白海报", "F3": "F3 城市建筑", "F4": "F4 治愈插画",
              "F5": "F5 东方古典", "F6": "F6 氛围实验", "F7": "F7 写实摄影", "F8": "F8 概念海报", "F9": "F9 照片转艺术"}
    total = sum(len(v) for v in speed.values())
    for fam, label in fam_of.items():
        m = re.search(rf"^### {re.escape(label)}[^\n]*?（(\d+)）", ledger, re.M)
        if not m:
            errors.append(f"台账缺少 {label} 族标题（或「（N）」计数格式失配）")
            continue
        declared = int(m.group(1))
        nxt = re.search(rf"^### {re.escape(label)}[^\n]*?（\d+）\n(.*?)(?=^### |\Z)", ledger, re.M | re.S)
        body = nxt.group(1) if nxt else ""
        actual_rows = len(re.findall(r"^\| (?:[A-Z0-9][A-Z0-9-]*) \| (?:✅|默认|🔶|⚠️)", body, re.M))
        if declared != actual_rows:
            errors.append(f"台账 {label} 标题称 {declared} 个，实际表体 {actual_rows} 行")
    um = re.search(r"^> 用途：(\d+) 个变体", ledger, re.M)
    if not um:
        errors.append("台账「用途」行锚点失配（「用途：N 个变体」被改动）")
    elif int(um.group(1)) != total:
        errors.append(f"台账「用途」称 {int(um.group(1))} 个变体，速查表实际 {total}")
    return errors


INTERNAL_TERMS = ["踏雪审美", "踏雪DNA", "踏雪 DNA", "踏雪留白", "踏雪 留白", "踏雪纸感", "踏雪 纸感", "踏雪化", "踏雪参考色板"]


def prompt_black_terms():
    """检查所有 references 代码块（即交付给生图模型的 prompt 模板）是否泄漏内部术语。"""
    hits = []
    for p in sorted((ROOT / "references").rglob("*.md")):
        text = p.read_text(encoding="utf-8")
        for m in re.finditer(r"```(.*?)```", text, re.S):
            block = m.group(1)
            for term in INTERNAL_TERMS:
                if term in block:
                    hits.append(f"{p.relative_to(ROOT)} 代码块含内部术语「{term}」")
    return hits


def spec_conflicts():
    """规范矛盾回归检查（canary）：五类已修复缺陷复发即 FAIL。"""
    errors = []
    cp = (ROOT / "references" / "create-pipeline.md").read_text(encoding="utf-8")
    if "留白强制：凡非写实家族" in cp:
        errors.append("create-pipeline 三道闸 #2 仍是一刀切留白（须按家族豁免 F3-O/F5-L/F5-M3/F6-D）")
    if "禁止向这类模板注入留白百分比" not in cp:
        errors.append("create-pipeline 三道闸 #2 缺少满构图豁免句")
    if "唯一例外 = geometric-monument-poster.md" not in cp:
        errors.append("create-pipeline 三道闸 #3 缺少纪念碑 ≤5 色例外标注（色数双标准复发）")
    pc = (ROOT / "references" / "prompt-craft.md").read_text(encoding="utf-8")
    if re.search(r"锚点参考：[^。]*≤5 色", pc):
        errors.append("prompt-craft 量化锚点仍是 ≤5 色（默认必须 ≤4，例外须显式标注）")
    sp = (ROOT / "references" / "scenario-pack.md").read_text(encoding="utf-8")
    if "只推荐已验证 / 默认变体与已固化参考模板" not in sp:
        errors.append("scenario-pack 门控基线缺失（已验证/默认/已固化参考模板可推荐）")
    if "不要求本体系复验" not in sp:
        errors.append("scenario-pack 门控退化为「本体系验证才能推荐」（与来源已验证语义冲突）")
    for token in ("F1-Z", "F1-AA", "F2-K", "F2-AB", "F5-AC",
                  "F1-AE", "F1-AH", "F2-AC", "F5-AE", "F5-AF", "F7-AE"):
        for line in sp.splitlines():
            if line.startswith("|") and re.search(rf"(?<![A-Z0-9-]){re.escape(token)}(?![A-Z0-9-])", line):
                errors.append(f"scenario-pack 推荐了实验/测试变体 {token}，违反门控")
    mp = (ROOT / "references" / "memory-protocol.md").read_text(encoding="utf-8")
    if "archive/YYYY-MM.md" not in mp:
        errors.append("memory-protocol 归档路径未落地（双写硬规则不可执行；本地版与发布版分别为素材库路径 / memory/archive 泛化路径，均含此片段）")
    rt = (ROOT / "references" / "imagegen-routing.md").read_text(encoding="utf-8")
    if "2048x816" not in rt:
        errors.append("imagegen-routing 比例真源缺 5:2 行（默认家族 F8-V8 查不到比例）")
    # 交付完整性计数同步（SKILL 硬约束 #2 vs optimize-pipeline 交付完整性检查，历史教训：加第 4 项后 SKILL 仍写 5 项）
    if "交付完整性 6 项" not in SKILL or "矛盾扫描结果 /" not in SKILL:
        errors.append("SKILL 硬约束 #2 交付完整性应为 6 项且含矛盾扫描结果（与 optimize-pipeline 同步）")
    op = (ROOT / "references" / "optimize-pipeline.md").read_text(encoding="utf-8")
    if "✅ 矛盾扫描结果" not in op:
        errors.append("optimize-pipeline 交付完整性检查缺「矛盾扫描结果」项")
    # 家族层硬规则回归：L2 禁写色温/ISO 数值（F7-AE 曾写「色温 3200K」）；禁「≤5 色」
    # （唯一例外 geometric-monument-poster.md 在 references 不在 style-library）；文字纯净句禁「除画面外」病句
    for p in sorted((ROOT / "references" / "style-library").glob("*.md")):
        text = p.read_text(encoding="utf-8")
        if re.search(r"(?:色温|ISO)\s*3200", text):
            errors.append(f"{p.name} 出现色温/ISO 3200 数值（违反 prompt-craft L2 分级：只写效果不写数值）")
        if re.search(r"≤5\s*[色种]", text):
            errors.append(f"{p.name} 量化出现 ≤5 色（全局色彩预算 ≤4，唯一例外 geometric-monument 不在本目录）")
        if "除画面外" in text:
            errors.append(f"{p.name} 文字纯净句含「除画面外」病句（指定文字槽未替换）")
    return errors


def body_status_sync():
    """正文状态行同步：索引表 ✅/⚠️/🔶 的变体，其正文小节（含标题行）须出现同一状态图标。"""
    errors = []
    for fam, fname in FAMILY_FILES.items():
        text = (ROOT / "references" / "style-library" / fname).read_text(encoding="utf-8")
        for variant, state in family_index_table(fam):
            if state not in ("✅", "⚠️", "🔶"):
                continue
            m = re.search(rf"(^## .*{re.escape(variant)}.*$.*?)(?=^## |\Z)", text, re.M | re.S)
            if not m:
                errors.append(f"{fam}-{variant} 索引标 {state}，但找不到正文小节")
            elif state not in m.group(1):
                errors.append(f"{fam}-{variant} 索引标 {state}，正文小节无对应状态图标")
    return errors


def variant_section(text, variant):
    """返回变体正文小节（含标题行），找不到返回 None。标题格式：## D — 名称 或 ## F2-K — 名称。"""
    # 变体代号在标题行是「## 代号 —」或「## F#-代号 —」形式，锚定行首避免跨行误匹配
    m = re.search(rf"(^## (?:F\d+-)?{re.escape(variant)} — .*?$.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def section_exists():
    """索引里的每个变体必须能在家族文件中找到 ## 标题段（任何状态，含默认）。
    历史教训：F1-TX 曾缺 ## 标题但索引有行，placeholder_balance/variant_trio 因
    「body_status_sync 已报」静默 continue，导致该变体三件套检查整段漏检。"""
    errors = []
    for fam, fname in FAMILY_FILES.items():
        text = (ROOT / "references" / "style-library" / fname).read_text(encoding="utf-8")
        for variant, _ in family_index_table(fam):
            if variant_section(text, variant) is None:
                errors.append(f"{fam}-{variant}: 索引表有行但家族文件无「## 标题段」（读取协议按标题定位，缺标题 = 按段读失效）")
    return errors


def placeholder_balance():
    """每个变体 prompt 块 [占位符]/{占位符} 配平（成对），且存在「用户输入内容」或模板外槽位说明。"""
    errors = []
    for fam, fname in FAMILY_FILES.items():
        text = (ROOT / "references" / "style-library" / fname).read_text(encoding="utf-8")
        for variant, _ in family_index_table(fam):
            section = variant_section(text, variant)
            if not section:
                continue  # body_status_sync 已报
            for code in re.finditer(r"```\n(.*?)```", section, re.S):
                prompt = code.group(1)
                opens = prompt.count("[") + prompt.count("{")
                closes = prompt.count("]") + prompt.count("}")
                if opens != closes:
                    errors.append(f"{fam}-{variant}: prompt 占位符不成对 ({opens} 开 vs {closes} 闭)")
                # 占位符必须有承接：用户输入内容槽位 / 槽位说明 / 占位符自带填法（填入/请在此/选项说明）
                placeholders = re.findall(r"\[([^\]]+)\]|\{([^}]+)\}", prompt)
                orphans = []
                for a, b in placeholders:
                    p = a or b
                    if "填入" in p or "请在此" in p or "：" in p or "/" in p or "选一" in p:
                        continue  # 自带填法或选项说明
                    orphans.append(p)
                if orphans and "用户输入内容" not in prompt and "槽位" not in section:
                    errors.append(f"{fam}-{variant}: 占位符 {orphans} 无「用户输入内容」槽位/「槽位」说明承接")
    return errors


def variant_trio():
    """每个变体三件套：量化行 齐备；默认/✅/⚠️/🔶 任一状态合法；有槽位声明时必须能在 prompt 中找到占位符承接。"""
    errors = []
    for fam, fname in FAMILY_FILES.items():
        text = (ROOT / "references" / "style-library" / fname).read_text(encoding="utf-8")
        for variant, state in family_index_table(fam):
            section = variant_section(text, variant)
            if not section:
                continue  # body_status_sync 已报
            if "**量化**" not in section:
                errors.append(f"{fam}-{variant}: 缺「量化」行")
            # 状态合法：索引状态列必须是 空（默认）/ ✅ / ⚠️ / 🔶 之一，非法即报
            has_state = state in ("", "默认", "✅", "⚠️", "🔶")
            if "**量化**" in section and not has_state:
                errors.append(f"{fam}-{variant}: 索引状态非法（{state}）")
            # 槽位声明 → prompt 内必须有 [占位符]/{占位符}，或槽位说明明确写「替换/可换/必填变量」等模板外槽位形态
            prompt = ""
            for code in re.finditer(r"```\n(.*?)```", section, re.S):
                prompt += code.group(1)
            if "槽位" in section:
                slot_line = ""
                for line in section.splitlines():
                    if "槽位" in line:
                        slot_line = line
                        break
                external_slot = any(k in slot_line for k in ("替换", "可换", "必填", "唯一", "可替换", "选一", "推演", "填"))
                if "[" not in prompt and "{" not in prompt and not external_slot:
                    errors.append(f"{fam}-{variant}: 声明了「槽位」但 prompt 无占位符，槽位说明也未写明替换/必填形态")
    return errors


def main():
    errors = []
    speed = speed_table()
    if len(speed) != 9:
        errors.append(f"SKILL 速查表家族数 != 9: {sorted(speed)}")

    total = sum(len(v) for v in speed.values())
    for fam, expected in speed.items():
        actual = family_index_table(fam)
        exp_tokens = [v for v, _ in expected]
        act_tokens = [v for v, _ in actual]
        if exp_tokens != act_tokens:
            errors.append(f"{fam} 变体清单漂移: SKILL={exp_tokens} vs 家族文件={act_tokens}")
        exp_states = {v: s for v, s in expected}
        act_states = {v: s for v, s in actual}
        if exp_states != act_states:
            errors.append(f"{fam} 状态图标漂移: SKILL={exp_states} vs 家族文件={act_states}")

    refs = references_counts()
    for fam, vs in speed.items():
        if fam not in refs:
            continue  # skill_summary_numbers 已报缺行
        if refs.get(fam)[0] != len(vs):
            errors.append(f"References 表 {fam} 声称 {refs.get(fam)[0]} 变体，实际 {len(vs)}")

    ledger = (ROOT / "references" / "verification-ledger.md").read_text(encoding="utf-8")
    ledger_rows = re.findall(r"^\| (?:[A-Z0-9][A-Z0-9-]*) \| (?:✅|默认|🔶|⚠️)", ledger, re.M)
    if len(ledger_rows) != total:
        errors.append(f"verification-ledger 台账行数 {len(ledger_rows)} != 速查表变体总数 {total}")

    # 参考模板台账必须覆盖新增的非家族模板
    if "参考模板台账" not in ledger or "brand-manual-visual.md" not in ledger:
        errors.append("verification-ledger 缺少参考模板台账（brand-manual-visual.md）")
    if "黑底错版复古文化海报" not in ledger:
        errors.append("verification-ledger 参考模板台账缺少黑底错版用户专属模板")

    # SKILL 加载协议与 References 必须接入 brand-manual-visual
    if "brand-manual-visual.md" not in SKILL:
        errors.append("SKILL.md 未接入 references/brand-manual-visual.md")

    # prompt 模板代码块不得泄漏内部黑话
    for hit in prompt_black_terms():
        errors.append(hit)

    # 叙述性数字断言（标题计数/References 名单/gallery 张数/台账族标题）
    for e in skill_summary_numbers():
        errors.append(e)
    for e in ledger_header_counts(speed):
        errors.append(e)
    # 变体段存在性（任何状态，防「索引有、正文无」静默漏检）
    for e in section_exists():
        errors.append(e)
    # 规范矛盾回归（canary）与正文状态行同步
    for e in spec_conflicts():
        errors.append(e)
    for e in body_status_sync():
        errors.append(e)
    # 占位符配平 + 变体三件套（量化/状态/槽位）
    for e in placeholder_balance():
        errors.append(e)
    for e in variant_trio():
        errors.append(e)

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: 9 家族 / {total} 变体，SKILL 速查表 = 家族索引 = References 计数 = 验证台账；"
          f"叙述性数字断言通过（标题/名单/gallery/台账族计数）；正文状态行同步通过；占位符配平 + 三件套检查通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
