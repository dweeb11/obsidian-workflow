#!/usr/bin/env python3
"""Session-close memory routing (Claude Code Stop hook).

When a session did meaningful work, BLOCK the stop once and instruct the
agent to route durable memory (vault note / PROJECT_STATE.md) before
finishing. Below threshold, or on the post-block continuation, stay silent.

Hook wiring is tool-specific and lives outside this script; this only decides
whether to speak and prints the Stop-hook JSON when it does.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

REENTRY_WINDOW_SEC = 600
DEFAULT_THRESHOLD_EDITS = 10
DEFAULT_THRESHOLD_SEC = 1800

REASON = (
    "Session-close memory routing (work threshold met). Do this now, without asking the user: "
    "(1) If this session produced a durable cross-project keeper — a decision, a correction, a "
    "solved problem that took effort, or a user preference discovered — file it into the vault "
    "now as a note in its durable home. (2) If the repo's working state changed materially, "
    "update PROJECT_STATE.md in the repo root. (3) If something warrants deeper synthesis, note "
    "it for the next vault synthesis pass. Apply the filing criteria strictly: skip ephemeral "
    "task state, anything already captured in git history, and easily searchable facts. If "
    "nothing qualifies, say 'Nothing to route.' Then stop."
)

# A vault can override the routing instruction without forking this script.
# WHERE durable memory goes is vault-specific -- one vault files to a remote
# memory service, another just writes a note -- but the decision of WHETHER to
# speak is identical everywhere. Keeping the message as vault-local data is what
# lets this file stay byte-identical across paired vaults.
OVERRIDE_RELATIVE_PATH = Path("memory") / "session-routing-message.md"


def routing_reason() -> str:
    """The override file's contents when a vault supplies one, else the default."""
    override = Path(__file__).resolve().parents[1] / OVERRIDE_RELATIVE_PATH
    try:
        text = override.read_text(encoding="utf-8").strip()
    except (OSError, UnicodeDecodeError):
        return REASON
    return text or REASON


def home_dir() -> Path:
    """Honour HOME first so tests can isolate, then the Windows equivalent."""
    return Path(os.environ.get("HOME") or os.environ.get("USERPROFILE") or Path.home())


def as_int(value: str | None, fallback: int = 0) -> int:
    """Non-numeric input counts as zero, matching the shell version it replaced."""
    if value is None or not value.strip().isdigit():
        return fallback
    return int(value.strip())


def recently_blocked(sentinel: Path) -> bool:
    """Belt-and-suspenders: never block more than once per window, so a
    routing pass cannot loop even if STOP_HOOK_ACTIVE is not passed through."""
    try:
        return (time.time() - sentinel.stat().st_mtime) < REENTRY_WINDOW_SEC
    except OSError:
        return False


def read_hook_input(enabled: bool) -> dict:
    """Parse the Stop-hook JSON on stdin. Only when --from-hook is passed.

    Claude Code delivers session metrics on stdin, not in the environment, so
    reading only env vars meant both thresholds parsed as zero and the hook
    never fired -- silently, on every session.

    Reading is explicit rather than sniffed. Guessing via isatty() looked fine
    and then blocked forever whenever stdin was an inherited pipe rather than a
    terminal, which would hang the very session this is supposed to close.
    """
    if not enabled:
        return {}
    try:
        raw = sys.stdin.read()
    except (OSError, UnicodeDecodeError, AttributeError):
        return {}
    if not raw.strip():
        return {}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def session_metrics(payload: dict) -> tuple:
    """(edits, duration_sec, stop_hook_active), env taking precedence."""
    edits_env = os.environ.get("SESSION_EDIT_COUNT")
    duration_env = os.environ.get("SESSION_DURATION_SEC")
    active_env = os.environ.get("STOP_HOOK_ACTIVE")

    edits = as_int(edits_env) if edits_env is not None else as_int(
        str(payload.get("cumulative_tool_use_count", payload.get("tool_use_count", 0)) or 0)
    )

    if duration_env is not None:
        duration = as_int(duration_env)
    elif payload.get("duration_sec") is not None:
        duration = as_int(str(int(payload["duration_sec"])))
    else:
        duration = as_int(str(int((payload.get("duration_ms") or 0) / 1000)))

    active = active_env if active_env is not None else str(payload.get("stop_hook_active", False))
    return edits, duration, str(active).lower() in {"true", "1"}


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if os.environ.get("SESSION_ROUTE_DISABLE") == "1":
        return 0

    payload = read_hook_input("--from-hook" in sys.argv[1:])
    edits, duration, stop_hook_active = session_metrics(payload)

    # Never block twice: the continuation turn carries stop_hook_active.
    if stop_hook_active:
        return 0

    claude_dir = home_dir() / ".claude"
    sentinel = claude_dir / ".session-route-last-block"
    if recently_blocked(sentinel):
        return 0

    # If a malformed threshold became 0, preserve the documented defaults
    # instead of firing constantly.
    threshold_edits = as_int(os.environ.get("SESSION_ROUTE_THRESHOLD_EDITS"), DEFAULT_THRESHOLD_EDITS) or DEFAULT_THRESHOLD_EDITS
    threshold_sec = as_int(os.environ.get("SESSION_ROUTE_THRESHOLD_SEC"), DEFAULT_THRESHOLD_SEC) or DEFAULT_THRESHOLD_SEC

    if edits < threshold_edits and duration < threshold_sec:
        return 0

    try:
        claude_dir.mkdir(parents=True, exist_ok=True)
        sentinel.touch()
    except OSError:
        pass

    print(json.dumps({"decision": "block", "reason": routing_reason()}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
