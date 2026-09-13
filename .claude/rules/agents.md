# Agents

Skills are procedures inside one foreground conversation. Two different mechanisms cover
work that happens outside that conversation, and picking between them is mechanical, not a
style preference:

- **`.claude/agents/<name>.md` subagent files** (`spec-executor.md` is the one real example)
  — auto-discovered by Claude Code, but only ever dispatched *inside a live session*: either
  explicitly (the Agent tool, by name) or by self-invocation when an incoming request matches
  the file's `description`. They cannot fire on their own — no session open, no dispatch, no
  exceptions. Author one when the job is delegation: work big or isolated enough to
  background (a different tool budget, an isolated worktree), but still something a user or
  a running conversation triggers, in that session or a later one.
- **Scheduled cloud routines** (created via `/schedule`, live at claude.ai/code/routines) —
  run unattended on a cron schedule, in an isolated cloud sandbox, with no session and
  usually no human present. They are **not files in this repo** — only a short description of
  one, if it's worth a durable pointer, belongs in the bullet list below. Author one when the
  job genuinely has to happen without anyone opening a session to trigger it.

**Concretely: Style-Watchlist Review is a routine, not a subagent file, because the
requirement was a timer.** The job is "re-check every ticker on the five style watchlists
every Sunday, whether or not anyone opens Claude Code that day." A subagent file cannot do
that — "weekly, unattended" was never on the table for that mechanism, so there was no
tradeoff to weigh; the routine was the only mechanism that could do the job at all.

(The `.claude/agents/decision-making-prioritization/` scaffolding was copied in from
elsewhere to try the subagent mechanism out, not authored for a job here, and isn't
registered — see `.claude/agents/README.md`. Don't read its presence, or `spec-executor.md`'s,
as this repo having settled on subagent files as the default place new agent work goes; each
job still gets checked against the two mechanisms above on its own terms.)

Actual unattended-agent infra:

- **`spec-executor`** (`.claude/agents/spec-executor.md`) — subagent that executes exactly
  one slice of an already-approved `spec-drift-gate` spec in an isolated worktree. It does
  not decide scope, does not merge or push; it reports what it did and flags anything that
  fell outside the spec, for a human to run through `spec-drift-gate` Step 4. Only dispatch
  it when a written spec already exists and the slice is big enough to background.
- **Weekly Catalog Drift Audit** — a scheduled cloud routine (not in this repo; lives at
  claude.ai/code/routines). Runs `catalog-drift-audit` against `main`, fixes mechanical
  drift on a branch, opens a PR. Never pushes to `main`. Its audit trail is
  `.claude/_Prompts/catalog-audit-log.md`.
- **Style-Watchlist Review** — a scheduled cloud routine (not in this repo; lives at
  claude.ai/code/routines, weekly, Sunday 6pm ET). Reads the "The five committed style
  screens" and "Style-watchlist review pass" sections of
  `.claude/skills/Finance/watchlist-screen-sync/SKILL.md` (the sole source of truth — the
  routine's own prompt duplicates none of the criteria) and re-checks every ticker on each
  of the five "AI [Style]" Webull watchlists against its style's table, reporting drift back
  in the run's own session. Deliberately read-only: it pulls each ticker's current metrics
  itself via Webull's financial-data tools rather than waiting on a human to supply them —
  the one unattended-specific deviation from the interactive skill — but is barred from
  calling any Webull tool that mutates state (`add_watchlist_instruments`,
  `remove_watchlist_instruments`, any order/trade action) and never touches this git repo
  beyond reading that one file. Never fixes drift itself; a human decides what to do with a
  no-longer-clearing ticker via the interactive skill.

To author a new agent, copy `template/spec-system/agent-spec-template.md` to
`.claude/agents/<name>.md` and fill it in (the template starts with a worthiness test —
fixed-sequence or high-stakes tasks should stay scripts, not agents).
