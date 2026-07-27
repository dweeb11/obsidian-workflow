# Daily Capture / Close-Day Workflow

This is the portable, vault-local contract for daily-note work. Tool-specific skills, prompts, memory, and adapters are **non-authoritative caches**. If they conflict with this note, follow this note and update the cache afterward.

> **CANONICAL.** This note is the source of truth for daily-note work; every tool-specific skill and adapter defers to it. Change it deliberately and in the open — as its own edit, with the vault owner in the loop, in a session where changing the contract is the point. What caused trouble before was the opposite: an **autonomous run** rewriting the contract as a side effect of doing something else, which is how the active daily note once got silently relocated out of the vault root. If a run doing daily-note work concludes this contract is wrong, record that under `### Needs Review` in its routing appendix and carry on under the current rules; don't rewrite the file mid-run.

## Entry path

An agent reaches this contract from the vault's front door:

`AGENTS.md` → routes to → **this note** → which points to → `system/Templates/Daily Note.md`.

This note is self-sufficient for daily-note work. You do not need to load all of `Vault-Map.md` or `Skills-Map.md` to follow it; `Skills-Map` is only an index that points here. The one file you must read alongside this note is the template: `system/Templates/Daily Note.md`.

## Note anatomy

The active note lives at the vault root as `YYYY-MM-DD.md` and has these sections:

| Section               | Purpose                                                                                                                                                           | Filled by                                    |
| --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------- |
| `## Morning Briefing` | Tight orient-in-a-minute view: carried-forward items, today's meetings, threads to close, vault energy                                                            | **Setup**                                    |
| `## Inbox / Capture`  | Links to agent-posted reports, real-world respond-to items, and persistent unchecked idea-seed follow-ups                                                         | Agents and the owner, plus Setup carry-forward |
| `## ToDo`             | The day's prioritized actions plus unchecked ToDo items carried forward from yesterday; older unresolved `#action/next` items can be added when they still matter | **Setup** + the owner during the day         |
| `## Meetings`         | One subsection per real meeting/interview on today's calendar; bodies filled during the day                                                                       | Setup seeds headers; the owner fills bodies  |
| `## Random Thoughts`  | Raw ideas, project sparks                                                                                                                                         | The owner, during the day                    |
| `## End of Day Log`   | Optional journal; never forced, never auto-filled                                                                                                                 | The owner, optionally                        |

Carry-forward tasks come in three buckets, all as ordinary unchecked tasks: yesterday's unchecked `## ToDo` items in today's `## ToDo`, older unresolved actions (`#action/next`) in `## ToDo` when still relevant, and idea seeds in `## Inbox / Capture` under `### Idea Seeds To Revisit`.

## Active note lifecycle

- The active note lives at the vault root as `YYYY-MM-DD.md`.
- **Close** processes the root note and files it to `calendar/daily notes/YYYY/YYYY-MM-DD.md` as the preserved archive.
- **Setup** creates the next active root note from `system/Templates/Daily Note.md`.
- The `calendar/daily notes/` path is the archived/processed record, not the active writing surface.

## Two operations

Daily-note work is two composable operations:

- **Setup** — seed a clean root note, gather context, and prime it for the day.
- **Close** — process today's root note, route its content to permanent homes, archive it.

An autonomous run chains `Close → Setup`. Each is also independently, manually invocable.

**Manual trigger phrases:**

- Close: "close out today," "close the day," "process today's note," "run close-day"
- Setup: "set up today's note," "start today's note," "run daily setup"

A tool may expose these as shorthands; those adapters defer entirely to this contract.

## Read/write boundary

Writes are **vault-local**. Do not create or update records outside the vault — no external task manager, ticket system, reminder app, message, or calendar event — unless the owner explicitly asks in the current conversation.

The one allowed **read-only** external input is the calendar (see *Calendar input* below). Reading the calendar to seed the note is permitted; writing to it is not.

## Calendar input

At Setup, pull today's calendar from the connected calendar integration, if there is one. **Filter to real meetings and interviews only:**

- **Include:** events with at least one other attendee (actual meetings), and any event whose title reads as an interview.
- **Exclude:** all-day events, holidays, OOO/PTO blocks, focus/solo time blocks, and reminders.

If no calendar is connected, or it returns nothing relevant, proceed without calendar entries — never block Setup on the calendar.

Filtered meetings feed two places: the `## Morning Briefing` "Today's meetings" line, and one empty subsection per meeting under `## Meetings`.

## Setup operation

1. Create the active root note `YYYY-MM-DD.md` from `system/Templates/Daily Note.md`.
   - Replace the date placeholder with the real date.
   - Preserve frontmatter.
   - No generic placeholder prose; no "keep pushing" / "keep thinking" block.
2. **Gather context** (parallel reads):
   - Yesterday's archived daily note in `calendar/daily notes/YYYY/YYYY-MM-DD.md` — copy every unchecked task from its `## ToDo` section into today's `## ToDo`, excluding checked/completed items and obvious duplicates. If yesterday's root note is still unprocessed, use that root note as the source instead and surface that it still needs Close.
   - Last ~7 days of archived notes in `calendar/daily notes/YYYY/` — scan their routing appendices for unresolved `#action/next`, recurring names/projects, and open loops that were not already captured from yesterday's ToDo.
   - Recent meeting notes (`calendar/meetings/`) — open follow-ups, decisions awaiting action.
   - Any unprocessed root daily note besides today's — surface it (yesterday may not have been closed).
   - Today's calendar (see *Calendar input*).
3. **Identify signals** from the gathered context: items to carry forward, threads to close, and **vault energy** — what the owner has been circling lately, named directly.
4. **Carry forward:**
   - Yesterday's unchecked `## ToDo` tasks → today's `## ToDo`, preserving the owner's wording where possible.
   - Older unresolved `#action/next` actions → today's `## ToDo` only when they are still relevant and not duplicates of yesterday's tasks.
   - Unchecked idea-seed follow-ups → `## Inbox / Capture` under `### Idea Seeds To Revisit` (see *Idea seed carry-forward*).
   - Drop anything already checked off; never resurrect checked tasks unless the owner explicitly asks.
5. **Prime `## ToDo`** with the highest-signal actions first. Keep all carried-forward yesterday tasks visible as checkboxes; if the list is long, group a short `### Carry Forward` subsection under `## ToDo` rather than hiding overflow elsewhere.
6. **Seed `## Meetings`** with one empty subsection per filtered calendar meeting (`### Meeting Name`); leave bodies blank.
7. **Write the `## Morning Briefing`** (format below).
8. Leave `## End of Day Log` empty.

Do **not** auto-promote yesterday's Random Thoughts into tasks. Leave raw thoughts in the archive unless the owner explicitly asks to keep one warm.

### Morning Briefing format

```markdown
## Morning Briefing

**Carried forward:**
- [Item] ← from [[Source Note]]

**Today's meetings:**
- [Time] — [Meeting/interview title] ([attendees if ≤5])

**Threads to close:**
- [Item] — [[Meeting Note]]

**Vault energy:** [1 sentence — what you've been circling lately, named directly]
```

Keep it tight — the goal is to orient in under a minute, not produce a report. For meetings with more than 5 attendees, omit the attendee list. Write the briefing into the note; an adapter may also echo it to the user.

## Idea seed carry-forward

Idea seeds persist as ordinary unchecked tasks until the owner checks them off. They are the warm input to [[rock-tumbler|Rock Tumbler]] — an idea kept alive long enough to be worth pressure-testing.

Use `## Inbox / Capture` with this shape when there are active seeds:

```markdown
### Idea Seeds To Revisit
- [ ] [[Seed Title]] — next: <small next action>
```

Rules:

- Carry forward only unchecked seed tasks; drop checked ones on the next pass.
- Keep the next action tiny: answer a question, make an outline, sketch one paragraph, or decide to park it.
- Do not create generic prompts or `> [!question]` callouts for seeds.
- Do not invent new seeds during daily setup; seeds arrive from capture and intake, not from the setup pass.

## Close operation

1. Read today's root note. **Preserve the raw note untouched** — never flatten it into a summary, never rewrite the owner's words. Content is *copied* to permanent homes; the original stays intact and is archived in full.
2. **Enrich in place:** wrap proper names that have or deserve a vault note in `[[wikilinks]]`, and apply appropriate tags on the lines where content lives. The archive inherits this enriched version, keeping the graph connected.
3. **Assemble a routing plan; resolve ambiguity according to run mode.** Build the full plan (what gets created/updated/appended/archived).
   - **Interactive run** (the owner is present — e.g. they asked to close out today): present the plan alongside any questions as **one confirmation gate** — do not ask mid-workflow and again at the end. Batch all new-person questions here: for each new person, ask how to classify them and their surname if only a first name is known. Wait for confirmation before writing.
   - **Unattended run** (scheduled, no human to answer): **never block.** Proceed with everything unambiguous. Do **not** guess on judgment calls — for a new person needing classification, an unknown surname, or an ambiguous routing target, skip the speculative write and record the item under `### Needs Review` in the Daily Cleanup Routing appendix for the next interactive pass. Safe machine bookkeeping (dated `## Notes` append to an *existing* person page, tagging, linking, archive-move) proceeds normally.
4. **Route content to homes:**
   - **People:** for a person mentioned with substance, append the day's relevant content as a dated `### YYYY-MM-DD` entry under that person's `## Notes` log in `atlas/people/[Name].md`; bump the page's `last_contact:` frontmatter to the note's date; create the page from `system/Templates/Person CRM.md` if it doesn't exist; tag per the gate answer; link the daily note to the person with `[[Name]]`. See [[system/memory/tag-reference|Tag Reference]] for the namespaces in use. (Frontmatter is agent-owned — the owner does not hand-edit it.) Do not create a page for a one-off name mentioned in passing with no context.
   - **Meetings:** for a substantive meeting (has topics or notes), create `calendar/meetings/YYYY-MM-DD - [Meeting Name].md` with date, attendees, topics, notes/decisions, action items; link people with `[[wikilinks]]`. Drop cancelled/skipped or empty-bodied meeting stubs — don't keep noise.
   - **Matured thread:** a *single* idea in `## Random Thoughts` or `## ToDo` that has clearly become robust enough today → promote it to a permanent home — `atlas/<subject>/` (durable knowledge) or `efforts/<area>/` (active work) — and backlink. Per-day, bounded judgment only. Do **not** run a week-scan here — that belongs to Weekly Review Lens + Vault Synthesis.
     - **Project-implying thoughts are excluded from this rule**, however robust they got today — they take the project-seed path below instead. Robustness is not what promotes an idea to a project page; the owner starting work on it is. Without this carve-out both rules fire on the same thought and contradict each other, since one would create the page the other forbids.
   - **Project seeds:** a thought in `## Random Thoughts` that *implies a project* — something the owner wants to build, ship, or package — is appended as a new `## Section` to `efforts/Project Ideas.md` in the owner's own wording, closing with `*Captured YYYY-MM-DD — [[<daily note>]]*`. Unlike the matured-thread rule this is **not** bounded to one per day, and it does **not** require the idea to be robust yet; naming it once is enough. Do not create a project page, folder, or effort for a seed — graduation to its own page happens when the owner actually starts working on it, not at capture. Distinguish from tasks: a chore or a research errand is not a project seed and belongs in the next day's `## ToDo`.
5. **Append the Daily Cleanup Routing appendix** to the preserved raw note (shape below).
6. **Archive-move** the processed note from vault root → `calendar/daily notes/YYYY/YYYY-MM-DD.md`. Do not delete the root original until the archive write is confirmed.

### Close archive shape

Preserve the original raw note, then append:

```md
---

## Daily Cleanup Routing

Original daily capture preserved above. Routed/triaged items below so the raw note remains recoverable if anything was missed.

### Carry Forward / Open Loops
- Unchecked `## ToDo` tasks carried into the next root note, plus older unresolved `#action/next` tasks, idea seeds, and any explicit user-authored open loops.

### Created / Updated Vault Notes
- People pages, meeting notes, and other vault notes created or updated during this pass.

### Needs Review
- Judgment calls an unattended run deferred rather than guessed: unclassified new people, unknown surnames, ambiguous routing targets. Empty after an interactive close.

### Possible Follow-ups
- Optional candidates to decide on later.
- No external systems changed unless explicitly noted by the owner's current instruction.

### Archive Only
- Items intentionally preserved only in this archive.

### Automation / Cleanup Trail
- Links to reports/logs used during cleanup.
```

## Division of labor (what this workflow does NOT do)

| Behavior | Home |
|---|---|
| Calendar read → today's meetings/interviews into briefing + `## Meetings` | Setup (here) |
| Context scan → carry-forward actions + idea seeds + vault energy | Setup (here) |
| Person mapping + `## Notes` log append, page creation, tagging, linking | Close (here) |
| Substantive meeting → `calendar/meetings/` note | Close (here) |
| A single **non-project** thought/task that clearly matured today → promote | Close (here) |
| A thought that implies a project → seed to `efforts/Project Ideas.md` | Close (here) |
| A seed becoming a real project page/folder | **The owner, when they start the work** (not an agent, not at capture) |
| Week-scan "what's been shaping" → candidate extractions → synthesis | **Weekly Review Lens + Vault Synthesis** (not here) |

## Do not

- Do not flatten the raw daily note into a summary, or lose/rewrite the owner's raw thoughts.
- Do not write to any external system (calendar, tasks, tickets, reminders, messages) — calendar is read-only input, nothing more — without the owner's explicit current instruction.
- Do not turn random thoughts or idea seeds into forcing/probing prompts.
- Do not use generic "keep pushing" / "keep thinking" language.
- Do not list attendees for meetings with more than 5 people.
- Do not move notes across major folders without a clear reason.
- Do not write into the Meetings section bodies at Setup — only seed empty subsection headers.

## Acceptance checklist (self-verify before declaring done)

**Setup produced a note where:**
- [ ] Root note `YYYY-MM-DD.md` exists for the target date, built from the template, frontmatter preserved.
- [ ] `## Morning Briefing` is filled: carried-forward items, today's filtered meetings, threads to close, and a one-sentence vault energy line.
- [ ] `## ToDo` carries forward every unchecked task from yesterday's `## ToDo`, drops checked tasks, and includes any older unresolved `#action/next` items that still matter without duplicating yesterday's list.
- [ ] `## Inbox / Capture` carries forward unchecked idea-seed tasks under `### Idea Seeds To Revisit` when any exist, and drops checked seeds.
- [ ] `## Meetings` has one empty subsection per filtered calendar meeting/interview (or none if the calendar was empty).
- [ ] `## End of Day Log` is empty.
- [ ] No "keep pushing" prose; no events (only meetings/interviews) pulled from the calendar; no external system written.
- [ ] Appended a line to [[system/logs/skill-usage-log|Skill Usage Log]] for this Setup run.

**Close produced an archive where:**
- [ ] The raw note is preserved verbatim above the appendix (enriched with links/tags, never flattened).
- [ ] Each person mentioned with substance has a dated `### YYYY-MM-DD` entry under their `atlas/people/[Name].md` `## Notes` log, `last_contact` bumped, page created if missing, tagged, and `[[linked]]` from the daily note.
- [ ] Each substantive meeting has a note in `calendar/meetings/`; cancelled/empty meetings were dropped.
- [ ] Any single matured thought/task was promoted to `atlas/<subject>/` or `efforts/<area>/` and backlinked (or none qualified) — and no project-implying thought was promoted this way, however robust, since those take the project-seed path.
- [ ] Every project-implying thought in `## Random Thoughts` was seeded to `efforts/Project Ideas.md` with a capture date and daily-note backlink; no project page or folder was created for a seed; chores/research errands went to the next day's `## ToDo` instead.
- [ ] The `## Daily Cleanup Routing` appendix is present and filled; on an unattended run, deferred judgment calls are parked under `### Needs Review` (not guessed).
- [ ] The note now lives at `calendar/daily notes/YYYY/YYYY-MM-DD.md` and the root original is gone.
- [ ] No external systems were touched.
- [ ] Appended a line to [[system/logs/skill-usage-log|Skill Usage Log]] for this Close run.
