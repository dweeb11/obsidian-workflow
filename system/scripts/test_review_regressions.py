#!/usr/bin/env python3
"""Regressions for the defects found in PR #14 review.

Each test names the failure it locks down. Several of these were shipped as
"verified green" before review, so they are worth keeping explicit.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, HERE / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gen = load("gen_rr", "generate-adapters.py")
sc = load("sc_rr", "sync-check.py")


def registry_fixture(tmp: Path) -> Path:
    (tmp / "system" / "skills").mkdir(parents=True)
    (tmp / "system" / "skills" / "a.md").write_text("c\n", encoding="utf-8")
    (tmp / "system" / "skills" / "registry.json").write_text(
        json.dumps(
            {"entries": [{"slug": "a", "title": "A", "description": "d", "contract": "system/skills/a.md"}]}
        ),
        encoding="utf-8",
    )
    return tmp


class TestCheckIsUsableFromAHook(unittest.TestCase):
    """--check printed on success, so a SessionStart hook would nag every session.

    sync-check.py already had --quiet-when-clean; this is the sibling flag, and
    the hook in .claude/settings.json depends on it staying silent when clean
    and loud when not.
    """

    def test_quiet_when_clean_prints_nothing_and_exits_zero(self):
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            gen.main(["--root", str(root)])
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = gen.main(["--root", str(root), "--check", "--quiet-when-clean"])
            self.assertEqual(code, 0)
            self.assertEqual(buf.getvalue().strip(), "")

    def test_quiet_when_clean_still_reports_drift(self):
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            gen.main(["--root", str(root)])
            orphan = root / ".claude" / "skills" / "gone"
            orphan.mkdir(parents=True)
            (orphan / "SKILL.md").write_text(gen.GENERATED_MARKER + "\n", encoding="utf-8")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = gen.main(["--root", str(root), "--check", "--quiet-when-clean"])
            self.assertEqual(code, 1)
            self.assertIn("ORPHANED", buf.getvalue())


class TestPruneReclaimsTheSkillDirectory(unittest.TestCase):
    """--prune unlinked SKILL.md but left an empty <slug>/ behind.

    An empty directory still reads as a skill folder to anyone browsing
    .claude/skills, and --check went green on it because it globs */SKILL.md.
    Found while cleaning up an orphan the unslop removal left on 2026-08-22.
    """

    def test_prune_removes_the_emptied_slug_directory(self):
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            gen.main(["--root", str(root)])

            orphan = root / ".claude" / "skills" / "gone"
            orphan.mkdir(parents=True)
            (orphan / "SKILL.md").write_text(
                "---\nname: gone\n---\n" + gen.GENERATED_MARKER + "\n", encoding="utf-8"
            )

            gen.main(["--root", str(root), "--prune"])

            self.assertFalse((orphan / "SKILL.md").exists(), "orphan file survived --prune")
            self.assertFalse(orphan.exists(), "--prune left an empty slug directory behind")

    def test_prune_keeps_the_tool_base_directory(self):
        """Reclaiming the slug dir must never walk up into .claude/skills itself."""
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            gen.main(["--root", str(root)])

            rules = root / ".cursor" / "rules"
            stray = rules / "gone.mdc"
            stray.write_text(gen.GENERATED_MARKER + "\n", encoding="utf-8")

            gen.main(["--root", str(root), "--prune"])

            self.assertFalse(stray.exists())
            self.assertTrue(rules.is_dir(), "--prune removed a tool's base directory")


class TestPartialEmitterDoesNotDelete(unittest.TestCase):
    """`--emitter claude` deleted every committed .cursor rule."""

    def test_single_emitter_leaves_other_emitters_alone(self):
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            gen.main(["--root", str(root)])
            cursor = root / ".cursor" / "rules" / "a.mdc"
            self.assertTrue(cursor.exists())
            gen.main(["--root", str(root), "--emitter", "claude", "--prune"])
            self.assertTrue(cursor.exists(), "--emitter claude deleted another emitter's output")

    def test_orphans_are_computed_against_the_full_build(self):
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            entries = gen.load_registry(root)
            gen.main(["--root", str(root)])
            partial = gen.build(entries, root, "claude")
            full = gen.build(entries, root)
            _, orphaned = gen.diff_against_disk(partial, root, orphan_reference=full)
            self.assertEqual(orphaned, [])


class TestPruningIsOptIn(unittest.TestCase):
    """Deletion has twice removed files it should not have. It is now opt-in."""

    def _stale_adapter(self, root: Path) -> Path:
        stale = root / ".claude" / "skills" / "gone" / "SKILL.md"
        stale.parent.mkdir(parents=True, exist_ok=True)
        stale.write_text("<!--\n%s\n-->\n" % gen.GENERATED_BANNER, encoding="utf-8")
        return stale

    def test_default_run_does_not_delete(self):
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            stale = self._stale_adapter(root)
            gen.main(["--root", str(root)])
            self.assertTrue(stale.exists(), "a default run deleted an adapter")

    def test_prune_flag_does_delete(self):
        with tempfile.TemporaryDirectory() as t:
            root = registry_fixture(Path(t))
            stale = self._stale_adapter(root)
            gen.main(["--root", str(root), "--prune"])
            self.assertFalse(stale.exists(), "--prune failed to remove a stale adapter")


class TestFrontmatterIsValidYaml(unittest.TestCase):
    """A description containing ': ' produced unparseable frontmatter."""

    def test_colon_in_description_is_quoted(self):
        body = gen.emit_claude(
            [{"slug": "x", "title": "X", "description": "changes: folder conventions", "contract": "system/skills/a.md"}]
        )[".claude/skills/x/SKILL.md"]
        line = [l for l in body.splitlines() if l.startswith("description:")][0]
        self.assertTrue(line.endswith('"'), line)
        self.assertIn('"changes: folder conventions"', line)

    def test_quotes_and_backslashes_are_escaped(self):
        out = gen.yaml_scalar('he said "hi" \\ there')
        self.assertEqual(out, '"he said \\"hi\\" \\\\ there"')


class TestTablePipesAreEscaped(unittest.TestCase):
    """Unescaped wikilink aliases broke the generated Markdown table."""

    def test_wikilink_alias_pipe_is_escaped(self):
        table = gen._registry_table(
            [{"slug": "a", "title": "A", "description": "d", "contract": "system/skills/a.md", "triggers": []}]
        )
        self.assertIn("\\|", table)
        for row in [r for r in table.splitlines() if r.startswith("| A ")]:
            self.assertEqual(row.count("|") - row.count("\\|"), 5, row)


class TestPinScoping(unittest.TestCase):
    """A pin must never silence a lockstep invariant."""

    MANIFEST = {
        "layers": {
            "lockstep": {"patterns": ["system/scripts/tool.py"]},
            "ported": {"patterns": ["system/skills/*.md"]},
        }
    }

    def test_pinned_lockstep_file_still_reports_drift(self):
        with tempfile.TemporaryDirectory() as t:
            pub, priv = Path(t) / "pub", Path(t) / "priv"
            for r in (pub, priv):
                (r / "system" / "scripts").mkdir(parents=True)
            (pub / "system/scripts/tool.py").write_text("a\n", encoding="utf-8")
            (priv / "system/scripts/tool.py").write_text("b\n", encoding="utf-8")
            state = {"this_vault_is": "public", "files": {"system/scripts/tool.py": {"pinned": True, "reason": "nope"}}}
            results = sc.evaluate(pub, priv, self.MANIFEST, state, "self")
            status = [s for s, p, _ in results if p == "system/scripts/tool.py"][0]
            self.assertEqual(status, sc.STATUS_LOCKSTEP_DRIFT)

    def test_cli_refuses_to_pin_a_lockstep_path(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "system" / "sync").mkdir(parents=True)
            (root / "system/sync/manifest.json").write_text(json.dumps(self.MANIFEST), encoding="utf-8")
            (root / "system/sync/state.json").write_text(
                json.dumps({"this_vault_is": "public", "counterpart_root": None, "files": {}}), encoding="utf-8"
            )
            code = sc.main(["--pin", "system/scripts/tool.py", "--reason", "x", "--root", str(root)])
            self.assertEqual(code, 2)

    def test_pin_works_without_a_counterpart(self):
        """--pin only writes local state; requiring a counterpart made it unreachable."""
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "system" / "sync").mkdir(parents=True)
            (root / "system/sync/manifest.json").write_text(json.dumps(self.MANIFEST), encoding="utf-8")
            (root / "system/sync/state.json").write_text(
                json.dumps({"this_vault_is": "public", "counterpart_root": None, "files": {}}), encoding="utf-8"
            )
            code = sc.main(
                ["--pin", "system/skills/a.md", "--reason", "intentional", "--root", str(root)]
            )
            self.assertEqual(code, 0)
            saved = json.loads((root / "system/sync/state.json").read_text())
            self.assertTrue(saved["files"]["system/skills/a.md"]["pinned"])


class TestCounterpartMisconfiguration(unittest.TestCase):
    """A typo'd counterpart path silently disabled all drift checking."""

    def test_bad_configured_path_raises(self):
        with self.assertRaises(sc.CounterpartMisconfigured):
            sc.resolve_counterpart({"counterpart_root": "/definitely/not/here"})

    def test_unset_still_returns_none(self):
        self.assertIsNone(sc.resolve_counterpart({"counterpart_root": None}))

    def test_cli_fails_loudly_even_when_quiet(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "system" / "sync").mkdir(parents=True)
            (root / "system/sync/manifest.json").write_text(json.dumps({"layers": {}}), encoding="utf-8")
            (root / "system/sync/state.json").write_text(
                json.dumps({"this_vault_is": "public", "counterpart_root": "/nope/nope", "files": {}}), encoding="utf-8"
            )
            code = sc.main(["--check", "--quiet-when-clean", "--root", str(root)])
            self.assertEqual(code, 2, "a broken counterpart path exited 0 under --quiet-when-clean")


class TestPullPopulatesMissingLockstep(unittest.TestCase):
    """--pull was a no-op in the initial-port case it was documented for."""

    def test_missing_private_lockstep_file_is_copied(self):
        with tempfile.TemporaryDirectory() as t:
            pub, priv = Path(t) / "pub", Path(t) / "priv"
            for r in (pub, priv):
                (r / "system" / "scripts").mkdir(parents=True)
                (r / "system" / "sync").mkdir(parents=True)
            (pub / "system/scripts/tool.py").write_text("new mechanism\n", encoding="utf-8")
            manifest = {"layers": {"lockstep": {"patterns": ["system/scripts/tool.py"]}, "ported": {"patterns": []}}}
            (pub / "system/sync/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (pub / "system/sync/state.json").write_text(
                json.dumps({"this_vault_is": "public", "counterpart_root": str(priv), "files": {}}), encoding="utf-8"
            )
            target = priv / "system/scripts/tool.py"
            self.assertFalse(target.exists())
            sc.main(["--pull", "--root", str(pub)])
            self.assertTrue(target.exists(), "--pull did not populate a missing lockstep file")
            self.assertEqual(target.read_text(), "new mechanism\n")


class TestPrivateOnlyIsReported(unittest.TestCase):
    """Publication candidates were computed and then filtered out of the report."""

    def test_private_only_row_appears_in_output(self):
        with tempfile.TemporaryDirectory() as t:
            pub, priv = Path(t) / "pub", Path(t) / "priv"
            for r in (pub, priv):
                (r / "system" / "skills").mkdir(parents=True)
                (r / "system" / "sync").mkdir(parents=True)
            (priv / "system/skills/only.md").write_text("x\n", encoding="utf-8")
            manifest = {"layers": {"lockstep": {"patterns": []}, "ported": {"patterns": ["system/skills/*.md"]}}}
            (pub / "system/sync/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            (pub / "system/sync/state.json").write_text(
                json.dumps({"this_vault_is": "public", "counterpart_root": str(priv), "files": {}}), encoding="utf-8"
            )
            out = subprocess.run(
                [sys.executable, str(HERE / "sync-check.py"), "--check", "--root", str(pub)],
                capture_output=True, text=True, timeout=30,
            )
            self.assertIn("private-only", out.stdout)
            self.assertIn("only.md", out.stdout)


class TestStopHookReadsSessionMetrics(unittest.TestCase):
    """The Stop hook never fired: metrics arrive on stdin, not in the env."""

    def _run(self, payload: dict, home: str):
        env = os.environ.copy()
        env["HOME"] = home
        env.pop("SESSION_EDIT_COUNT", None)
        env.pop("SESSION_DURATION_SEC", None)
        env.pop("STOP_HOOK_ACTIVE", None)
        return subprocess.run(
            [sys.executable, str(HERE / "session-end-route.py"), "--from-hook"],
            input=json.dumps(payload), capture_output=True, text=True, env=env, timeout=30,
        )

    def test_above_threshold_blocks_from_stdin_alone(self):
        with tempfile.TemporaryDirectory() as home:
            out = self._run({"cumulative_tool_use_count": 50, "duration_ms": 2_400_000}, home)
            self.assertIn('"decision": "block"', out.stdout)

    def test_below_threshold_stays_silent(self):
        with tempfile.TemporaryDirectory() as home:
            out = self._run({"cumulative_tool_use_count": 1, "duration_ms": 1000}, home)
            self.assertEqual(out.stdout.strip(), "")

    def test_continuation_turn_does_not_block_again(self):
        with tempfile.TemporaryDirectory() as home:
            out = self._run({"cumulative_tool_use_count": 99, "stop_hook_active": True}, home)
            self.assertEqual(out.stdout.strip(), "")

    def test_env_vars_still_win_for_existing_wrappers(self):
        with tempfile.TemporaryDirectory() as home:
            env = os.environ.copy()
            env.update({"HOME": home, "SESSION_EDIT_COUNT": "99", "SESSION_DURATION_SEC": "0"})
            out = subprocess.run(
                [sys.executable, str(HERE / "session-end-route.py")],
                input="", capture_output=True, text=True, env=env, timeout=30,
            )
            self.assertIn('"decision": "block"', out.stdout)


if __name__ == "__main__":
    unittest.main()


class TestHooksAreInterpreterAgnostic(unittest.TestCase):
    """Hooks hard-coded `python3`, which the Windows python.org installer
    does not provide. Scripts are invoked directly instead: the shebang picks
    the interpreter on Unix, the .py file association does it on Windows."""

    def _settings(self) -> dict:
        return json.loads((ROOT / ".claude" / "settings.json").read_text(encoding="utf-8"))

    def _commands(self):
        out = []
        for event in self._settings()["hooks"].values():
            for group in event:
                for hook in group.get("hooks", []):
                    out.append(hook["command"])
        return out

    def test_no_hook_hardcodes_an_interpreter(self):
        for cmd in self._commands():
            self.assertNotIn("python3", cmd, cmd)
            self.assertNotRegex(cmd, r"(^|\s)python(\s|\")", cmd)

    def test_every_hook_script_is_executable_and_has_a_shebang(self):
        for cmd in self._commands():
            rel = cmd.split('"')[1].replace("$CLAUDE_PROJECT_DIR/", "")
            path = ROOT / rel
            self.assertTrue(path.exists(), rel)
            self.assertTrue(
                path.read_text(encoding="utf-8").startswith("#!"),
                "%s needs a shebang to run without an interpreter prefix" % rel,
            )
            self.assertTrue(os.access(path, os.X_OK), "%s is not executable" % rel)

    def test_exec_bit_is_recorded_in_git(self):
        """A clone must get the exec bit, or Unix invocation breaks."""
        for cmd in self._commands():
            rel = cmd.split('"')[1].replace("$CLAUDE_PROJECT_DIR/", "")
            out = subprocess.run(
                ["git", "ls-files", "-s", rel], cwd=ROOT,
                capture_output=True, text=True, timeout=30,
            )
            if not out.stdout.strip():
                continue
            self.assertTrue(
                out.stdout.startswith("100755"),
                "%s is not mode 100755 in git: %s" % (rel, out.stdout.strip()),
            )


class TestModeDriftIsDetected(unittest.TestCase):
    """Hooks invoke scripts directly, so the exec bit is part of the lockstep
    contract. Hashing content alone declared two copies identical while one of
    them could not actually run."""

    MANIFEST = {"layers": {"lockstep": {"patterns": ["system/scripts/tool.py"]}, "ported": {"patterns": []}}}

    def _pair(self, tmp, pub_exec: bool, priv_exec: bool):
        pub, priv = Path(tmp) / "pub", Path(tmp) / "priv"
        for r in (pub, priv):
            (r / "system" / "scripts").mkdir(parents=True)
            (r / "system/scripts/tool.py").write_text("#!/usr/bin/env python3\n", encoding="utf-8")
        (pub / "system/scripts/tool.py").chmod(0o755 if pub_exec else 0o644)
        (priv / "system/scripts/tool.py").chmod(0o755 if priv_exec else 0o644)
        state = {"this_vault_is": "public", "files": {}}
        results = sc.evaluate(pub, priv, self.MANIFEST, state, "self")
        return [s for s, p, _ in results if p == "system/scripts/tool.py"][0]

    def test_same_content_different_exec_bit_is_flagged(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._pair(tmp, True, False), sc.STATUS_MODE_DRIFT)

    def test_matching_exec_bits_are_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._pair(tmp, True, True), sc.STATUS_OK)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._pair(tmp, False, False), sc.STATUS_OK)

    def test_mode_drift_is_actionable(self):
        self.assertIn(sc.STATUS_MODE_DRIFT, sc.ACTIONABLE)
