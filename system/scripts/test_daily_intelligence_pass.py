#!/usr/bin/env python3
"""Tests for daily-intelligence-pass.py."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("daily-intelligence-pass.py")


def run(vault: Path, days: int = 7) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--vault", str(vault), "--days", str(days)],
        capture_output=True,
        text=True,
        timeout=15,
    )


def make_daily(vault: Path, date: str, body: str) -> None:
    year = date[:4]
    daily_dir = vault / "calendar" / "daily notes" / year
    daily_dir.mkdir(parents=True, exist_ok=True)
    (daily_dir / f"{date}.md").write_text(textwrap.dedent(body).strip() + "\n")


class DailyIntelligencePassTests(unittest.TestCase):
    def test_silent_when_no_dailies(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = run(Path(tmp))
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout.strip(), "")

    def test_surfaces_carry_forward_decay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-12", "2026-05-13", "2026-05-14"]:
                make_daily(vault, d, """
                ## Carry forward
                - [ ] Reply to Alice about contract
                """)
            result = run(vault)
            self.assertEqual(result.returncode, 0)
            self.assertIn("decay", result.stdout.lower())
            self.assertIn("Alice", result.stdout)
            self.assertIn("seen 3", result.stdout)

    def test_limits_to_recent_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            make_daily(vault, "2026-05-10", "## Carry forward\n- [ ] Old thing")
            make_daily(vault, "2026-05-11", "## Carry forward\n- [ ] Old thing")
            make_daily(vault, "2026-05-12", "## Carry forward\n- [ ] Old thing")
            make_daily(vault, "2026-05-13", "## Carry forward\n- [ ] Different thing")
            result = run(vault, days=2)
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("Old thing", result.stdout)


if __name__ == "__main__":
    unittest.main()
