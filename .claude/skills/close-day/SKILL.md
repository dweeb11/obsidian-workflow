---
name: close-day
description: "Use when today's daily note in the vault root needs to be closed out -- processed, routed to permanent homes, and archived."
---

<!--
GENERATED FILE -- do not edit by hand.
Source: system/skills/registry.json
Regenerate: python3 system/scripts/generate-adapters.py
-->

# Close Day

This file is a **non-authoritative adapter**. It contains no workflow logic. The
authoritative, agent-agnostic contract lives in the vault and supersedes it:

- `system/skills/daily-capture.md`
- `system/Templates/Daily Note.md`

## What to do

1. Read the contract file above.
2. Perform the **Close** operation in that contract exactly as it specifies.
3. Self-verify against the contract's own acceptance checklist before declaring
   the work done.

If this adapter ever conflicts with the contract, follow the contract and report
the drift -- the fix belongs in `system/skills/registry.json`, not here.
