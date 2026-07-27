#!/usr/bin/env python3
"""Tests for generate-adapters.py.

The load-bearing test here is test_committed_adapters_are_current: it is what
structurally prevents this vault from drifting into a Claude-first vault. If
someone hand-edits a SKILL.md to add a workflow step, the committed file stops
matching what the registry generates and CI fails. Logic therefore cannot
accumulate in a tool directory -- it has to go back into the contract, where
every agent can see it.
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("generate-adapters.py")
VAULT_ROOT = SCRIPT.parents[2]


def load_module():
    spec = importlib.util.spec_from_file_location("generate_adapters", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gen = load_module()


class TestRegistry(unittest.TestCase):
    def test_registry_loads_and_validates(self):
        entries = gen.load_registry(VAULT_ROOT)
        self.assertTrue(entries)

    def test_every_contract_file_exists(self):
        for entry in gen.load_registry(VAULT_ROOT):
            self.assertTrue(
                (VAULT_ROOT / entry["contract"]).exists(),
                "%s points at a missing contract" % entry["slug"],
            )

    def test_slugs_are_unique_and_filesystem_safe(self):
        slugs = [e["slug"] for e in gen.load_registry(VAULT_ROOT)]
        self.assertEqual(len(slugs), len(set(slugs)))
        for slug in slugs:
            self.assertRegex(slug, r"^[a-z0-9][a-z0-9-]*$")

    def test_missing_contract_is_rejected(self):
        import json
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "system" / "skills").mkdir(parents=True)
            (root / "system" / "skills" / "registry.json").write_text(
                json.dumps(
                    {
                        "entries": [
                            {
                                "slug": "ghost",
                                "title": "Ghost",
                                "description": "d",
                                "contract": "system/skills/nope.md",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(gen.RegistryError):
                gen.load_registry(root)


class TestAdaptersStayInert(unittest.TestCase):
    def test_committed_adapters_are_current(self):
        """Regenerate everything and diff against what is committed."""
        entries = gen.load_registry(VAULT_ROOT)
        files = gen.build(entries, VAULT_ROOT)
        stale, orphaned = gen.diff_against_disk(files, VAULT_ROOT)
        self.assertEqual(
            (stale, orphaned),
            ([], []),
            "adapters are out of date -- run: python3 system/scripts/generate-adapters.py",
        )

    def test_every_entry_emits_a_claude_and_cursor_adapter(self):
        entries = gen.load_registry(VAULT_ROOT)
        files = gen.build(entries, VAULT_ROOT)
        for entry in entries:
            self.assertIn(".claude/skills/%s/SKILL.md" % entry["slug"], files)
            self.assertIn(".cursor/rules/%s.mdc" % entry["slug"], files)

    def test_adapters_are_short(self):
        """An adapter that grows is an adapter that has started holding logic."""
        entries = gen.load_registry(VAULT_ROOT)
        files = gen.build(entries, VAULT_ROOT)
        for rel, contents in files.items():
            if rel.endswith((".md", ".mdc")) and rel.startswith((".claude", ".cursor")):
                self.assertLess(
                    len(contents.splitlines()), 40, "%s is too long to be a pointer" % rel
                )

    def test_adapters_name_their_contract(self):
        entries = gen.load_registry(VAULT_ROOT)
        files = gen.build(entries, VAULT_ROOT)
        for entry in entries:
            for rel in (
                ".claude/skills/%s/SKILL.md" % entry["slug"],
                ".cursor/rules/%s.mdc" % entry["slug"],
            ):
                self.assertIn(entry["contract"], files[rel])


class TestRoutingChainStaysSufficient(unittest.TestCase):
    """An agent with no adapter must lose nothing but a shortcut."""

    def test_every_entry_is_reachable_from_the_generated_index(self):
        entries = gen.load_registry(VAULT_ROOT)
        skills_map = (VAULT_ROOT / "Skills-Map.md").read_text(encoding="utf-8")
        self.assertIn(gen.BEGIN_MARKER, skills_map)
        for entry in entries:
            stem = Path(entry["contract"]).stem
            self.assertIn(stem, skills_map, "%s missing from Skills-Map" % entry["slug"])

    def test_agents_md_still_points_at_the_contract_directory(self):
        agents = (VAULT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("system/skills/", agents)
        self.assertIn("Skills-Map", agents)


if __name__ == "__main__":
    unittest.main()
