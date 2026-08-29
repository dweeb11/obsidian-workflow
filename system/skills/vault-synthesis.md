# Vault Synthesis Workflow

Use this when turning raw notes, generated briefs, research dumps, audits, stale project material, or high-signal AI conversations into a durable Obsidian synthesis note.

## Conversation Sources

Treat a chat conversation as just another source type. Chronicle a conversation here only when it has future retrieval value — durable decisions, reusable workflow/skill design, architecture or operating-model changes, project context future agents need, or preference updates. Do not synthesize routine command output or low-signal troubleshooting with no reusable lesson.

Destination follows the normal area rules below (e.g. `atlas/<topic>/` for evergreen concepts after synthesis, or the relevant `efforts/<project>/research/` for project-specific decisions). Route any resulting map/skill changes through [[system/skills/map-maintenance|Map Maintenance Workflow]].

Trigger phrases such as "chronicle this," "save this conversation," or "capture this decision trail" map here.

## Role Boundary

Obsidian is the thinking, synthesis, source-trail, and re-entry layer. Actionable follow-ups stay in the vault — surfaced in the note, not hidden. Do not route follow-ups to an external task system unless the owner explicitly asks in the current conversation.

## Read First

1. `AGENTS.md`
2. `Vault-Map.md`
3. `Skills-Map.md`
4. `system/memory/tag-reference.md`
5. The relevant area `_index.md`, if one exists

## Output Shape

Prefer `system/Templates/synthesis-note.md` for new synthesis notes. A durable synthesis note should usually include:

- a concise Memory Card
- a source trail / reading pack
- currentness warning if the sources may be stale or superseded
- synthesized takeaways in the owner's language, not consultant prose
- explicit boundaries: what this note is and is not
- Link / Tag Review
- Routed Follow-ups

## Currentness Warnings

Add a currentness warning when a note is historical, generated, stale, or based on assumptions that may have changed.

Use this pattern:

```md
> [!warning] Currentness
> This note is useful as source/history, but it is not the current operating model. Start from [[Current Note]] before acting on it.
```

## Link / Tag Hygiene

- Apply obvious wikilinks directly.
- Preserve source paths and recovery trails.
- Preserve Dataview blocks unless intentionally changing their behavior.
- Read `system/memory/tag-reference.md` before adding tags.
- Avoid creating new tag namespaces unless they are durable enough to document.

## Follow-up Routing Rule

Treat `Proposed Next Actions`, `Candidates`, and `Routed Follow-ups` as routing surfaces — all vault-local.

| Follow-up type | Action |
|---|---|
| New actionable work | Surface it in the note's follow-ups. If it's a raw idea worth developing, keep it warm as an idea seed for [[rock-tumbler\|Rock Tumbler]]. |
| Needs a decision before it is work | Put the question in the note as a decision gate. |
| Non-actionable context | Keep it in Obsidian as context. |
| Archive/move/delete proposal | Surface it; do not move/delete without explicit approval. |

Do not create or update external task-system records unless the owner explicitly asks in the current conversation.

## Do Not

- Rewrite creative/personal notes into generic executive-summary prose.
- Destructively rewrite, move, or delete source notes without approval.
- Treat old dashboards or status files as current truth without checking the current index/design note.

## Automation / Invocation

Manual trigger phrases:

- "synthesize this"
- "turn this into a durable note"
- "write up a synthesis on X"
- "chronicle this," "save this conversation" (see Conversation Sources above)

Eligible inputs:

- raw notes, generated briefs, research dumps, or audits the owner points to
- a chat conversation worth preserving
- stale project material identified during a janitor or intake pass

Allowed automatic actions:

- draft the synthesis note using `system/Templates/synthesis-note.md`
- add currentness warnings
- apply obvious wikilinks and existing tags

Requires the owner's approval:

- rewriting or deleting the source notes being synthesized
- routing follow-ups to an external task system
- creating a new tag namespace

## Verification

Before finishing:

- check the note has a Memory Card when useful
- check source trails are preserved
- check actionable follow-ups are surfaced in the note (not routed to an external system unless the owner asked)
- check any changed index links resolve by path/title search
- append a line to [[system/logs/skill-usage-log|Skill Usage Log]]
