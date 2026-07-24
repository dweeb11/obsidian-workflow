# Intake Extraction Workflow

Use this when processing raw items from `+/clippings/`.

## Purpose

Turn raw intake into durable notes, source trails, or clean discard decisions. The goal is not to empty the folder blindly. The goal is to decide what each item is worth.

## Read First

1. `AGENTS.md`
2. `Vault-Map.md`
3. `Skills-Map.md`
4. `system/memory/tag-reference.md`
5. The relevant destination `_index.md`, if one exists

## Classification

Classify each item as exactly one:

| Class | Meaning | Default action |
|---|---|---|
| `discard` | Junk, duplicate, empty, or no longer useful. | Delete only when obvious. |
| `source-only` | Worth preserving as source/history, but not worth synthesis yet. | Archive original with source trail. |
| `interest-stub` | Thin item saved because it may be bought, played, read, watched, run, or learned from later. | Keep in intake until a lightweight durable/watchlist stub is created or the owner declines it. |
| `extract` | Contains a durable idea, tool, project seed, or reference. | Create or update a durable note, then archive original. |
| `merge` | Belongs in an existing note. | Update that note, preserve source trail, then archive original. |
| `ask` | Ambiguous, sensitive, or potentially valuable but unclear. | Report the question; do not move/delete. |

## Durable Homes

The classification principle is the transferable part: **route by what the material is for, not by what it is about.** A durable idea goes to `atlas/`; something tied to work in motion goes to `efforts/`; a dated record goes to `calendar/`; live automation goes to `system/`. The topical subfolder underneath is yours to grow.

| Material | Likely destination |
|---|---|
| Durable concept, framework, or reference in a topic you keep returning to | `atlas/<topic>/` |
| Material tied to a specific active project or responsibility | `efforts/<area>/` |
| Dated records | `calendar/` |
| Automation or agent infrastructure | `system/` only when it is live infrastructure |

These destinations are examples, not a closed taxonomy. If a repeated pattern merits new organization, create a new folder only when:

- it is a durable domain, not a one-off clipping
- several future notes are plausible
- no existing ACE area fits cleanly
- the folder can be named plainly

When a new folder becomes a re-entry surface, create or update its `_index.md` and update `Vault-Map.md` if it becomes a durable convention.

## Interest Stubs

Do not discard or immediately archive thin commercial/store/product pages just because the capture has little commentary. These are often clipped because of a later intent — buy, play, run, read, watch, or learn from.

Common interest-stub sources:

- store, storefront, crowdfunding, and publisher pages
- articles that mostly point at a product or title worth checking out
- tools or apps worth trying later
- books, comics, music, or other media pages with little context

For these, prefer a lightweight durable/watchlist note over archive-only handling when the domain is obvious. Keep the note honest and small:

```md
---
status: interested
interest_type: maybe buy / maybe play / maybe read / learn-from candidate
source: URL
created: YYYY-MM-DD
last_reviewed:
tags:
  - type/source
---

# Title

Source: URL

Status: interested / maybe buy / maybe play / learn-from candidate

Why saved: clipped as a possible future purchase/play/read/learn-from item. No deeper synthesis yet.

## What To Check Later
- price / availability
- reviews or reports from people who used it
- the angle that made it interesting
- whether it belongs in an active project
```

Interest stubs must be surfaced somewhere visible. Put them under the `atlas/` topical folder that owns the domain, and give that folder's `_index.md` a Dataview `Interest Queue` listing every note with `status: interested` once there are enough stubs to need a queue.

Interest stubs are subject to the **stale filed-item cull** in [[weekly-review-lens|Weekly Review Lens]]: a stub left untouched (`status: interested`, no `last_reviewed`/`created` movement) for more than 8 weeks resurfaces for a keep/act/cull decision. Leave `last_reviewed` empty at creation; the cull pass sets it when the owner chooses "keep watching."

If the domain is not obvious, classify as `ask` and leave it in intake.

## Media

Durable notes may include media when it improves recognition or re-entry: screenshots, maps, diagrams, product images, generated visual aids, or UI captures.

Rules:

- Store media near the note under `assets/<note-slug>/` inside the relevant `atlas/` or `efforts/` area.
- Embed with Obsidian syntax such as `![[assets/example.png]]`.
- Prefer your own screenshots, generated diagrams, or clearly sourced references.
- Preserve source/license trails for web images.
- Do not bulk-hoard images from every clipping.

## Source Trails

Every extraction or merge must preserve where the idea came from. Use one or more:

- `Source:` line with the original intake wikilink or path
- `sources:` frontmatter list when the destination note already uses it
- a dated `## Source Trail` or `## Updates` entry

After extraction, archive originals to `x/archive/intake/YYYY-MM/` unless they are obvious junk. Delete only after the durable note has the source trail.

## Wikilink Requirements

Intake reports are navigation surfaces, not plain logs. When a processed file is archived and a report is created:

- Link every processed item with an Obsidian wikilink to its final location. If the intake file was archived, the report table should link the archived path, e.g. `[[x/archive/intake/YYYY-MM/example|example]]`, not the now-missing `+/clippings/` path.
- Link every created or updated durable note with a wikilink.
- In report tables, use wikilinks in the `Item` / `Action` cells instead of backticked plain paths.
- In `## Archived Originals`, list archived originals as wikilinks, not bare paths.
- Use path-qualified wikilinks when titles collide or the note lives outside a unique title space.
- Verification must include a line confirming report wikilinks were used for archived originals and created/updated notes.

## Automation / Invocation

Manual trigger phrases:

- "process intake"
- "extract these clippings"
- "triage clippings"
- "run intake extraction"

Eligible inputs:

- `+/clippings/`
- explicit file paths the owner names

Allowed automatic actions:

- classify items
- create or update durable notes when the destination is obvious
- add source trails
- archive processed originals under `x/archive/intake/YYYY-MM/`
- delete obvious junk items
- add media embeds when assets are already available or explicitly generated for the note
- create lightweight interest stubs for obvious purchase/play/read/learn-from captures

Requires the owner's approval:

- deleting non-obvious source material
- creating a new top-level domain
- moving existing durable notes
- using sensitive/private material externally
- creating broad new taxonomy or tag namespaces

Report output:

- For small runs, summarize in the chat.
- For larger runs, write `system/reports/intake-extraction/YYYY-MM-DD-<scope>.md`.

## Verification

Before finishing:

- every item has a classification
- created/updated notes preserve source trails
- archived originals landed under `x/archive/intake/YYYY-MM/`
- deleted items were obvious junk
- new folders have an `_index.md` when they need one
- wikilinks and media embeds resolve by path/title search
- commit vault changes from the vault root
- append a line to [[system/logs/skill-usage-log|Skill Usage Log]]
