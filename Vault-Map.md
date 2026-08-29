# Vault Map

This is the portable map for your Obsidian vault. It is tool-agnostic: Claude, Codex, Gemini, NotebookLM, or any future AI should be able to read this file and understand how to move through the vault without needing app-specific instructions.

Related maps:
- [[Me]] — who you are and how to work with you
- [[Skills-Map]] — repeatable workflows and processes
- [[system/memory/tag-reference|Tag Reference]] — active tag vocabulary and namespace hygiene for agents

## Agent Quickstart

Use this section as the default vault context. Read deeper sections only when the task touches them.

- This is a personal Obsidian vault, not a code project.
- Preserve Obsidian wikilinks, Dataview blocks, YAML/frontmatter, tags, and local note style.
- Search before creating a note to avoid duplicates.
- Do not move, rename, delete, or restructure notes unless the task explicitly asks for it.
- New notes follow ACE: `+/clippings/` for live general intake, `atlas/` for durable knowledge/people/sources, `calendar/` for dated records, `efforts/` for active work, `system/` for automation infrastructure, and `x/` for passive archive/support material.
- Read [[Me]] only when the task involves the vault owner's voice, preferences, identity, priorities, or assistant behavior.
- Read [[Skills-Map]] as a workflow index; read the linked `system/skills/*.md` note only for the workflow being run.
- Prefer `system/scripts/context-router.py <profile>` for task-shaped context bundles.
- After modifying vault files, commit from the vault root.

## What This Vault Is

A personal Obsidian vault.

It is not a code repository. There are no build steps or executables for the vault itself. Treat it as a living knowledge system: personal notes, daily notes, research, clippings, AI collaboration maps, and generated digests.

## Operating Principles

- Prefer durable plain-text notes over app-specific state.
- Use the existing structure; do not reorganize folders casually.
- Search before creating a new note to avoid duplicates.
- Preserve the owner's voice and existing note style.
- Treat the vault as the owner's source of truth, not an AI scratchpad.
- Keep agent infrastructure in `system/` unless the owner explicitly asks otherwise.
- Use the ACE target grammar for new notes: `+` for intake, `atlas/` for durable knowledge, `calendar/` for dated records, `efforts/` for active projects/responsibilities, and `system/` for automation infrastructure.
- ACE folders are lowercase. Casing matters on case-sensitive filesystems and in wikilinks — do not capitalize them.
- After modifying the vault, commit changes to git from the vault root.
- Treat [[system/memory/tag-reference|Tag Reference]] as the live agent-facing tag vocabulary; update it after vault-wide tag scans or when durable namespaces are added.

## Core Conventions

### Wikilinks

Use Obsidian wiki-link syntax:

- `[[Note Name]]`
- `[[Note Name|Display Text]]`

Do not convert existing wikilinks into standard Markdown links.

### Dataview

Fenced `dataview` code blocks are dynamic queries. Do not rewrite them as static lists.

### Tags

Tags are hierarchical and inline — a namespace prefix, then a leaf:

- `#action/next`
- `#area/subarea`

Keep namespaces few and durable. Read [[system/memory/tag-reference|Tag Reference]] before adding tags, and record a new namespace there once it earns its place.

## Major Areas

### Target Grammar: ACE + Intake + System

This is the filing grammar for new notes.

```text
<vault root>/
  +/                       — intake root; live general intake is `+/clippings/`
    clippings/             — live general intake and web clippings
  atlas/                   — durable knowledge, people, and topical concept areas
    people/                — unified people pages
    <topic>/               — durable topical areas; create one only when it is a real domain
  calendar/                — daily notes, meeting notes, dated records
    daily notes/YYYY/      — archived daily notes
    meetings/              — retained meeting notes
  efforts/                 — active projects, goals, responsibilities, work-in-motion
  system/                  — live agent/automation infrastructure; keep separate from ACE
    scripts/               — portable automation scripts used by agents
    skills/                — portable vault workflow procedures indexed from [[Skills-Map]]
    Templates/             — Obsidian note templates
    memory/                — small agent-facing reference (tag vocabulary)
    reports/               — workflow run reports (janitor, intake, weekly review)
    logs/                  — append-only evidence logs
  x/                       — passive support/archive material
    archive/intake/YYYY-MM/ — processed raw intake originals after source trails are preserved

  Me.md                    — portable identity map
  Vault-Map.md             — this file: vault navigation and structure
  Skills-Map.md            — repeatable workflows/process index
  AGENTS.md                — the agent front door; points at these maps
```

Important: `system/` is not an archive bucket and should not be collapsed into `+/`, `atlas/`, or `x/`. It contains live automation materials. Use `x/` only for passive support/archive material such as superseded rollups after synthesis.

### Idea graveyards (`x/archive/<lane>/… graveyard.md`)

A lane may keep a graveyard note in its `x/archive/` mirror. It holds ideas that were considered and deliberately killed — not ideas that are merely inactive, and not the lane's working scratchpad, which stays in `efforts/`.

The graveyard exists so a resurfaced idea can be checked against its own history instead of re-argued from scratch. Each entry therefore records four things: what the idea was, where it came from, when it was killed, and why. Keep the reasoning in the owner's words; a graveyard that summarizes away the reasoning cannot do its job.

Entries are append-only. When an idea returns and the old reasoning no longer holds, add a new dated line under the existing entry rather than editing or deleting the original verdict — the changed mind is itself part of the record.

### Wiki index pages (`_index.md`)

Major folders may have a `_index.md` page as a human-friendly table of contents. Indexes are for orientation and navigation, not task control. Prefer a Memory Card, a `## Start Here` table, a `## Main Areas` table when useful, and Dataview blocks for navigation/maintenance lists. Actionable follow-ups discovered while indexing should remain vault-local candidates unless the owner explicitly asks for an external action. Use `system/Templates/wiki-index.md` as the starting template.

Do not recreate a task cockpit in Obsidian; the vault should stay an orientation/context surface unless the owner explicitly asks for a task-control workflow.

### Structured Reference (`system/memory/`)

`system/memory/` is not a factual source about the owner, people, or active projects. It is a small agent-infrastructure area:

| File | Purpose |
|------|---------|
| `tag-reference.md` | Live tag vocabulary and namespace hygiene. |

Prefer `Me.md`, `atlas/people/`, `efforts/`, the current maps, and the relevant workflow notes for everything else.

## Daily Capture Notes

Same-day dated notes are **Daily Capture** files: temporary raw logs for inbox material, friction, decisions, possible follow-ups, and end-of-day notes. They are not dashboards and should not duplicate project repositories, generated briefs, or external task systems.

Current grammar:

- the active note lives at the vault root as `YYYY-MM-DD.md` while it is today
- at close of day it is archived to `calendar/daily notes/YYYY/YYYY-MM-DD.md`
- Daily Capture owns day-to-day raw capture and cleanup breadcrumbs; Obsidian owns capture, reflection, context, source trails, and re-entry
- do not assume or update any external task manager, ticket system, calendar, reminder app, or automation target unless the owner explicitly asks in the current conversation

At close of day, the raw capture note is processed in place:

- people mentions may update relevant pages in `atlas/people/`
- research, decisions, and ideas are routed selectively to durable homes, preferring `atlas/` for reusable concepts and `efforts/` for active work
- possible follow-ups are preserved in the vault only unless the owner explicitly asks for an external action
- the note is preserved in `calendar/daily notes/YYYY/YYYY-MM-DD.md` with routing and cleanup breadcrumbs appended
- the root original is removed only after the archive copy has been verified

The full procedure is [[system/skills/daily-capture|Daily Capture / Close-Day Workflow]].

## Naming Conventions

- Daily notes: `YYYY-MM-DD.md`
- Meeting notes: `YYYY-MM-DD - Meeting Name.md`
- Prefer readable human names over opaque IDs.

## Note Types

### Capture
Temporary raw input. Daily Capture notes, inbox notes, quick captures. New general unsorted intake goes in `+/clippings/` unless it is a dated Daily Capture file.

### Source
Notes about external material: books, videos, articles, podcasts, meetings. Reusable source notes go under `atlas/` (in the relevant topical subfolder); project-local sources may live inside the relevant `efforts/` folder only when they are not generally reusable.

Raw source files that have already been extracted may be archived under `x/archive/intake/YYYY-MM/` after source trails are preserved. Delete only obvious junk, duplicates, or empty captures.

Thin items saved because they may be bought, played, run, read, watched, or learned from later should become lightweight `status: interested` stubs when the domain is clear. Surface those stubs from the relevant folder `_index.md`.

### Concept
Atomic notes for durable ideas, frameworks, patterns, principles, recurring terms. Concept notes go under `atlas/` in the matching topical subfolder.

Durable homes listed in workflow docs are examples, not a closed taxonomy. If an intake pattern merits a new folder, create one only when it is a real durable domain, likely to hold several notes, and not cleanly covered by an existing ACE area. Add or update that folder's `_index.md` when the folder becomes a re-entry surface.

### Person
Notes about people. Canonical location is `atlas/people/`.

### Project / Effort
Notes tied to active work, creative projects, writing, family logistics, or responsibilities. New effort folders go under `efforts/`.

### Calendar Record
Time-based records: daily notes, meeting notes, dated logs. Archived dated records go under `calendar/`; the same-day raw capture lives at the vault root until close.

### Output
Essays, briefs, finished writing, and generated artifacts. Durable synthesized output may belong in `atlas/` or `efforts/` depending on use. Workflow run reports belong in `system/reports/`.

### Media Assets
Durable notes may include images, screenshots, diagrams, maps, or generated visual aids when media improves re-entry. Store assets near the note under an `assets/` folder, for example `atlas/<area>/assets/<note-slug>/` or `efforts/<lane>/assets/<note-slug>/`, and embed with Obsidian syntax such as `![[assets/example.png]]`. Preserve source/license trails for web images; prefer your own screenshots, generated diagrams, or clearly sourced references.

## AI Navigation Rules

When an AI works in this vault:

1. Start with `AGENTS.md` and `system/scripts/context-router.py <profile>` whenever possible.
2. Use `## Agent Quickstart` as the default Vault-Map context; read deeper sections only when they are relevant.
3. Read [[Me]] only when the task involves the owner's preferences, identity, voice, priorities, or assistant behavior.
4. For operational context, prefer current source notes: `Me.md` for the owner and their preferences, `atlas/people/` for people, `efforts/` for active work, `Vault-Map.md` / `Skills-Map.md` for process, and `system/memory/tag-reference.md` only for tags.
5. Read [[Skills-Map]] as an index when the task involves a repeatable workflow; then read the linked `system/skills/*.md` workflow note when one exists.
6. Search for existing notes before creating new ones.
7. Preserve wikilinks, tags, Dataview blocks, properties/frontmatter, and local formatting.
8. For new notes, use the ACE target grammar.
9. Do not move or rename notes unless the task explicitly asks for reorganization.
10. Do not edit `system/` casually; it is automation infrastructure.
11. Commit changes after writing or modifying vault files.

## Git Rule

This vault is a git repo. After writing or modifying files:

```bash
git add <changed files>
git commit -m "Concise description"
```
