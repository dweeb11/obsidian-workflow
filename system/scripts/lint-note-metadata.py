#!/usr/bin/env python3
"""Lint lightweight Obsidian note metadata conventions.

Checks are intentionally report-only: this script never rewrites notes.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
VISIBLE_LAST_TOUCHED_RE = re.compile(r"\*\*Last touched:\*\*\s*([0-9]{4}-[0-9]{2}-[0-9]{2}|YYYY-MM-DD)")
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
LINEAR_ISSUE_RE = re.compile(r"^[A-Z][A-Z0-9]+-\d+$")
LINEAR_URL_RE = re.compile(r"linear\.app/.+/issue/([A-Z][A-Z0-9]+-\d+)(?:/|$)")
SKIP_DIRS = {".git", ".obsidian", ".trash", "node_modules", ".venv", "__pycache__"}


def iter_markdown(paths: list[Path]) -> Iterable[Path]:
    for path in paths:
        if path.is_file() and path.suffix.lower() == ".md":
            yield path
            continue
        if not path.is_dir():
            continue
        for child in path.rglob("*.md"):
            if any(part in SKIP_DIRS for part in child.parts):
                continue
            yield child


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    frontmatter = text[4:end]
    fields: dict[str, str] = {}
    for line in frontmatter.splitlines():
        if not line or line.startswith(" ") or line.startswith("-") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"\'')
    return fields


def valid_linear_value(value: str) -> bool:
    if not value:
        return False
    if LINEAR_ISSUE_RE.match(value):
        return True
    return bool(LINEAR_URL_RE.search(value))


def lint_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    fields = parse_frontmatter(text)
    messages: list[str] = []

    frontmatter_date = fields.get("last_touched")
    # Ignore examples/templates inside fenced code blocks; only rendered Memory Cards count.
    rendered_text = FENCED_BLOCK_RE.sub("", text)
    visible_dates = VISIBLE_LAST_TOUCHED_RE.findall(rendered_text)

    if frontmatter_date and frontmatter_date != "YYYY-MM-DD" and not DATE_RE.match(frontmatter_date):
        messages.append(f"invalid last_touched date: {frontmatter_date!r}")

    if frontmatter_date and visible_dates:
        mismatches = [date for date in visible_dates if date != frontmatter_date]
        if mismatches:
            messages.append(
                "last_touched mismatch: "
                f"frontmatter={frontmatter_date!r}, visible={', '.join(sorted(set(mismatches)))}"
            )

    linear_issue = fields.get("linear_issue")
    if linear_issue and not valid_linear_value(linear_issue):
        messages.append(f"malformed linear_issue: {linear_issue!r}")

    return messages


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Report Obsidian last_touched and linear_issue metadata problems."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path(".")],
        help="Files or directories to scan; defaults to the current vault.",
    )
    args = parser.parse_args()

    failures = 0
    scanned = 0
    for path in sorted(set(iter_markdown(args.paths))):
        scanned += 1
        messages = lint_file(path)
        for message in messages:
            failures += 1
            print(f"{path}: {message}")

    if failures:
        print(f"\n{failures} metadata issue(s) found across {scanned} markdown file(s).", file=sys.stderr)
        return 1

    print(f"No metadata issues found across {scanned} markdown file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
