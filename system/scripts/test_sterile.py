#!/usr/bin/env python3
"""Guard the public template against a careless port from the private vault.

The two vaults share a mechanism layer, so files move between them by hand. The
failure mode is obvious and one commit away: someone ports a skill contract and
brings real names, hostnames, or home paths with it. Discipline does not catch
that reliably. This does.

The denylist lives in system/sync/manifest.json so sync-check.py can reuse it to
decide whether a diff hunk is sanitization (expected) or a portable improvement
(flag it).
"""
from __future__ import annotations

import json
import re
import subprocess
import unittest
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST = VAULT_ROOT / "system" / "sync" / "manifest.json"

# Scanned as text. Everything else (images, binaries) is skipped.
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".mdc", ".sh", ".txt"}

# Only the manifest is exempt, because it necessarily holds the denylist
# patterns themselves. Everything else is scanned.
#
# sync-check.py used to be exempt, dating from a sanitization-classifier that
# was removed. It loads the patterns dynamically and contains none of them, so
# the exemption bought nothing and left the single highest-risk file -- the one
# that moves content between vaults -- unscanned.
SELF_EXEMPT = {
    "system/sync/manifest.json",
}


def tracked_files() -> list:
    """Only git-tracked files. Untracked scratch is not our problem."""
    out = subprocess.run(
        ["git", "ls-files"],
        cwd=VAULT_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )
    if out.returncode != 0:
        return []
    return [line for line in out.stdout.splitlines() if line.strip()]


class TestPublicRepoIsSterile(unittest.TestCase):
    def setUp(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        patterns = manifest["sterility_denylist"]["patterns"]
        self.rules = [(p, re.compile(p)) for p in patterns]

    def test_no_denylisted_tokens_in_tracked_files(self):
        violations = []
        for rel in tracked_files():
            if rel in SELF_EXEMPT:
                continue
            path = VAULT_ROOT / rel
            if path.suffix.lower() not in TEXT_SUFFIXES or not path.exists():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            for lineno, line in enumerate(text.splitlines(), start=1):
                for pattern, rx in self.rules:
                    if rx.search(line):
                        violations.append(
                            "%s:%d matches %r -> %s" % (rel, lineno, pattern, line.strip()[:90])
                        )
        self.assertEqual(
            violations,
            [],
            "private content leaked into the public template:\n  " + "\n  ".join(violations),
        )

    def test_denylist_is_not_empty(self):
        """A silently emptied denylist would make this suite pass vacuously."""
        self.assertGreaterEqual(len(self.rules), 5)

    def test_denylist_patterns_compile(self):
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for pattern in manifest["sterility_denylist"]["patterns"]:
            re.compile(pattern)


if __name__ == "__main__":
    unittest.main()
