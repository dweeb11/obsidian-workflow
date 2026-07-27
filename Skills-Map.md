# Skills Map

This is the portable process map for the vault. It indexes repeatable workflows that AI tools should understand. Keep this file tool-agnostic; tool-specific details belong in adapter files.

Related maps:
- [[Me]] — who you are and how to work with you
- [[Vault-Map]] — how to navigate the vault
- [[system/memory/tag-reference|Tag Reference]] — active tag vocabulary and namespace hygiene

## Purpose

A skill is a repeatable process written down in plain text. Skills should be portable across AI tools and should make future agents faster, safer, and less likely to improvise badly.

This file is the index. When a process gets large, move the full procedure to its own note and link it here.

## Load Policy

Use this file as a registry, not a context dump. For common tasks, prefer `system/scripts/context-router.py <profile>` first.

- Small note edits: do not read this file unless a repeatable workflow is involved.
- Workflow tasks: read only the matching entry here, then read the linked workflow note under `system/skills/` when one exists.
- Map or skill maintenance: read this file, [[Vault-Map]], `AGENTS.md`, and `system/skills/map-maintenance.md`.
- Voice/preference work: read [[Me]] in addition to the relevant workflow.

## Workflow Registry

The table below is generated from `system/skills/registry.json`. To change it, edit
that file and run `python3 system/scripts/generate-adapters.py` — the same command
regenerates every per-tool adapter, so the registry, this index, and the tool
directories can never disagree.

<!-- BEGIN GENERATED: skills-registry -->
<!-- GENERATED FILE -- do not edit by hand. | Source: system/skills/registry.json | Regenerate: python3 system/scripts/generate-adapters.py -->

| Skill | Trigger phrases | Context profile | Contract |
|---|---|---|---|
| Today (Setup) | "set up today's note", "start today's note", "run daily setup" | `daily` | [[system/skills/daily-capture|daily-capture]] |
| Close Day (Close) | "close out today", "close the day", "process today's note", "run close-day" | `daily` | [[system/skills/daily-capture|daily-capture]] |
| Intake Extraction Workflow | "process clippings", "process intake", "extract from clippings" | `intake` | [[system/skills/intake-extraction|intake-extraction]] |
| Vault Synthesis Workflow | "write a synthesis note", "synthesize these notes", "make a durable note from this" | `synthesis` | [[system/skills/vault-synthesis|vault-synthesis]] |
| Wiki Index Workflow | "update the folder index", "create an _index.md", "refresh the wiki index" | `index` | [[system/skills/wiki-index|wiki-index]] |
| Rock Tumbler Workflow | "tumble this idea", "pressure-test this idea", "help me develop this thought" | `synthesis` | [[system/skills/rock-tumbler|rock-tumbler]] |
| Vault Janitor Workflow | "clean up the vault", "run a hygiene pass", "vault maintenance" | `default` | [[system/skills/vault-janitor|vault-janitor]] |
| Weekly Review Lens | "weekly review", "review my week", "second pass over the week" | `synthesis` | [[system/skills/weekly-review-lens|weekly-review-lens]] |
| Map Maintenance Workflow | "update the maps", "the vault conventions changed", "fix stale workflow truth" | `map` | [[system/skills/map-maintenance|map-maintenance]] |
<!-- END GENERATED: skills-registry -->

Not workflows, but common enough to route here:

| Trigger / Task | Minimal context profile | Detailed procedure |
|---|---|---|
| Small note edit, typo, narrow formatting fix | `default` | Target note only |
| Your voice, preferences, boundaries | `voice` | [[Me]] |

## Global Rules for Vault Work

- Read [[Me]] before doing personal or preference-sensitive work.
- Read [[Vault-Map]] `## Agent Quickstart` before creating, moving, or editing vault notes. Read deeper sections only when they are relevant to the task.
- Preserve wikilinks, Dataview blocks, tags, and existing note style.
- Search before creating duplicate notes.
- For new notes, prefer the ACE grammar documented in [[Vault-Map]]: `+` for intake, `atlas/` for knowledge/people/sources, `calendar/` for dated records, `efforts/` for active work, and `system/` for automation. ACE folders are lowercase.
- Ask before destructive edits, mass moves, or folder restructuring.
- Read [[system/memory/tag-reference|Tag Reference]] before adding or normalizing tags; prefer existing namespaces and update the reference when a new namespace becomes durable.
- Treat `Proposed Next Actions`, `Candidates`, and `Routed Follow-ups` in synthesis/audit notes as routing surfaces, not hidden task lists: preserve them as vault-local candidates unless the owner explicitly asks for an external action in the current conversation.
- Always commit vault changes from the vault root after writing.
- After a real run of any named workflow below (not a dry-run or ordinary chat), append one line to [[system/logs/skill-usage-log|Skill Usage Log]]: `YYYY-MM-DDTHH:MM:SS | **skill-slug** | one-line note`. This is the evidence trail for future usage audits — see each workflow's Verification step.

## Vault Synthesis Workflow

**Purpose:** Turn raw notes, generated briefs, stale project material, or research dumps into durable synthesis without losing source trails or hiding action items.

**Workflow note:** [[system/skills/vault-synthesis|Vault Synthesis Workflow]]

**Template:** `system/Templates/synthesis-note.md`

**Core rule:** Obsidian stores synthesis/context; external follow-through only happens when the owner explicitly asks in the current conversation.

## Wiki Index Workflow

**Purpose:** Create or update `_index.md` pages as wiki-style navigation and re-entry surfaces, not dashboards.

**Workflow note:** [[system/skills/wiki-index|Wiki Index Workflow]]

**Template:** `system/Templates/wiki-index.md`

**Core rule:** Use Start Here/Main Areas tables and Dataview for navigation. Preserve cleanup/action items as vault-local candidates unless the owner explicitly asks for an external action.

## Daily Capture Workflow

**Purpose:** Capture raw daily material and route it during Close — the day-to-day raw capture and cleanup surface, not a dashboard.

**Workflow note:** [[system/skills/daily-capture|Daily Capture / Close-Day Workflow]] — this is the single canonical contract for section anatomy, Setup, and Close. Do not duplicate its procedure here; read the note directly.

**Location:** The active note lives at the vault root as `YYYY-MM-DD.md`; `calendar/daily notes/YYYY/YYYY-MM-DD.md` is the archive Close produces.

## Close-Day Workflow

**Purpose:** Convert the raw Daily Capture note into a preserved archive, routed vault notes, and a clean routing trail.

**Workflow note:** [[system/skills/daily-capture|Daily Capture / Close-Day Workflow]] (Close operation) is the single canonical procedure — including the archive/appendix shape, person and meeting routing, and the interactive-vs-autonomous confirmation gate. Do not duplicate its procedure here; read the note directly.

**Do not:**

- Rewrite creative or personal notes into corporate prose.
- Move notes across major folders without a clear reason.

## Meeting Notes Workflow

**Purpose:** Preserve meeting context in durable notes.

**Location:** `calendar/meetings/`

**Naming:** `YYYY-MM-DD - Meeting Name.md`

**Guidelines:**

- Keep meeting titles human-readable.
- Link people with wikilinks when useful.
- Extract action items clearly.
- Prefer concise notes with enough context to be useful later.

## People Pages Workflow

**Purpose:** Maintain useful context about people without turning the vault into a creepy CRM.

**Location:** `atlas/people/`

**Template:** `system/Templates/Person CRM.md`

- Use properties to distinguish context, e.g. `contexts: [personal]` vs `contexts: [work]`.

**Guidelines:**

- Add durable facts, collaboration context, and follow-up-relevant notes.
- Avoid dumping private or sensitive details unless the owner explicitly asks.
- Link from meeting notes when helpful.

## Research Note Workflow

**Purpose:** Turn research into durable knowledge, not just a clipping dump.

**Template:** `system/Templates/research-brief.md`

**Guidelines:**

- Prefer synthesis over pasted source text.
- Cite sources with links.
- Link to related vault notes.
- Distinguish fact, interpretation, and recommendation.
- If a topic is exploratory, capture open questions explicitly.

## Clippings Workflow

**Purpose:** Store source material for later use.

**Location:** `+/clippings/`

**Guidelines:**

- Keep original source links when available.
- Do not treat clippings as synthesized notes.
- If a clipping becomes important, create or update a durable note in `atlas/` or a relevant `efforts/` area and link back to the clipping/source.

## Intake Extraction Workflow

**Purpose:** Classify raw `+/clippings/` items, extract durable signal, preserve source trails, and archive or delete the original only when the disposition is clear.

**Workflow note:** [[system/skills/intake-extraction|Intake Extraction Workflow]]

**Core rule:** Durable homes listed in the workflow are examples, not a closed taxonomy. Create new folders or indexes when a repeated pattern merits new organization.

## Vault Janitor Workflow

**Purpose:** Maintain vault hygiene without turning cleanup into a silent rewrite.

**Workflow note:** [[system/skills/vault-janitor|Vault Janitor Workflow]]

**Report location:** `system/reports/vault-janitor/YYYY-MM-DD-<scope>.md`

**Core rule:** The janitor may fix narrow, reversible hygiene issues and report bigger decisions. Mass moves, deletes, or taxonomy changes need the owner's approval.

## Map Maintenance Workflow

**Purpose:** Keep the portable AI operating-system files useful and non-contradictory.

**Workflow note:** [[system/skills/map-maintenance|Map Maintenance Workflow]]

**Core files:**

- [[Me]] — identity and preferences
- [[Vault-Map]] — vault navigation
- [[Skills-Map]] — process map
- `AGENTS.md` — the thin agent front door

**Core rule:** Portable truth lives in the maps and skill files. Tool adapters point at them instead of duplicating behavior.

## Rock Tumbler Workflow

**Purpose:** Find and pressure-test interesting ideas without rewriting them into generic AI prose.

**Workflow note:** [[system/skills/rock-tumbler|Rock Tumbler Workflow]]

**Core rule:** The agent should nominate interesting targets from intake, daily notes, clippings, and active efforts, then ask diagnostic questions, surface risks, and offer alternatives. The owner keeps authorship and taste.

## Weekly Review Lens

**Purpose:** Use AI as a second-pass review lens after your own week, not as the author of the week.

**Workflow note:** [[system/skills/weekly-review-lens|Weekly Review Lens]]

**Core rule:** Surface missed loops, repeated friction, decisions, stale promises, and candidate extractions. Do not manufacture a new weekly digest obligation.

## Obsidian CLI Workflow

When Obsidian is running, the CLI is available with:

```bash
# macOS
PATH="$PATH:/Applications/Obsidian.app/Contents/MacOS" obsidian <command>

# Linux (AppImage or package install; adjust to where Obsidian landed)
PATH="$PATH:/opt/Obsidian" obsidian <command>
```

```powershell
# Windows (PowerShell)
$env:PATH += ";$env:LOCALAPPDATA\Obsidian"
obsidian <command>
```

If `obsidian` is already on your `PATH`, drop the prefix and just call it.

Prefer the Obsidian CLI for:

- searching notes
- checking tags
- reading by wikilink name
- checking backlinks
- finding unresolved links
- moving notes
- querying tasks

Use direct file tools for:

- creating structured files
- complex multi-section edits
- bulk content writes
