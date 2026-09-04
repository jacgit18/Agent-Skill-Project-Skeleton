# Skill Catalog

Every Claude Skill in this repo — what it does, what triggers it, what it refuses to do, and
what it produces. Add a row here when a skill lands; move it out of "Planned" when it does.

Most of these skills are **gates**: they withhold the answer until a precondition is met (a
hypothesis, a listed unknown, a settled prior decision, a stated pressure with numbers), so the
assistant doesn't quietly do a reasoning rep the user could do themselves. Each skill was
written from a note in the `PersonalBrain` Obsidian vault ("DevHiveMind") — the source note is
named in each entry.

**Count:** 25 skills — across `Architecture/` (incl. `Architecture/Data/`), `Business/`,
`Skill Development/`, `Testing/`, `Prompts/`, and `Git/`.

---

## Data — a gated pipeline for data-architecture decisions

The five Data skills chain in sequence. Each stops before implementation and hands off.

```
database-architecture   →  WHERE the source of truth lives + WHICH store   → ADR
relational-modeling      →  design the OLTP tables (normalized)             → data-model doc
data-tier-operations     →  scale / distribute an existing store            → ADR
dimensional-modeling     →  design the OLAP model (star / dimensions / SCD) → data-model doc
caching-strategy         →  cache a read path (layer / pattern / freshness) → ADR
```

### `Architecture/Data/database-architecture`
- **Does:** Decides where a piece of data's source of truth should live — database-first,
  code-first, or contract-first — and which store, given the system boundaries and consumers.
- **Triggers on:** about to design or change a schema, an API shape, or a domain model; "where
  should this data live", "should the DB or the code own this".
- **Gate:** will not emit a schema or recommendation until the user answers consumers /
  ownership / exposure / evolution / source-of-truth leaning **in their own words**.
- **Produces:** a recommendation block in chat, then a numbered ADR in
  `docs/architecture/decisions/` on approval.
- **Source note:** `database schema disscusiion.md`. Companion files: `decision-framework.md`,
  `schema-taxonomy.md`, `adr-template.md`.

### `Architecture/Data/relational-modeling`
- **Does:** Turns a settled "we're relational" into a table design — normal form and the
  denormalization exceptions, key strategy (surrogate vs natural, int vs UUID), constraint
  placement, an index plan, lifecycle/audit columns, relationship patterns.
- **Triggers on:** "model the schema for X", "how should I normalize this", "what should I
  index", "surrogate or natural key", "how do I handle soft deletes".
- **Gate:** requires the `database-architecture` ADR (or an explicit "we're on Postgres and
  staying"). Bounces the user back rather than modeling on an assumption.
- **Produces:** an ERD sketch and table-by-table spec in `docs/data-model/<slug>.md`.
- **Source notes:** `Architecture/02. Backing Service Options/Databases/` — Normalization &
  Denormalization, Database Indexing, Database Core Functionality, GUIDs, Record Life Cycle,
  Database Table Relationship Types, Self-joining relationships. Companion files:
  `modeling-framework.md`, `normalization-and-keys.md`, `indexing-and-constraints.md`.

### `Architecture/Data/data-tier-operations`
- **Does:** Scales and distributes an existing database — read replicas and replication
  topology, partitioning vs sharding and the shard-key choice, transaction isolation,
  distributed-transaction pattern (2PC / Saga / outbox / eventual), failover and RPO/RTO,
  connection pooling.
- **Triggers on:** "we're hitting a wall on the DB", "do we need to shard", "which shard key",
  "read replicas", "our writes don't fit on one node". Not for diagnosing one slow endpoint.
- **Gate:** refuses a topology until the user supplies a real measured pressure, current
  numbers (data size, read/write QPS, p95, connection headroom, growth), per-operation
  consistency needs, and RPO/RTO + operational capacity. Walks the cheaper options first.
- **Produces:** a recommendation block, then an ADR reusing `database-architecture`'s template.
- **Source notes:** `Architecture/02. Backing Service Options/Databases/` — Database Sharding,
  Sharding & Pagination, Replication Strategies, Master-Slave, Leaderless Architecture,
  Distributed Transactions, Transaction Locking, Connection Pooling, Database Points of Failure,
  Database Hosting. Companion files: `operations-framework.md`, `scaling-topologies.md`,
  `consistency-and-transactions.md`.

### `Architecture/Data/dimensional-modeling`
- **Does:** Designs an analytical (OLAP) model — the business process and the fact-table grain,
  the dimensions and which are conformed / role-playing / degenerate / junk, additive vs
  semi-additive measures, star vs snowflake vs galaxy, slowly-changing-dimension strategy per
  dimension, fact-table type.
- **Triggers on:** "model this for reporting", "star schema for X", "how do I track history on
  this dimension", "warehouse vs mart".
- **Gate:** refuses to draw fact/dimension tables until the user supplies the business process,
  the grain, the actual report list, the dimensions, per-dimension history needs, and source +
  refresh cadence + scale.
- **Produces:** a design summary and a dimensional ERD + table specs in
  `docs/data-model/analytics/<slug>.md`, grain statement at the top.
- **Source notes:** `Architecture/02. Backing Service Options/Databases/` — Data Warehouse,
  Data Mart, Star Schema, Snowflake Schema, Fact Table, Dimension Table, Data Grain, Choosing
  Schema, Materialized Views. Companion files: `modeling-framework.md`, `star-vs-snowflake.md`,
  `dimensions-and-scd.md`.

### `Architecture/Data/caching-strategy`
- **Does:** Decides whether a cache belongs in front of a read path, and if so the layer
  (client/HTTP, CDN, reverse proxy, in-process, distributed Redis/Memcached, DB cache), the
  read/write pattern (cache-aside / read-through / write-through / write-behind / refresh-ahead),
  the freshness mechanism (explicit invalidation vs TTL vs versioned keys), the eviction policy
  and sizing, and the failure-mode handling (stampede / penetration / avalanche / cache-down).
- **Triggers on:** "we should add a cache", "put Redis in front of X", "what TTL", "cache-aside
  or write-through", "the cache serves stale data", "thundering herd when a hot key expires",
  "cache it at the CDN". Not for scaling the DB itself, not for cost-sizing the cache tier.
- **Gate:** refuses a cache design until the user supplies a measured pressure (latency miss /
  source load / downstream limit), current numbers (read QPS, p95/p99 vs target, payload,
  source load, key cardinality), per-data-class change rate + writer set + staleness tolerance,
  and whether the cache is an optimization or load-bearing. Rules out the non-cache fixes
  (index, replica, pagination, denormalization, HTTP headers) first.
- **Produces:** a recommendation block, then an ADR reusing `database-architecture`'s template.
- **Source notes:** `Architecture/Library/Memory/` — `Caches.md` (cache types, strategies,
  policies, SPOF), `Content Delivery Network.md`. Companion files: `caching-framework.md`,
  `cache-placement.md`, `patterns-and-policies.md`.

---

## Testing — deciding how to test, before writing tests

Three skills. Two are decision gates that stop before implementation; one is a rep gate over
the act of writing a test.

```
test-strategy       →  which test levels exist, effort split, pipeline stage, TDD/BDD   → plan + ADR
coverage-policy      →  the coverage metric, target %, exclusions, CI enforcement         → policy doc
test-practice-gate   →  the charter you must state before Claude writes a test            → gate, no artifact
```

### `Testing/test-strategy`
- **Does:** Picks the test mix for one surface — which levels (unit / integration / contract
  / E2E / smoke / acceptance), what share each gets, which pipeline stage each runs in,
  whether non-functional testing (load / perf / security) is in scope, and whether a TDD or
  BDD/Gherkin workflow fits.
- **Triggers on:** "how should we test this service", "do we need E2E here", "unit or
  integration", "should we do TDD", "is BDD worth it", "tests pass but prod keeps breaking",
  or a proposed mix to pressure-test ("100% E2E").
- **Gate:** no mix until the user states the surface and its seams, the cost of failure per
  area, consumers/contracts, the pipeline stages that actually exist, any non-functional
  numbers, change rate/lifetime, and who maintains the suite + the CI budget.
- **Produces:** a recommendation block, a test plan in `docs/testing/<slug>.md`, and an ADR
  in `docs/architecture/decisions/` for the contested calls only.
- **Source notes:** `Architecture/Testing/` — Testing Hierarchy (70/20/10), Testing Stages
  Relationship, Unit / Integration vs System Integration / End to End / Smoke / Acceptance
  family, Functional & Non-functional Testing, Types of Testing Technique, Data Driven
  Testing, TDD, BDD, Cucumber vs Gherkin. Companion files: `selection-framework.md`,
  `test-levels.md`, `adr-template.md`.

### `Testing/coverage-policy`
- **Does:** Sets one codebase's or module's coverage policy — the metric (statement /
  branch / function / line), the target number, what's excluded from measurement, and
  whether CI blocks on it (overall vs new-code vs delta).
- **Triggers on:** "what coverage should we require", "enforce 80% in CI?", "do we need
  100%", "the coverage gate is a checklist exercise", "how do we handle coverage on this
  legacy module", "the build failed on a coverage drop — is that right".
- **Gate:** no number until the user states what kind of code it is (criticality), its
  change frequency and lifespan, where coverage is now + what has actually broken, the
  team's enforcement appetite, and whether a legacy backfill is realistic.
- **Produces:** a recommendation block, then a policy document in
  `docs/testing/coverage-policy.md` (ADR optional, only if enforcement was contested).
- **Source notes:** `Architecture/Testing/` — Code Coverage (the four metrics), Code
  Coverage Best Practices (no universal ideal, the 60/75/90 band, gate bases, the
  boy-scout ratchet, the checklist trap, mutation testing), Test Branch Coverage. Companion
  files: `policy-framework.md`, `coverage-metrics.md`.

### `Testing/test-practice-gate`
- **Does:** A rep gate — the test-domain sibling of `problem-solving-gates`. Before writing
  tests for a specific piece of code (when the user is building testing skill, not just
  producing a suite they already know), makes them state a **test charter**: the behavior
  each test protects, the failure modes worth covering, the seam (stub vs real), the done
  condition. Then Claude renders the charter as code and gap-checks it — nothing more.
- **Triggers on:** "write tests for this function", "help me test this", "what should I test
  here", "add unit tests for X" — without the user having said what the tests verify.
- **Does not apply to:** plain execution ("I know what these cover, port them"), the test
  mix for a surface (`test-strategy`), the coverage % (`coverage-policy`), reviewing
  existing tests (`code-review`).
- **Produces:** no artifact — it gates a coding action. Pointed to from `learning-gate`
  Step 3.
- **Source notes:** `Architecture/Testing/` — Test Setup, Stubbing, Test Cases Guideline,
  Causes of Test Failure, Data Driven Testing, Testing Lifecycle Hooks, Design patterns in
  testing. Companion file: `charter-guide.md`; `examples/`.

---

## Prompts — authoring, testing, and session hygiene

### `Prompts/ambiguity-gate`
- **Does:** Stops and asks one focused question when a request could reasonably be read more
  than one way and the wrong reading would waste real work.
- **Triggers on:** vague verbs ("clean up", "fix this", "make it better", "shorter"), unstated
  scope / format / audience / time frame; also when a reply is about to open with a menu of
  clarifying questions or framings the user never used.
- **Does not apply to:** reference lookups, factual questions, casual conversation.
- **Source note:** the ambiguity / clarification note in the vault.

### `Prompts/prompt-archive`
- **Does:** Two modes — **archive** a keeper prompt into `.claude/_Prompts/` as a formatted
  markdown file, or **log** the current session's prompts to `.claude/_Prompts/logs/YYYY-MM-DD.md`.
- **Triggers on:** "save this prompt", "add to my prompt library", "dump my prompts".
- **Relationship:** the `UserPromptSubmit` hook already captures every prompt automatically;
  this skill is the curated / on-demand path on top of that. Not for evaluating a prompt (that
  is `prompt-tester`).
- **Companion file:** `frontmatter-template.md`.

### `Prompts/prompt-tester`
- **Does:** Runs a prompt against a few examples and reports whether it does what it claims,
  including an assessment phase that flags gaps and says whether the prompt should stay as-is,
  be refined, or move into a skill/agent container.
- **Triggers on:** "test this prompt", "does this prompt work", "is this prompt any good".
- **Boundary:** reports findings; does not rewrite the prompt.

### `Prompts/session-handoff`
- **Does:** Writes a structured handoff file — goals, current state, files touched, what
  changed, next steps — before context is lost.
- **Triggers on:** session running long or about to compact; "pick this up later", "new chat",
  "save my progress", "handoff", "recap file". Fires proactively.

### `Prompts/skill-interaction-testing`
- **Does:** Tests a new or changed skill against every other skill in the repo for stacking
  (multiple gates firing in sequence), contradiction, silent override (a broader skill claims
  the request first), and beneficial chaining.
- **Triggers on:** after writing or substantially revising a skill, before calling it done;
  also after an existing skill's trigger description is widened.
- **Run record:** five rounds logged in `memory/` (prompt-archive, relational-modeling,
  data-tier-operations, dimensional-modeling, api-interface-style) — each produced description
  edits or a structural fix (e.g. the `learning-gate` routing/double-gating fixes).

---

## Architecture, Business, Skill Development, Git

### `Skill Development/learning-gate`
- **Does:** Classifies intent (reference / execution / learning / ambiguous) and, only for
  genuine learning intent, sets how much of the thinking the assistant may do — a 0–5
  assistance scale — and names the next rep the user should do first.
- **Triggers on:** "what is X", "how does X work", "help me understand X", open-ended
  design/debug questions where it's not obvious the user just wants the answer.
- **Anti-paternalism:** first act is always the intent check; execution and reference requests
  bypass the gate entirely; "just tell me" switches it off for the thread.
- **Sits above** `problem-solving-gates` (decides *whether* you reason now; that skill defines
  *what* the reasoning is) and hands off to the Data skills on data questions rather than
  double-gating.
- **Source note:** `learning Gate.md`. Companion files: `concept-learning.md`,
  `assistance-levels.md`.

### `Skill Development/problem-solving-gates`
- **Does:** Four gated modes — **Rubber Duck** (debugging, bring a hypothesis), **Options
  Generator** (architecture decision, bring constraints + a lean), **Knowledge Checker** (bring
  a first-pass explanation), **Optimization** (making something faster/cheaper, bring a
  profile / benchmark of where the time actually goes). Each keeps the assistant's
  contribution deliberately narrow.
- **Triggers on:** "what's wrong with my code", "what should I do", "am I right that X", "how
  do I speed this up" — without a shown attempt (or, for Optimization, a measurement).
- **Does not apply to:** writing new code from scratch, or reviewing a finished draft.
- **Companion folder:** `examples/` (one per mode).

### `Architecture/microservices-decision`
- **Does:** Whether and how to adopt microservices, split a monolith, or draw service
  boundaries — forcing the arithmetic of *who can own each service* into the open before any
  boundary is drawn.
- **Triggers on:** "should we go microservices", "split this monolith", "how many services",
  "here's our service list — check it"; including when the decision is presented as already
  made.
- **Boundary:** stops at a decision, a design posture, and an ADR. Not performance triage, not
  database sharding (that's `data-tier-operations`).

### `Architecture/api-interface-style`
- **Does:** Picks the interaction style for **one** API surface — REST / GraphQL / gRPC /
  WebSocket / SSE / webhooks / async messaging — plus sync-vs-async and request-response-vs-push,
  given the surface's consumers, the interaction shape, and its query / latency / real-time
  needs. Recommends a primary style and a secondary for any sub-case that doesn't fit.
- **Triggers on:** "REST or GraphQL", "should we use gRPC", "how should the frontend talk to
  the backend", "we need real-time updates — websockets?", "webhooks vs polling", "is our API
  over-fetching", or a proposed style to check.
- **Gate:** will not name a protocol until the user states the surface and its two ends,
  consumers and their platform limits, interaction shape (request-response / server-push /
  streaming / bidirectional / events), data-and-query shape, latency & throughput, real-time
  need and direction, consumer reachability, and public-vs-internal — in their own words.
- **Boundary:** *not* where the authoritative definition lives (contract-first vs code-first →
  `database-architecture`); *not* whether to split into services (→ `microservices-decision`);
  *not* cost-at-volume or managed-vs-self-hosted gateway (→ `technical-cost-decision`).
  Defers versioning mechanics, auth-scheme choice, and gateway/BFF placement — names them, does
  not decide them.
- **Produces:** a recommendation block in chat, then a numbered ADR in
  `docs/architecture/decisions/` on approval.
- **Source notes:** `Architecture/02. Backing Service Options/API/` — API Architecture Styles,
  API Design Basics, rest & Websockets, Designing APIs with WebHooks, Evolution of APIs, API
  Call. Companion files: `selection-framework.md`, `style-tradeoffs.md`, `adr-template.md`.

### `Architecture/observability-strategy`
- **Does:** Decides how a service/system is made observable — which signals to invest in
  (metrics, structured logs, distributed traces, profiling, events), the SLIs that define
  "working" and whether to set SLOs + an error budget, the instrumentation approach (OTel
  SDK / auto-instrumentation / vendor agent + collector topology), sampling (head vs tail)
  and the metric-label / log-field cardinality budget, the alerting policy (symptom / SLO-burn
  paging vs cause-based tickets), retention tiers per signal, and self-hosted vs managed.
- **Triggers on:** "we need monitoring / observability", "add Datadog / Grafana / Honeycomb",
  "set up distributed tracing", "what should we alert on", "we can't tell why prod is slow",
  "incidents take hours to diagnose", "we're committing to an SLA", or a proposed approach to
  check ("log everything", "100% trace sampling", "alert on every error").
- **Gate:** refuses a signal/tool/alert until the user supplies the triggering pressure (a
  specific incident / named blind spot / SLA / cost problem — not "best practice"), the
  user-facing SLIs, the architecture shape + request-path hop count, request volume +
  high-cardinality dimensions, retention/PII constraints, and operational capacity + on-call.
- **Boundary:** *not* the dollar sizing of the telemetry backend (→ `technical-cost-decision`);
  *not* diagnosing one slow endpoint now (→ `problem-solving-gates` Rubber Duck / Optimization);
  *not* whether to split services (→ `microservices-decision`, whose shape it consumes);
  *not* SIEM / audit logging as a compliance control (future `security-architecture`).
- **Produces:** a recommendation block, then an ADR reusing `database-architecture`'s template.
- **Source notes:** `Architecture/` — `Monitoring & Observability.md`, `Distributed Tracking &
  Monitoring.md`, `OpenTelemetry.md`, `12 Key Metrics for Measuring Service Performance.md`,
  `Fault Tolerance.md`, `Chaos Engineering.md`. Companion files: `observability-framework.md`,
  `signals-and-slos.md`.

### `Architecture/resilience-strategy`
- **Does:** Decides how a service or request path protects itself under overload and
  dependency failure — priority-aware load shedding, rate limiting (per-client vs global,
  token-bucket / sliding-window), concurrency limiting and backpressure, circuit breakers on
  outbound calls, timeout / retry-budget / backoff-with-jitter, bulkhead pool isolation,
  graceful degradation with fallbacks — plus where each control sits (edge / gateway / mesh /
  in-process).
- **Triggers on:** "we need rate limiting", "add a circuit breaker", "the service falls over
  under load", "a slow dependency took everything down", "one noisy client starved everyone",
  "how do we degrade gracefully", "we need backpressure", "load shedding", or a proposed
  mechanism to check ("retry 3× on every failure", "rate-limit everyone to 100 rps").
- **Gate:** refuses a mechanism until the user supplies the triggering incident or capacity
  ceiling, what resource binds first (load-tested if unknown), the priority tiers of the
  traffic, the client model (attributable vs aggregate), the downstream dependencies and
  their fallbacks, and reject-vs-buffer semantics per class.
- **Boundary:** *not* detecting or alerting on overload (→ `observability-strategy`, whose
  SLIs it consumes); *not* scaling the datastore or DB pooling (→ `data-tier-operations`, a
  complement to the upstream limit); *not* the cache design (→ `caching-strategy`, though
  stale-serve is a degradation fallback it names); *not* diagnosing one endpoint's failure
  last night (→ `problem-solving-gates` Rubber Duck).
- **Produces:** a recommendation block, then an ADR reusing `database-architecture`'s template.
- **Source notes:** `Architecture/02. Backing Service Options/` — `Load Shedding.md`, `Load
  Shedding Implementation.md`, `Load Balancer.md`, `Rate Limiting.md`; `Architecture/` —
  `Fault Tolerance.md`, `Chaos Engineering.md`. Companion files: `resilience-framework.md`,
  `mechanisms-and-tradeoffs.md`.

### `Architecture/migration-cutover`
- **Does:** Decides how a live workload moves from one system to another — a datastore
  replacement, an application replatform, a hosting relocation — covering the cutover pattern
  (big-bang / phased-by-slice / parallel-run with dual-write + shadow reads / strangler-fig),
  the data-move mechanic (freeze-and-copy / bulk load + CDC / dual-write + backfill +
  reconcile), the verification bar that authorises the flip, the rollback window and its
  point of no return, and the consumer sequence.
- **Triggers on:** "we're migrating from X to Y", "move off the old system", "cut over to the
  new database", "replatform this", "lift-and-shift to the cloud", "the legacy system is
  being retired", "move the data without downtime", or a proposed migration plan to check.
- **Gate:** refuses a cutover plan until the user supplies the dated driver (EOL / cost /
  capability gap / compliance / consolidation — not "modernise"), the scope and an explicit
  out-of-scope list, the data volume × change rate × schema delta, the downtime and RPO
  budget, the rollback window and point of no return, the consumer coupling, and the
  verification threshold.
- **Boundary:** *not* choosing the target store / paradigm (→ `database-architecture`); *not*
  scaling a store that's staying (→ `data-tier-operations`, which hands the execution of a
  live move here); *not* a routine version release of an existing unit (→ `deployment-strategy`).
- **Produces:** a recommendation block, then an ADR reusing `database-architecture`'s template.
- **Source note:** `Architecture/01. System Design/Migration Plan.md`. Companion files:
  `cutover-framework.md`, `cutover-patterns.md`.

### `Architecture/deployment-strategy`
- **Does:** Decides how a new version of one deployable unit reaches production — the rollout
  mechanism (recreate / rolling / blue-green / canary / feature-flag-gated), the environment
  progression that actually gates a release, the expand/contract discipline for
  backward-compatible schema and contract changes, the health signal that aborts a rollout
  and the auto-rollback trigger, and the release cadence.
- **Triggers on:** "we need zero-downtime deploys", "blue-green or canary", "our deploys
  cause an outage", "rollbacks take too long", "releases are scary so we batch them", "set up
  a staging pipeline", or a proposed rollout approach to check.
- **Gate:** refuses a mechanism until the user supplies what's wrong with releases today
  (measured downtime / a blast-radius incident / slow rollback / the batching doom-loop), the
  unit and its class, the downtime tolerance and traffic shape, the rollback speed needed,
  the state and contract coupling, the progressive-delivery infrastructure that exists, the
  environments that actually gate, and the cadence.
- **Boundary:** *not* moving a workload to a different system (→ `migration-cutover`); *not*
  which test levels run in the pipeline (→ `test-strategy`, whose stage list it consumes);
  *not* the health signal's own design (→ `observability-strategy`); *not* the cost of a
  second stack (→ `technical-cost-decision`).
- **Produces:** a recommendation block, then an ADR reusing `database-architecture`'s template.
- **Source notes:** `Architecture/Devops/` — `Deployment Strategies.md`, `Release.md`, `Staged
  Deployment.md`, `Steps to Release Stage.md`, `Deployment Artifacts.md`; 12-factor `V Build,
  release, run.md`; `Database Migrations.md`. Companion files: `deployment-framework.md`,
  `rollout-patterns.md`.

### `Business/technical-cost-decision`
- **Does:** Forces three specific calculations on any technical decision that carries a
  recurring price — infra vs managed, sizing against a stated volume, build-vs-buy, planning
  work to cut a cloud bill.
- **Triggers on:** a request mentioning a monthly spend, a budget, a savings target, a stated
  volume (requests/day, users, GB, tokens), or "is this going to get expensive".
- **Discipline:** one significant figure with stated assumptions. `~$3k/month` is an answer;
  `$2,847.61/month` is a lie. A Cost Surface showing $80/month is a valid reason to stop.

### `Business/ticket-evaluation`
- **Does:** Separates what a ticket *says* from what it's *missing* from what can *actually be
  judged*, and keeps the verdict (proceed / defer / needs more info / reconsider) at the bottom
  where it can't outrun its caveats.
- **Triggers on:** a Jira/Linear/GitHub issue or pasted feature description shared for sizing,
  prioritization, or a go/no-go read; backlog grooming; comparing tickets.
- **Boundary:** does not rewrite the ticket or design the feature.

### `Business/explaining-my-work`
- **Does:** Builds one evidence base from the session and the repo, then renders it three times
  — plain-language summary, spoken conversation script, LinkedIn draft — with every claim
  traced to something that actually happened.
- **Triggers on:** "turn this into a LinkedIn post", "how do I explain this to a
  non-technical person", "write this up for my resume", "what do I say at the meetup";
  preparing for an interview, standup, or recruiter call.
- **Boundary:** drafts only; never posts. Manufactured metrics are a hard failure.

### `Git/commit-and-push`
- **Does:** Stage → commit → push, with the message built from the actual diff. Matches the
  repo's convention, splits unrelated changes, runs a pre-commit sanity pass (secrets, `.env`,
  large blobs, debug code, merge markers), branches off the default branch when told nothing.
- **Triggers on:** "commit this", "push my changes", "save this to git", "write the commit
  message".
- **Boundary:** stops after `git push`. No PRs, no merge-conflict resolution, no history
  rewriting. Defers bulk file additions to `scripts/git/batch-git-push.sh`.

---

## Planned / candidate skills

Directions the source notes already sketch. None built yet.

| Candidate | What it would do | Source |
|---|---|---|
| **Git-workflow skills** | Beyond `commit-and-push` — PR authoring, branch strategy, conflict resolution. | `.claude/skills/Git/` (currently only `commit-and-push`). |
| **contract-authoring** | API/event contract *authoring* once the style is chosen — versioning scheme, backward/forward compatibility, DTO and error-shape design, deprecation policy. The pieces `api-interface-style` explicitly defers. | `database-architecture` README, "Still not built"; `api-interface-style` "Deferred". |
| **implementation** | Turning an approved ADR into migrations, models, DTOs, and wiring — the step the Data skills deliberately stop before. | `database schema disscusiion.md`, sketched as an agent. |
| **Practice Gates** (code / database) | Rep-oriented gating for implementation work — siblings of `problem-solving-gates` and `Testing/test-practice-gate` (the test one, now built), pointed to from `learning-gate` Step 3. | `learning-gate` README, "Not built". |
| **Architecture Impact / Risk Analysis / Test Generation / Refactoring agents** | Four of the five agents mapped to system surfaces, run at PR / dev / deploy stages. (The fifth, Observability, is partly served by `observability-strategy` — a decision gate, not a PR-stage agent.) | `Goals/AI/Agents.md`, "The Five Agents I Would Build". |

---

## How a skill gets added

1. Draft it under the right group: `SKILL.md` (entry point + gate + output contract),
   companion `*.md` reference files, `README.md` (where it sits relative to siblings).
2. Screen it in isolation — baseline fails without it, the skill fixes the failure, refactoring
   keeps it fixed.
3. Run `Prompts/skill-interaction-testing` against the existing set. Record the outcome
   (hand-off, absorption, chaining) or the fix (stacking, contradiction, silent override) in
   `memory/`.
4. Add a row to this catalog.
