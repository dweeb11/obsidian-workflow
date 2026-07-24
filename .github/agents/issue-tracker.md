# Issue tracker: GitHub

Issues for this repo live as GitHub issues on `dweeb11/obsidian-workflow` (private). Use the `gh` CLI for all operations. `gh` infers the repo from `git remote -v` when run inside the clone; add `-R dweeb11/obsidian-workflow` when running from elsewhere.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body-file <path>`. Prefer `--body-file` over `--body` for multi-line bodies — heredocs through the shell mangle backticks and wikilink brackets, both of which are everywhere in this repo's subject matter.
- **Read an issue**: `gh issue view <n> --comments`
- **List issues**: `gh issue list --state open --json number,title,labels --jq '.[] | "#\(.number) [\(.labels[0].name // "-")] \(.title)"'`
- **Comment**: `gh issue comment <n> --body-file <path>`
- **Label**: `gh issue edit <n> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <n>`

**PRs as a request surface: no.** This repo's audience is a friend plus whoever else is shown it; suggestions are expected as issues. Nothing reads PRs as a triage queue.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <n> --comments`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is a single issue with **child** issues as tickets. Sub-issues and issue dependencies are both enabled on this repo and verified working — use the native relationships, not body conventions.

The live map is [#1 — Map: Extract a shareable vault-workflow skeleton](https://github.com/dweeb11/obsidian-workflow/issues/1).

### Map

A single issue labelled `wayfinder:map`, holding the Destination / Notes / Decisions-so-far / Not-yet-specified / Out-of-scope body.

```bash
gh issue create --title "Map: ..." --label wayfinder:map --body-file map.md
```

### Child ticket

An issue attached to the map as a native GitHub sub-issue, labelled `wayfinder:<type>` — one of `research`, `prototype`, `grilling`, `task`. All five `wayfinder:*` labels already exist on this repo.

```bash
gh issue create --title "..." --label wayfinder:grilling --body-file ticket.md
# then attach it to the map:
gh api -X POST repos/dweeb11/obsidian-workflow/issues/1/sub_issues \
  -F sub_issue_id=<child-db-id>
```

### Database ids, not issue numbers

**Both relationship endpoints take the target's numeric database id, not its `#number` and not its `node_id`:**

```bash
gh api repos/dweeb11/obsidian-workflow/issues/<n> --jq .id   # -> e.g. 4972509190
```

Use `-F` (numeric field), **not** `-f` (string field). With `-f` the API rejects the value and `gh` exits non-zero with no useful message — it looks like a permissions or feature-availability problem when it is purely a type error. This is the single easiest thing to lose an hour to here.

### Blocking

GitHub's native issue dependencies — the canonical, UI-visible representation, which is what makes the frontier legible in the tracker without opening the map.

```bash
gh api -X POST repos/dweeb11/obsidian-workflow/issues/<blocked>/dependencies/blocked_by \
  -F issue_id=<blocker-db-id>
```

GitHub reports `issue_dependencies_summary.blocked_by`, which counts **open** blockers only — so it is the live gate. A ticket is unblocked when every blocker is closed; no bookkeeping needed on close.

### Frontier query

Open, unblocked, unclaimed children, in map order. First one wins:

```bash
gh api repos/dweeb11/obsidian-workflow/issues/1/sub_issues --jq '
  .[]
  | select(.state=="open")
  | select(.assignee==null)
  | select(.issue_dependencies_summary.blocked_by==0)
  | "#\(.number) \(.title)"'
```

### Claim

```bash
gh issue edit <n> --add-assignee @me
```

The session's first write, before any work — an open unassigned ticket is what "unclaimed" means, so concurrent sessions rely on this landing first.

### Resolve

1. `gh issue comment <n> --body-file answer.md` — the resolution comment
2. `gh issue close <n>`
3. Append a one-line gist + link to the map's **Decisions so far**, and clear any fog the answer graduated out of **Not yet specified**

## Note on this file

This is repo infrastructure, not extracted vault content. It describes how agents work *on* this repo; it is not part of the vault workflow being shared.

It lives under `.github/` deliberately. The repo root *is* the vault root — a cloner opens this directory in Obsidian — and Obsidian ignores dot-directories entirely. So `.github/agents/` keeps this file reachable by agents and by git while leaving it invisible in the vault a cloner actually sees. Anything else that is about *this repo* rather than about *the vault* belongs here too, for the same reason. (Settled by the extraction ticket, which inherited the question from the skill-docs triage; it was previously at `docs/agents/issue-tracker.md`.)
