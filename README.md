# Agent-Skill-Project-Skeleton

A reusable starting point for **system-design work driven by Claude skills**. It bundles
three things that normally live apart:

1. A curated library of authored [Claude Skills](.claude/skills/) — mostly *decision gates*
   that force a reasoning step before Claude does the work.
2. The [`Architecture/`](Architecture/) knowledge base those skills are built from — the
   system-design notes that supply each skill's frameworks and vocabulary.
3. The plumbing to keep it honest — a prompt-logging hook, a batch-push script, and a
   skill that tests every new skill against its siblings for conflicts.

Drop this skeleton in front of a design problem and the relevant skill fires, asks for the
decision or the rep it needs, and produces an ADR / model / handoff doc from there.

## Layout

| Path | What's in it |
|---|---|
| [`.claude/skills/`](.claude/skills/) | The skill library (see below). |
| [`.claude/settings.json`](.claude/settings.json) | Wires the `UserPromptSubmit` prompt-logging hook. |
| [`.claude/_Prompts/logs/`](.claude/_Prompts/logs/) | Dated logs of every prompt submitted in the repo. |
| [`Architecture/`](Architecture/) | System-design notes: system design, backing services, web-server architecture, design patterns, devops, networking, security, testing, 12-factor. Source material for the skills. |
| [`Goals/`](Goals/) | Personal learning roadmap and AI-engineering framework notes. |
| [`Books/`](Books/) | Business and tech book notes. |
| [`scripts/`](scripts/) | `hooks/log-prompt.sh`, `git/batch-git-push.sh`. |
| `READ DELETE/` | Pre-reorg flat copies of skills, kept for diffing. Slated for deletion. |

## The skill library

Skills follow one shape: a `SKILL.md` entry point, companion `*.md` reference files for the
deep material, and a `README.md` explaining where the skill sits relative to its siblings.
Many are **gates** — they withhold the answer until a precondition (a hypothesis, a listed
unknown, a settled prior decision) is met, so AI doesn't quietly replace a learning rep.

### Data — a gated pipeline for data-architecture decisions

| Skill | Role |
|---|---|
| [`Architecture/Data/database-architecture`](.claude/skills/Architecture/Data/database-architecture/) | Decides **where** the source of truth lives (database-first / code-first / contract-first) and **which** store. Produces an ADR. |
| [`Architecture/Data/relational-modeling`](.claude/skills/Architecture/Data/relational-modeling/) | Turns a settled "we're relational" into table design — normal form and exceptions, keys, constraints, index plan, lifecycle columns. |
| [`Architecture/Data/data-tier-operations`](.claude/skills/Architecture/Data/data-tier-operations/) | Scales an existing database — replication topology, partitioning vs sharding, isolation level, distributed-transaction pattern, failover, pooling. |
| [`Architecture/Data/dimensional-modeling`](.claude/skills/Architecture/Data/dimensional-modeling/) | Designs an analytical OLAP model — fact-table grain, conformed / role-playing / degenerate dimensions, SCD strategy, star vs snowflake vs galaxy. |
| [`Architecture/Data/caching-strategy`](.claude/skills/Architecture/Data/caching-strategy/) | Decides whether to cache a read path and how — cache layer, cache-aside / write-through / etc., TTL vs explicit invalidation, eviction policy, stampede / avalanche handling. Produces an ADR. |

```
database-architecture   →  WHERE the schema lives + WHICH store  (ADR)
relational-modeling      →  tables for a relational store
data-tier-operations     →  sharding / replication / pooling / txn isolation
dimensional-modeling     →  star / snowflake / fact / dimension / warehouse
caching-strategy         →  cache layer / pattern / freshness / eviction
```

### Testing — deciding how to test, before writing tests

| Skill | Role |
|---|---|
| [`Testing/test-strategy`](.claude/skills/Testing/test-strategy/) | Picks the test mix for one surface — which levels (unit / integration / contract / E2E / smoke / acceptance), the effort split, the pipeline stage for each, non-functional scope, and whether TDD or BDD fits. Produces a test plan + ADR. |
| [`Testing/coverage-policy`](.claude/skills/Testing/coverage-policy/) | Sets one codebase's coverage policy — the metric, the target %, exclusions, and CI enforcement (overall vs new-code vs delta). Produces a policy doc. |
| [`Testing/test-practice-gate`](.claude/skills/Testing/test-practice-gate/) | Rep gate — the test-domain sibling of `problem-solving-gates`. Makes you state a test charter (behavior protected, failure modes, seam, done condition) before Claude writes a test. |

```
test-strategy       →  which levels exist, effort split, pipeline stage, TDD/BDD  (plan + ADR)
coverage-policy      →  coverage metric / target % / exclusions / CI enforcement   (policy doc)
test-practice-gate   →  the charter you state before Claude writes a test          (gate)
```

### Documents — pre-flight checks on files before using them

| Skill | Role |
|---|---|
| [`Documents/document-page-check`](.claude/skills/Documents/document-page-check/) | Integrity check for a paginated document (PDF / EPUB) before Claude reads, quotes, or summarizes it — confirms the file is complete and untruncated, flags blank / image-only pages, resolves the printed-vs-physical page-number offset, and spot-checks the citations an answer will lean on. Emits a report, then asks whether to gate or proceed. A mechanical pre-flight, not a reasoning gate. |

### Prompts — authoring, testing, and session hygiene

| Skill | Role |
|---|---|
| [`Prompts/ambiguity-gate`](.claude/skills/Prompts/ambiguity-gate/) | Asks before acting when a request could reasonably be read more than one way. |
| [`Prompts/prompt-archive`](.claude/skills/Prompts/prompt-archive/) | Archives a keeper prompt into `.claude/_Prompts/`, or logs the current session's prompts. |
| [`Prompts/prompt-tester`](.claude/skills/Prompts/prompt-tester/) | Runs a prompt against a few examples and reports whether it does what it claims. |
| [`Prompts/session-handoff`](.claude/skills/Prompts/session-handoff/) | Writes a structured handoff file before a session compacts or work resumes elsewhere. |
| [`Prompts/skill-interaction-testing`](.claude/skills/Prompts/skill-interaction-testing/) | Tests a new or changed skill against every sibling for stacking, contradiction, silent override, and beneficial chaining. |

### Architecture, Business, Skill Development, Git

| Skill | Role |
|---|---|
| [`Skill Development/learning-gate`](.claude/skills/Skill%20Development/learning-gate/) | Classifies intent (learning / execution / reference) and sets how much of the thinking Claude may do. |
| [`Skill Development/problem-solving-gates`](.claude/skills/Skill%20Development/problem-solving-gates/) | Rubber Duck (debugging), Options Generator (architecture), Knowledge Checker, Optimization (faster/cheaper, bring a profile) — each requires prior independent effort. |
| [`Architecture/design-scoping`](.claude/skills/Architecture/design-scoping/) | **Front-door gate** for a system-design effort — refuses to design until purpose + audience, functional + explicit out-of-scope, the six non-functional numeric targets, constraints (incl. compliance), and the 1–2 deep-dive decisions are stated. Output: a scope statement that sequences into `capacity-estimation` → `microservices-decision` → `api-interface-style` → `database-architecture` → `failure-mode-analysis`. Defers to `ambiguity-gate` for "what does this request even mean". |
| [`Architecture/microservices-decision`](.claude/skills/Architecture/microservices-decision/) | Whether and how to split services, bounded by the number of people who can own them. |
| [`Architecture/capacity-estimation`](.claude/skills/Architecture/capacity-estimation/) | A-priori back-of-the-envelope for a system that doesn't exist yet — gated on stated assumptions (DAU, actions/user, payload sizes, R:W, peak:avg, retention + growth, replication), walks storage → traffic → cache → servers, and names **what binds first**. Feeds `technical-cost-decision` (dollars), `data-tier-operations` (topology), `resilience-strategy` (defense). |
| [`Architecture/failure-mode-analysis`](.claude/skills/Architecture/failure-mode-analysis/) | Structured FMEA / pre-mortem procedure (not a gate) — walks every component + interaction across nine failure categories, scores an RPN register (severity × occurrence × detection, or a 5×5 grid), separates a high-severity watchlist, emits a prioritized failure-mode register + handoffs to `resilience-strategy` / `observability-strategy` / `test-strategy`. Asks register-only vs block-sign-off. |
| [`Architecture/api-interface-style`](.claude/skills/Architecture/api-interface-style/) | Picks the interaction style for one API surface — REST / GraphQL / gRPC / WebSocket / SSE / webhooks / async messaging — from its consumers, interaction shape, and latency / real-time needs. Produces an ADR. |
| [`Architecture/observability-strategy`](.claude/skills/Architecture/observability-strategy/) | Decides how a system is instrumented — signal set (metrics / logs / traces / profiling), SLIs & SLOs, sampling & cardinality budget, symptom-based alerting, retention, self-hosted vs managed. Produces an ADR. |
| [`Architecture/resilience-strategy`](.claude/skills/Architecture/resilience-strategy/) | Decides how a request path protects itself under overload and dependency failure — priority-aware load shedding, rate limiting, concurrency limits & backpressure, circuit breakers, timeout / retry-budget / jitter, bulkheads, graceful degradation — and where each control sits. Produces an ADR. |
| [`Architecture/migration-cutover`](.claude/skills/Architecture/migration-cutover/) | Decides how a live workload moves to a new system — cutover pattern (big-bang / phased / parallel-run / strangler), data-move mechanic (freeze-copy / bulk+CDC / dual-write+reconcile), the verification bar, the rollback window and its point of no return, the consumer sequence. Produces an ADR. |
| [`Architecture/deployment-strategy`](.claude/skills/Architecture/deployment-strategy/) | Decides how a new version of one deployable unit reaches production — rollout mechanism (recreate / rolling / blue-green / canary / feature-flag), environment progression, expand/contract schema discipline, the health signal that aborts a rollout, cadence. Produces an ADR. |
| [`Architecture/cloud-iam-boundary`](.claude/skills/Architecture/cloud-iam-boundary/) | Decides who/what gets access to a cloud resource and its network placement — principal, least-privilege permission set, trust boundary & credential lifetime (STS-assumed role vs long-lived keys), permissions-boundary/SCP ceiling, public vs private subnet. Produces an ADR. |
| [`Architecture/serverless-execution-model`](.claude/skills/Architecture/serverless-execution-model/) | Decides how one unit of work runs — compute primitive (FaaS / container task / long-running service), invocation model (sync / async / poll-based), orchestration vs choreography, and the per-invocation failure contract (Retry/Catch, DLQ, idempotency). Produces an ADR. |
| [`Business/technical-cost-decision`](.claude/skills/Business/technical-cost-decision/) | Forces the cost arithmetic on any decision that carries a recurring price. |
| [`Business/ticket-evaluation`](.claude/skills/Business/ticket-evaluation/) | Separates what a ticket says from what it's missing from what can be judged; verdict last. |
| [`Business/explaining-my-work`](.claude/skills/Business/explaining-my-work/) | One evidence base rendered at three altitudes — plain summary, spoken script, public post. |
| [`Git/commit-and-push`](.claude/skills/Git/commit-and-push/) | Stages, commits, and pushes with a message derived from the actual diff. |

## Prompt logging

[`.claude/settings.json`](.claude/settings.json) registers a `UserPromptSubmit` hook that
runs [`scripts/hooks/log-prompt.sh`](scripts/hooks/log-prompt.sh). Every submitted prompt is
appended to `.claude/_Prompts/logs/YYYY-MM-DD.md` with a timestamp and short session id. The
hook is defensive by design — it always exits 0 and prints nothing, so it can neither block a
prompt nor inject text into context.

## Adding a skill

1. Draft it (`SKILL.md` + reference files + `README.md`) under the right group in `.claude/skills/`.
2. Screen it in isolation — baseline fails without it, the skill fixes the failure.
3. Run [`Prompts/skill-interaction-testing`](.claude/skills/Prompts/skill-interaction-testing/)
   against the existing skill set. Record what you found (hand-off, absorption, chaining, or a
   fix for stacking / contradiction / silent override).
