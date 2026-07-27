#!/usr/bin/env python3
"""Tests for sync-check.py.

The interesting cases are the three-way ones. A plain diff can only say "these
differ"; the ledger has to say WHICH SIDE moved, because that is the difference
between "port this outward" and "pull this inward".
"""
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("sync-check.py")


def load_module():
    spec = importlib.util.spec_from_file_location("sync_check", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sc = load_module()

MANIFEST = {
    "layers": {
        "lockstep": {"patterns": ["system/scripts/context-router.py", "system/scripts/tool.py"]},
        "ported": {"patterns": ["system/skills/*.md"]},
        "local": {"patterns": ["atlas/**"]},
    },
    "sterility_denylist": {"patterns": [r"(?i)\bdave\b", r"/Users/[a-z]"]},
}


class Fixture:
    """A pair of vaults on disk."""

    def __init__(self, tmp: str):
        self.public = Path(tmp) / "public"
        self.private = Path(tmp) / "private"
        for root in (self.public, self.private):
            (root / "system" / "scripts").mkdir(parents=True)
            (root / "system" / "skills").mkdir(parents=True)
            (root / "system" / "sync").mkdir(parents=True)

    def write(self, root: Path, rel: str, text: str):
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def both(self, rel: str, public_text: str, private_text: str = None):
        self.write(self.public, rel, public_text)
        self.write(self.private, rel, private_text if private_text is not None else public_text)

    def run(self, state_files: dict = None):
        state = {"this_vault_is": "public", "files": state_files or {}}
        return sc.evaluate(self.public, self.private, MANIFEST, state, "self")

    def status_of(self, rel: str, state_files: dict = None) -> str:
        for status, path, _ in self.run(state_files):
            if path == rel:
                return status
        return "not-evaluated"


class TestLockstep(unittest.TestCase):
    def test_identical_lockstep_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/scripts/tool.py", "print(1)\n")
            self.assertEqual(fx.status_of("system/scripts/tool.py"), sc.STATUS_OK)

    def test_differing_lockstep_is_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/scripts/tool.py", "print(1)\n", "print(2)\n")
            self.assertEqual(
                fx.status_of("system/scripts/tool.py"), sc.STATUS_LOCKSTEP_DRIFT
            )

    def test_excluded_test_files_are_not_lockstep(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/scripts/test_tool.py", "a\n", "b\n")
            self.assertEqual(fx.status_of("system/scripts/test_tool.py"), "not-evaluated")


class TestThreeWayLedger(unittest.TestCase):
    def test_untracked_ported_file_asks_for_reconciliation(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/skills/a.md", "public\n", "private\n")
            self.assertEqual(fx.status_of("system/skills/a.md"), sc.STATUS_UNTRACKED)

    def test_neither_side_moved_is_in_sync(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/skills/a.md", "public\n", "private\n")
            ledger = {
                "system/skills/a.md": {
                    "public": sc.digest(fx.public / "system/skills/a.md"),
                    "private": sc.digest(fx.private / "system/skills/a.md"),
                }
            }
            self.assertEqual(fx.status_of("system/skills/a.md", ledger), sc.STATUS_OK)

    def test_private_change_reports_private_ahead(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/skills/a.md", "shared\n", "shared\n")
            ledger = {
                "system/skills/a.md": {
                    "public": sc.digest(fx.public / "system/skills/a.md"),
                    "private": sc.digest(fx.private / "system/skills/a.md"),
                }
            }
            fx.write(fx.private, "system/skills/a.md", "shared\nnew rule added\n")
            self.assertEqual(
                fx.status_of("system/skills/a.md", ledger), sc.STATUS_PRIVATE_AHEAD
            )

    def test_public_change_reports_public_ahead(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/skills/a.md", "shared\n", "shared\n")
            ledger = {
                "system/skills/a.md": {
                    "public": sc.digest(fx.public / "system/skills/a.md"),
                    "private": sc.digest(fx.private / "system/skills/a.md"),
                }
            }
            fx.write(fx.public, "system/skills/a.md", "shared\nupstream fix\n")
            self.assertEqual(
                fx.status_of("system/skills/a.md", ledger), sc.STATUS_PUBLIC_AHEAD
            )

    def test_both_sides_moving_is_divergence(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/skills/a.md", "shared\n", "shared\n")
            ledger = {
                "system/skills/a.md": {
                    "public": sc.digest(fx.public / "system/skills/a.md"),
                    "private": sc.digest(fx.private / "system/skills/a.md"),
                }
            }
            fx.write(fx.public, "system/skills/a.md", "shared\nA\n")
            fx.write(fx.private, "system/skills/a.md", "shared\nB\n")
            self.assertEqual(
                fx.status_of("system/skills/a.md", ledger), sc.STATUS_DIVERGED
            )

    def test_pinned_file_stops_flagging(self):
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.both("system/skills/a.md", "x\n", "y\n")
            ledger = {"system/skills/a.md": {"pinned": True, "reason": "never matches"}}
            self.assertEqual(fx.status_of("system/skills/a.md", ledger), sc.STATUS_PINNED)

    def test_private_only_ported_file_is_a_candidate_not_an_obligation(self):
        """Plenty of contracts are never meant to go public. Report, don't demand."""
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.write(fx.private, "system/skills/only-private.md", "x\n")
            self.assertEqual(
                fx.status_of("system/skills/only-private.md"), sc.STATUS_PRIVATE_ONLY
            )
            self.assertNotIn(sc.STATUS_PRIVATE_ONLY, sc.ACTIONABLE)

    def test_public_only_ported_file_is_actionable(self):
        """The reverse is a real gap: the vault is missing something upstream has."""
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.write(fx.public, "system/skills/only-public.md", "x\n")
            self.assertEqual(
                fx.status_of("system/skills/only-public.md"), sc.STATUS_MISSING
            )
            self.assertIn(sc.STATUS_MISSING, sc.ACTIONABLE)

    def test_missing_lockstep_file_is_always_actionable(self):
        """Mechanism must exist on both sides, no exceptions."""
        with tempfile.TemporaryDirectory() as tmp:
            fx = Fixture(tmp)
            fx.write(fx.public, "system/scripts/context-router.py", "x\n")
            self.assertEqual(
                fx.status_of("system/scripts/context-router.py"), sc.STATUS_MISSING
            )


class TestFreshCloneIsSafe(unittest.TestCase):
    def test_no_counterpart_configured_exits_zero(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "system" / "sync").mkdir(parents=True)
            (root / "system" / "sync" / "manifest.json").write_text(
                json.dumps(MANIFEST), encoding="utf-8"
            )
            (root / "system" / "sync" / "state.json").write_text(
                json.dumps({"this_vault_is": "public", "counterpart_root": None, "files": {}}),
                encoding="utf-8",
            )
            code = sc.main(["--check", "--root", str(root)])
            self.assertEqual(code, 0)


if __name__ == "__main__":
    unittest.main()
