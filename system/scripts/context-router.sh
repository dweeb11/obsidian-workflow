#!/usr/bin/env bash
# Minimal vault context router for agents.
# Prints a small task-shaped bundle so agents do not read every map by default.

set -u

profile="${1:-default}"

# Default to the vault this script lives in (system/scripts/context-router.sh),
# so the router works from a fresh clone wherever it was put. Override with
# VAULT_CONTEXT_ROOT to point at a different vault.
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
vault_root="${VAULT_CONTEXT_ROOT:-$(dirname "$(dirname "$script_dir")")}"

die() {
    printf 'context-router: %s\n' "$1" >&2
    exit 1
}

[ -d "$vault_root" ] || die "vault root not found: $vault_root"
cd "$vault_root" || die "cannot enter vault root: $vault_root"

print_section() {
    local file="$1"
    local title="$2"
    [ -f "$file" ] || return 0
    awk -v title="$title" '
        $0 == "## " title { in_section = 1; print; next }
        in_section && /^## / { exit }
        in_section { print }
    ' "$file"
}

cat <<'EOF'
# Vault Context Router

Use this as the initial context bundle. Read deeper files only when the task profile says to.

EOF

quickstart="$(print_section "Vault-Map.md" "Agent Quickstart")"
if [ -n "$quickstart" ]; then
    printf '%s\n\n' "$quickstart"
else
    cat <<'EOF'
## Agent Quickstart

- Preserve wikilinks, Dataview blocks, frontmatter, tags, and local note style.
- Search before creating notes.
- Do not move, rename, or delete notes unless explicitly asked.
- Commit vault changes from the vault root.

EOF
fi

cat <<EOF
## Task Profile: ${profile}

EOF

case "$profile" in
    default|typo|small)
        cat <<'EOF'
- Read: `AGENTS.md`, this router output, and the target note/file.
- Optional: relevant `Vault-Map.md` section if creating notes or touching folder structure.
- Avoid: loading all of `Vault-Map.md`, `Skills-Map.md`, or `Me.md` for small edits.
EOF
        ;;
    daily)
        cat <<'EOF'
- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart, `Skills-Map.md` Daily Capture and Close-Day entries.
- Read when writing: `system/Templates/Daily Note.md`.
- Read `system/skills/daily-capture.md` in full before running Setup or Close.
EOF
        ;;
    intake|clippings)
        cat <<'EOF'
- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart and Note Types, `Skills-Map.md` Intake Extraction entry.
- Then read: `system/skills/intake-extraction.md`.
- Treat `+/clippings/` as the live general intake surface.
EOF
        ;;
    synthesis|audit)
        cat <<'EOF'
- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart and Note Types, `Skills-Map.md` Vault Synthesis entry.
- Then read: `system/skills/vault-synthesis.md`.
- Use `system/Templates/synthesis-note.md` when creating a synthesis note.
EOF
        ;;
    index|wiki-index)
        cat <<'EOF'
- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart and Wiki index pages section, `Skills-Map.md` Wiki Index entry.
- Then read: `system/skills/wiki-index.md`.
- Use `system/Templates/wiki-index.md` when creating an `_index.md`.
EOF
        ;;
    voice|me)
        cat <<'EOF'
- Read: `AGENTS.md`, `Vault-Map.md` Agent Quickstart, and `Me.md`.
- Use this profile for the vault owner's voice, preferences, boundaries, assistant behavior, and outward-facing drafts.
EOF
        ;;
    operational|context)
        cat <<'EOF'
- Read: `AGENTS.md` and `Vault-Map.md` Agent Quickstart.
- For operational context, prefer current sources: `Me.md`, `atlas/people/`, `efforts/`, `Skills-Map.md`, and relevant `system/skills/*.md` notes.
- Use `system/memory/tag-reference.md` for tag vocabulary.
EOF
        ;;
    map|maps|agent-os)
        cat <<'EOF'
- Read: `AGENTS.md`, `Vault-Map.md`, `Skills-Map.md`, and `system/skills/map-maintenance.md`.
- Read `Me.md` when changing preferences, assistant behavior, boundaries, or voice guidance.
- Search for contradicted old wording before finishing.
EOF
        ;;
    help|-h|--help)
        cat <<'EOF'
Profiles: default, daily, intake, synthesis, index, voice, operational, map.
Set `VAULT_CONTEXT_ROOT=/path/to/vault` to run against a non-default vault.
EOF
        ;;
    *)
        cat <<'EOF'
- Unknown profile. Use `context-router.sh help` for options.
- Fallback: read `AGENTS.md`, this quickstart, and only the note/section directly relevant to the task.
EOF
        ;;
esac

cat <<'EOF'

## Closeout

- Verify with evidence before calling work done.
- After modifying vault files, commit from the vault root.
EOF
