# Area Base Workflow

Use this when making a vault area navigable — creating or updating the area's `.base` file.

This workflow replaced the `_index.md` convention on 2026-08-27. Those pages and their template are retired; see *Do not* below.

## Purpose

An area base is a **live** navigation and re-entry surface. Obsidian evaluates its filters at read time, so it cannot drift the way a hand-maintained index did — the failure mode that retired `_index.md` was that it went stale the moment a note was added.

A base is navigation, not a dashboard, task cockpit, or status ledger.

## Read First

1. `AGENTS.md`
2. `Vault-Map.md`
3. `Skills-Map.md`
4. The area's existing `.base`, and the parent area's, if either exists

There is deliberately no template. A base is a short YAML file and the shape below is easier to follow directly than to fill in; a template was one more thing to keep in sync, and keeping it in sync is exactly what failed last time.

## Default File

`_<Area Name>.base` at the root of the area folder. The leading underscore sorts it to the top of the folder; the name is the area in Title Case.

```
atlas/AI/_AI.base
atlas/game design/_Game Design.base
efforts/personal/writing/_Writing.base
```

## Which folders get a base

Every durable ACE area gets one, from the top level down — `atlas/`, `efforts/`, and each durable subject or lane folder beneath them.

**Individual project folders do not.** A project folder holds one canonical note plus its working notes; that is a project, not a browsable set. Orient from the project's `role: canonical` note instead.

A parent area's base covers its children — `file.inFolder("efforts")` is recursive — so a parent and its child areas both having a base is expected, not duplication. The parent answers "what is in this whole area", the child answers "what is in this part of it".

## Output Shape

```yaml
filters:
  and:
    - file.inFolder("<area path>")
    - file.ext == "md"
properties:
  file.name:
    displayName: Note
  note.role:
    displayName: Role
  note.status:
    displayName: Status
  file.mtime:
    displayName: Updated
views:
  - type: table
    name: Start here
    filters:
      and:
        - role == "canonical"
    order: [file.name, file.folder, file.mtime]
    sort:
      - property: file.name
        direction: ASC
  - type: table
    name: All
    order: [file.name, file.folder, file.tags, file.mtime]
    sort:
      - property: file.mtime
        direction: DESC
  # ... area-specific views ...
  - type: table
    name: Untagged
    filters:
      and:
        - file.tags.isEmpty()
    order: [file.name, file.folder, file.mtime]
    sort:
      - property: file.mtime
        direction: DESC
```

**Start here** and **Untagged** are mandatory and keep those names. Start here is the orientation set; Untagged is the hygiene view that surfaces notes which fell out of the tag vocabulary. Untagged goes last.

Everything between them is judgment. Add a view when the area has a real subset someone would want to browse on its own — usually a type tag (`file.hasTag("type/concept")`, `type/tool`, `type/synthesis`, `type/source`) or a status (`status == "interested"` in `_Game Design.base`). Do not add a view per tag that happens to exist.

Adapt the filter and properties to the area. A homogeneous area can narrow on a tag rather than an extension — `_People.base` filters `file.hasTag("type/person")` — and should surface the frontmatter it actually uses (`note.relationship`, `note.stage`) instead of the generic set.

## Canonical Notes

**Start here** is only as good as the frontmatter behind it. A note earns `role: canonical` when it is where you would send someone to orient in the area — the durable topic page, the project note, the current design doc. Not source material, not a synthesis of one conversation, not a note that happens to be recent.

An area with no canonical note has an empty Start here view. That is a finding, not a base to work around: propose which note should carry the role rather than filling the view with something else.

Agents without Obsidian can read the orientation set directly:

```bash
rg -l '^role: canonical' <area path>
```

## Follow-up Routing

A base is YAML, not a note. It cannot carry the Memory Card, `Routed Follow-ups`, or Link / Tag Review sections `_index.md` used to hold. That is a real loss of a surface, so route findings deliberately instead of dropping them:

- **Cleanup the base reveals** — untagged notes, a missing canonical, broken links — goes in the reply to the owner as a vault-local candidate list.
- **Durable area context** belongs in the area's canonical note, not the base.
- **Moves, deletes, archives** — propose; never perform without the owner's explicit approval.

Do not create or update external task-system records (Linear or otherwise) unless the owner explicitly asks in the current conversation.

## Do not

- Do not create `_index.md` pages. The convention and its template were retired 2026-08-27; recreating one silently reintroduces the staleness this replaced.
- Do not hand-maintain a note list in Markdown alongside a base. If the list is worth having, it is a view.
- Do not duplicate Linear task state, or turn a base into a cockpit or a task rollup.
- Do not add a Dataview block to do a job a view already does.

## Automation / Invocation

Manual trigger phrases:

- "make this area navigable"
- "create a base for this folder"
- "refresh the index"

Eligible inputs:

- a durable ACE area with no `.base`
- an existing base whose views no longer match how the area is used
- an area whose Start here view is empty or whose Untagged view has grown

Allowed automatic actions:

- create or update `_<Area Name>.base` in the shape above
- add, remove, or reorder views to match the area's real subsets
- fix a filter that references a renamed folder, tag, or property

Requires owner approval:

- adding `role: canonical` to a note, or removing it
- restructuring the folder the base describes
- deleting an existing base instead of updating it

## Verification

Before finishing:

- open the base in Obsidian and confirm every view returns what it claims — an empty view is either a real finding or a broken filter, and the two must not be confused
- confirm Start here lists the notes you would actually hand someone first
- confirm the folder path in `filters` matches the base's real location
- check Untagged, and report what is in it rather than silently tagging
- confirm no `_index.md` was created or left behind in the area
- append a line to [[system/logs/skill-usage-log|Skill Usage Log]]
