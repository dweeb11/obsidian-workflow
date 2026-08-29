# Vault Janitor Workflow

Use this for maintenance passes that keep the vault legible without silently rewriting the owner's system.

## Purpose

Find and fix small hygiene problems: stale assumptions, broken links, duplicate stubs, tag drift, ugly intake leftovers, orphaned indexes, and notes that need currentness warnings.

## Read First

1. `AGENTS.md`
2. `Vault-Map.md`
3. `Skills-Map.md`
4. `system/memory/tag-reference.md`
5. Any relevant area `.base` file

## Scope

Good janitor targets:

- stale docs that claim a retired workflow is current truth
- broken or unresolved wikilinks
- duplicate source-only notes
- missing currentness warnings
- stale `role: canonical` marks, and notes in an area base's `Untagged` view
- tag namespace drift
- processed intake originals that were not archived
- operational reports that should be filed under `system/reports/`

Do not treat janitor work as permission to redesign the vault.

## Report Location

Write larger janitor reports to:

`system/reports/vault-janitor/YYYY-MM-DD-<scope>.md`

Use this shape:

```md
# Vault Janitor Report - YYYY-MM-DD - Scope

## Fixed Now

## Needs a Decision

## Do Not Touch

## Source Trail

## Verification
```

Report link rule: use real Obsidian wikilinks for vault notes, e.g. `[[atlas/systems thinking/Some Note|Some Note]]`. A wikilink is clickable in Obsidian; a backticked path is not.

## Automation / Invocation

Manual trigger phrases:

- "run vault janitor"
- "janitor pass"
- "clean up stale vault docs"
- "check vault hygiene"

Eligible inputs:

- explicit folders
- map files
- `system/skills/`
- `+/clippings/`

Allowed automatic actions:

- add currentness warnings
- fix obvious broken links
- update stale pointers in maps/indexes
- normalize small tag mistakes when `tag-reference.md` is clear
- create janitor reports
- propose archive/delete candidates

Requires the owner's approval:

- mass moves
- non-obvious deletions
- restructuring folders
- changing canonical workflows
- creating new tag namespaces
- rewriting personal or creative notes

## Verification

Before finishing:

- report what was fixed and what was only proposed
- check changed wikilinks by search, including quoted/backticked wikilinks and backslash path separators
- verify no Dataview blocks were flattened
- verify no hidden task list was left in Obsidian
- append a line to [[system/logs/skill-usage-log|Skill Usage Log]]
