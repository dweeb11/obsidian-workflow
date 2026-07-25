#!/usr/bin/env python3
"""Scan recent daily notes and surface carry-forward decay candidates.

A task that keeps getting carried forward is either not really a task or not
really yours. This is a read-only detector for that pattern: it counts items
that repeat across recent daily notes and stays silent when nothing crosses the
threshold.

Two surfaces, because a day that was closed records its carry-forward and a day
that was not does not:

- **Closed days** (the precise signal). A note carrying the
  `## Daily Cleanup Routing` appendix is read at `### Carry Forward / Open
  Loops` and nowhere else, so the raw `## ToDo` above the appendix is never
  counted twice. Every bullet in that section counts, checkbox or not — the
  section is carry-forward material by definition, and idea seeds are written
  there as plain bullets.
- **Unclosed days** (a proxy). A note with no appendix falls back to `## ToDo`,
  counting checkboxes only. An item genuinely carried forward reappears in each
  day's ToDo, so the signal is still there.

Known limit of the fallback: a recurring task re-entered every morning ("walk
the dog") trips the threshold and gets reported as decay. On the appendix path
it would not, since a habit never lands in Open Loops. Close your days and the
noise goes away.
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

DAILY_STEM = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ROUTING_APPENDIX = re.compile(r"^##\s+Daily Cleanup Routing\s*$", re.IGNORECASE | re.MULTILINE)
OPEN_LOOPS_HEADER = re.compile(
    r"^###\s+Carry Forward\s*/\s*Open Loops\s*$", re.IGNORECASE | re.MULTILINE
)
TODO_HEADER = re.compile(r"^##\s+ToDo\s*$", re.IGNORECASE | re.MULTILINE)
# Open Loops is followed by a sibling h3, so scoping stops at h3 as well as h2.
NEXT_H3_OR_H2 = re.compile(r"^#{2,3}\s+", re.MULTILINE)
NEXT_H2 = re.compile(r"^##\s+", re.MULTILINE)
CHECKBOX_LINE = re.compile(r"^\s*-\s+\[[ xX]\]\s+(.+?)\s*$", re.MULTILINE)
# Any bullet, with the checkbox marker optional and stripped, so `- [ ] Foo` and
# `- Foo` normalize to the same item across the two renderings.
BULLET_LINE = re.compile(r"^\s*-\s+(?:\[[ xX]\]\s+)?(.+?)\s*$", re.MULTILINE)


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


def section_block(text: str, header: re.Pattern[str], terminator: re.Pattern[str]) -> str:
    """Return the body of one section so repeated items elsewhere do not count."""
    match = header.search(text)
    if not match:
        return ""
    rest = text[match.end() :]
    next_section = terminator.search(rest)
    return rest[: next_section.start()] if next_section else rest


def carry_forward_block(text: str) -> tuple[str, re.Pattern[str]]:
    """Return the block to count and the line pattern to count it with.

    A closed day is read at its routing appendix and never falls back, so the
    raw `## ToDo` preserved above the appendix cannot be counted twice.
    """
    if ROUTING_APPENDIX.search(text):
        return section_block(text, OPEN_LOOPS_HEADER, NEXT_H3_OR_H2), BULLET_LINE
    return section_block(text, TODO_HEADER, NEXT_H2), CHECKBOX_LINE


def normalize_item(item: str) -> str:
    """Normalize whitespace without rewriting the owner's wording."""
    return re.sub(r"\s+", " ", item).strip()


def collect_carry_forward_lines(paths: list[Path]) -> Counter[str]:
    counter: Counter[str] = Counter()
    for path in paths:
        block, line_pattern = carry_forward_block(path.read_text(encoding="utf-8"))
        for match in line_pattern.finditer(block):
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
