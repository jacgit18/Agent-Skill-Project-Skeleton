# Repo map

> **Not in this repo:** the vault directories the skills were distilled from —
> `Architecture/`, `Finance/`, `Goals/`, `Business Venture/`, `Communication/` — belong to
> the surrounding PersonalBrain vault. Don't expect to find them here; don't try to
> "restore" them. Runtime paths some skills write to (`Finance/Error Log/` for
> `problem-journal`'s Capture mode) are in that vault too, not here.

What is actually tracked: `.claude/`, `.claude-plugin/`, `adr/`, `Artifact/`, `Books/`,
`curriculum/`, `.superpowers/`, `Other/`, `.out-of-scope/`, `scripts/`, `template/`, and the
root `*.md` files. `README.md`'s "Layout" table is the human-facing version of the table
below and is kept in sync with it by hand.

| Path | What's in it |
|---|---|
| `.claude/skills/<Group>/<name>/` | The skill library. Groups: `AI Engineering`, `Architecture` (+ `Architecture/Data`), `Business`, `Documents`, `Finance`, `Git`, `Health`, `Prompts`, `Research`, `Skill Development`, `Testing`. |
| `.claude/rules/` | This guidance, split into topic files and imported by `CLAUDE.md`. Edit the rule files, not the `CLAUDE.md` list. |
| `.claude/commands/` | Slash commands. `/new-skill <Group>/<name>` drives the add-a-skill workflow end to end; `/sync-catalog` is a read-only catalog consistency check. (Directory is `commands`, plural — Claude Code ignores a singular `command/`.) |
| `.claude/agents/spec-executor.md` | The one auto-discovered subagent (see `agents.md`). |
| `.claude/agents/decision-making-prioritization/` | Notes and scaffolding, **not** a registered agent — Claude Code only auto-discovers `.claude/agents/*.md`, not subdirectories. See `.claude/agents/README.md`. |
| `.claude/settings.json` | Wires two hooks: `UserPromptSubmit` → prompt logging, `SessionStart` → mechanical catalog-drift glance. |
| `.claude/_Prompts/logs/YYYY-MM-DD.md` | Auto-appended log of every submitted prompt. **Gitignored** — local only, never committed. |
| `.claude/_Prompts/catalog-audit-log.md` | Durable trail of `catalog-drift-audit` runs; each run reads it first to avoid re-flagging resolved items. |
| `README.md` | Human-facing catalog index with one table row per skill. Kept in sync by hand. |
| `SKILL-BACKLOG.md` | Skill candidates; each entry is marked `[x] Built …` with its isolation + interaction-test result recorded inline. |
| `template/skill-template/` | Scaffold for a new skill — `SKILL.md` + `reference-file.md` + `README.md` skeletons. Copy to `.claude/skills/<Group>/<name>/`. |
| `template/spec-system/agent-spec-template.md` | Template + worthiness test for authoring a new agent. |
| `scripts/` | `hooks/log-prompt.sh`, `hooks/catalog-drift-check.sh`; `git/state.sh` (snapshot), `git/commit.sh` (staged-pathspec commit + trailer), `git/push.sh` (timeout/fallback/retry), `git/land.sh` (merge a PR via `gh` + resync local), `git/batch-git-push.sh` (bulk). See `commands.md` / `conventions.md`. |
| `Artifact/` | Talking points / catalog write-ups for external posts. |
| `Books/` | Business and tech book notes — source material some skills draw on. |
| `adr/` | Architecture decision records for the repo's own conventions (e.g. the setup-pointer rule). |
| `curriculum/`, `.superpowers/sdd/` | A separate spec-driven learning-portfolio project (specs, plans, task briefs/reports). Unrelated to the skill catalog. |
| `Other/Misc/` | A handful of imported third-party skills, kept around but **not** integrated into the catalog (not in `README.md`, `SKILL-BACKLOG.md`, or the interaction-test web). Triage or delete. |
| `.out-of-scope/` | Short notes on skill ideas evaluated and deliberately ruled out. |
| `.claude-plugin/plugin.json` | A copied-in Claude Code plugin manifest (`mattpocock-skills`) that references skills not present in this repo — vestigial; safe to delete. |
