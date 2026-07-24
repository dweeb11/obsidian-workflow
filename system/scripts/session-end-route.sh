#!/usr/bin/env bash
# Session-close memory routing (Claude Code Stop hook).
# When a session did meaningful work, BLOCK the stop once and instruct the
# agent to route durable memory (vault note / PROJECT_STATE.md) before
# finishing. Below threshold, or on the post-block continuation, stay silent.

set -u

if [ "${SESSION_ROUTE_DISABLE:-}" = "1" ]; then
    exit 0
fi

# Never block twice: the wrapper passes stop_hook_active from the hook input
# on the continuation turn.
case "${STOP_HOOK_ACTIVE:-}" in
    True|true|1) exit 0 ;;
esac

# Belt-and-suspenders (older wrapper may not pass STOP_HOOK_ACTIVE): never
# block more than once per 10 minutes, so a routing pass can't loop.
sentinel="$HOME/.claude/.session-route-last-block"
if [ -f "$sentinel" ]; then
    now="$(date +%s)"
    then="$(stat -f %m "$sentinel" 2>/dev/null || stat -c %Y "$sentinel" 2>/dev/null || echo 0)"
    if [ $(( now - then )) -lt 600 ]; then
        exit 0
    fi
fi

as_int() {
    case "${1:-}" in
        ''|*[!0-9]*) printf '0' ;;
        *) printf '%s' "$1" ;;
    esac
}

edits="$(as_int "${SESSION_EDIT_COUNT:-0}")"
duration="$(as_int "${SESSION_DURATION_SEC:-0}")"
threshold_edits="$(as_int "${SESSION_ROUTE_THRESHOLD_EDITS:-10}")"
threshold_sec="$(as_int "${SESSION_ROUTE_THRESHOLD_SEC:-1800}")"

# If a malformed threshold became 0, preserve the documented defaults instead of firing constantly.
[ "$threshold_edits" -gt 0 ] || threshold_edits=10
[ "$threshold_sec" -gt 0 ] || threshold_sec=1800

if [ "$edits" -lt "$threshold_edits" ] && [ "$duration" -lt "$threshold_sec" ]; then
    exit 0
fi

mkdir -p "$HOME/.claude" && touch "$sentinel"

cat <<'EOF'
{"decision": "block", "reason": "Session-close memory routing (work threshold met). Do this now, without asking the user: (1) If this session produced a durable cross-project keeper — a decision, a correction, a solved problem that took effort, or a user preference discovered — file it into the vault now as a note in its durable home. (2) If the repo's working state changed materially, update PROJECT_STATE.md in the repo root. (3) If something warrants deeper synthesis, note it for the next vault synthesis pass. Apply the filing criteria strictly: skip ephemeral task state, anything already captured in git history, and easily searchable facts. If nothing qualifies, say 'Nothing to route.' Then stop."}
EOF
exit 0
