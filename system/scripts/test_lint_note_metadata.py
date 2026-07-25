#!/usr/bin/env python3
"""Tests for lint-note-metadata.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("lint-note-metadata.py")


def run(target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(target)],
        capture_output=True,
        text=True,
        timeout=10,
    )


def write(vault: Path, name: str, body: str) -> Path:
    path = vault / name
    path.write_text(textwrap.dedent(body).lstrip())
    return path


class LintNoteMetadataTests(unittest.TestCase):
    def test_clean_vault_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(
                vault,
                "clean.md",
                """
                ---
                last_touched: 2026-01-02
                ---
                > **Last touched:** 2026-01-02
                """,
            )
            result = run(vault)
            self.assertEqual(result.returncode, 0)
            self.assertIn("No metadata issues found", result.stdout)

    def test_flags_invalid_last_touched(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(vault, "bad-date.md", "---\nlast_touched: last tuesday\n---\n")
            result = run(vault)
            self.assertEqual(result.returncode, 1)
            self.assertIn("invalid last_touched date", result.stdout)

    def test_flags_visible_date_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(
                vault,
                "mismatch.md",
                """
                ---
                last_touched: 2026-01-02
                ---
                > **Last touched:** 2026-03-04
                """,
            )
            result = run(vault)
            self.assertEqual(result.returncode, 1)
            self.assertIn("last_touched mismatch", result.stdout)

    def test_ignores_dates_inside_fenced_blocks(self) -> None:
        # Templates carry example Memory Cards in fenced blocks; those are not
        # the note's own metadata and must not trip the linter.
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(
                vault,
                "template-ish.md",
                """
                ---
                last_touched: 2026-01-02
                ---
                ```md
                > **Last touched:** 1999-12-31
                ```
                """,
            )
            result = run(vault)
            self.assertEqual(result.returncode, 0)

    def test_placeholder_date_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            write(vault, "template.md", "---\nlast_touched: YYYY-MM-DD\n---\n")
            result = run(vault)
            self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
