#!/usr/bin/env bash
# Portable session-start context loader.
# Prints PROJECT_STATE.md and vault orientation when present.
# Silent on the happy path: exits 0 with no stdout when there is nothing useful.

set -u

cwd="$(pwd)"

# Default to the vault this script lives in (system/scripts/session-start-context.sh),
# so a fresh clone is recognised wherever it was put. Override with
# SESSION_CONTEXT_VAULT_ROOT to point at a different vault.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
vault_root="${SESSION_CONTEXT_VAULT_ROOT:-$(dirname "$(dirname "$script_dir")")}"
output=""

append_section() {
    local title="$1"
    local body="$2"
    [ -n "$body" ] || return 0
    output+="## ${title}"$'\n\n'
    output+="${body}"$'\n\n'
}

if [ -f "${cwd}/PROJECT_STATE.md" ]; then
    append_section "PROJECT_STATE.md" "$(cat "${cwd}/PROJECT_STATE.md")"
fi

case "$cwd" in
    "$vault_root"|"$vault_root"/*)
        if [ -x "${vault_root}/system/scripts/context-router.sh" ]; then
            append_section "Vault" "$(VAULT_CONTEXT_ROOT="${vault_root}" "${vault_root}/system/scripts/context-router.sh" default)"
        else
            append_section "Vault" "Working in vault: see AGENTS.md for the session lifecycle contract."
        fi
        ;;
esac

if [ -n "${output}" ]; then
    printf '%s' "${output}"
fi

exit 0
