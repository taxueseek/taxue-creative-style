#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""taxue-creative-style 一致性检查（只读，不改文件）。

检查项：
1. SKILL.md §1 速查表 9 家族变体清单
2. 各家族文件「变体索引」表与速查表是否一致（含状态图标）
3. References 表声称的变体数与速查表是否一致
4. verification-ledger.md 台账行数是否等于速查表变体总数
5. 规范矛盾回归（五类已修复缺陷的 canary：留白一刀切 / 色数双标准 /
   scenario 门控（实验/测试变体不得进场景包）/ 归档路径缺失 / 比例真源缺 5:2）
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
    text = (ROOT / "references" / "style-library" / FAMILY_FILES[fam]).read_text(encoding="utf-8")
    idx = text.index("**变体索引**")
    out = []
    for line in text[idx:].splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or cells[0] in ("变体", "------"):
            continue
        token, state = cells[0], cells[-1]
        for s in STATUS:
            if token.endswith(s):
                state, token = s, token[: -len(s)]
                break
        state = "✅" if "✅" in state else ("⚠️" if "⚠️" in state else ("🔶" if "🔶" in state else ""))
        out.append((token.strip(), state))
    return out


def references_counts():
    out = {}
    for line in SKILL.splitlines():
        m = re.match(r"\| `references/style-library/(F\d)-[\w-]+\.md` \| (F\d)[^|]*?(\d+) 变体", line)
        if m:
            out[m.group(2)] = int(m.group(3))
    return out


INTERNAL_TERMS = ["踏雪审美", "踏雪DNA", "踏雪留白", "踏雪纸感", "踏雪化", "踏雪参考色板"]


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
    for token in ("F1-Z", "F1-AA", "F2-K", "F2-AB", "F5-AC", "F1-AE"):
        for line in sp.splitlines():
            if line.startswith("|") and re.search(rf"(?<![A-Z0-9-]){re.escape(token)}(?![A-Z0-9-])", line):
                errors.append(f"scenario-pack 推荐了实验/测试变体 {token}，违反门控")
    mp = (ROOT / "references" / "memory-protocol.md").read_text(encoding="utf-8")
    if "memory/archive/YYYY-MM.md" not in mp:
        errors.append("memory-protocol 归档路径未落地（双写铁律不可执行）")
    rt = (ROOT / "references" / "imagegen-routing.md").read_text(encoding="utf-8")
    if "2048x816" not in rt:
        errors.append("imagegen-routing 比例真源缺 5:2 行（默认家族 F8-V8 查不到比例）")
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
        if refs.get(fam) != len(vs):
            errors.append(f"References 表 {fam} 声称 {refs.get(fam)} 变体，实际 {len(vs)}")

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

    # 规范矛盾回归（canary）与正文状态行同步
    for e in spec_conflicts():
        errors.append(e)
    for e in body_status_sync():
        errors.append(e)

    if errors:
        print("FAIL")
        for e in errors:
            print(" -", e)
        return 1
    print(f"OK: 9 家族 / {total} 变体，SKILL 速查表 = 家族索引 = References 计数 = 验证台账；"
          f"规范矛盾回归 5 项通过；正文状态行同步通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
