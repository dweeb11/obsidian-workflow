#!/usr/bin/env python3
"""Portable session-start context loader.

Prints PROJECT_STATE.md and vault orientation when present.
Silent on the happy path: exits 0 with no stdout when there is nothing useful.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

# Default to the vault this script lives in (system/scripts/session-start-context.py),
# so a fresh clone is recognised wherever it was put. Override with
# SESSION_CONTEXT_VAULT_ROOT to point at a different vault.
DEFAULT_VAULT_ROOT = Path(__file__).resolve().parents[2]


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n\n" if body.strip() else ""


def vault_root() -> Path:
    override = os.environ.get("SESSION_CONTEXT_VAULT_ROOT")
    return Path(override) if override else DEFAULT_VAULT_ROOT


def inside(cwd: Path, root: Path) -> bool:
    try:
        return cwd == root or cwd.is_relative_to(root)
    except (OSError, ValueError):
        return False


def router_output(root: Path) -> str:
    """Run the context router against `root`, or fall back to a one-liner."""
    router = root / "system" / "scripts" / "context-router.py"
    if not router.is_file():
        return "Working in vault: see AGENTS.md for the session lifecycle contract."
    env = os.environ.copy()
    env["VAULT_CONTEXT_ROOT"] = str(root)
    result = subprocess.run(
        [sys.executable, str(router), "default"],
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0 or not result.stdout.strip():
        return "Working in vault: see AGENTS.md for the session lifecycle contract."
    return result.stdout.strip()


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    cwd = Path.cwd().resolve()
    root = vault_root()
    try:
        root = root.resolve()
    except OSError:
        pass

    output = ""

    project_state = cwd / "PROJECT_STATE.md"
    if project_state.is_file():
        output += section("PROJECT_STATE.md", project_state.read_text(encoding="utf-8"))

    if root.is_dir() and inside(cwd, root):
        output += section("Vault", router_output(root))

    if output:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
