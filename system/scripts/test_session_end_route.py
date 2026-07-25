#!/usr/bin/env python3
"""Tests for session-end-route.py."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("session-end-route.py")


def run(env_extra: dict[str, object] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if env_extra:
        env.update({k: str(v) for k, v in env_extra.items()})
    return subprocess.run(
        [sys.executable, str(SCRIPT)],
        env=env,
        capture_output=True,
        text=True,
        timeout=5,
    )


class SessionEndRouteTests(unittest.TestCase):
    def setUp(self) -> None:
        # The script's re-entry guard writes a sentinel under $HOME/.claude and
        # then stays silent for 10 minutes. Give every test its own HOME so one
        # firing test cannot silence the next one -- or touch the real user's
        # sentinel.
        home = tempfile.TemporaryDirectory()
        self.addCleanup(home.cleanup)
        self.home = home.name

    def run_script(self, env_extra: dict[str, object] | None = None):
        env: dict[str, object] = {"HOME": self.home}
        if env_extra:
            env.update(env_extra)
        return run(env)

    def test_silent_below_threshold(self) -> None:
        result = self.run_script({"SESSION_EDIT_COUNT": 1, "SESSION_DURATION_SEC": 60})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_prompts_above_edit_threshold(self) -> None:
        result = self.run_script({"SESSION_EDIT_COUNT": 15, "SESSION_DURATION_SEC": 60})
        self.assertEqual(result.returncode, 0)
        self.assertIn("cross-project", result.stdout.lower())
        self.assertIn("project_state", result.stdout.lower())
        self.assertIn("vault", result.stdout.lower())

    def test_prompts_above_duration_threshold(self) -> None:
        result = self.run_script({"SESSION_EDIT_COUNT": 1, "SESSION_DURATION_SEC": 2000})
        self.assertEqual(result.returncode, 0)
        self.assertIn("cross-project", result.stdout.lower())

    def test_custom_threshold(self) -> None:
        result = self.run_script(
            {
                "SESSION_EDIT_COUNT": 5,
                "SESSION_DURATION_SEC": 60,
                "SESSION_ROUTE_THRESHOLD_EDITS": 3,
            }
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("cross-project", result.stdout.lower())

    def test_kill_switch_is_silent(self) -> None:
        result = self.run_script(
            {
                "SESSION_ROUTE_DISABLE": 1,
                "SESSION_EDIT_COUNT": 15,
                "SESSION_DURATION_SEC": 2000,
            }
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_invalid_numbers_default_to_zero(self) -> None:
        result = self.run_script({"SESSION_EDIT_COUNT": "abc", "SESSION_DURATION_SEC": "nope"})
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_stop_hook_active_is_silent(self) -> None:
        result = self.run_script(
            {
                "STOP_HOOK_ACTIVE": "true",
                "SESSION_EDIT_COUNT": 15,
                "SESSION_DURATION_SEC": 2000,
            }
        )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "")

    def test_reentry_guard_blocks_only_once(self) -> None:
        first = self.run_script({"SESSION_EDIT_COUNT": 15, "SESSION_DURATION_SEC": 60})
        self.assertIn("cross-project", first.stdout.lower())
        second = self.run_script({"SESSION_EDIT_COUNT": 15, "SESSION_DURATION_SEC": 60})
        self.assertEqual(second.stdout.strip(), "")


if __name__ == "__main__":
    unittest.main()
