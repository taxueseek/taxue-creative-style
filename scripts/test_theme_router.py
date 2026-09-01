#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""主题路由 + 开放注册表的量化回归。"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_family_count_open():
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    m = re.search(r"^## 1\. 风格库（(\d+) 家族，(\d+) 个变体）", skill, re.M)
    assert m, "SKILL §1 标题必须是开放计数，不能写死「9 家族」"
    nfam, nvar = int(m.group(1)), int(m.group(2))
    assert nfam >= 14, nfam
    assert nvar == 77, nvar
    lib = list((ROOT / "references" / "style-library").glob("F*-*.md"))
    assert len(lib) == nfam, (len(lib), nfam)


def test_independence_protocol():
    text = (ROOT / "references" / "style-independence.md").read_text(encoding="utf-8")
    for token in ("媒介", "禁忌", "称呼", "题材", "≥3 分必须独立"):
        assert token in text, token
    assert "F5-M1" in text and "混卡" in text


def test_theme_router_mece():
    text = (ROOT / "references" / "theme-router.md").read_text(encoding="utf-8")
    types = ["符号文字", "节气物候", "生肖民俗", "神话戏文", "城市地标", "器物工艺", "日常治愈", "人物形象", "旧照改造"]
    for t in types:
        assert t in text, t
    assert "点名「皮影」一律 F11-PY" in text
    assert "禁止再走 F5-M1" in text
    # 备选必须换媒介：同一主题的剪纸不得互相当唯一备选
    assert "禁止两个剪纸变体互相当备选" in text


def test_new_variants_have_trio():
    needed = {
        "F10-papercut.md": ["F10-ST", "F10-WH"],
        "F11-puppetry.md": ["F11-PY", "F11-MU"],
        "F12-glaze.md": ["F12-QH", "F12-BX"],
        "F13-archive.md": ["F13-AR", "F13-PL"],
        "F14-animation.md": ["F14-YZ", "F14-ZZ", "F14-SM"],
        "F1-ink-wash.md": ["F1-YS", "F1-BY"],
        "F5-oriental.md": ["F5-YL", "F5-QS"],
        "F7-photography.md": ["F7-ED"],
    }
    for fname, variants in needed.items():
        text = (ROOT / "references" / "style-library" / fname).read_text(encoding="utf-8")
        for v in variants:
            assert f"## {v} —" in text, v
            section = re.search(rf"(^## {v} — .*?$.*?)(?=^## |\Z)", text, re.M | re.S)
            assert section, v
            body = section.group(1)
            assert "**量化**" in body
            assert "**槽位**" in body
            assert "```" in body


def test_consistency_check():
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "consistency-check.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    assert "14 家族 / 77 变体" in r.stdout


if __name__ == "__main__":
    tests = [
        test_family_count_open,
        test_independence_protocol,
        test_theme_router_mece,
        test_new_variants_have_trio,
        test_consistency_check,
    ]
    failed = []
    for t in tests:
        try:
            t()
            print("PASS", t.__name__)
        except Exception as e:
            print("FAIL", t.__name__, e)
            failed.append(t.__name__)
    sys.exit(1 if failed else 0)
