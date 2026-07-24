#!/usr/bin/env python3
"""Tests for context-router.sh."""
from __future__ import annotations

import os
import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("context-router.sh")
VAULT_ROOT = SCRIPT.parents[2]


def run(profile: str) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["VAULT_CONTEXT_ROOT"] = str(VAULT_ROOT)
    return subprocess.run(
        ["bash", str(SCRIPT), profile],
        cwd=VAULT_ROOT,
        env=env,
        capture_output=True,
        text=True,
        timeout=10,
    )


class ContextRouterTests(unittest.TestCase):
    def test_default_profile_prints_quickstart_and_closeout(self) -> None:
        result = run("default")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Agent Quickstart", result.stdout)
        self.assertIn("Task Profile: default", result.stdout)
        self.assertIn("commit from the vault root", result.stdout)
        self.assertNotIn("Skills Map", result.stdout)

    def test_intake_profile_points_to_intake_skill(self) -> None:
        result = run("intake")
        self.assertEqual(result.returncode, 0)
        self.assertIn("system/skills/intake-extraction.md", result.stdout)
        self.assertIn("+/clippings/", result.stdout)

    def test_unknown_profile_has_fallback(self) -> None:
        result = run("nope")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Unknown profile", result.stdout)


if __name__ == "__main__":
    unittest.main()
