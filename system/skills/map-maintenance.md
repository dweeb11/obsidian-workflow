# Map Maintenance Workflow

Use this when the portable AI operating system changes: folder conventions, skill behavior, adapter instructions, assistant preferences, or stale workflow truth.

## Purpose

Keep `AGENTS.md`, `Vault-Map.md`, `Skills-Map.md`, `Me.md`, and related indexes coherent. Future agents should be able to re-enter from the maps without reading old chat history.

## Read First

1. `AGENTS.md`
2. `system/scripts/context-router.py map`
3. `Vault-Map.md`
4. `Skills-Map.md`
5. `Me.md` when preferences, assistant behavior, boundaries, or voice are involved
6. The affected skill files under `system/skills/`

## Canonical Surfaces

| Surface | Owns |
|---|---|
| `AGENTS.md` | Thin vault entry contract for agents. |
| `Vault-Map.md` | Layout, naming, navigation, source-of-truth locations. |
| `Skills-Map.md` | Skill index and workflow routing. |
| `Me.md` | The owner's identity, preferences, boundaries, and voice. |
| `system/skills/*.md` | Detailed portable procedures. |
| Tool adapters | Pointers to the portable maps, not duplicated rules. |

## Rules

- Put durable workflow truth in maps and skill files.
- Keep adapters thin.
- Keep maps section-addressable: quickstart and registry first, detailed procedures in `system/skills/*.md`.
- Remove or warn on stale instructions instead of leaving contradictory rules.
- Search for old wording before declaring a convention updated.
- Update `_index.md` pages when a new durable area needs to be discoverable.

## Automation / Invocation

Manual trigger phrases:

- "update the maps"
- "map maintenance"
- "make this portable"
- "fix the agent docs"

Eligible inputs:

- map files
- skill files
- adapter files such as `AGENTS.md`
- relevant `_index.md` pages

Allowed automatic actions:

- add or revise skill index entries
- add currentness warnings
- remove direct contradictions
- update last-updated notes
- create new `system/skills/*.md` files when the owner has approved the skill direction

Requires the owner's approval:

- changing personal boundaries in `Me.md`
- changing folder grammar
- deleting old docs instead of warning/archive-linking
- editing tool-specific adapters in ways that change agent permissions

## Verification

Before finishing:

- search for contradicted old wording
- confirm new skill links resolve by path/title search
- ensure maps do not duplicate detailed procedures better kept in `system/skills/`
- run `system/scripts/context-router.py default` and the task profile you changed
- commit vault changes from the vault root
- append a line to [[system/logs/skill-usage-log|Skill Usage Log]]
