#!/usr/bin/env python3
"""Scan recent daily notes and surface carry-forward decay candidates.

A task that keeps getting carried forward is either not really a task or not
really yours. This is a read-only detector for that pattern: it counts repeated
checkbox items under a `## Carry forward` heading across recent daily notes and
stays silent when nothing crosses the threshold.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

DAILY_STEM = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CARRY_FORWARD_HEADER = re.compile(r"^##\s+Carry forward\s*$", re.IGNORECASE | re.MULTILINE)
CHECKBOX_LINE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.+?)\s*$", re.MULTILINE)


def gather_dailies(vault: Path, days: int) -> list[Path]:
    """Return the most recent daily-note files from supported vault layouts."""
    candidates: list[Path] = []
    roots = [vault, vault / "calendar" / "daily notes", vault / "daily"]
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.md"):
            if DAILY_STEM.match(path.stem):
                candidates.append(path)
    return sorted(set(candidates), key=lambda p: p.stem, reverse=True)[:days]


def carry_forward_block(text: str) -> str:
    """Return only the Carry forward section so repeated tasks elsewhere do not count."""
    match = CARRY_FORWARD_HEADER.search(text)
    if not match:
        return ""
    rest = text[match.end() :]
    next_section = re.search(r"^##\s+", rest, re.MULTILINE)
    return rest[: next_section.start()] if next_section else rest


def normalize_item(item: str) -> str:
    """Normalize whitespace without rewriting the owner's wording."""
    return re.sub(r"\s+", " ", item).strip()


def collect_carry_forward_lines(paths: list[Path]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for path in paths:
        block = carry_forward_block(path.read_text(encoding="utf-8"))
        for match in CHECKBOX_LINE.finditer(block):
            item = normalize_item(match.group(1))
            if item:
                counter[item] += 1
    return counter


def render_decay(candidates: list[tuple[str, int]], days: int) -> str:
    lines = ["## Carry-forward decay candidates", ""]
    for item, count in sorted(candidates, key=lambda row: (-row[1], row[0].lower())):
        lines.append(f"- {item} (seen {count} times in last {days} daily notes)")
    return "\n".join(lines)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--days", type=int, default=7)
    # Three daily setups, or roughly 7 calendar days. Keep configurable for tuning.
    parser.add_argument("--decay-threshold", type=int, default=3)
    args = parser.parse_args()

    paths = gather_dailies(args.vault, max(args.days, 0))
    if not paths:
        return 0

    counts = collect_carry_forward_lines(paths)
    decay = [(item, count) for item, count in counts.items() if count >= args.decay_threshold]
    if not decay:
        return 0

    print(render_decay(decay, args.days))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
