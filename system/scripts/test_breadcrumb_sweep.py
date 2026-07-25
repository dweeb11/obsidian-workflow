#!/usr/bin/env python3
"""Tests for breadcrumb-sweep.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("breadcrumb-sweep.py")


def run(index_path: Path, vault: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--index", str(index_path), "--vault", str(vault)],
        capture_output=True,
        text=True,
        timeout=10,
    )


class BreadcrumbSweepTests(unittest.TestCase):
    def test_flags_missing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "real-note.md").write_text("# Real\n")
            index = vault / "_index.md"
            index.write_text("- [[real-note]]\n- [[ghost-note]]\n")
            result = run(index, vault)
            self.assertEqual(result.returncode, 0)
            self.assertIn("ghost-note", result.stdout)
            self.assertNotIn("real-note —", result.stdout)

    def test_resolves_aliases_anchors_and_folder_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            nested = vault / "atlas" / "topic"
            nested.mkdir(parents=True)
            (nested / "Real Note.md").write_text("# Real\n")
            index = vault / "_index.md"
            index.write_text("- [[atlas/topic/Real Note#Section|display]]\n")
            result = run(index, vault)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")

    def test_resolves_pipe_escaped_alias_in_a_table(self) -> None:
        # Inside a Markdown table the alias pipe must be written `\|`, or the
        # table splits on it. The backslash is not part of the target.
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "real-note.md").write_text("# Real\n")
            index = vault / "_index.md"
            index.write_text("| Task | Doc |\n|---|---|\n| Thing | [[real-note\\|Real Note]] |\n")
            result = run(index, vault)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")

    def test_silent_when_clean(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            (vault / "real-note.md").write_text("# Real\n")
            index = vault / "_index.md"
            index.write_text("- [[real-note]]\n")
            result = run(index, vault)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
