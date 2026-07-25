# obsidian-workflow

An empty Obsidian vault that comes with an agent-facing workflow layer already installed.

Clone it, open it in Obsidian, and you have a working vault with no notes in it, plus a set of plain-text contracts that tell Claude, Codex, Gemini, or whatever you use how to move around that vault.

It's a snapshot of my own vault's `system/` layer with all of my notes removed. There's no sync back to my vault, so once you clone it, it's yours and it starts drifting from mine. Take the parts that are useful and delete the rest. Most of what's here is a shape you can adapt rather than a system to adopt as-is.

## Why I've worked on this

First of all, this is shamelessly lifted from Nick Milo's suggestions.  I heavily agree with his idea to keep your notes vault agnostic of a particular tool or agent.  Reference videos:  <https://www.youtube.com/watch?v=rRa9td4oe7k>

If you point an AI agent at a personal vault with no instructions, it tends to invent its own conventions each session: new folders, new tag schemes, a dashboard nobody asked for, notes rewritten into corporate prose. Writing your conventions down in files the agent reads first helps more than picking a smarter agent.

So that's what this is. Four map files at the root, a folder of workflow docs, and some scripts that make the maps cheap to load.

- `AGENTS.md` — the front door. Deliberately thin; it routes to the maps rather than restating them.
- `Vault-Map.md` — how the vault is laid out, and the filing grammar for new notes.
- `Skills-Map.md` — an index of repeatable workflows, pointing at `system/skills/`.
- `Me.md` — who you are and how you want to be worked with. Read only when a task touches your voice or preferences.

The load policy matters about as much as the content. The maps are routers, not a context dump, so an agent fixing a typo should end up reading almost nothing.  This has been lots of back and forth to reduce token burn.  Installing Obsidian CLI can also help with this.

## First five minutes

1. Clone it and open the folder as a vault in Obsidian (*Open folder as vault*). Trust the folder when prompted.
2. Install the three community plugins it expects: Calendar, Dataview, and Notebook Navigator. The vault ships the plugin list (`.obsidian/community-plugins.json`) but not the plugin code, so Obsidian will prompt you. Dataview is the only real dependency — a few templates use `dataview` blocks that render as code until it's enabled.
3. Fill in `Me.md`. It ships as a scaffold of headers and prompts with no content. Short and specific works better than long and tidy, and you can delete any section that isn't earning its keep. It's probably the highest-leverage file here, since it's what agents read to know how to talk to you.
4. Check daily notes. They're already configured: new daily notes land at the vault root as `YYYY-MM-DD.md` and use `system/Templates/Daily Note.md`. Root-level is intentional, since the day's note is a working surface; closing the day archives it to `calendar/daily notes/YYYY/`.
5. Sanity-check the plumbing:
   ```bash
   python3 system/scripts/context-router.py default   # macOS / Linux
   python system\scripts\context-router.py default    # Windows
   ```
   That prints the context bundle an agent gets by default. If you see the Agent Quickstart section from `Vault-Map.md`, everything is wired up.

Then point your agent at the vault and ask it to do something small. `AGENTS.md` is what it should find first.  Honestly you could just point your agent at the repo and tell it to read the README and you're probably set.

## What's deliberately empty

The folders ship as empty scaffolding (`.gitkeep` files), since the structure is the part worth sharing and my notes aren't:

```
+/clippings/        intake — web clippings, raw dumps
atlas/              durable knowledge; atlas/people/ for people pages
calendar/           dated records; calendar/daily notes/ archives
efforts/            active work
system/             the workflow layer (the only populated one)
x/                  passive archive
```

`Me.md` is empty for the same reason, though it's the one gap worth closing early.

What is populated: `system/skills/` (eight workflow docs), `system/Templates/` (seven templates), `system/scripts/` (six scripts plus tests), and `system/memory/tag-reference.md`.

## The scripts

Six portable scripts under `system/scripts/`. All of them are Python — stock python 3.9, nothing to install, no shell — so they run the same on macOS, Linux, and Windows, and they locate the vault from their own path, so they work wherever you cloned to.

| Script | What it does |
|---|---|
| `context-router.py <profile>` | Prints a task-shaped context bundle. Profiles: `default`, `daily`, `intake`, `synthesis`, `index`, `voice`, `operational`, `map`. |
| `session-start-context.py` | Session-start loader; silent when there's nothing useful to say. |
| `session-end-route.py` | Claude Code Stop hook. Blocks once at session end to prompt durable memory routing. |
| `daily-intelligence-pass.py` | Read-only. Flags tasks you keep carrying forward across daily notes. |
| `breadcrumb-sweep.py` | Finds routing breadcrumbs left behind in notes. |
| `lint-note-metadata.py` | Checks frontmatter consistency. |

Tests, with no third-party runner:

```bash
cd system/scripts && python3 -m unittest discover -s . -p 'test_*.py'
# Ran 27 tests — OK
```

On Windows that's `python -m unittest discover -s . -p "test_*.py"` — the python.org installer gives you `python` and `py`, not `python3`.

One thing worth saying in plain prose rather than leaving to the all-caps disclaimer in `LICENSE`: scripts like these can write to and delete files inside the vault you point them at. Worth reading one before running it against a vault you care about, and worth having a backup or a commit to get back to. As shipped, three of them are read-only detectors and the other three only print and route, but that's true of this version specifically.

## Sending something back

Open an issue: <https://github.com/dweeb11/obsidian-workflow/issues>. That's the whole channel — bugs, contradictions between docs, workflows you think are missing, or just telling me a part of it didn't make sense. I don't watch pull requests as a suggestion queue.

## License

MIT, see [`LICENSE`](LICENSE).

For the case that actually comes up: copy anything here into your own vault freely, no attribution needed. The notice only matters if you redistribute or publish it as a package of its own.
