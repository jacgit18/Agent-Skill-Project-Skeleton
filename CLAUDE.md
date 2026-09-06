# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **catalog**, not an application. It holds authored Claude skills (mostly decision *gates*),
a small amount of unattended-agent infrastructure, and the plumbing that keeps the catalog
honest. There is nothing to compile, serve, or unit-test. "Work" here means authoring a
skill, testing it against its siblings, and keeping the bookkeeping files in sync.

> **README drift:** `README.md` "Layout" references top-level directories — `Architecture/`,
> `Finance/`, `Goals/`, `Business Venture/`, `Communication/` — that are **not in this repo**.
> They belong to the surrounding PersonalBrain vault and were the source notes the skills
> were distilled from. Do not expect to find them here; do not try to "restore" them. What
> is actually tracked: `.claude/`, `Artifact/`, `Books/`, `curriculum/`, `.superpowers/`,
> `scripts/`, `template/`, and the root `*.md` files.

## Layout (what's actually here)

| Path | What's in it |
|---|---|
| `.claude/skills/<Group>/<name>/` | The skill library. Groups: `AI Engineering`, `Architecture` (+ `Architecture/Data`), `Business`, `Documents`, `Finance`, `Git`, `Health`, `Prompts`, `Research`, `Skill Development`, `Testing`. |
| `.claude/agents/spec-executor.md` | The one auto-discovered subagent (see Agents). |
| `.claude/agents/decision-making-prioritization/`, `.claude/agents/ai-qa-testing/` | Notes and scaffolding, **not** registered agents — Claude Code only auto-discovers `.claude/agents/*.md`, not subdirectories. See `.claude/agents/README.md`. |
| `.claude/settings.json` | Wires the `UserPromptSubmit` prompt-logging hook. |
| `.claude/_Prompts/logs/YYYY-MM-DD.md` | Auto-appended log of every submitted prompt. |
| `.claude/_Prompts/catalog-audit-log.md` | Durable trail of `catalog-drift-audit` runs; each run reads it first to avoid re-flagging resolved items. |
| `README.md` | Human-facing catalog index with one table row per skill. Kept in sync by hand. |
| `SKILL-BACKLOG.md` | Skill candidates; each entry is marked `[x] Built …` with its isolation + interaction-test result recorded inline. |
| `Priority Dev Roadmap.md` | Personal career/learning roadmap (vault doc, not catalog process). |
| `template/skill-template/` | Scaffold for a new skill — `SKILL.md` + `reference-file.md` + `README.md` skeletons. Copy to `.claude/skills/<Group>/<name>/`. |
| `template/spec-system/agent-spec-template.md` | Template + worthiness test for authoring a new agent. |
| `scripts/` | `hooks/log-prompt.sh`, `git/batch-git-push.sh`. |
| `Artifact/` | Talking points / catalog write-ups for external posts. |
| `curriculum/`, `.superpowers/sdd/` | A separate spec-driven learning-portfolio project (specs, plans, task briefs/reports). Unrelated to the skill catalog. |

## Commands

There is no build, lint, or test runner. The two operational commands:

```bash
# Chunked commit + push — never puts more than N files in one push.
# Args: [batch_size=90] [branch=current] [commit_prefix="Add files"]
scripts/git/batch-git-push.sh 50 main "Add skills"
DRY_RUN=1 scripts/git/batch-git-push.sh            # preview only
INCLUDE_MODIFIED=1 scripts/git/batch-git-push.sh   # also stage modified/deleted, not just untracked
```

The prompt-logging hook (`scripts/hooks/log-prompt.sh`) runs automatically on every prompt.
It needs `jq` on PATH; it is defensive by design — always exits 0, prints nothing, cannot
block a prompt or inject context.

**"Testing" a skill is done by invoking a skill, not a shell command:**

- `Prompts/skill-interaction-testing` — run a new/changed skill against its siblings for
  stacking, contradiction, silent override, and beneficial chaining.
- `Prompts/catalog-drift-audit` — periodic whole-catalog hygiene pass.
- `Skill Development/spec-drift-gate` — gate a multi-file/multi-session build behind a
  written spec, then diff work against it at checkpoints.

## Skill architecture

Every skill is a directory with a fixed shape:

- **`SKILL.md`** — YAML frontmatter (`name`, `description`) then the procedure. The
  `description` is large and does real work: it packs literal trigger phrases **and**
  explicit "this is NOT for X — that's `sibling-skill`" carve-outs. Disambiguation between
  overlapping skills lives in these descriptions, not in a router. When you change a
  skill's scope, you almost always must edit sibling descriptions reciprocally.
- **Companion `*.md`** — the deep reference material (methods, worked examples, rubrics),
  kept out of `SKILL.md` so the entry point stays short.
- **`README.md`** — where this skill sits relative to its siblings (hand-off, absorption,
  chaining boundaries).

Most skills are **gates**: they withhold the answer until a precondition is met — a stated
hypothesis, a listed set of unknowns, a settled prior decision, a learning rep the user
must do themselves. A few (`index-tuning`, `failure-mode-analysis`, `reliability-math`,
`change-surface-audit`, `document-page-check`) are procedures, not gates. The README's per-group
tables say which is which.

### Cross-cutting meta-skills

These four are referenced by many others and are the usual integration points for a new skill:

- `Skill Development/learning-gate` — classifies intent (learning / execution / reference),
  sets how much thinking Claude may do. New skills add a Step 3 row here.
- `Skill Development/problem-solving-gates` — prior-effort gates (Rubber Duck / Options
  Generator / Knowledge Checker / Optimization).
- `Skill Development/spec-drift-gate` — spec-before-build + drift checkpoints.
- `Prompts/ambiguity-gate` — ask before acting on a request with more than one reading.

## Agents

Skills are procedures inside one foreground conversation. Actual unattended-agent infra:

- **`spec-executor`** (`.claude/agents/spec-executor.md`) — subagent that executes exactly
  one slice of an already-approved `spec-drift-gate` spec in an isolated worktree. It does
  not decide scope, does not merge or push; it reports what it did and flags anything that
  fell outside the spec, for a human to run through `spec-drift-gate` Step 4. Only dispatch
  it when a written spec already exists and the slice is big enough to background.
- **Weekly Catalog Drift Audit** — a scheduled cloud routine (not in this repo; lives at
  claude.ai/code/routines). Runs `catalog-drift-audit` against `main`, fixes mechanical
  drift on a branch, opens a PR. Never pushes to `main`. Its audit trail is
  `.claude/_Prompts/catalog-audit-log.md`.

To author a new agent, copy `template/spec-system/agent-spec-template.md` to
`.claude/agents/<name>.md` and fill it in (the template starts with a worthiness test —
fixed-sequence or high-stakes tasks should stay scripts, not agents).

## Adding or changing a skill

1. Copy `template/skill-template/` to `.claude/skills/<Group>/<name>/` and fill in
   `SKILL.md` + reference files + `README.md`. Budget real effort on the `description`
   frontmatter — it alone decides when the skill fires and carries the carve-outs against
   siblings.
2. **Isolation screen** — confirm a baseline (no skill) fails the way the skill exists to
   fix, and that the skill fixes it.
3. **Interaction test** — run `Prompts/skill-interaction-testing` against the sibling set.
   Record what you find: hand-off, absorption, chaining, or a fix for stacking /
   contradiction / silent override.
4. **Reciprocal edits** — apply the sibling `description` changes and cross-pointers the
   interaction test surfaced, both directions.
5. **Bookkeeping** — add/refresh the skill's row in `README.md`; mark the `SKILL-BACKLOG.md`
   entry `[x] Built` with the test result inline; leave the auto-memory marker
   (`memory/MEMORY.md` index line + a file).

For a whole-catalog pass rather than one skill, use `catalog-drift-audit` and append to
`.claude/_Prompts/catalog-audit-log.md`.

## Conventions

- **Branches / PRs:** branch per change; PRs target `main`. Automated routines open PRs,
  they do not push to `main`.
- **`.gitignore`:** `*.csv` is ignored (personal financial exports live in the working tree
  but are never committed).
- **Commit messages** end with:
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`
