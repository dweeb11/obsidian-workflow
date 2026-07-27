#!/usr/bin/env python3
"""Emit per-tool skill adapters from the agent-agnostic registry.

The registry (system/skills/registry.json) says WHICH workflows exist. The
contract files under system/skills/ hold the actual workflow prose. This script
projects the registry into whatever shape each tool wants to read:

  claude  -> .claude/skills/<slug>/SKILL.md
  cursor  -> .cursor/rules/<slug>.mdc
  index   -> generated blocks inside Skills-Map.md and AGENTS.md

Adapters are POINTERS, never homes. Each one is a handful of lines that names
the contract and gets out of the way. That is the whole reason this vault can
add a tool directory without becoming a single-tool vault: nothing an agent
needs to know lives in the adapter, so an agent with no adapter at all loses
nothing but a shortcut.

Adapters are committed to the repo so a fresh clone works with no install step.
This script exists for maintenance and for the CI check that regenerates them
and diffs -- see test_generate_adapters.py.

Usage:
    python3 system/scripts/generate-adapters.py            # write adapters
    python3 system/scripts/generate-adapters.py --check    # exit 1 if stale
    python3 system/scripts/generate-adapters.py --emitter claude
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

VAULT_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = VAULT_ROOT / "system" / "skills" / "registry.json"

# Sentinel that identifies a file as ours. Orphan cleanup keys off this so a
# hand-authored tool skill sitting next to the generated ones is never deleted.
GENERATED_MARKER = "GENERATED FILE -- do not edit by hand."

GENERATED_BANNER = (
    GENERATED_MARKER + "\n"
    "Source: system/skills/registry.json\n"
    "Regenerate: python3 system/scripts/generate-adapters.py"
)

BEGIN_MARKER = "<!-- BEGIN GENERATED: skills-registry -->"
END_MARKER = "<!-- END GENERATED: skills-registry -->"


class RegistryError(Exception):
    """Raised when the registry is malformed or points at missing files."""


def load_registry(root: Path = VAULT_ROOT) -> List[Dict[str, Any]]:
    """Read and validate the registry, returning its entries."""
    path = root / "system" / "skills" / "registry.json"
    if not path.exists():
        raise RegistryError("registry not found at %s" % path)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RegistryError("registry is not valid JSON: %s" % exc) from exc

    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        raise RegistryError("registry has no entries")

    seen = set()
    for entry in entries:
        for field in ("slug", "title", "description", "contract"):
            if not entry.get(field):
                raise RegistryError(
                    "entry %r is missing required field %r"
                    % (entry.get("slug", "<unknown>"), field)
                )
        slug = entry["slug"]
        if slug in seen:
            raise RegistryError("duplicate slug %r" % slug)
        seen.add(slug)
        if not (root / entry["contract"]).exists():
            raise RegistryError(
                "entry %r points at a missing contract: %s" % (slug, entry["contract"])
            )
        for extra in entry.get("also_read", []):
            if not (root / extra).exists():
                raise RegistryError(
                    "entry %r also_read points at a missing file: %s" % (slug, extra)
                )
    return entries


def _reads_block(entry: Dict[str, Any]) -> str:
    lines = ["- `%s`" % entry["contract"]]
    for extra in entry.get("also_read", []):
        lines.append("- `%s`" % extra)
    return "\n".join(lines)


def _operation_clause(entry: Dict[str, Any]) -> str:
    operation = entry.get("operation")
    if operation:
        return "the **%s** operation in that contract" % operation
    return "that contract"


# --------------------------------------------------------------------------
# Emitters. Each returns {relative_path: file_contents}.
# --------------------------------------------------------------------------


def emit_claude(entries: List[Dict[str, Any]]) -> Dict[str, str]:
    """Claude Code project skills: .claude/skills/<slug>/SKILL.md"""
    out = {}
    for entry in entries:
        body = """---
name: {slug}
description: {description}
---

<!--
{banner}
-->

# {title}

This file is a **non-authoritative adapter**. It contains no workflow logic. The
authoritative, agent-agnostic contract lives in the vault and supersedes it:

{reads}

## What to do

1. Read the contract file above.
2. Perform {operation} exactly as it specifies.
3. Self-verify against the contract's own acceptance checklist before declaring
   the work done.

If this adapter ever conflicts with the contract, follow the contract and report
the drift -- the fix belongs in `system/skills/registry.json`, not here.
""".format(
            slug=entry["slug"],
            description=entry["description"],
            banner=GENERATED_BANNER,
            title=entry["title"],
            reads=_reads_block(entry),
            operation=_operation_clause(entry),
        )
        out[".claude/skills/%s/SKILL.md" % entry["slug"]] = body
    return out


def emit_cursor(entries: List[Dict[str, Any]]) -> Dict[str, str]:
    """Cursor project rules: .cursor/rules/<slug>.mdc"""
    out = {}
    for entry in entries:
        body = """---
description: {description}
alwaysApply: false
---

<!--
{banner}
-->

# {title}

Non-authoritative adapter -- no workflow logic lives here. Read the contract:

{reads}

Perform {operation} exactly as written, then self-verify against its acceptance
checklist before declaring the work done.
""".format(
            description=entry["description"],
            banner=GENERATED_BANNER,
            title=entry["title"],
            reads=_reads_block(entry),
            operation=_operation_clause(entry),
        )
        out[".cursor/rules/%s.mdc" % entry["slug"]] = body
    return out


def _registry_table(entries: List[Dict[str, Any]]) -> str:
    rows = [
        "| Skill | Trigger phrases | Context profile | Contract |",
        "|---|---|---|---|",
    ]
    for entry in entries:
        triggers = ", ".join('"%s"' % t for t in entry.get("triggers", [])) or "--"
        contract = entry["contract"]
        stem = Path(contract).stem
        link = "[[%s|%s]]" % (contract[: -len(".md")], stem)
        operation = entry.get("operation")
        title = entry["title"]
        if operation:
            title = "%s (%s)" % (title, operation)
        rows.append(
            "| %s | %s | `%s` | %s |"
            % (title, triggers, entry.get("profile", "default"), link)
        )
    return "\n".join(rows)


def emit_index(entries: List[Dict[str, Any]], root: Path = VAULT_ROOT) -> Dict[str, str]:
    """Rewrite the generated block inside Skills-Map.md and AGENTS.md.

    Only the region between the BEGIN/END markers is replaced, so hand-written
    prose around it survives. A file with no markers is left untouched.
    """
    generated = "%s\n<!-- %s -->\n\n%s\n%s" % (
        BEGIN_MARKER,
        GENERATED_BANNER.replace("\n", " | "),
        _registry_table(entries),
        END_MARKER,
    )
    out = {}
    for name in ("Skills-Map.md", "AGENTS.md"):
        path = root / name
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if BEGIN_MARKER not in text or END_MARKER not in text:
            continue
        head, _, rest = text.partition(BEGIN_MARKER)
        _, _, tail = rest.partition(END_MARKER)
        out[name] = head + generated + tail
    return out


EMITTERS = {
    "claude": emit_claude,
    "cursor": emit_cursor,
    "index": emit_index,
}


def build(
    entries: List[Dict[str, Any]],
    root: Path = VAULT_ROOT,
    only: str = None,
) -> Dict[str, str]:
    """Return {relative_path: contents} for every selected emitter."""
    out = {}
    for name, emitter in EMITTERS.items():
        if only and name != only:
            continue
        if name == "index":
            out.update(emitter(entries, root))
        else:
            out.update(emitter(entries))
    return out


def diff_against_disk(
    files: Dict[str, str], root: Path = VAULT_ROOT
) -> Tuple[List[str], List[str]]:
    """Return (missing_or_stale, orphaned) relative paths."""
    stale = []
    for rel, contents in sorted(files.items()):
        path = root / rel
        if not path.exists() or path.read_text(encoding="utf-8") != contents:
            stale.append(rel)

    orphaned = []
    for tool_dir, pattern in ((".claude/skills", "*/SKILL.md"), (".cursor/rules", "*.mdc")):
        base = root / tool_dir
        if not base.exists():
            continue
        for path in sorted(base.glob(pattern)):
            rel = path.relative_to(root).as_posix()
            if rel in files:
                continue
            # Only ever reclaim files WE wrote. A vault is free to hand-author
            # tool skills alongside the generated ones -- they have no registry
            # entry by design, and deleting them would be data loss, not cleanup.
            try:
                if GENERATED_MARKER not in path.read_text(encoding="utf-8"):
                    continue
            except (OSError, UnicodeDecodeError):
                continue
            orphaned.append(rel)
    return stale, orphaned


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Do not write. Exit 1 if any adapter is stale, missing, or orphaned.",
    )
    parser.add_argument(
        "--emitter",
        choices=sorted(EMITTERS),
        help="Run a single emitter instead of all of them.",
    )
    parser.add_argument(
        "--root",
        default=str(VAULT_ROOT),
        help="Vault root to operate on (default: the vault this script lives in).",
    )
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    try:
        entries = load_registry(root)
    except RegistryError as exc:
        print("registry error: %s" % exc, file=sys.stderr)
        return 2

    files = build(entries, root, args.emitter)
    stale, orphaned = diff_against_disk(files, root)

    if args.check:
        if not stale and not orphaned:
            print("adapters are current (%d files, %d entries)" % (len(files), len(entries)))
            return 0
        for rel in stale:
            print("STALE    %s" % rel)
        for rel in orphaned:
            print("ORPHANED %s  (no registry entry -- delete it)" % rel)
        print(
            "\nRun: python3 system/scripts/generate-adapters.py",
            file=sys.stderr,
        )
        return 1

    for rel, contents in sorted(files.items()):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")
    for rel in orphaned:
        (root / rel).unlink()
        print("removed orphan %s" % rel)
    print("wrote %d adapter files from %d registry entries" % (len(files), len(entries)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
