# Agents

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
