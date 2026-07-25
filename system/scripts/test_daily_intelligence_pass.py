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
TEMPLATE = SCRIPT.parent.parent / "Templates" / "Daily Note.md"

# The routing appendix a closed day carries, per system/skills/daily-capture.md.
CLOSED = """
## ToDo
- [ ] Something only today asked for

---

## Daily Cleanup Routing

### Carry Forward / Open Loops
{loops}

### Created / Updated Vault Notes
- [ ] Not a carried item

### Needs Review
"""


def run(vault: Path, days: int = 7) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--vault", str(vault), "--days", str(days)],
        capture_output=True,
        text=True,
        timeout=15,
    )


def make_daily(vault: Path, date: str, body: str) -> None:
    """Write an archived (closed) daily note."""
    year = date[:4]
    daily_dir = vault / "calendar" / "daily notes" / year
    daily_dir.mkdir(parents=True, exist_ok=True)
    (daily_dir / f"{date}.md").write_text(textwrap.dedent(body).strip() + "\n")


def make_root_daily(vault: Path, date: str, body: str) -> None:
    """Write an active root daily note — a day that was set up but never closed."""
    (vault / f"{date}.md").write_text(textwrap.dedent(body).strip() + "\n")


def make_closed(vault: Path, date: str, loops: str) -> None:
    make_daily(vault, date, CLOSED.format(loops=textwrap.dedent(loops).strip()))


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
                make_closed(vault, d, "- [ ] Reply to Alice about contract")
            result = run(vault)
            self.assertEqual(result.returncode, 0)
            self.assertIn("decay", result.stdout.lower())
            self.assertIn("Alice", result.stdout)
            self.assertIn("seen 3", result.stdout)

    def test_counts_plain_bullets_in_open_loops(self) -> None:
        """Idea seeds are written there without a checkbox and still count."""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-12", "2026-05-13", "2026-05-14"]:
                make_closed(vault, d, "- Idea seed: two-phase renovation")
            result = run(vault)
            self.assertIn("Idea seed: two-phase renovation", result.stdout)
            self.assertIn("seen 3", result.stdout)

    def test_checkbox_and_plain_renderings_are_the_same_item(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            make_closed(vault, "2026-05-12", "- [ ] Call the building manager")
            make_closed(vault, "2026-05-13", "- Call the building manager")
            make_closed(vault, "2026-05-14", "- [ ] Call the building manager")
            result = run(vault)
            self.assertIn("seen 3", result.stdout)

    def test_closed_day_never_falls_back_to_its_raw_todo(self) -> None:
        """The raw note preserved above the appendix must not be counted twice."""
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-12", "2026-05-13", "2026-05-14"]:
                make_daily(vault, d, """
                ## ToDo
                - [ ] Something only today asked for

                ---

                ## Daily Cleanup Routing

                ### Carry Forward / Open Loops

                ### Needs Review
                """)
            result = run(vault)
            self.assertEqual(result.stdout.strip(), "")

    def test_open_loops_scoping_stops_at_the_next_h3(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-12", "2026-05-13", "2026-05-14"]:
                make_closed(vault, d, "- [ ] Carried")
            result = run(vault)
            self.assertIn("Carried", result.stdout)
            self.assertNotIn("Not a carried item", result.stdout)

    def test_unclosed_days_fall_back_to_todo(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-12", "2026-05-13", "2026-05-14"]:
                make_root_daily(vault, d, """
                ## ToDo
                - [ ] Call the building manager about the water shutoff

                ## Random Thoughts
                - [ ] Not a task surface
                """)
            result = run(vault)
            self.assertIn("Call the building manager", result.stdout)
            self.assertIn("seen 3", result.stdout)
            self.assertNotIn("Not a task surface", result.stdout)

    def test_todo_fallback_ignores_plain_bullets(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-12", "2026-05-13", "2026-05-14"]:
                make_root_daily(vault, d, """
                ## ToDo
                - Prose, not an obligation
                """)
            result = run(vault)
            self.assertEqual(result.stdout.strip(), "")

    def test_fires_on_notes_built_from_the_shipped_template(self) -> None:
        """The evidence the whole reconciliation exists to produce."""
        template = TEMPLATE.read_text(encoding="utf-8")
        self.assertIn("## ToDo", template)
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-12", "2026-05-13", "2026-05-14"]:
                note = template.replace("# YYYY-MM-DD", f"# {d}").replace(
                    "## ToDo",
                    "## ToDo\n- [ ] Call the building manager about the water shutoff",
                )
                make_root_daily(vault, d, note)
            result = run(vault)
            self.assertEqual(result.returncode, 0)
            self.assertIn("Call the building manager", result.stdout)
            self.assertIn("seen 3", result.stdout)

    def test_limits_to_recent_window(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp)
            for d in ["2026-05-10", "2026-05-11", "2026-05-12"]:
                make_closed(vault, d, "- [ ] Old thing")
            make_closed(vault, "2026-05-13", "- [ ] Different thing")
            result = run(vault, days=2)
            self.assertEqual(result.returncode, 0)
            self.assertNotIn("Old thing", result.stdout)


if __name__ == "__main__":
    unittest.main()
