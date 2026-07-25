#!/usr/bin/env python3
"""Tests for session-start-context.py."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("session-start-context.py")
VAULT_ROOT = SCRIPT.parents[2]


def run(cwd: Path, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )


class SessionStartContextTests(unittest.TestCase):
    def test_silent_in_empty_dir(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            # Pin the vault root so the temp dir cannot sit inside it by accident.
            result = run(Path(tmp), {"SESSION_CONTEXT_VAULT_ROOT": str(VAULT_ROOT)})
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")

    def test_prints_project_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "PROJECT_STATE.md").write_text("# Example Project\n\nCurrent: M2 polish.\n")
            result = run(Path(tmp), {"SESSION_CONTEXT_VAULT_ROOT": str(VAULT_ROOT)})
            self.assertEqual(result.returncode, 0)
            self.assertIn("PROJECT_STATE.md", result.stdout)
            self.assertIn("Example Project", result.stdout)
            self.assertIn("Current: M2 polish", result.stdout)

    def test_prints_vault_context_when_inside_vault(self) -> None:
        # The script defaults its vault root to the vault it lives in, so a
        # fresh clone works with no configuration.
        result = run(VAULT_ROOT)
        self.assertEqual(result.returncode, 0)
        self.assertIn("vault", result.stdout.lower())
        self.assertIn("AGENTS.md", result.stdout)

    def test_missing_vault_root_is_silent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(
                Path(tmp),
                {"SESSION_CONTEXT_VAULT_ROOT": str(Path(tmp) / "does-not-exist")},
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
