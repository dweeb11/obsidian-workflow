# AGENTS.md

This is the portable agent contract for this Obsidian vault. Tool-specific adapter files should stay thin and point here instead of duplicating vault rules. The deeper source of truth lives in the map files.

## Context Routing

This vault uses portable map files. Load only what is relevant. The maps are routers, not mandatory context dumps: start from the smallest applicable bundle, then pull deeper sections only when the task needs them.

Optional low-token shortcut when shell access is available:

```bash
system/scripts/context-router.sh <profile>
```

Profiles include `default`, `daily`, `intake`, `synthesis`, `index`, `voice`, `operational`, and `map`. The script is convenience only; the vault files are the source of truth. If the script is unavailable or conflicts with the map/workflow files, follow the rules below manually.

Always read before modifying vault structure or content:

- [[Vault-Map]] `## Agent Quickstart` — compact vault layout, naming, Obsidian conventions, git rule
- Relevant [[Vault-Map]] sections only when the task touches that area

Read when the task involves the vault owner's preferences, identity, voice, priorities, or assistant behavior:

- [[Me]]

Read when you need operational context (active projects, key people, recurring terms):

- Prefer current sources: [[Me]] for the owner and their preferences, `atlas/people/` for people, `efforts/` for active work, [[Vault-Map]] / [[Skills-Map]] for process, and `system/memory/tag-reference.md` for tags.

Read when the task involves a repeatable workflow or process:

- [[Skills-Map]] as an index, then the relevant `system/skills/*.md` workflow note when one exists

Examples:

- Fix a typo in one note → `context-router.sh default`, then inspect the target note
- Draft something in the owner's voice → `context-router.sh voice`, then read [[Me]]
- Process a daily note → read [[system/skills/daily-capture|Daily Capture / Close-Day Workflow]] and `system/Templates/Daily Note.md`; `context-router.sh daily` is only an optional shortcut
- Process intake or clippings → `context-router.sh intake`, then read `system/skills/intake-extraction.md`
- Create/update a synthesis note or audit → `context-router.sh synthesis`, then read `system/skills/vault-synthesis.md`
- Create/update a folder `_index.md` → `context-router.sh index`, then read `system/skills/wiki-index.md`
- Update the maps themselves → `context-router.sh map`, then read the affected maps/skills

## What This Repository Is

This is an **Obsidian vault**. It is not a code project — there are no build steps or executables for the vault itself. (The scripts under `system/scripts/` do have tests; see the README.)

## Vault Working Agreements

- Preserve Obsidian wikilinks: `[[Note Name]]` or `[[Note Name|Display Text]]`.
- In generated reports, render raw web URLs as Markdown autolinks (`<https://example.com>`) or labeled links. Do not wrap URLs in backticks or single quotes; that makes them non-clickable in Obsidian/Markdown surfaces.
- Preserve Dataview blocks; do not rewrite them as static lists.
- Do not restructure folders or move notes unless explicitly asked.
- Use the Obsidian CLI when appropriate and available.

Prefer CLI for searching notes, checking tags, reading by wikilink, backlinks, unresolved links, moving notes, and querying tasks.

Use file tools for creating structured files, complex multi-section edits, and bulk writes.

## Session Lifecycle and Two-Surface Routing

Session lifecycle behavior lives in portable scripts under `system/scripts/`. Tool adapters and skills must call those scripts instead of duplicating the behavior.

At session start, load context from whichever surfaces apply:

- **Project state:** if the current repo has `PROJECT_STATE.md`, read it before digging through git history or project docs.
- **Vault:** when working in this vault, consult this file, `system/scripts/context-router.sh default`, and any relevant `_index.md` or effort dashboard.

The canonical implementation is `system/scripts/session-start-context.sh`.

Durable closeout should happen at the moment work crystallizes, not when someone remembers to run a command before quitting. Use this trigger order:

1. **Commit creation** is a lightweight checkpoint for repo-local state changes, especially when touching `AGENTS.md`, `PROJECT_STATE.md`, docs, scripts, hooks, or skills.
2. **Session close** is only a passive safety net. It may surface routing prompts, but important memory capture must not depend on interaction after the session ends.

For `## Handoff / Memory Routing`, answer:

- `PROJECT_STATE.md` updated? yes/no/n/a — why.
- Vault keeper? yes/no — why; file the durable note into the vault when yes.
- Vault synthesis candidate? yes/no — why; flag it or add an approved vault breadcrumb/note when yes.

The canonical closeout prompt implementation is `system/scripts/session-end-route.sh`. It stays silent below the configured threshold and surfaces routing prompts above it as a backup.

Kill switch: set `SESSION_ROUTE_DISABLE=1` to disable the close-route prompt.

## Evidence Rule

Always verify before calling work done. Evidence only — no "should work."
