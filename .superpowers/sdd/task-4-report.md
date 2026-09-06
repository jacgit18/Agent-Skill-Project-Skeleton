# Task 4 Report: Plan Full-Stack Project #1

## Status: DONE

## What happened

Initially returned NEEDS_CONTEXT because the project choice, stack, and non-trivial-challenge focus weren't known and this task explicitly forbids inventing them. The coordinator then supplied the user's decision (see below), so the task was completed in a follow-up pass.

## Project chosen

**Personal Finance Dashboard** — a multi-user personal finance app where users import transactions (CSV for v1) and Claude API automatically categorizes expenses and generates periodic natural-language spending insights.

**Why this project:**
- Real user value — the user can use it themselves and share with friends/family
- Multi-user adds genuine technical complexity: auth, per-user data isolation, and pipeline concurrency
- Claude API integration is central (not bolted on): classification at volume + reasoning-heavy insight generation, which teaches API cost/latency management at scale
- Clear, concrete interview story: a cost/correctness problem with a defensible solution, not a tutorial clone

## Technical decisions made (with reasoning captured in the plan)

- **Backend:** FastAPI (async-native — needed for concurrent DB + Claude API I/O; chosen over Flask)
- **Database:** PostgreSQL (relational integrity for the ledger, row-level multi-tenant isolation, JSONB for flexible Claude response storage; chosen over MongoDB)
- **Frontend:** React (per coordinator spec)
- **Claude integration:** Anthropic Python SDK — `claude-haiku-4-5` for per-transaction categorization (cheap/fast classification tier), `claude-sonnet-5` for periodic insight generation (more reasoning depth); Batches API for bulk/historical categorization (~50% cost reduction); prompt caching on the stable category-taxonomy system prompt. I loaded the `claude-api` skill before writing this section to confirm current model IDs/pricing and the Batches/caching mechanics rather than relying on possibly-stale training knowledge — model list and figures used ($1/$5 Haiku 4.5, $2/$10 Sonnet 5, $5/$25 Opus 5 per MTok) came from that skill's cached reference table.
- **Deployment:** Render (backend + managed Postgres) + Vercel (React frontend), with Fly.io/Railway and AWS noted as alternatives — user was open to suggestion.

**Non-trivial challenges documented (3):** Claude API cost/latency management at scale (batching + caching + model-tier routing), multi-user auth/data isolation (query-layer scoping + isolation tests + optional Postgres RLS), and concurrency/correctness of the categorization pipeline (idempotent status tracking, rate-limited job processing, retry on 429/5xx).

## Files created

- `/home/jac/AI/Agents/PromptingAgent/projects/PROJECT-1-plan.md` — full architecture brief: goal, high-level architecture (3 paragraphs), technical decisions table, 3 non-trivial challenges with approaches, success criteria checklist, 8-week timeline, draft interview story, and a placeholder note to add a "Final Interview Story" section once shipped.
- `/home/jac/AI/Agents/PromptingAgent/projects/PROJECT-1-log.md` — empty working-log template (2-entry example structure), ready for the user to fill in during the weeks 5-12 build phase.

## Commit

`e856702` — "doc: project 1 plan and working log" (2 files changed, 63 insertions)

## Next steps (explained for the user, per brief Step 4)

Planning (this task) covers weeks 1-4. Actual building happens weeks 5-12: the user should build incrementally (test each piece), use the problem-solving gate system (`problem-solving-gates/`) when stuck rather than immediately searching for answers, and log each problem/solution/insight as a new entry in `PROJECT-1-log.md`. Once the project ships, add a "Final Interview Story" section to `PROJECT-1-plan.md` reflecting what actually happened (per brief Step 5) — the current interview story is a draft based on the plan, not the lived build.

## Notes / open questions for the user

- CSV import is scoped as the v1 data-entry method; a live bank-feed integration (e.g. Plaid) is called out in the plan as an explicit stretch goal, not required for the 8-week timeline — worth confirming this scoping matches expectations.
- A real-time channel (WebSockets/SSE) for live categorization status is likewise flagged as a stretch goal, not core scope.
- Deployment platform (Render + Vercel) was chosen as a reasonable default since the user was open to suggestion; easy to swap for Fly.io/Railway/AWS if preferred before Week 8.
