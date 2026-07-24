---
tags:
  - type/log
---
# Skill Usage Log

Append-only. Each vault skill/workflow appends one line here after a real run (not on dry-runs, aborted starts, or ordinary chat).

**Format:** `- YYYY-MM-DDTHH:MM:SS | **skill-slug** | one-line note of what ran`

Use the workflow's `system/skills/<slug>.md` filename as the slug. This exists so a future audit can answer "how often is this actually used" from evidence instead of guessing from git history.

Two things make it work: append, never rewrite; and log the run, not the intent. An empty log after a month is itself a finding.

## Log
