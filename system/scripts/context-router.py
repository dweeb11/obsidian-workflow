#!/usr/bin/env python3
"""Minimal vault context router for agents.

Prints a small task-shaped bundle so agents do not read every map by default.
Python rather than shell so the scripts layer runs on Windows with nothing
installed but python3.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Default to the vault this script lives in (system/scripts/context-router.py),
# so the router works from a fresh clone wherever it was put. Override with
# VAULT_CONTEXT_ROOT to point at a different vault.
DEFAULT_VAULT_ROOT = Path(__file__).resolve().parents[2]

HEADER = """# Vault Context Router

Use this as the initial context bundle. Read deeper files only when the task profile says to.
"""

FALLBACK_QUICKSTART = """## Agent Quickstart

- Preserve wikilinks, Dataview blocks, frontmatter, tags, and local note style.
- Search before creating notes.
- Do not move, rename, or delete notes unless explicitly asked.
"""

PROFILES: dict[str, str] = {
    "default": """- Read: `AGENTS.md`, this router output, and the target note/file.
- Optional: relevant `Vault-Map.md` section if creating notes or touching folder structure.
- Avoid: loading all of `Vault-Map.md`, `Skills-Map.md`, or `Me.md` for small edits.""",
    "daily": """- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart, `Skills-Map.md` Daily Capture and Close-Day entries.
- Read when writing: `system/Templates/Daily Note.md`.
- Read `system/skills/daily-capture.md` in full before running Setup or Close.""",
    "intake": """- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart and Note Types, `Skills-Map.md` Intake Extraction entry.
- Then read: `system/skills/intake-extraction.md`.
- Treat `+/clippings/` as the live general intake surface.""",
    "synthesis": """- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart and Note Types, `Skills-Map.md` Vault Synthesis entry.
- Then read: `system/skills/vault-synthesis.md`.
- Use `system/Templates/synthesis-note.md` when creating a synthesis note.""",
    "index": """- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart and Wiki index pages section, `Skills-Map.md` Wiki Index entry.
- Then read: `system/skills/wiki-index.md`.
- Use `system/Templates/wiki-index.md` when creating an `_index.md`.""",
    "voice": """- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart, and `Me.md`.
- Use this profile for the vault owner's voice, preferences, boundaries, assistant behavior, and outward-facing drafts.""",
    "operational": """- Read: `AGENTS.md` and `Vault-Map.md` Agent Quickstart.
- For operational context, prefer current sources: `Me.md`, `atlas/people/`, `efforts/`, `Skills-Map.md`, and relevant `system/skills/*.md` notes.
- Use `system/memory/tag-reference.md` for tag vocabulary.""",
    "map": """- Read: `AGENTS.md`, `Vault-Map.md`, `Skills-Map.md`, and `system/skills/map-maintenance.md`.
- Read `Me.md` when changing preferences, assistant behavior, boundaries, or voice guidance.
- Search for contradicted old wording before finishing.""",
    "help": """Profiles: default, daily, intake, synthesis, index, voice, operational, map.
Set `VAULT_CONTEXT_ROOT=/path/to/vault` to run against a non-default vault.""",
}

ALIASES = {
    "typo": "default",
    "small": "default",
    "clippings": "intake",
    "audit": "synthesis",
    "wiki-index": "index",
    "me": "voice",
    "context": "operational",
    "maps": "map",
    "agent-os": "map",
    "-h": "help",
    "--help": "help",
}

UNKNOWN_PROFILE = """- Unknown profile. Use `context-router.py help` for options.
- Fallback: read `AGENTS.md`, this quickstart, and only the note/section directly relevant to the task."""

CLOSEOUT = """
## Closeout

- Verify with evidence before calling work done."""


def print_section(path: Path, title: str) -> str:
    """Return one `## <title>` section of a Markdown file, heading included."""
    if not path.is_file():
        return ""
    lines: list[str] = []
    in_section = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == f"## {title}":
            in_section = True
            lines.append(line)
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            lines.append(line)
    return "\n".join(lines).rstrip()


def vault_root() -> Path:
    override = os.environ.get("VAULT_CONTEXT_ROOT")
    return Path(override) if override else DEFAULT_VAULT_ROOT


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    profile = argv[1] if len(argv) > 1 else "default"
    root = vault_root()
    if not root.is_dir():
        print(f"context-router: vault root not found: {root}", file=sys.stderr)
        return 1

    print(HEADER)

    quickstart = print_section(root / "Vault-Map.md", "Agent Quickstart")
    print(f"{quickstart}\n" if quickstart else FALLBACK_QUICKSTART)

    print(f"## Task Profile: {profile}\n")
    print(PROFILES.get(ALIASES.get(profile, profile), UNKNOWN_PROFILE))
    print(CLOSEOUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
