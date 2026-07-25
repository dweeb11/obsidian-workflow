#!/usr/bin/env python3
"""Sweep one index file for missing wikilink targets.

An index that points at notes which no longer exist is worse than no index.
This is a read-only check for that: it resolves every wikilink in the given
file against the vault and reports the ones with no target. It stays silent
when nothing is missing.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

WIKILINK = re.compile(r"\[\[(.+?)\]\]")


def normalize_link(raw: str) -> str:
    """Reduce a wikilink body to its target path.

    Drops the alias and any anchor, and preserves folder paths. Inside a
    Markdown table the alias pipe has to be written `\\|`, so unescape it
    before splitting or the backslash lands in the target.
    """
    return raw.replace("\\|", "|").split("|", 1)[0].split("#", 1)[0].strip()


def candidate_paths(vault: Path, link: str) -> list[Path]:
    """Return Obsidian-style target candidates for path and bare-note links."""
    link = normalize_link(link)
    if not link:
        return []
    path = Path(link)
    with_suffix = path if path.suffix.lower() == ".md" else path.with_suffix(".md")
    candidates = [vault / with_suffix]
    if len(path.parts) == 1:
        target_name = with_suffix.name.lower()
        candidates.extend(p for p in vault.rglob("*.md") if p.name.lower() == target_name)
    return candidates


def target_exists(vault: Path, link: str) -> bool:
    return any(path.exists() for path in candidate_paths(vault, link))


def display_index(index: Path, vault: Path) -> str:
    try:
        return str(index.relative_to(vault))
    except ValueError:
        return str(index)


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", required=True, type=Path)
    parser.add_argument("--vault", required=True, type=Path)
    args = parser.parse_args()

    if not args.index.exists():
        print(f"ERROR: index not found: {args.index}")
        return 1

    text = args.index.read_text(encoding="utf-8")
    missing: list[str] = []
    seen: set[str] = set()
    for match in WIKILINK.finditer(text):
        link = normalize_link(match.group(1))
        if not link or link in seen:
            continue
        seen.add(link)
        if not target_exists(args.vault, link):
            missing.append(link)

    if not missing:
        return 0

    print(f"## Breadcrumb decay in {display_index(args.index, args.vault)}")
    print("")
    for link in missing:
        print(f"- [[{link}]] — no matching note found")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
