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
  claude.ai/code/routines, weekly, Sunday 6pm ET). Reads
  `.claude/skills/Finance/watchlist-screen-sync/SKILL.md` fresh each run (the sole source of
  truth — the routine's own prompt duplicates none of the criteria or tool mappings) and runs
  two phases. **Phase A, read-only:** re-checks every ticker on each of the five "AI [Style]"
  Webull watchlists against its style's criteria table, pulling current metrics itself via
  Webull's financial-data tools (the one deviation from the interactive skill's "the user
  supplies values" rule — no human is present to ask). **Phase B, scoped write:** runs the
  skill's "Candidate discovery" mode per style — pulls a raw candidate pool from Webull's real
  market-scan tools, pre-filters, fully evaluates at most 5 new candidates per style, retrieves
  financials progressively with early exits and a run-wide cache, runs the same criteria tables,
  and auto-files passers. Existing watchlist names are reviewed first; if that can't finish
  within the connector's call limit the run stops before discovery ("degrade by stopping, never
  by weakening a screen"). Deep Value and Quality Compounder source from one rotating batch of 9
  Webull sectors per run (ISO week number modulo batch count), not every sector at once — the
  cross-sector rule is met over several weeks rather than in a single run. Momentum's top-30%
  percentile tests report `data not available` when the discovery universe is too narrow to
  support them — deliberately left conservative, not yet resolved. This is the routine's only permitted
  mutating action, and it's narrow on purpose: `add_watchlist_instruments`, only into the one
  style watchlist a candidate just verified against, only after a duplicate check. Still
  barred from `remove_watchlist_instruments`, any watchlist create/delete/update, any
  order/trade action, and any write to this git repo. Neither phase fixes drift or removes a
  no-longer-clearing ticker — that stays a human call via the interactive skill. Also resyncs
  **AI Shortlist** at the end of each run — a cross-style aggregator with no criteria of its
  own that mirrors each style's top-2-ranked passer(s) from that run's fresh results; folded
  in "for free" since it reuses data the re-check pass already pulled, no extra Webull calls
  beyond its own add/duplicate-check. **AI Day Trade is deliberately never touched by this
  routine** — intraday liquidity/volatility setups go stale within hours, so a weekly batch
  can't track them; that screen and its discovery mode are manual-only, invoked in-session
  per `watchlist-screen-sync`'s own file. First fire
  (2026-09-13, Phase-A-only version, before Phase B existed) confirmed correct via
  `get_run_log`: found all five watchlists genuinely empty, made zero mutating calls, sent no
  notification since there was nothing to flag.

To author a new agent, copy `template/spec-system/agent-spec-template.md` to
`.claude/agents/<name>.md` and fill it in (the template starts with a worthiness test —
fixed-sequence or high-stakes tasks should stay scripts, not agents).
