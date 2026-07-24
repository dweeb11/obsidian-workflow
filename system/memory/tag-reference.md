# Tag Reference

Tags are hierarchical and inline — no YAML frontmatter unless the note type already uses it. Namespaces group related tags under a common prefix. This file catalogs what's in use and the conventions that govern them.

It starts empty on purpose. A tag vocabulary is only useful once it describes tags you actually apply; inheriting someone else's namespaces gives you a taxonomy you'll never use and a reference file that lies. Add a section the first time a namespace earns one.

---

## Conventions

1. **Hierarchical.** Tags use `/` for namespace — `#area/subarea`, not `#subarea`.
2. **YAML frontmatter** for `type/` tags only — those classify what kind of note it is (`type/person`, `type/index`, `type/synthesis`, `type/source`, `type/topic`, `type/capture`, `type/log`). All other tags are **inline only**.
3. **Prefer existing tags** over creating new ones. Scan this file first.
4. **Workflow tags stay lean.** Keep the action namespace small — `#action/next` and at most one or two siblings. Subdividing it is how a tag system becomes a task manager.
5. **Avoid accidental tags.** Color codes (`#FFFFFF`, `#0000FF`) and pasted numbers (`#1`, `#195`) are artifacts, not tags. Strip them when you find them.
6. **Bare workflow words are a smell.** `#todo`, `#idea`, `#plan`, `#research`, `#reference` classify nothing on their own — namespace them or drop them.

---

## Namespaces In Use

<!--
One section per durable namespace. Keep the table shape:

## Area Name

| Tag | Purpose |
|-----|---------|
| `#area/subarea` | What it marks, and when to reach for it. |

A short paragraph after the table is the right place for the rule that isn't obvious from the tag name — what's deliberately excluded, why a namespace sits outside another one, or where the tag is applied (inline vs frontmatter).
-->

---

## Ungrouped / Lightly Used

Tags that appear once or twice and haven't earned a namespace. Keep this list short; it is a staging area, not a home. Either promote a tag to a namespace above or stop using it.

---

## Agent Rule

Before adding a new tag namespace, scan this note and prefer an existing namespace. If a new namespace is genuinely needed, add it above and explain why — a namespace with no stated reason gets re-litigated every few months.

---

*Update this file whenever you add a namespace or change a convention. Dating the change is worth the two seconds.*
