# Skill Backlog

Candidates found by reviewing `Architecture/` notes for skill-worthy material.
Last reviewed: 2026-09-04.

Process for each new skill: draft under the right group in `.claude/skills/` →
screen in isolation (baseline fails without it, skill fixes it) → run
`Prompts/skill-interaction-testing` against the existing set → record the result.
See [README.md](README.md) "Adding a skill".

---

## New skills — to build

### 1. `capacity-estimation` — priority 1 (strong)
- [x] Built `2026-09-04` — `.claude/skills/Architecture/capacity-estimation/` (SKILL + `estimation-method.md` + `worked-examples.md` + README). Isolation screen passed (baseline fabricates all 9 assumptions; skill gates then delivers). `skill-interaction-testing` run (~9 scenarios, 3 agents): no stacking/contradiction/starvation; the `technical-cost-decision` "assume vs refuse-to-invent" tension composes (usage drivers vs unit prices). Reciprocal edits applied: `technical-cost-decision` desc + "when a figure is missing", `learning-gate` Step 3 row + hand-off list + Never list, `data-tier-operations` & `resilience-strategy` out-of-scope pointers. Memory: `skill-interaction-capacity-estimation.md`.
- A-priori estimate from stated assumptions → QPS (avg + peak), bandwidth / egress GB, storage per day + per year + replicated, cache memory, server count, and **what binds first**.
- Gate: refuse to estimate until the user supplies DAU / traffic driver, actions per user, payload sizes, read:write ratio, peak:average ratio, growth horizon, replication factor. Stating the assumptions is the rep.
- Group: `Architecture/`
- Sources: [Bandwidth Estimation](Architecture/01.%20System%20Design/Bandwidth%20Estimation.md) · [Capacity Estimation](Architecture/01.%20System%20Design/Questions/Capacity%20Estimation.md) · [Music Streaming Service Estimation](Architecture/01.%20System%20Design/Questions/Music%20Streaming%20Service%20Estimation.md)
- Feeds: `technical-cost-decision` (dollars), `data-tier-operations` (is the DB the bottleneck), `resilience-strategy` (what binds first), `observability-strategy` (volume / cardinality)
- Boundary lines: NOT dollar cost (`technical-cost-decision`); NOT shard/replicate given the numbers (`data-tier-operations`); NOT a measured live bottleneck (`problem-solving-gates` Optimization / Rubber Duck). This is the estimate *before* telemetry exists.
- Caveat: the math in the source notes is self-flagged shaky (`#todo Double check calculations`) — clean up the method (walk order, unit/time tables, scoring) in the reference file.

### 2. `failure-mode-analysis` — priority 2 (strong)
- [x] Built `2026-09-04` — `.claude/skills/Architecture/failure-mode-analysis/` (SKILL + `nine-categories.md` + `scoring-and-register.md` + README). Procedure skill (modelled on `document-page-check`), not a gate. Isolation screen passed (baseline gives a narrative review, not a systematic nine-category walk / RPN register / watchlist / 3-way routing; skill delivers all of it). `skill-interaction-testing` (~9 scenarios, 3 agents): no contradiction / stacking / starvation; FMEA → resilience/observability/test-strategy handoffs are clean *from* FMEA, but FMEA was referenced by zero siblings. Reciprocal edits applied: `resilience-strategy`, `observability-strategy` (+ its "top failure modes" phrase), `test-strategy` (+ selection-framework Step 7) out-of-scope pointers; `learning-gate` Step 3 row + enumerations. Memory: `skill-interaction-failure-mode-analysis.md`.
- Structured FMEA / pre-mortem over a design or workflow: walk each component + interaction, enumerate failure modes by category (functional, availability, performance, consistency, integration, dependency, security, operational, human/process), record cause → manifestation → impact, score and rank → prioritized failure-mode register.
- Not a withhold-the-answer gate — a structured procedure skill (like `document-page-check`).
- Group: `Architecture/`
- Source: [Failure Modes](Architecture/01.%20System%20Design/Failure%20Modes.md) (+ chaos/fault-injection thread also appears in [Monitoring & Observability](Architecture/Monitoring%20%26%20Observability.md))
- Feeds: `resilience-strategy` (mitigations for dependency/overload modes), `observability-strategy` (alert on impact ranking), `test-strategy` (fault-injection / chaos target list)
- Boundary lines: this is **enumerate & prioritize all modes, proactively, whole design**; `resilience-strategy` is **pick the mechanism for a known overload/dependency failure**. `problem-solving-gates` Rubber Duck is one bug happening now. Needs reciprocal description edits on `resilience-strategy`, `observability-strategy`, `test-strategy`.
- Caveat: source note (`author: gitUserNamePlaceHolder`, no Status) explains *what* failure modes are but gives no repeatable procedure — the skill must add the walk order, the scoring rubric (RPN or lighter 2-axis), and the register format.

### 3. `design-scoping` — priority 3 (borderline, 3 consolidated sources)
- [ ] Build it. Front-door of the Architecture group. Refuse to design until the user has stated: purpose + audience; functional requirements + explicit out-of-scope; non-functional numeric targets (RPS ceiling, concurrency, latency budget, uptime, error budget, cost cap); constraints (team, timeline, existing stack, platforms, compliance); and the 1–2 features to design deeply.
- Output: a scope statement. Sequences into `capacity-estimation`, `microservices-decision`, `api-interface-style`, `database-architecture`, `failure-mode-analysis`.
- Group: `Architecture/`
- Sources (consolidate all three into ONE skill): [Specifying Scope indepth](Architecture/01.%20System%20Design/Specifying%20Scope%20indepth.md) · [Userbase](Architecture/01.%20System%20Design/Userbase.md) (user-base characterization + compliance checklist) · [Define system threshold](Architecture/Define%20system%20threshold.md) (non-functional numeric targets)
- Fold in — [Boundaries of LLD and HLD](Architecture/Boundaries%20of%20LLD%20and%20HLD.md): the blast-radius discriminator ("if I change this, how much breaks?" → whole system / data model = HLD · many modules = mid · one function = LLD), the *"who cares?"* test (architect / team lead / dev), and the "needs a migration plan / data rewrite / ops change → was never low-level" tell. Use it as the significance filter for the deep-dive-feature-selection step (which decisions deserve deep design + write-down). Port the classifier only — reversibility / expense-to-replace already lives in `technical-cost-decision`; don't duplicate the decision. Also cite it in `repo-topology`'s ADR thread ("was this ever low-level design? if it needs a migration plan, no").
- Boundary lines: must defer to `ambiguity-gate` for "what do you even mean by this request" and take over only once "architect / design a system" is the established intent (precedent: `test-practice-gate` ↔ `ambiguity-gate`). Also a line vs `ticket-evaluation` (judges/sizes a defined ticket; this elaborates scope on an undefined ask).
- Caveat: highest absorption risk of the four — `ambiguity-gate` already claims "unstated scope". Descriptions must nail the system-design-specific split (functional / non-functional / scale numbers / deep-dive feature selection) that `ambiguity-gate` wouldn't know to ask.

### 4. `repo-topology` — priority 4 (borderline, enrich note first)
- [ ] Enrich the source note before building — it is a thin ChatGPT pros/cons list, `Peer Reviewed: 0`. Add: monorepo build tooling (Nx / Turborepo / Bazel), affected-graph / build-graph detection, version-skew vs dependency-hell tradeoff, `CODEOWNERS` / ownership model, CI cost at scale, and the repo split/merge as a migration.
- [ ] Then decide whether to build. Gated decision for how many repositories a codebase lives in — one repo / repo-per-service-or-app / hybrid — driven by team structure and code ownership, release coupling, tech-stack divergence and shared-code needs, CI/CD tooling reality, and scale ceilings. Output: an ADR.
- Group: `Architecture/`
- Source: [Separate vs Combined Codebase Repositories](Architecture/Separate%20vs%20Combined%20Codebase%20Repositories.md)
- Boundary lines: repo layout is NOT service boundaries (`microservices-decision`); consumes pipeline-per-repo vs one-pipeline (`deployment-strategy`); monorepo tooling / CI minutes cost (`technical-cost-decision`); executing a repo split (`migration-cutover`). Needs reciprocal description edits on all four.

---

## Fold into existing skills — reference material, no new skill

- [ ] [File System Storage](Architecture/02.%20Backing%20Service%20Options/File%20System%20Storage.md) → **`database-architecture`** store-options reference: object / block / distributed-file-system storage (S3) as a store choice, "blob in object storage vs DB row" heuristics, large-binary / media / document patterns, HIPAA-on-S3 note. No trigger change.
- [ ] [12 Key Metrics for Measuring Service Performance](Architecture/12%20Key%20Metrics%20for%20Measuring%20Service%20Performance.md) — service-metrics half (TTFB, latency, throughput, response time, error rate, MTBF/MTTR, request rate, concurrent connections, cache hit ratio, SLA compliance) → **`observability-strategy`** SLI-menu reference. Drop the team-metrics half (velocity / cycle time / lead time — out of scope, half-baked).
- [ ] [SAGA](Architecture/SAGA.md) → **`data-tier-operations`** distributed-transaction step: choreography vs orchestration, compensating transactions. (Choreography/orchestration also feeds the event-driven thread below.)
- [ ] [Fault Tolerance](Architecture/Fault%20Tolerance.md) → **`resilience-strategy`** — retry / backoff, circuit breaker, bulkhead, timeout, failover, graceful degradation, isolation. Likely already a source note; cross-check the retry/backoff reference is captured.
- [ ] [Monitoring & Observability](Architecture/Monitoring%20%26%20Observability.md) → **`observability-strategy`** — monitoring-vs-observability, logging / tracing / metrics vocabulary. Likely already a source note; cross-check.

---

## No skill / no action

- [Impact of Architectural Styles](Architecture/01.%20System%20Design/Impact%20of%20Architectural%20Styles.md) — survey with a self-admitted non-standard taxonomy; a "pick your architectural style" skill would silently override `microservices-decision` / `api-interface-style` / `data-tier-operations`. Points at the two loose threads below.
- [HLD vs LLD](Architecture/HLD%20vs%20LLD.md) — textbook HLD/LLD definitions (city-map vs building-blueprint analogy) + a differences table. Pure vocabulary, no procedure and no decision. A "pick your design altitude" skill would silently front-run `microservices-decision` / `api-interface-style` / `data-tier-operations` (same failure mode as Impact of Architectural Styles). The one reusable idea in its companion note lands in `design-scoping` (see item 3).
- [Reactive programming](Architecture/Reactive%20programming.md) — code-level paradigm (async streams, Observables, Rx), wrong altitude for an architecture skill. Belongs to the JS Reactive Programming ecosystem note.

---

## Loose threads — evaluate separately

- [ ] **Event-driven architecture pattern choice** (event sourcing, choreography vs orchestration, system-wide EDA). Evaluate [Event-driven Architectural Pattern Decisions](Architecture/Event-driven%20Architectural%20Pattern%20Decisions.md) + [Event Driven Architecture](Architecture/Event%20Driven%20Architecture.md) as the sources. SAGA's choreography/orchestration content also feeds this.
- [ ] **Application-internal structure** gate (hexagonal / clean / layered / onion / DDD) — real catalog gap (nothing covers "how to structure the inside of one service"), but no written note yet (only a `#todo` link in Impact of Architectural Styles). Write the note first, drawing on the Clean Architecture book notes.
- **Chaos / fault injection** — not its own skill: target list → `failure-mode-analysis`, in-the-mix decision → `test-strategy`.
