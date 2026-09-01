#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate taxue print-contract catalogs. Stdlib only."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYSTEM_DIR = ROOT / "references" / "design-system"
HEX = re.compile(r"^#[0-9A-F]{6}$")
EXPECTED = {
    "colors.json",
    "compositions.json",
    "rhythm.json",
    "typography.json",
    "processes.json",
    "imperfections.json",
}


def fail(message: str) -> None:
    print(f"design-system validation failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(name: str) -> dict:
    path = SYSTEM_DIR / name
    if not path.exists():
        fail(f"missing {name}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail(f"{name} must use schema_version 1")
    return data


def unique_ids(items: list, label: str) -> set[str]:
    ids = [item.get("id") for item in items]
    if any(not isinstance(i, str) or not i for i in ids):
        fail(f"every {label} needs a non-empty id")
    if len(ids) != len(set(ids)):
        fail(f"{label} ids must be unique")
    return set(ids)


def main() -> int:
    json_files = {p.name for p in SYSTEM_DIR.glob("*.json")}
    if json_files != EXPECTED:
        fail(f"expected {sorted(EXPECTED)}, found {sorted(json_files)}")

    contract = SYSTEM_DIR / "print-contract.md"
    if not contract.exists():
        fail("missing print-contract.md")

    colors = load("colors.json")
    compositions = load("compositions.json")
    rhythm = load("rhythm.json")
    typography = load("typography.json")
    processes = load("processes.json")
    imperfections = load("imperfections.json")

    substrates = colors.get("substrates", [])
    substrate_ids = unique_ids(substrates, "substrate")
    if len(substrates) < 4:
        fail("need at least four substrates (xuan, newsprint, archive, ink-black or cool white)")
    for substrate in substrates:
        if not HEX.fullmatch(substrate.get("hex", "")) or substrate.get("counts_as_ink") is not False:
            fail(f"{substrate['id']} must use uppercase hex and counts_as_ink false")
        if not substrate.get("use_for"):
            fail(f"{substrate['id']} needs use_for")

    inks = colors.get("inks", [])
    ink_ids = unique_ids(inks, "ink")
    if len(inks) < 6:
        fail("need at least six named inks")
    for ink in inks:
        if not HEX.fullmatch(ink.get("hex", "")):
            fail(f"{ink['id']} hex must be uppercase")

    palettes = colors.get("palettes", [])
    palette_ids = unique_ids(palettes, "palette")
    defaults = colors.get("defaults", {})
    if defaults.get("substrate_id") not in substrate_ids:
        fail("color defaults.substrate_id must exist")
    if defaults.get("palette_id") not in palette_ids:
        fail("color defaults.palette_id must exist")
    if defaults.get("style_direction") != "contemporary_print":
        fail("defaults.style_direction must be contemporary_print")
    for palette in palettes:
        for ink_id in palette.get("ink_ids", []):
            if ink_id not in ink_ids:
                fail(f"{palette['id']} references unknown ink {ink_id}")
        if palette.get("mode") == "pure_one_ink" and len(palette.get("ink_ids", [])) != 1:
            fail(f"{palette['id']} one-ink must have exactly one ink")
        if palette.get("mode") != "pure_one_ink" and not (2 <= len(palette.get("ink_ids", [])) <= 2):
            fail(f"{palette['id']} two-ink modes must have exactly two inks")

    comps = compositions.get("compositions", [])
    unique_ids(comps, "composition")
    if len(comps) < 8:
        fail("need at least eight composition families")
    for comp in comps:
        empty = comp.get("empty_paper_percent")
        if not (isinstance(empty, list) and len(empty) == 2 and empty[0] <= empty[1]):
            fail(f"{comp['id']} empty_paper_percent must be [lo, hi]")
        if comp.get("manual_gesture_limit") != 1:
            fail(f"{comp['id']} manual_gesture_limit must be 1")

    tensions = unique_ids(rhythm.get("tensions", []), "tension")
    focals = unique_ids(rhythm.get("focal_events", []), "focal_event")
    releases = unique_ids(rhythm.get("release_zones", []), "release_zone")
    rdef = rhythm.get("defaults", {})
    if rdef.get("tension_id") not in tensions:
        fail("rhythm default tension missing")
    if rdef.get("focal_event_id") not in focals:
        fail("rhythm default focal_event missing")
    if rdef.get("release_zone_id") not in releases:
        fail("rhythm default release_zone missing")
    if "focal_evidence_crossing" not in focals:
        fail("taxue-original focal_evidence_crossing is required")

    unique_ids(typography.get("voices", []), "voice")
    unique_ids(typography.get("hierarchies", []), "hierarchy")
    tdef = typography.get("defaults", {})
    if tdef.get("invented_text_language") != "zh":
        fail("invented display text must default to zh")
    if tdef.get("max_voices") != 3:
        fail("max_voices must be 3")

    procs = processes.get("processes", [])
    proc_ids = unique_ids(procs, "process")
    if "process_photography" not in proc_ids:
        fail("photography process required for exemption routing")
    if processes.get("defaults", {}).get("contemporary_not_vintage") is not True:
        fail("print must default to contemporary, not vintage")

    fx = imperfections.get("effects", [])
    unique_ids(fx, "effect")
    never = imperfections.get("defaults", {}).get("never_without_request", [])
    if "yellowed paper" not in never:
        fail("yellowed paper must stay in never_without_request")

    poster_print = Path.home() / ".agents/skills/taxue-poster-studio/references/print-mode.md"
    if not poster_print.is_file():
        fail("poster-studio print-mode.md is the print SoT and is missing")
    contract_text = contract.read_text(encoding="utf-8")
    if "print-mode.md" not in contract_text:
        fail("print-contract.md must point to poster-studio print-mode.md")

    evals_path = ROOT / "evals" / "evals.json"
    if not evals_path.exists():
        fail("missing evals/evals.json")
    evals = json.loads(evals_path.read_text(encoding="utf-8"))
    cases = evals.get("evals", [])
    if len(cases) < 8:
        fail("need at least 8 print-contract evals")
    for case in cases:
        if not case.get("expected_recipe") or not case.get("must_not"):
            fail(f"eval {case.get('id')} needs expected_recipe and must_not")

    print(
        f"OK: design-system {len(substrate_ids)} substrates / {len(ink_ids)} inks / "
        f"{len(palette_ids)} palettes / {len(comps)} compositions / {len(cases)} evals"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
