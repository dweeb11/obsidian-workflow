# A First Week With This Vault

> [!info] This is fiction, and it's deletable
> Priya Raman does not exist. Neither does their flat, their contractor, or the tile shop. This is the one worked example in the repo, and it lives entirely inside this file — every note it discusses is quoted here as a fenced block, so nothing of Priya's is filed anywhere. `atlas/`, `+/`, `efforts/`, and `calendar/` stay genuinely empty.
>
> If you don't want it, delete this file. You lose nothing else.

The eight workflow docs in `system/skills/` are each written as a procedure. Read one on its own and it's clear enough. What none of them can show you is the part that actually matters: they feed each other. A capture routed on Monday is what the weekly lens has to look at on Sunday; an idea seed carried forward for three days is what the rock tumbler works on; the durable note the tumbler leads to is what makes the folder worth indexing.

That loop is the thing an empty vault can't demonstrate, so here is one week of it, invented.

**The persona.** Priya Raman (they/them) bought a small 1950s flat in February and is renovating the kitchen over the spring on a budget that doesn't have much give in it. They are not a builder. They have a normal job that has nothing to do with any of this. They installed Obsidian, cloned this repo, filled in `Me.md`, and pointed an agent at it on Monday morning.

**The week:** Monday 2026-03-02 to Sunday 2026-03-08.

**The arc:** `daily-capture` → `intake-extraction` → `rock-tumbler` → `vault-synthesis` → `wiki-index` → `weekly-review-lens`.

---

## Monday — the first daily note is the worst one, and that's fine

Priya asks the agent to set up today's note. Setup gathers context: yesterday's archive (nothing), the last seven days (nothing), meeting notes (nothing), the calendar (not connected yet). Every input is empty, so the honest output is a nearly empty note.

```markdown
---
tags:
  - type/capture
---
# 2026-03-02

## Morning Briefing

**Carried forward:**

**Today's meetings:**

**Threads to close:**

**Vault energy:** First day in the vault — nothing to draw on yet.

## Inbox / Capture

## ToDo
- [ ] Call the building manager about where the water shutoff is
- [ ] Measure the alcove properly, including the skirting

## Meetings
### Site walkthrough — Tomas Berg

## Random Thoughts

## End of Day Log
```

This is the least impressive artifact the workflow ever produces, and it's worth staring at for a second. The agent did not invent a carried-forward item to make the briefing look full. It did not write a "keep pushing" line under Vault energy. `## Morning Briefing` has three empty fields because three of the four sources genuinely had nothing in them, and an agent that fills them anyway is an agent that will keep filling them anyway once the sources are real.

The two ToDo items and the meeting header are Priya's, typed in by hand. The seeded meeting subsection is empty on purpose — [[system/skills/daily-capture|Daily Capture]] seeds headers at Setup and never writes bodies.

By evening the note has grown:

```markdown
## Meetings
### Site walkthrough — Tomas Berg
- Tomas came at 2. Contractor, did Ellen's bathroom last year, that's how I found him.
- The wall between the kitchen and the hall is load-bearing. He was certain, tapped it,
  said the flats above are stacked on it. So the "open it up" version is off the table
  unless I want an RSJ and a structural engineer, which I don't.
- Sink can move to the window wall but the waste run would have to cross the room. He
  said doable, not cheap, and it'd mean lifting the floor.
- Fuse box is original. 5 circuits. He said an electrician will want to look before
  anything with a new oven happens.
- Quote by Friday.

## Random Thoughts
- What if I did this in two phases? Cabinets and worktop now, floor and the sink move
  in the autumn when there's money again. Half the disruption at once.
- Everyone keeps asking if I'm doing it for resale. I'm not planning to sell. I don't
  know why that keeps coming up.

## ToDo
- [ ] Call the building manager about where the water shutoff is
- [x] Measure the alcove properly, including the skirting
```

Priya asks the agent to close out the day. Close is where the routing decisions live, and this one has a good one in it.

**The judgment call.** Everything Tomas said arrived in the same conversation, but it doesn't all belong in the same place. Two facts — *the hall wall is load-bearing* and *the fuse box is original, five circuits* — are true about the flat, and they will still be true in ten years when this renovation is a thing that happened. Those are durable knowledge: `atlas/`. The quote timing, the phasing question, the waste-run cost: those are true about *this project*, and they stop being interesting the day it's finished. That's work in motion: `efforts/`.

[[system/skills/intake-extraction|Intake Extraction]] states the principle the other way round, and it's the same principle: route by what the material is *for*, not what it's *about*. All of it is "about" the kitchen. Only some of it is *for* anything after the kitchen.

So Close writes three things. A person page, created from `system/Templates/Person CRM.md`, because Tomas was mentioned with substance rather than in passing:

```markdown
---
tags:
  - type/person
contexts:
  - personal
company: Berg Building
role: Contractor
status: active
relationship: Found via Ellen — did her bathroom in 2025
last_contact: 2026-03-02
next_followup: 2026-03-06
followup_reason: Quote promised by Friday
priority: normal
---

# Tomas Berg

## Snapshot

**Role:** Contractor
**Context:**
**Relationship:**
**Relevant context:**
**How to work with them:**

## Notes

### 2026-03-02

- Site walkthrough. Confirmed the hall wall is load-bearing; sink move to the window
  wall is possible but means crossing the waste run and lifting the floor. Flagged the
  original fuse box as an electrician job before any new oven.
- Quote promised by Friday.
```

The `## Snapshot` block is empty because nothing in one walkthrough earns a durable claim about how to work with someone. It fills in over months, or it doesn't.

A meeting note at `calendar/meetings/2026-03-02 - Site walkthrough - Tomas Berg.md`, holding the full body with `[[Tomas Berg]]` linked. And the appendix, appended to the raw note before it's archived:

```markdown
---

## Daily Cleanup Routing

Original daily capture preserved above. Routed/triaged items below so the raw note
remains recoverable if anything was missed.

### Carry Forward / Open Loops
- [ ] Call the building manager about where the water shutoff is
- Idea seed: two-phase renovation (cabinets now, floor + sink in autumn)

### Created / Updated Vault Notes
- [[atlas/people/Tomas Berg|Tomas Berg]] — created, first dated entry
- [[calendar/meetings/2026-03-02 - Site walkthrough - Tomas Berg|Site walkthrough]] — created

### Needs Review
- (empty — interactive close, the surname question was answered at the gate)

### Possible Follow-ups
- The load-bearing wall and the fuse box rating want a durable home in atlas/, not just
  a meeting note. Not promoting today — one day's mention isn't a note yet.

### Archive Only
- "Everyone keeps asking if I'm doing it for resale." Left in the archive. It's a real
  thought but it isn't an action and it isn't knowledge.
```

Then the note moves from the vault root to `calendar/daily notes/2026/2026-03-02.md`, and the root is clear for tomorrow.

Two restraints there are worth naming, because both are the workflow declining to do something an eager agent would do. The load-bearing wall fact was *identified* as wanting an atlas note and then not promoted — Close promotes at most a single thought that has clearly matured today, and one mention in one meeting is not maturity. And the resale remark went to `### Archive Only` rather than becoming a task. [[system/skills/daily-capture|Daily Capture]] is explicit that random thoughts don't get auto-promoted into obligations. It comes back on its own on Thursday, which is a much better reason to act on it.

---

## Tuesday — the first note that has something to carry

Same Setup procedure, entirely different output, because now one of the four sources is non-empty.

```markdown
# 2026-03-03

## Morning Briefing

**Carried forward:**
- Call the building manager about the water shutoff ← from [[2026-03-02]]

**Today's meetings:**

**Threads to close:**
- Tomas's quote, promised Friday — [[2026-03-02 - Site walkthrough - Tomas Berg]]

**Vault energy:** Circling whether to split the job into two phases.

## Inbox / Capture

### Idea Seeds To Revisit
- [ ] Two-phase renovation — next: work out what phase two actually costs to *restart*

## ToDo
- [ ] Call the building manager about where the water shutoff is
```

The measuring task is gone, because it was checked off. The shutoff call came across unchecked and in Priya's own words. The idea seed landed in `## Inbox / Capture` as an ordinary unchecked task with a small next action attached — not a callout, not a prompt to reflect, just a checkbox that will keep showing up until Priya ticks it.

That's the whole carry-forward mechanism, and it's the first moment the vault does something a blank file couldn't.

---

## Wednesday — intake, and five different answers to "what is this worth?"

Priya has been clipping things all week into `+/clippings/` with the Obsidian web clipper: six items, no commentary on most of them. They ask the agent to process intake.

[[system/skills/intake-extraction|Intake Extraction]] is explicit that the goal is not to empty the folder. It's to decide what each item is worth. Six items, five different verdicts:

| Item | Class | Why |
|---|---|---|
| `fenwick-tiles-zellige.md` — a shop page, one photo, price | `interest-stub` | Clipped because they might buy it. No idea in it to extract, but discarding it throws away the intent. |
| `planning-a-kitchen-layout.md` — long blog post | `extract` | Three genuinely reusable constraints. Becomes a durable note. |
| `small-kitchen-mistakes.md` — mostly the same advice | `merge` | Repeats the post above but adds one number worth having. Folds into that note; doesn't get its own. |
| `fenwick-tiles-zellige-2.md` | `discard` | Same page clipped twice. Obvious junk, deleted. |
| `forum-wylex-fusebox-thread.md` | `source-only` | Directly about their fuse box model, but three quarters inapplicable. Worth keeping, not worth synthesizing yet. |
| `quote-screenshot.md` — a photo of a second quote | `ask` | Left where it is, question reported. |

The last one is the interesting one. It's a screenshot of a rival quote with a person's name and a number on it. Is that a person page? A decision record? Something Priya would rather not have sitting in plain text? The workflow's answer to all three is the same: don't guess. `ask` means report the question and move nothing.

The extract, with the merge already folded in:

```markdown
---
tags:
  - type/topic
last_touched: 2026-03-04
---

# Kitchen Layout Rules Of Thumb

Source: [[x/archive/intake/2026-03/planning-a-kitchen-layout|planning-a-kitchen-layout]]

- Work triangle: sink, hob, fridge. Total of the three legs under about 8m, no leg
  under 1.2m.
- Leave 900mm of uninterrupted worktop next to the hob on the handle side.
- Walkway between opposing runs: 1200mm minimum if two people ever pass, 1000mm if
  it's a galley one person uses.

## Source Trail

- 2026-03-04 — extracted from [[x/archive/intake/2026-03/planning-a-kitchen-layout|planning-a-kitchen-layout]]
- 2026-03-04 — 1200mm walkway figure merged in from [[x/archive/intake/2026-03/small-kitchen-mistakes|small-kitchen-mistakes]]
```

And the stub, which is doing something subtler:

```markdown
---
status: interested
interest_type: maybe buy
source: https://example.com/fenwick/zellige-white
created: 2026-03-04
last_reviewed:
tags:
  - type/source
---

# Zellige Tile — Fenwick Tiles

Source: https://example.com/fenwick/zellige-white

Status: interested / maybe buy

Why saved: clipped as a possible future purchase. No deeper synthesis yet.

## What To Check Later
- price / availability
- whether the handmade variation is a problem behind a hob
- lead time — these are usually made to order
```

`last_reviewed` is deliberately empty. That isn't an oversight; it's what makes the stale-item cull work later. A stub with `status: interested` and no `last_reviewed` ages from its `created` date, and after eight weeks the weekly lens drags it back out for a keep / act / cull decision. Filling `last_reviewed` at creation would silently buy it two months of invisibility.

All four survivors are archived to `x/archive/intake/2026-03/`, and `+/clippings/` is left holding exactly one file — the screenshot nobody could classify. The run was six items, so the agent summarised in chat rather than writing a report under `system/reports/`, and appended one line to the usage log.

---

## Thursday — the tumbler, which does not answer anything

The two-phase seed has now carried forward three mornings running. Priya hasn't ticked it off and hasn't acted on it, which is exactly the signal [[system/skills/rock-tumbler|Rock Tumbler]] exists for: an idea kept alive long enough to be worth pressure-testing. They ask the agent to tumble it.

What comes back is questions. Not a recommendation, not a pros-and-cons table, and above all not a paragraph in Priya's voice explaining what they think.

```markdown
## Rock Tumbler Notes — 2026-03-05

**Imagine**
- What's the version where phase two is the *good* part rather than the leftover part?
- Is there a split that isn't cabinets-then-floor? Sink move first, everything else
  later, is a different bet with a different failure mode.

**Discern**
- The claim underneath this is "half the disruption at once." Is that actually true, or
  is it *twice the disruption, spread out*? Tomas said the sink move means lifting the
  floor. Does phase two mean pulling up a floor you laid in phase one?
- What are you assuming about autumn? Phase two costs whatever it costs *plus* a
  restart — getting a contractor back, a second set of days off, second delivery.
- Where's this weakest? If phase two never happens, what have you got? Answer that
  before the phasing question, because it's the outcome you're actually risking.

**Integrate**
- You wrote on Monday that people keep asking if this is for resale and you don't know
  why it keeps coming up. Is the phasing question the same question wearing a hat? A
  two-phase plan is a bet you'll still be here in the autumn.
- Nothing in the vault yet records what's structurally fixed about the flat. The
  load-bearing wall and the fuse box are both constraints on any version of this. That
  probably wants to exist before the plan does.
```

Priya's reply, in their own note, in their own words:

> Phase two would mean lifting a floor I just paid to lay. That's not half the disruption, that's the same disruption twice and a floor I've damaged. Doing it in one go. And yes, the resale thing is the same question — I keep answering it as though someone's asking me to justify staying.

The agent wrote none of that. It asked whether the disruption claim was true and pointed at Monday's note; Priya did the thinking and the writing. That's the questions-only guardrail working, and it's the reason the paragraph is worth having — a version of it generated by an agent would read fine and mean nothing.

The tumbler's last bullet is the useful by-product: it noticed the vault has no home for the constraints, which is what Friday is.

---

## Friday — synthesis, and the note that outlives the project

Tomas's quote arrives. The electrician has been round and confirmed the consumer unit needs replacing before a new oven goes in. Priya asks the agent to turn what's now known about the flat into a durable note.

Note where it goes. Not `efforts/kitchen/`, where the quote and the plan live. `atlas/home/`, because none of this stops being true when the kitchen is finished.

```markdown
---
tags:
  - type/synthesis
last_touched: 2026-03-06
---

# The Flat — What's Behind The Walls

> [!info] Memory Card
> **What this is:** The structural and services facts about the flat, gathered during
> the 2026 kitchen job. Constraints on any future work, not a plan for this one.
> **Connects to:** [[Tomas Berg]], [[Kitchen Layout Rules Of Thumb]]
> **Last touched:** 2026-03-06

## Scope / Question

What is actually fixed about this flat, as opposed to chosen? Written down once so the
next project doesn't rediscover it.

## Short Answer

The hall/kitchen wall is load-bearing — the flats above stack on it. Anything that
opens it up needs an RSJ and a structural engineer. Treat it as fixed.

The soil stack is on the bathroom side. Moving the sink to the window wall means the
waste run crosses the room under the floor: possible, quoted, but it couples any sink
move to a floor lift. Those two decisions are one decision.

The consumer unit is the original Wylex, five circuits, no RCD. It has to be replaced
before a new oven circuit goes in. That's a fixed prerequisite for anything electrical,
not a kitchen line item.

## Sources Considered

| Source | Used for |
|---|---|
| [[calendar/meetings/2026-03-02 - Site walkthrough - Tomas Berg\|Site walkthrough]] | Wall, waste run, fuse box flag |
| [[x/archive/intake/2026-03/forum-wylex-fusebox-thread\|Wylex forum thread]] | Model context; most of it didn't apply |
| [[atlas/people/Tomas Berg\|Tomas Berg]] | Quote detail, 2026-03-06 |

## Decisions / Working Rules

- Sink move and floor lift are one decision, never two.
- Consumer unit replacement precedes any new circuit. Not negotiable, not a preference.

## Open Questions

- Is the wall load-bearing along its whole length, or only the section under the stack?
  Nobody has actually checked the far end.

## Routed Follow-ups

| Action | Route |
|---|---|
| Get the far end of the wall checked | Surfaced here; belongs to efforts/kitchen when the work starts |
| Water shutoff location still unknown | Still an open ToDo in the daily notes since 2026-03-02 |
```

The forum thread is cited as a source and stays archived rather than being pulled in wholesale — it was classified `source-only` on Wednesday, and synthesis is where that classification pays off. And the open question is left open. An agent that resolved "is the whole wall load-bearing?" by inference would have produced a confident sentence about a wall nobody has looked at.

---

## Saturday — the folder earns an index

`atlas/home/` now holds four notes: the flat constraints, the layout rules of thumb, the tile stub, and a short note on the boiler service history that Priya wrote on Tuesday and hasn't mentioned since. Four is roughly where a folder stops being self-evident, so they ask for an index.

````markdown
---
tags:
  - type/index
last_touched: 2026-03-07
---

# Home Index

> [!info] Memory Card
> **What this is:** Navigation page for `atlas/home/`.
> **Connects to:** [[Tomas Berg]]
> **Last touched:** 2026-03-07

## Start Here

| Note | Use it for |
|---|---|
| [[The Flat — What's Behind The Walls]] | What's structurally fixed. Read before planning any work. |
| [[Kitchen Layout Rules Of Thumb]] | Measurements and clearances, sourced. |

## Breadcrumbs / Ideas

- 2026-03-07 — Boiler service note has no service date in it, which is the only thing
  it needed to have. Related: [[Boiler]]. Status: watch.

## Interest Queue

```dataview
TABLE interest_type, created, last_reviewed
FROM "atlas/home"
WHERE status = "interested"
SORT created ASC
```

## Link / Tag Review

### Routed Follow-ups

- Boiler note is missing its service date — surfaced as a breadcrumb, not fixed here.
````

Two things the index deliberately isn't. It isn't a task board — the boiler problem is a dated breadcrumb with a status, not a checkbox, because [[system/skills/wiki-index|Wiki Index]] draws a hard line at indexes becoming cockpits. And it isn't a summary of the notes it points at; the "Use it for" column says when to reach for each one, which is a different question from what each one says.

The Dataview block is the one place the vault has a real dependency. Without the Dataview plugin enabled it renders as a code block, which is why the README puts it first among the three plugins.

---

## Sunday — the lens, and the things no single day could see

Priya reads back over their own week first. Then they ask the agent for a second pass. This is the ordering [[system/skills/weekly-review-lens|Weekly Review Lens]] insists on: the owner's review leads, the agent's is a second pass over it, and nothing here is an AI-authored weekly digest.

```markdown
# Weekly Review Lens — 2026-03-02 to 2026-03-08

## Signals Worth Keeping
- [[The Flat — What's Behind The Walls]] is the week's most reusable artifact and it
  was a by-product. It came out of a rock tumbler question about a phasing decision,
  not out of anyone setting out to write it.

## Missed Loops
- `+/clippings/quote-screenshot.md` has been sitting classified `ask` since Wednesday.
  Four days, no answer. The classification worked; the question never got asked out loud.
- "Call the building manager about the water shutoff" has carried forward every single
  morning since Monday — five times, unchecked, never re-worded. `daily-intelligence-pass.py`
  flags it too.

## Repeated Friction
- The 1200mm walkway figure was looked up on Wednesday, Thursday, and Saturday. It only
  became findable on Wednesday afternoon when it landed in a durable note; before that it
  lived in a daily note and was effectively gone. Two of those three lookups were the
  cost of not having written it down yet.

## Decisions That Need A Home
- The single-phase decision is real and settled, and it exists only in Thursday's
  `## Random Thoughts`. Once that note is archived it's findable by search and by nothing
  else. It belongs in the efforts note as a decision with its reasoning.

## Candidate Extractions
- [[atlas/people/Tomas Berg|Tomas Berg]] has three dated entries and an empty `## Snapshot`.
  Enough has accumulated to fill it now.

## Stale Filed Items — Keep / Act / Cull
- Nothing stale. The only stub in the vault ([[Zellige Tile — Fenwick Tiles]]) is four
  days old against an eight-week threshold. This section will be empty until late April,
  which is correct and not a failure.
- Note: the frontmatter scan for `status: interested` also matches
  `system/skills/intake-extraction.md` and `system/example-first-week.md`, where the
  string appears inside fenced examples. Both are excluded — the match has to be real
  frontmatter at the top of a real note.

## Open Questions
- Is the far end of the hall wall load-bearing? Raised Friday, still open, and it's a
  question for a person rather than a note.
```

Read those seven sections back and none of them could have come from a single day. The carried task looks reasonable on any one morning and only reads as avoidance on the fifth. The three lookups of the same number are invisible until you can see all three. The decision with no home was made confidently on Thursday and is quietly stranded by Sunday.

That's the loop, and it's the answer to why any of the daily filing was worth doing. The routing isn't tidiness. It's what makes the week legible to a second pass.

---

## The evidence trail

Every workflow that ran appended one line to `system/logs/skill-usage-log.md`. After a week it looks like this:

```markdown
## Log

- 2026-03-02T08:14:03 | **daily-capture** | Setup 2026-03-02 — empty vault, no carry-forward available
- 2026-03-02T21:40:11 | **daily-capture** | Close 2026-03-02 — Tomas Berg page + meeting note created
- 2026-03-03T08:02:55 | **daily-capture** | Setup 2026-03-03 — 1 task + 1 idea seed carried
- 2026-03-04T08:11:20 | **daily-capture** | Setup 2026-03-04
- 2026-03-04T14:22:47 | **intake-extraction** | 6 clippings — 1 extract, 1 merge, 1 stub, 1 source-only, 1 discard, 1 ask
- 2026-03-05T08:09:31 | **daily-capture** | Setup 2026-03-05
- 2026-03-05T19:55:02 | **rock-tumbler** | Two-phase renovation seed — IDI pass, questions only
- 2026-03-06T18:31:44 | **vault-synthesis** | atlas/home/The Flat — What's Behind The Walls
- 2026-03-07T11:05:19 | **wiki-index** | atlas/home/_index.md created (4 notes)
- 2026-03-08T16:48:37 | **weekly-review-lens** | Week of 2026-03-02 — 2 missed loops, 1 homeless decision
```

Ten lines is not a lot of information, and that's the point of it. Six weeks from now it answers "which of these do I actually use" from evidence instead of from memory, and a slug with nothing next to it is a finding. If `wiki-index` has one line ever, the honest read is that the workflow isn't earning its doc.

---

## The two that didn't run, and why

Eight workflows ship. Six appear above. The other two are absent because week one genuinely doesn't trigger them, and a demonstration of them here would be a demonstration of nothing.

[[system/skills/vault-janitor|Vault Janitor]] cleans up what accumulates: broken wikilinks, duplicate stubs, tag drift, an `_index.md` pointing at a note that got renamed, a doc confidently describing a workflow you stopped running months ago. All of those are functions of *time and volume*. After seven days and roughly a dozen notes there is nothing stale, nothing orphaned, and nothing contradictory — the vault's problem in week one is that it's empty, and the janitor has no remedy for empty. The first honest janitor pass is somewhere around month three, or the first time you rename a folder and want to know what you broke.

[[system/skills/map-maintenance|Map Maintenance]] runs when *the system itself* changes — when you alter a folder convention, change what a skill does, add a tag namespace, or notice that `Vault-Map.md` describes something you no longer do. Priya spent the week using the conventions as shipped, so there was nothing to reconcile. Their first real trigger is visible on the horizon, though: they now have three notes carrying photos of the flat with nowhere agreed to put them, and the moment they settle on a convention for that, `Vault-Map.md` has to say so or the next agent will invent a different one. That's map maintenance — the map changing to match reality, deliberately, instead of drifting behind it.

Both of these are worth knowing about before you need them, which is why they ship. Neither is worth faking a run of.

---

## What to take from this

The individual procedures are the boring part. You will adapt them, and you should — the folder names, the sections in the daily note, the eight-week staleness threshold are all just one person's settings.

The part worth keeping is the shape: capture is cheap and lossy, routing at close is where judgment happens, ideas that survive several days earn pressure rather than storage, pressure produces durable notes as a by-product, folders get indexed once they stop being obvious, and a weekly second pass sees the things no single day can. Each step is only worth doing because of the one after it.

Then delete this file.
