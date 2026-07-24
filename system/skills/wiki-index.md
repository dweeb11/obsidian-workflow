# Wiki Index Workflow

Use this when creating or updating `_index.md` pages for major vault folders.

## Purpose

A wiki index is a human-friendly table of contents and re-entry page. It is not a dashboard, task cockpit, or status ledger.

## Read First

1. `AGENTS.md`
2. `Vault-Map.md`
3. `Skills-Map.md`
4. `system/Templates/wiki-index.md`
5. Parent or sibling `_index.md` pages, if they exist

## Default File

Use `_index.md` at the root of the folder being indexed. The leading underscore keeps the page near the top of the folder.

## Output Shape

Start from `system/Templates/wiki-index.md`.

A good index usually has:

- YAML `type/index` tag when frontmatter is already appropriate
- Memory Card
- `## Start Here` table
- `## Main Areas` table when the folder has subareas
- `## Current Links` for stable external pointers
- Dataview navigation lists where they reduce manual upkeep
- Link / Tag Review
- Routed Follow-ups

## Start Here Table

Use a navigation table instead of a generic prose summary:

```md
| Note | Use it for |
|---|---|
| [[Current Design]] | Canonical orientation. |
| [[Research Source]] | Source trail and deeper context. |
```

## Dataview Guidance

Use Dataview for navigation and maintenance lists, not for recreating a project-management dashboard.

Good uses:

- list child indexes
- list recently updated notes in the area

Avoid:

- duplicating external task state
- turning `_index.md` into a cockpit
- hand-maintained task rollups

## Follow-up Routing

Indexes often reveal cleanup work. Route it instead of burying it — vault-local by default.

- New actionable work → surface it in the index's `Routed Follow-ups` as a vault-local candidate.
- Related work → append to the existing follow-up entry instead of duplicating it.
- Non-actionable context → keep in the index or relevant note.
- Moves/deletes/archives → propose in the index; do not perform without explicit approval.

Do not create or update external task-system records unless the owner explicitly asks in the current conversation.

## Automation / Invocation

Manual trigger phrases:

- "create an index for this folder"
- "update the index"
- "make this folder discoverable"
- "build a wiki index for X"

Eligible inputs:

- a folder that lacks a discoverable `_index.md`
- an existing `_index.md` with stale pointers or missing new notes

Allowed automatic actions:

- create or update `_index.md` from `system/Templates/wiki-index.md`
- refresh Start Here / Main Areas tables and Dataview lists
- fix broken wikilinks within the index

Requires the owner's approval:

- restructuring the folder the index describes
- deleting an existing index instead of updating it

## Verification

Before finishing:

- confirm the index points to the current canonical notes
- check obvious wikilinks work by searching paths/titles
- verify no hidden task list was left in Obsidian
- update parent index if the new index should be discoverable
- commit vault changes from the vault root
- append a line to [[system/logs/skill-usage-log|Skill Usage Log]]
