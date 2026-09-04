# Skill Catalog

Every Claude Skill in this repo — what it does, what triggers it, what it refuses to do, and
what it produces. Add a row here when a skill lands; move it out of "Planned" when it does.

Most of these skills are **gates**: they withhold the answer until a precondition is met (a
hypothesis, a listed unknown, a settled prior decision, a stated pressure with numbers), so the
assistant doesn't quietly do a reasoning rep the user could do themselves. Each skill was
written from a note in the `PersonalBrain` Obsidian vault ("DevHiveMind") — the source note is
named in each entry.

**Count:** 17 skills — 8 top-level, 4 in `Data/`, 5 in `Prompts/`. `Git/` is an empty
placeholder.

---

## Data — a gated pipeline for data-architecture decisions

The four Data skills chain in sequence. Each stops before implementation and hands off.

```
database-architecture   →  WHERE the source of truth lives + WHICH store   → ADR
relational-modeling      →  design the OLTP tables (normalized)             → data-model doc
data-tier-operations     →  scale / distribute an existing store            → ADR
dimensional-modeling     →  design the OLAP model (star / dimensions / SCD) → data-model doc
```

### `Data/database-architecture`
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

### `Data/relational-modeling`
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

### `Data/data-tier-operations`
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

### `Data/dimensional-modeling`
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

## Decision skills (top level)

### `learning-gate`
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

### `problem-solving-gates`
- **Does:** Three gated modes — **Rubber Duck** (debugging, bring a hypothesis), **Options
  Generator** (architecture decision, bring constraints + a lean), **Knowledge Checker** (bring
  a first-pass explanation). Each keeps the assistant's contribution deliberately narrow.
- **Triggers on:** "what's wrong with my code", "what should I do", "am I right that X" —
  without a shown attempt.
- **Does not apply to:** writing new code from scratch, or reviewing a finished draft.
- **Companion folder:** `examples/`.

### `microservices-decision`
- **Does:** Whether and how to adopt microservices, split a monolith, or draw service
  boundaries — forcing the arithmetic of *who can own each service* into the open before any
  boundary is drawn.
- **Triggers on:** "should we go microservices", "split this monolith", "how many services",
  "here's our service list — check it"; including when the decision is presented as already
  made.
- **Boundary:** stops at a decision, a design posture, and an ADR. Not performance triage, not
  database sharding (that's `data-tier-operations`).

### `api-interface-style`
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

### `technical-cost-decision`
- **Does:** Forces three specific calculations on any technical decision that carries a
  recurring price — infra vs managed, sizing against a stated volume, build-vs-buy, planning
  work to cut a cloud bill.
- **Triggers on:** a request mentioning a monthly spend, a budget, a savings target, a stated
  volume (requests/day, users, GB, tokens), or "is this going to get expensive".
- **Discipline:** one significant figure with stated assumptions. `~$3k/month` is an answer;
  `$2,847.61/month` is a lie. A Cost Surface showing $80/month is a valid reason to stop.

### `ticket-evaluation`
- **Does:** Separates what a ticket *says* from what it's *missing* from what can *actually be
  judged*, and keeps the verdict (proceed / defer / needs more info / reconsider) at the bottom
  where it can't outrun its caveats.
- **Triggers on:** a Jira/Linear/GitHub issue or pasted feature description shared for sizing,
  prioritization, or a go/no-go read; backlog grooming; comparing tickets.
- **Boundary:** does not rewrite the ticket or design the feature.

### `explaining-my-work`
- **Does:** Builds one evidence base from the session and the repo, then renders it three times
  — plain-language summary, spoken conversation script, LinkedIn draft — with every claim
  traced to something that actually happened.
- **Triggers on:** "turn this into a LinkedIn post", "how do I explain this to a
  non-technical person", "write this up for my resume", "what do I say at the meetup";
  preparing for an interview, standup, or recruiter call.
- **Boundary:** drafts only; never posts. Manufactured metrics are a hard failure.

### `commit-and-push`
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
| **Git-workflow skills** | Beyond `commit-and-push` — PR authoring, branch strategy, conflict resolution. | Empty `.claude/skills/Git/` placeholder. |
| **contract-authoring** | API/event contract *authoring* once the style is chosen — versioning scheme, backward/forward compatibility, DTO and error-shape design, deprecation policy. The pieces `api-interface-style` explicitly defers. | `database-architecture` README, "Still not built"; `api-interface-style` "Deferred". |
| **implementation** | Turning an approved ADR into migrations, models, DTOs, and wiring — the step the Data skills deliberately stop before. | `database schema disscusiion.md`, sketched as an agent. |
| **Practice Gates** (code / test / database) | Rep-oriented gating for implementation work — siblings of `problem-solving-gates`, pointed to from `learning-gate` Step 3. | `learning-gate` README, "Not built". |
| **Architecture Impact / Risk Analysis / Test Generation / Observability / Refactoring agents** | Five agents mapped to system surfaces, run at PR / dev / deploy stages. | `Goals/AI/Agents.md`, "The Five Agents I Would Build". |

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
