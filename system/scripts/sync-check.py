#!/usr/bin/env python3
"""Detect QoL/process improvements that have not crossed between paired vaults.

Two vaults share this system: a private one (real notes) and a public template
one (sterile). They deliberately hold DIFFERENT content -- the public copy is
sanitized -- so a plain diff flags everything forever and gets ignored. This
script separates the two failure modes:

  lockstep files  must be byte-identical. Any difference is actionable, full stop.

  ported files    are EXPECTED to differ. A raw diff is useless, so the missing
                  common ancestor is synthesized: system/sync/state.json records
                  the hash of BOTH sides at last reconciliation. Compare each
                  side against its recorded hash and the direction of an
                  unported change falls out:

                      private moved, public didn't  -> private has an improvement
                      public moved, private didn't  -> public has an improvement
                      both moved                    -> divergent, merge by hand
                      neither moved                 -> in sync

No attempt is made to auto-classify a diff as "just sanitization". Matching a
real name against its sanitized replacement is not decidable by regex -- the
replacement vocabulary is open-ended -- and the failure mode would be silently
suppressing a genuine improvement, which is the one thing this script exists to
prevent. The ledger already makes noise self-limiting: reconcile once with
--accept and the file stays quiet until something actually moves. Files that will
never match get pinned with a reason.

Usage:
    sync-check.py --check                    # report; exit 1 if action needed
    sync-check.py --check --quiet-when-clean # for hooks: silent when in sync
    sync-check.py --pull                     # copy lockstep files public->private
    sync-check.py --accept <path>            # record current pair as reconciled
    sync-check.py --pin <path> --reason "…"  # stop flagging an intentional split

The counterpart vault is found via $VAULT_COUNTERPART_ROOT, or the
"counterpart_root" key in system/sync/state.json. With neither set the script
exits 0 and says so: a fresh clone has no counterpart and must not fail CI.
"""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VAULT_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = VAULT_ROOT / "system" / "sync" / "manifest.json"
STATE_PATH = VAULT_ROOT / "system" / "sync" / "state.json"

STATUS_OK = "in-sync"
STATUS_PRIVATE_AHEAD = "private-ahead"
STATUS_PUBLIC_AHEAD = "public-ahead"
STATUS_DIVERGED = "diverged"
STATUS_LOCKSTEP_DRIFT = "lockstep-drift"
STATUS_MISSING = "missing"
STATUS_PINNED = "pinned"
STATUS_UNTRACKED = "untracked"
STATUS_PRIVATE_ONLY = "private-only"

# A ported file that exists only in the private vault is a publication CANDIDATE,
# not an obligation -- plenty of contracts are never meant to go public. It is
# reported but does not fail the check. Everything else here is a real ask.
ACTIONABLE = {
    STATUS_PRIVATE_AHEAD,
    STATUS_PUBLIC_AHEAD,
    STATUS_DIVERGED,
    STATUS_LOCKSTEP_DRIFT,
    STATUS_MISSING,
    STATUS_UNTRACKED,
}


def load_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> Optional[str]:
    if not path.exists() or path.is_dir():
        return None
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def matches(rel: str, patterns: List[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(rel, pattern):
            return True
        # Treat "a/**" as also matching everything below a/
        if pattern.endswith("/**") and (
            rel == pattern[:-3] or rel.startswith(pattern[:-2])
        ):
            return True
    return False


def classify_layer(rel: str, layers: Dict[str, Any]) -> Optional[str]:
    """Return the layer name for a path, or None if it belongs to none."""
    if matches(rel, layers.get("local", {}).get("patterns", [])):
        return "local"
    for name in ("lockstep", "ported"):
        spec = layers.get(name, {})
        if matches(rel, spec.get("patterns", [])) and not matches(
            rel, spec.get("exclude", [])
        ):
            return name
    return None


def tracked_files(root: Path, layers: Dict[str, Any]) -> Dict[str, List[str]]:
    """Walk both layer patterns and collect existing relative paths per layer."""
    found: Dict[str, List[str]] = {"lockstep": [], "ported": []}
    for name in ("lockstep", "ported"):
        spec = layers.get(name, {})
        for pattern in spec.get("patterns", []):
            for path in sorted(root.glob(pattern)):
                if not path.is_file():
                    continue
                rel = path.relative_to(root).as_posix()
                if matches(rel, spec.get("exclude", [])):
                    continue
                if rel not in found[name]:
                    found[name].append(rel)
    return found


def evaluate(
    root: Path,
    counterpart: Path,
    manifest: Dict[str, Any],
    state: Dict[str, Any],
    public_is: str,
) -> List[Tuple[str, str, str]]:
    """Return [(status, rel_path, detail)] for every tracked file in both vaults."""
    layers = manifest.get("layers", {})
    ledger = state.get("files", {})
    results: List[Tuple[str, str, str]] = []

    here = tracked_files(root, layers)
    there = tracked_files(counterpart, layers)

    for layer in ("lockstep", "ported"):
        for rel in sorted(set(here[layer]) | set(there[layer])):
            a, b = root / rel, counterpart / rel
            # Orient: which side is the public template?
            public_path, private_path = (a, b) if public_is == "self" else (b, a)
            pub_hash, priv_hash = digest(public_path), digest(private_path)

            record = ledger.get(rel, {})
            # Pins are a ported-layer concept. Lockstep files must stay
            # identical, so a pin there would silence the central invariant.
            if record.get("pinned") and layer == "ported":
                results.append(
                    (STATUS_PINNED, rel, record.get("reason", "pinned, no reason given"))
                )
                continue

            if pub_hash is None or priv_hash is None:
                side = "public" if pub_hash is None else "private"
                if layer == "ported" and pub_hash is None:
                    results.append(
                        (
                            STATUS_PRIVATE_ONLY,
                            rel,
                            "exists only in the private vault; publish it or ignore",
                        )
                    )
                else:
                    results.append(
                        (STATUS_MISSING, rel, "absent from the %s vault" % side)
                    )
                continue

            if layer == "lockstep":
                if pub_hash != priv_hash:
                    results.append(
                        (
                            STATUS_LOCKSTEP_DRIFT,
                            rel,
                            "must be identical; run --pull to take the public copy",
                        )
                    )
                else:
                    results.append((STATUS_OK, rel, ""))
                continue

            # ported: three-way against the ledger
            if not record:
                results.append(
                    (
                        STATUS_UNTRACKED,
                        rel,
                        "no ledger entry; run --accept once you have reconciled it",
                    )
                )
                continue

            pub_moved = pub_hash != record.get("public")
            priv_moved = priv_hash != record.get("private")

            if not pub_moved and not priv_moved:
                results.append((STATUS_OK, rel, ""))
            elif priv_moved and pub_moved:
                results.append(
                    (STATUS_DIVERGED, rel, "both sides changed since last reconcile")
                )
            else:
                if priv_moved:
                    results.append(
                        (STATUS_PRIVATE_AHEAD, rel, "private vault has unported changes")
                    )
                else:
                    results.append(
                        (STATUS_PUBLIC_AHEAD, rel, "public repo has unpulled changes")
                    )
    return results


class CounterpartMisconfigured(Exception):
    """A counterpart was configured but does not resolve to a directory."""


def resolve_counterpart(state: Dict[str, Any]) -> Optional[Path]:
    """None means intentionally unconfigured. A configured-but-bad path raises.

    Collapsing the two was a silent-failure hole: a typo'd or unmounted path
    looked exactly like a fresh clone, so the quiet session hook printed nothing
    and cross-vault checking could stay disabled indefinitely -- the precise
    failure this script exists to prevent.
    """
    raw = os.environ.get("VAULT_COUNTERPART_ROOT") or state.get("counterpart_root")
    if not raw:
        return None
    path = Path(os.path.expanduser(raw))
    if not path.is_dir():
        raise CounterpartMisconfigured(str(path))
    return path


def save_state(state: Dict[str, Any], path: Path = STATE_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: List[str] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report status.")
    parser.add_argument(
        "--quiet-when-clean",
        action="store_true",
        help="Print nothing and exit 0 when no action is needed (for hooks).",
    )
    parser.add_argument(
        "--pull", action="store_true", help="Copy lockstep files from public to private."
    )
    parser.add_argument("--accept", metavar="PATH", help="Record the current pair as reconciled.")
    parser.add_argument("--pin", metavar="PATH", help="Stop flagging an intentional split.")
    parser.add_argument("--reason", help="Required with --pin.")
    parser.add_argument("--root", default=str(VAULT_ROOT))
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    manifest = load_json(root / "system" / "sync" / "manifest.json", {})
    state = load_json(root / "system" / "sync" / "state.json", {}) or {}
    state.setdefault("files", {})
    public_is = state.get("this_vault_is", "public")

    # --pin only writes local state, so it must work before the counterpart is
    # resolved; requiring one made pinning unreachable on a fresh clone.
    if args.pin:
        if not args.reason:
            print("--pin requires --reason", file=sys.stderr)
            return 2
        layers = manifest.get("layers", {})
        if classify_layer(args.pin, layers) == "lockstep":
            print(
                "refusing to pin a lockstep path: %s\n"
                "Lockstep files must stay byte-identical; pinning one would "
                "silence the invariant rather than resolve it." % args.pin,
                file=sys.stderr,
            )
            return 2
        state["files"].setdefault(args.pin, {})
        state["files"][args.pin].update({"pinned": True, "reason": args.reason})
        save_state(state, root / "system" / "sync" / "state.json")
        print("pinned %s" % args.pin)
        return 0

    try:
        counterpart = resolve_counterpart(state)
    except CounterpartMisconfigured as exc:
        # Always loud, even under --quiet-when-clean: a configured-but-broken
        # path means drift checking is off, and silence is how it stays off.
        print(
            "sync-check: counterpart vault is configured but not found: %s\n"
            "Fix VAULT_COUNTERPART_ROOT or state.json:counterpart_root, or unset "
            "it deliberately to disable cross-vault checking." % exc,
            file=sys.stderr,
        )
        return 2

    if counterpart is None:
        if not args.quiet_when_clean:
            print(
                "no counterpart vault configured "
                "(set VAULT_COUNTERPART_ROOT or state.json:counterpart_root) -- nothing to compare"
            )
        return 0

    if args.accept:
        rel = args.accept
        a, b = root / rel, counterpart / rel
        public_path, private_path = (a, b) if public_is == "public" else (b, a)
        pub_hash, priv_hash = digest(public_path), digest(private_path)
        if pub_hash is None or priv_hash is None:
            print("cannot accept %s: missing on one side" % rel, file=sys.stderr)
            return 2
        state["files"][rel] = {"public": pub_hash, "private": priv_hash}
        save_state(state, root / "system" / "sync" / "state.json")
        print("reconciled %s" % rel)
        return 0

    results = evaluate(
        root, counterpart, manifest, state, "self" if public_is == "public" else "other"
    )

    if args.pull:
        pulled = 0
        layers = manifest.get("layers", {})
        for status, rel, _ in results:
            # Byte-drift AND first-time population. A newly allowlisted
            # mechanism file is absent privately, not different -- that is the
            # initial-port case, and skipping it made --pull a no-op exactly
            # when it was most needed.
            if status == STATUS_MISSING:
                if classify_layer(rel, layers) != "lockstep":
                    continue
                if not ((root if public_is == "public" else counterpart) / rel).is_file():
                    continue
            elif status != STATUS_LOCKSTEP_DRIFT:
                continue
            src = (root if public_is == "public" else counterpart) / rel
            dst = (counterpart if public_is == "public" else root) / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print("pulled %s" % rel)
            pulled += 1
        print("pulled %d lockstep file(s)" % pulled)
        return 0

    actionable = [r for r in results if r[0] in ACTIONABLE]
    # Informational rows still get printed. Computing a publication candidate
    # and then filtering it out of the report made it invisible, so "nothing to
    # migrate" could be printed while candidates were sitting there.
    informational = [r for r in results if r[0] in (STATUS_PRIVATE_ONLY,)]

    if not actionable:
        if not args.quiet_when_clean:
            print("sync-check: %d tracked files, nothing to migrate" % len(results))
            for status, rel, detail in sorted(informational):
                print("  %-16s %-42s %s" % (status, rel, detail))
        return 0

    print("sync-check: %d file(s) need attention" % len(actionable))
    for status, rel, detail in sorted(actionable):
        print("  %-16s %-42s %s" % (status, rel, detail))
    for status, rel, detail in sorted(informational):
        print("  %-16s %-42s %s" % (status, rel, detail))
    print("\nReconcile a ported file with: sync-check.py --accept <path>")
    print("Take the public copy of a lockstep file with: sync-check.py --pull")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
