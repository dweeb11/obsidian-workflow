---
tags:
  - type/index
last_touched: YYYY-MM-DD
---

# {{Folder Name}} Index

> [!info] Memory Card
> **What this is:** Navigation page for `{{folder/path}}`.
> **Connects to:** [[Related Note]], [[Related Area]]
> **Last touched:** YYYY-MM-DD

## Start Here

| Note | Use it for |
|---|---|
| [[Primary Note]] | Current orientation / canonical starting point. |
| [[Supporting Note]] | Deeper context or source material. |

## Main Topic Clusters

| Area | Start here | Notes |
|---|---|---|
| Area name | [[Area Start Note]] | What belongs here and when to use it. |

## Breadcrumbs / Ideas

Use for interesting-but-not-yet-actionable signals. Keep these lightweight; indexes should not become task dashboards.

```md
- YYYY-MM-DD — One-line idea or signal. Related: [[Note]], [[Source]]. Status: keep | watch | dropped | promoted.
```

Review `watch` breadcrumbs that linger for roughly 30 days or accumulate repeated related entries without movement. Outcomes: keep, drop, consolidate into a durable topic page, or leave as archive context. Do not promote to an external task system unless the owner explicitly asks.

## Current Links

Use this section for stable external pointers such as repos, project websites, or generated sites. Do not duplicate task state here when a repo or tracker owns it.

- Repo:
- Site:

## Notes in This Area

```dataview
TABLE status, created, file.mtime AS updated
FROM "{{folder/path}}"
WHERE file.name != "_index"
SORT file.mtime DESC
```

## Link / Tag Review

### Applied

- Linked the most useful entry points for this folder.

### Routed Follow-ups

- Surface actionable cleanup or follow-up work as a vault-local candidate here; do not create external task-system records unless the owner explicitly asks.
- Keep non-actionable observations as context or breadcrumbs instead of creating hidden task lists.

<!-- Template notes: update frontmatter last_touched and visible Memory Card Last touched together when both exist. Visible Last touched is mainly for hubs/indexes/important orientation pages. -->
