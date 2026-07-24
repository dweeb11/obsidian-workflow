# Weekly Review Lens

Use this when the owner wants an AI second pass over a week, not an AI-authored weekly digest.

## Purpose

Surface missed loops, repeated friction, decisions, stale promises, and candidate extractions after the owner's own notes lead the review.

## Read First

1. `AGENTS.md`
2. `Vault-Map.md`
3. `Skills-Map.md`
4. `Me.md`
5. Relevant daily notes, effort notes, intake folders, and project indexes

## Inputs

Possible inputs:

- `calendar/daily notes/YYYY/`
- recent `+/clippings/`
- active effort notes
- janitor or intake extraction reports in `system/reports/`

## Output

Prefer concise sections:

- `Signals Worth Keeping`
- `Missed Loops`
- `Repeated Friction`
- `Decisions That Need A Home`
- `Candidate Extractions`
- `Stale Filed Items — Keep / Act / Cull`
- `Open Questions`

Do not create a recurring weekly digest obligation by default.

## Automation / Invocation

Manual trigger phrases:

- "weekly review lens"
- "review this week"
- "what did I miss this week"
- "find patterns in the week"

Eligible inputs:

- a week date range
- daily note paths
- selected intake or effort folders

Allowed automatic actions:

- summarize patterns
- propose extractions
- create a report under `system/reports/weekly-review/YYYY-MM-DD.md`
- link to source notes

Requires the owner's approval:

- creating external task-system records
- changing project state
- moving/deleting notes
- sending a digest anywhere

## Stale Filed-Item Cull

Resurface filed interest-stubs that have gone stale, so they don't accumulate as vault bloat. The agent **surfaces**; the owner **decides**. Never delete or move a note on your own in this lens.

### Find the watch-set

Find interest-stubs by **scanning frontmatter** — do **not** rely on Dataview (a headless/CLI agent cannot render it). The watch-set is every note whose frontmatter has `status: interested`.

```bash
# from the vault root — list candidate stubs
grep -rl --include='*.md' -E '^status:[[:space:]]*interested[[:space:]]*$' . 2>/dev/null
```

The grep matches the line anywhere, so confirm each hit is a **real interest-stub**: the `status: interested` must sit in the note's own YAML frontmatter (between the opening `---` fences at the top), not in body text or a fenced example. Exclude workflow/spec/template files where it appears as an example — e.g. `system/skills/intake-extraction.md`.

### Staleness rule

A stub is **stale** when `status: interested` **and** the most recent of (`last_reviewed`, `created`) is more than **8 weeks** before the review date.

- If `last_reviewed` is absent or empty (legacy or freshly-created stubs), use `created`.
- If `created` is absent too, use the file's modification time.

### Output

List stale stubs under a `Stale Filed Items — Keep / Act / Cull` section. For each:

- title as a `[[wikilink]]`
- source (`source:` frontmatter or a `Source:` line)
- age stated plainly ("11 weeks, untouched")
- a one-line recommendation

### Decisions (the owner picks per item)

- **Act** — they will buy/play/read/use it → graduate the stub: change `status` off `interested` (e.g. `acquired` / `active`) or fold it into a durable note. Leaves the watch-set.
- **Keep watching** — still interested, not now → set `last_reviewed: <review date>` so it won't resurface for another 8 weeks. (The anti-nag reset.)
- **Cull** — done with it → delete the stub, or archive it under `x/archive/intake/YYYY-MM/`. **Only after an explicit yes.**

Frontmatter is agent-owned — the owner does not hand-edit it. Apply the chosen action only after they decide; never auto-delete.

### Acceptance checklist (self-verify before declaring the cull done)

- [ ] Stale stubs were found by frontmatter scan for `status: interested`, not by rendering Dataview.
- [ ] Staleness compared the later of `last_reviewed`/`created` (fallback to file mtime) against an 8-week threshold from the review date.
- [ ] The `Stale Filed Items — Keep / Act / Cull` section lists each stale stub with title, source, age, and a one-line recommendation.
- [ ] No note was deleted or moved without explicit approval.
- [ ] On "keep watching", `last_reviewed` was set to the review date; on "act", `status` was graduated off `interested`.

## Verification

Before finishing:

- source every major claim to a note/path
- label uncertain inferences
- keep action items out of external systems unless the owner approves routing
- commit vault changes from the vault root if files were edited
- append a line to [[system/logs/skill-usage-log|Skill Usage Log]]
