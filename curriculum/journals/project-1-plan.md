# Project 1: Personal Finance Dashboard

## Goal
Build a multi-user personal finance app where users import their transactions and Claude automatically categorizes expenses and generates plain-English spending insights, so the user can see and understand where their money goes without manual bookkeeping.

## Architecture

### High-Level

The core workflow starts with transaction import: a user uploads a CSV export from their bank (MVP; a live-feed integration like Plaid is an explicit stretch goal, not required for v1), and the backend stores the raw rows per user in Postgres. An async categorization pipeline then sends new/uncategorized transactions to Claude, which assigns each one a category (groceries, rent, subscriptions, dining, etc.) with a confidence signal; the user can review and correct any miscategorization, and corrections are logged for future prompt tuning. On a schedule (e.g., weekly), an insights job aggregates a user's categorized spending and asks Claude to produce a short natural-language summary — trends, anomalies ("dining spend is 40% above your 3-month average"), and simple budget nudges.

The core components are: a FastAPI backend exposing a REST API; PostgreSQL holding users, accounts, transactions, categories, and generated insights; a categorization service that batches transactions to Claude (via the Batches API for bulk historical imports, and near-real-time calls for new transactions); an insights service that runs periodic reasoning calls over aggregated spending; and a React frontend (transaction list/review UI, category breakdown charts, an insights feed, and a basic budget view). Auth is JWT-based, and every data access path is scoped to the authenticated user so one user's finances are never visible to another — this multi-tenant isolation is one of the project's deliberate technical challenges, not an afterthought.

Components talk to each other over well-defined boundaries: React calls FastAPI over REST (JSON, JWT bearer auth); FastAPI talks to Postgres via SQLAlchemy (async); the categorization and insights services call Claude via the Anthropic Python SDK and write results back to Postgres; the frontend re-fetches/polls for updated categorization and insight state rather than holding a persistent connection (a real-time channel, e.g. WebSockets/SSE for live categorization status, is a stretch goal if time allows after the core loop works end-to-end).

### Technical Decisions

| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Backend framework | FastAPI | Async-native, which matters here because the app makes concurrent I/O-bound calls (DB + Claude API) that would block a sync framework; built-in Pydantic validation pairs naturally with structured Claude outputs; auto-generated OpenAPI docs help while iterating solo | Flask — simpler mental model, but sync-first; would need extra tooling (Celery, gevent) to get the same concurrency FastAPI gives for free |
| Database | PostgreSQL | Relational integrity matters for a financial ledger (users -> accounts -> transactions is a real foreign-key relationship); strong support for row-level multi-tenant isolation; JSONB columns let raw Claude responses (category + confidence + reasoning) be stored flexibly alongside structured columns | MongoDB — weaker guarantees for ledger-style data with real relationships; would fight the data model instead of helping it |
| Frontend | React | Component model suits a dashboard (charts, tables, review UI); large ecosystem for charting libraries; broadly recognized in interviews | Vue — equally capable, but React has wider interview/job-market relevance, which matters for the portfolio goal |
| Claude integration | Anthropic Python SDK. `claude-haiku-4-5` for per-transaction categorization (cheap/fast classification, $1/$5 per MTok). `claude-sonnet-5` for periodic insight generation (more reasoning depth for narrative summaries, $2/$10 per MTok). Batches API for bulk/historical categorization (async, ~50% cost reduction vs. synchronous calls). Prompt caching on the stable system prompt (category taxonomy + few-shot examples) so it isn't repaid on every classification call. | Matches task to model tier: classification is high-volume and doesn't need Opus-level reasoning, so Haiku 4.5 keeps per-transaction cost low; insight generation is low-volume but benefits from more reasoning, so Sonnet 5 is worth the extra cost there. Batches + caching are the two "free" levers (per Anthropic's own cost-optimization guidance) for cutting cost at scale without touching quality. | Using one model (e.g. Opus 5, $5/$25 per MTok) for everything — simpler code path, but ~5x the cost on the highest-volume workload (categorization) for no quality benefit on a task that's fundamentally simple classification |
| Deployment | Render (backend + managed Postgres) + Vercel (React frontend) | Cheap/free tiers appropriate for a portfolio project, simple GitHub-based CI/CD, managed Postgres removes ops burden so time goes into the app, not infra | Fly.io / Railway — comparable, fine alternatives if Render's free tier proves too limited; AWS — more "production-grade" and a stronger resume line, but higher setup overhead than justified for a solo 6-8 week build |

### Non-Trivial Challenges

1. **Claude API cost/latency management at scale** — Naively calling Claude synchronously per transaction would be slow (blocking the request) and expensive at hundreds/thousands of transactions per import. Approach: use the Batches API for bulk/historical categorization (async, ~50% cheaper), use prompt caching on the stable system prompt (category taxonomy + few-shot examples) so repeated classification calls aren't re-paying for the same tokens, use Haiku 4.5 (the cheapest/fastest tier) for the classification workload specifically, and queue new transactions for near-real-time categorization instead of blocking the import request on Claude's response.

2. **Multi-user auth and data isolation** — A leak of one user's transactions to another is the worst-case failure mode for a finance app, so this can't be an afterthought. Approach: JWT-based auth; every query scoped by the authenticated `user_id` at the query/ORM layer (not just checked at the API boundary); integration tests that specifically assert cross-user isolation (user A's token can never read user B's data); consider Postgres row-level security as a second line of defense beyond application-layer checks.

3. **Concurrency and correctness of the categorization pipeline** — A CSV import can drop hundreds of transactions at once, and the categorization worker has to process them without race conditions, duplicate Claude calls, or partial failures leaving the data in a broken state. Approach: track categorization status per transaction (`pending` / `in_progress` / `done` / `failed`) so work is idempotent and resumable; use a Postgres-backed job table (or lightweight task queue) to serialize/rate-limit outbound Claude calls per user; retry with backoff on 429/5xx responses; make re-running the pipeline safe (no duplicate categorization of already-done transactions).

## Success Criteria
- [ ] Shipped and deployed (backend + frontend + DB reachable at a public URL)
- [ ] Core features working: CSV import, Claude-driven categorization with user correction, periodic insight generation, multi-user auth/isolation
- [ ] Clean code (reviewable): consistent structure, no dead code, secrets out of source control
- [ ] Tests for critical paths: cross-user data isolation, categorization pipeline idempotency, auth flows
- [ ] Can explain the architecture and tradeoffs: why FastAPI/Postgres/React, why Haiku vs. Sonnet, why batching/caching, how isolation is enforced

## Timeline
- Week 1-2: Setup, scaffold, core backend — FastAPI project structure, Postgres schema (users/accounts/transactions/categories), auth (JWT), CSV import endpoint
- Week 3-4: Backend features + testing — Claude categorization service (Haiku 4.5, prompt caching, Batches API for bulk import), categorization status/job tracking, cross-user isolation tests
- Week 5-6: Frontend — React dashboard: transaction list/review UI, category charts, auth flows wired to backend
- Week 7: Integration, debugging, polish — insights service (Sonnet 5, periodic aggregation + summary), end-to-end testing, error handling, rate-limit/retry hardening
- Week 8: Deploy, document, interview story — Render + Vercel deployment, README, final architecture write-up, interview story polish

## Interview Story (Draft)
"I built a multi-user personal finance dashboard that uses Claude to automatically categorize expenses and generate spending insights. The main technical challenge was managing Claude API cost and correctness at scale across many users' transaction histories — a naive per-transaction synchronous call approach would have been both slow and expensive. I solved it by combining the Batches API for bulk historical imports (roughly half the cost of synchronous calls), prompt caching on the stable categorization prompt so repeated classification calls didn't re-pay for the same context, and routing the classification workload to a cheaper, faster model tier while reserving a stronger model for the lower-volume, higher-reasoning insight-generation step. I also had to get multi-user data isolation right, since a leak between users is the worst failure mode for a finance app — I enforced isolation at the query layer, not just the API boundary, and wrote tests specifically to catch cross-user leaks. What I learned: matching the model and the API surface (synchronous vs. batch, cached vs. not) to the actual shape of the workload — high-volume/simple vs. low-volume/complex — is a real cost and latency lever, not just a theoretical one."

---

*Once shipped, add a "Final Interview Story" section here reflecting what actually happened during the build.*
