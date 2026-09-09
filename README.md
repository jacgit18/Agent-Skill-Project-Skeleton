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
| [`.claude/settings.json`](.claude/settings.json) | Wires two hooks: `UserPromptSubmit` → prompt logging, `SessionStart` → mechanical catalog-drift glance. |
| [`.claude/_Prompts/logs/`](.claude/_Prompts/logs/) | Dated logs of every prompt submitted in the repo. |
| [`Architecture/`](Architecture/) | System-design notes: system design, backing services, web-server architecture, design patterns, devops, networking, security, testing, 12-factor. Source material for the skills. |
| [`Communication/Companies Worked At/`](Communication/Companies%20Worked%20At/) | BSA/agile process notes. Source material for the `Business/` and `Prompts/` group's BSA-derived skills. |
| [`Business Venture/`](Business%20Venture/) | Startup/business-acquisition notes. Source material for the `Finance/` group. |
| [`Finance/`](Finance/) | Personal error-log templates — `Error Log/Language Error.md` is the template `problem-journal`'s Capture mode writes into. |
| [`Goals/`](Goals/) | Personal learning roadmap and AI-engineering framework notes. |
| [`Books/`](Books/) | Business and tech book notes. |
| [`scripts/`](scripts/) | `hooks/log-prompt.sh`, `hooks/catalog-drift-check.sh`; `git/state.sh`, `git/commit.sh`, `git/push.sh`, `git/land.sh`, `git/batch-git-push.sh`. |
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
| [`Architecture/Data/relational-modeling`](.claude/skills/Architecture/Data/relational-modeling/) | Turns a settled "we're relational" into table design — normal form and exceptions, keys, constraints, first-cut index plan, lifecycle columns. |
| [`Architecture/Data/index-tuning`](.claude/skills/Architecture/Data/index-tuning/) | Revises, adds, or audits indexes on a **deployed, populated** schema — composite column order against a real `EXPLAIN` plan, covering / partial / expression indexes, a selectivity check, a redundant/unused-index audit, and a write-cost budget. Procedure, not a gate. |
| [`Architecture/Data/data-tier-operations`](.claude/skills/Architecture/Data/data-tier-operations/) | Scales an existing database — replication topology, partitioning vs sharding, isolation level, distributed-transaction pattern, failover, pooling. |
| [`Architecture/Data/dimensional-modeling`](.claude/skills/Architecture/Data/dimensional-modeling/) | Designs an analytical OLAP model — fact-table grain, conformed / role-playing / degenerate dimensions, SCD strategy, star vs snowflake vs galaxy. |
| [`Architecture/Data/caching-strategy`](.claude/skills/Architecture/Data/caching-strategy/) | Decides whether to cache a read path and how — cache layer, cache-aside / write-through / etc., TTL vs explicit invalidation, eviction policy, stampede / avalanche handling. Produces an ADR. |

```
database-architecture   →  WHERE the schema lives + WHICH store  (ADR)
relational-modeling      →  tables for a relational store + first-cut index plan
index-tuning             →  revise / add / audit indexes on a deployed, populated schema
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

### Documents — producing and checking document files

| Skill | Role |
|---|---|
| [`Documents/document-page-check`](.claude/skills/Documents/document-page-check/) | Integrity check for a paginated document (PDF / EPUB) before Claude reads, quotes, or summarizes it — confirms the file is complete and untruncated, flags blank / image-only pages, resolves the printed-vs-physical page-number offset, and spot-checks the citations an answer will lean on. Emits a report, then asks whether to gate or proceed. A mechanical pre-flight, not a reasoning gate. |
| [`Documents/codebase-file-orientation`](.claude/skills/Documents/codebase-file-orientation/) | Procedure (not a gate) that authors or reconciles a per-file companion **orientation doc** for a source file just created or substantially changed — a sidecar `.md` (matched to the repo's own doc convention) covering the file's role, entry points, dependencies in/out, and non-obvious gotchas. Complementary to inline comments, not a replacement. Author mode fills the template and flags what it can't trace; Reconcile mode diffs an existing doc against the current file and proposes a patch. |

### Finance — personal/business-finance decisions and reviews

| Skill | Role |
|---|---|
| [`Finance/seller-financing-evaluation`](.claude/skills/Finance/seller-financing-evaluation/) | Evaluates a seller-financed (owner-financed) business purchase — computes the amortized monthly payment rather than trusting a stated figure, benchmarks down payment / rate / term against real market ranges, checks it against the business's cash flow, and runs the "7 Ds" seller-motivation diagnostic before any fairness verdict. Not a substitute for an attorney, accountant, or appraiser. |
| [`Finance/equity-trade-decision`](.claude/skills/Finance/equity-trade-decision/) | Forces a pre-trade checklist, an evidence-backed economic-cycle-stage call, and a position size computed as risk-budget ÷ per-share-risk (kept separate from money actually spent) before sizing or entering a real stock trade. |
| [`Finance/portfolio-thesis-audit`](.claude/skills/Finance/portfolio-thesis-audit/) | Audits positions already held: for each, withholds the keep/sell verdict until the user supplies the written thesis, a current-validity call with evidence, and a specific exit condition — a position missing any of the three can't be graded "hold". Assigns hold / exit / research-required (time-boxed) per the rubric and flags disposition effect, luck-read-as-skill, informal-input-as-research, and return-target urgency distortion as hypotheses. Never authors the thesis. The mirror of `equity-trade-decision` (new entries) for the other end of a position's life. |
| [`Finance/position-exit-rules`](.claude/skills/Finance/position-exit-rules/) | Gate that withholds "entry plan complete" until the user commits, in writing and as numbers, to a hard price stop (one number, no discretion), thesis-invalidating events mapped clause-by-clause to the user's own thesis, and a position-size ceiling that also caps averaging down — plus an optional upside review trigger. Removes the disposition effect at the process level by forcing the exit to be defined pre-entry. Feeds its price stop forward to `equity-trade-decision` for sizing; `portfolio-thesis-audit` routes here when a held position has no exit rule. Claude checks the rules are real, doesn't author them. |
| [`Finance/covered-call-decision`](.claude/skills/Finance/covered-call-decision/) | Gate for writing covered calls on a held 100+ share lot: runs a six-check qualification screen (share lot, chain liquidity, genuinely willing to be assigned, strike at/above the user's own price target, not the top-conviction name, assignment tax character understood) before naming a strike — a fail on the key checks means "write on a different position", not "different strike". For a qualifying position: strike, expiration (earnings + ex-dividend/early-assignment), contract count, premium math (annualized, with the caveat it's neither guaranteed nor real downside protection), and the assignment outcome (cash, realized gain + tax character, position closed). Downstream of `portfolio-thesis-audit`; consumes `position-exit-rules`' price target as the strike floor; the options skill `equity-trade-decision` hands off to. |
| [`Finance/watchlist-screener-criteria`](.claude/skills/Finance/watchlist-screener-criteria/) | The gate before `equity-trade-decision`'s gate. **Define** mode: the user commits a stated style (value / quality / growth / momentum / dividend) + 4–8 numeric criteria (metric + threshold + direction + why it predicts returns) + hard disqualifiers + a review cadence — Claude checks each criterion is numeric and coheres with the style, and does not supply the thresholds. **Screen** mode: run one candidate against the existing screen with user-supplied metric values (Claude never fetches or estimates fundamentals) → pass/fail per line, a verdict (watchlist / proceed / reject), and an explicit flag when a narrative-sourced candidate is failing. Replaces YouTube and product familiarity as the primary filter. |
| [`Finance/weekly-portfolio-review`](.claude/skills/Finance/weekly-portfolio-review/) | **Procedure**, not a gate — the recurring integration pass over the other Finance skills. A fixed seven-step weekly walk (positions vs. thesis, stops still valid, options expiring, earnings/events ahead, allocation drift vs. size ceiling, watchlist in range, since-last-review delta) that **surfaces and routes** each finding to the skill that owns the decision (`portfolio-thesis-audit` / `position-exit-rules` / `covered-call-decision` / `equity-trade-decision` / a trim flag) rather than deciding inline. Runs on a calendar cadence on purpose. Includes an automation-boundary table (script does the data, human does the judgment). Distinct from `portfolio-thesis-audit` — that's the per-position keep/sell audit this pass flags positions for. |
| [`Finance/equity-research-writeup`](.claude/skills/Finance/equity-research-writeup/) | Gate that withholds a finished single-company research writeup — and refuses to author the analysis — until the user fills eight sections in their own words with sourced figures: the business, unit economics, competitive-position *evidence*, 3–5y financial trend, valuation reasoning, their own bear case, a falsifiable ≥3-sentence thesis, and what-would-change-my-mind. Claude supplies the structure, checks every claim has a figure and a named source, pushes on a weak bear case, and flags stale-from-memory financials — it never writes a section, supplies a figure, or runs a valuation. Sits between `watchlist-screener-criteria` and `position-exit-rules` / `equity-trade-decision`; section 7 satisfies the trade checklist's fundamentals item and section 8 becomes `position-exit-rules`' thesis-invalidating events. Not for ETFs. |
| [`Finance/asset-allocation-policy`](.claude/skills/Finance/asset-allocation-policy/) | Gate for the whole-book target shape every position-level Finance skill defers. Withholds an allocation recommendation — and refuses target %s off a risk quiz — until the user supplies the capital map (runway vs. investable, by account), the withdrawal plan as a % of the pool (income vs. drawdown), risk capacity vs. tolerance, and an explicit concentrated-vs-diversified stance. Then the user commits a six-area policy (asset-class targets + bands, equity sub-splits, position-sizing bands, diversification limits, tax-aware rebalancing, contribution routing); Claude checks completeness + internal consistency and stress-tests it against the withdrawal plan. Its single-name cap is the house default `position-exit-rules` rule 3 uses; its bands are what `weekly-portfolio-review` step 5 checks drift against. |
| [`Finance/etf-selection`](.claude/skills/Finance/etf-selection/) | Gate for choosing / comparing / re-checking a specific ETF or index fund by ticker. Withholds a hold/buy/swap verdict until the user assigns the fund an `asset-allocation-policy` sleeve and pulls its real facts from the issuer fact sheet (expense ratio, holdings + top-10 weight, AUM/volume, multi-year tracking difference, structure, ROC/yield, age; duration + YTM for a bond fund; physical-vs-futures + tax for a commodity fund), plus a holdings-overlap check against every adjacent holding and a why-this-tilt-why-now + decay check for any non-core thematic fund. Claude structures, flags the traps, and gives a verdict; it never fetches fund data, picks a theme, or sizes the sleeve. The funds counterpart to `equity-research-writeup`; feeds `equity-trade-decision` for sizing. |

```
Equity pipeline — each stage a gate, running inside the one above:

asset-allocation-policy      whole-book target shape — the frame the rest operates inside     (gate)
  watchlist-screener-criteria  numeric pre-filter: does a name earn research?   Define/Screen  (gate)
    equity-research-writeup    8-section thesis writeup for one company                        (gate)
    etf-selection              fact-sheet evaluation for one fund                              (gate)
      position-exit-rules      price stop + invalidating events + size cap, before entry      (gate)
        equity-trade-decision  size and enter, inside the allocation bands                    (gate)
covered-call-decision        premium income on a held 100-share lot                           (gate)
weekly-portfolio-review      recurring pass — routes each finding to the skill that owns it   (procedure)
portfolio-thesis-audit       re-check a held position's thesis → hold / exit / research       (gate)

seller-financing-evaluation  a seller-financed *business* purchase — not equities             (gate)
```

### Health — musculoskeletal recovery decisions

| Skill | Role |
|---|---|
| [`Health/return-to-play-progression`](.claude/skills/Health/return-to-play-progression/) | Criteria-based 4-phase return-to-activity gate for a self-manageable injury — no phase advances on elapsed time alone, only on stated symptoms/ROM/function clearing a bar — with an immediate red-flag screen to a doctor and a next-morning-pain-vs-during-exercise-pain rule most self-assessments skip. |

### AI Engineering — building with LLMs, not just about them

| Skill | Role |
|---|---|
| [`AI Engineering/model-routing-decision`](.claude/skills/AI%20Engineering/model-routing-decision/) | Places a "route between models" request in the right bucket first (cost-tiering / cross-provider / agentic task-type routing are this skill's; failover, ops triage, and multi-agent labor division are not), gates on real inputs (task categories, volume, latency, cost sensitivity, auditability) before recommending build-your-own vs. a proxy, and hands pricing off to `technical-cost-decision` rather than computing it. |

### Prompts — authoring, testing, and session hygiene

| Skill | Role |
|---|---|
| [`Prompts/ambiguity-gate`](.claude/skills/Prompts/ambiguity-gate/) | Asks before acting when a request could reasonably be read more than one way. |
| [`Prompts/prompt-authoring`](.claude/skills/Prompts/prompt-authoring/) | Turns a rough idea or a weak draft into one finished, copy-paste-and-send prompt — no placeholders, content baked in or a self-gathering step included. The authoring end of the pipeline: `prompt-authoring` → `prompt-tester` → `prompt-archive`. |
| [`Prompts/prompt-archive`](.claude/skills/Prompts/prompt-archive/) | Archives a keeper prompt into `.claude/_Prompts/`, or logs the current session's prompts. |
| [`Prompts/problem-journal`](.claude/skills/Prompts/problem-journal/) | Two modes: **Capture** — the moment an error appears, save it verbatim as its own file in `Finance/Error Log/` (the vault's existing template), no judgment attached. **Journal** — after a fix, a curated entry with a recurrence count grepped from both `Finance/Error Log/` and prompt-archive's logs, and a worth-learning verdict that must name the count behind it. Hands teaching back to `learning-gate`/`problem-solving-gates` rather than doing it inline. |
| [`Prompts/prompt-tester`](.claude/skills/Prompts/prompt-tester/) | Runs a prompt against a few examples and reports whether it does what it claims. |
| [`Prompts/session-handoff`](.claude/skills/Prompts/session-handoff/) | Writes a structured handoff file before a session compacts or work resumes elsewhere. |
| [`Prompts/skill-interaction-testing`](.claude/skills/Prompts/skill-interaction-testing/) | Tests a new or changed skill against every sibling for stacking, contradiction, silent override, and beneficial chaining. |
| [`Prompts/catalog-drift-audit`](.claude/skills/Prompts/catalog-drift-audit/) | Periodic whole-catalog hygiene pass (not per-skill, unlike `skill-interaction-testing`) — stale `SKILL-BACKLOG.md` markers, skills missing from this README, dead cross-references, untested old skill pairs, and skills nobody else's description points to. |

### Research — current-awareness lookups

| Skill | Role |
|---|---|
| [`Research/reddit-researcher`](.claude/skills/Research/reddit-researcher/) | Current-awareness research across three free sources — Reddit (public JSON + a `site:reddit.com` fallback), Hacker News (Algolia API), and the open web — for roughly the last 30 days. Relevance filtering, dedup, cross-source signal detection, anti-hallucination guardrails. A standalone tool, not a decision gate; no paid APIs or MCP servers. |

### Architecture, Business, Skill Development, Git

| Skill | Role |
|---|---|
| [`Skill Development/learning-gate`](.claude/skills/Skill%20Development/learning-gate/) | Classifies intent (learning / execution / reference) and sets how much of the thinking Claude may do. For a multi-step task the user will carry out themselves, sets the one-step-at-a-time walkthrough (`guided-walkthrough.md`). |
| [`Skill Development/problem-solving-gates`](.claude/skills/Skill%20Development/problem-solving-gates/) | Rubber Duck (debugging), Options Generator (architecture), Knowledge Checker, Optimization (faster/cheaper, bring a profile) — each requires prior independent effort. |
| [`Skill Development/spec-drift-gate`](.claude/skills/Skill%20Development/spec-drift-gate/) | Refuses to start a multi-file/multi-session AI-assisted build until a written spec exists (problem framing, tradeoffs actually weighed, explicit in/out scope, an optional controlled-experiment slice), then at later checkpoints diffs the work against that spec and forces an explicit amend-or-pull-back decision instead of letting scope silently drift. Runs a scoped extraction interview (Step 2a) when the request is a one-liner with no spec to draft from. |
| [`Architecture/design-scoping`](.claude/skills/Architecture/design-scoping/) | **Front-door gate** for a system-design effort — refuses to design until purpose + audience, functional + explicit out-of-scope, the six non-functional numeric targets, constraints (incl. compliance), and the 1–2 deep-dive decisions are stated. Output: a scope statement that sequences into `capacity-estimation` → `microservices-decision` → `api-interface-style` → `database-architecture` → `failure-mode-analysis`. Defers to `ambiguity-gate` for "what does this request even mean". |
| [`Architecture/microservices-decision`](.claude/skills/Architecture/microservices-decision/) | Whether and how to split services, bounded by the number of people who can own them. |
| [`Architecture/capacity-estimation`](.claude/skills/Architecture/capacity-estimation/) | A-priori back-of-the-envelope for a system that doesn't exist yet — gated on stated assumptions (DAU, actions/user, payload sizes, R:W, peak:avg, retention + growth, replication), walks storage → traffic → cache → servers, and names **what binds first**. Feeds `technical-cost-decision` (dollars), `data-tier-operations` (topology), `resilience-strategy` (defense). |
| [`Architecture/failure-mode-analysis`](.claude/skills/Architecture/failure-mode-analysis/) | Structured FMEA / pre-mortem procedure (not a gate) — walks every component + interaction across nine failure categories, scores an RPN register (severity × occurrence × detection, or a 5×5 grid), separates a high-severity watchlist, emits a prioritized failure-mode register + handoffs to `resilience-strategy` / `observability-strategy` / `test-strategy`. Asks register-only vs block-sign-off. |
| [`Architecture/api-interface-style`](.claude/skills/Architecture/api-interface-style/) | Picks the interaction style for one API surface — REST / GraphQL / gRPC / WebSocket / SSE / webhooks / async messaging — from its consumers, interaction shape, and latency / real-time needs. Produces an ADR. |
| [`Architecture/observability-strategy`](.claude/skills/Architecture/observability-strategy/) | Decides how a system is instrumented — signal set (metrics / logs / traces / profiling), SLIs & SLOs, sampling & cardinality budget, symptom-based alerting, retention, self-hosted vs managed. Produces an ADR. |
| [`Architecture/resilience-strategy`](.claude/skills/Architecture/resilience-strategy/) | Decides how a request path protects itself under overload and dependency failure — priority-aware load shedding, rate limiting, concurrency limits & backpressure, circuit breakers, timeout / retry-budget / jitter, bulkheads, graceful degradation — and where each control sits. Produces an ADR. |
| [`Architecture/reliability-math`](.claude/skills/Architecture/reliability-math/) | Procedure (not a gate) for reading live production telemetry correctly — percentiles before trusting an average, Little's Law arithmetic, SLO-to-minutes + error-budget burn rate, a utilization reading against the queueing-collapse curve, a graph-literacy checklist. Feeds `resilience-strategy` (a quantified pressure) and `problem-solving-gates` (a reachable hypothesis or bottleneck number). |
| [`Architecture/migration-cutover`](.claude/skills/Architecture/migration-cutover/) | Decides how a live workload moves to a new system — cutover pattern (big-bang / phased / parallel-run / strangler), data-move mechanic (freeze-copy / bulk+CDC / dual-write+reconcile), the verification bar, the rollback window and its point of no return, the consumer sequence. Produces an ADR. |
| [`Architecture/deployment-strategy`](.claude/skills/Architecture/deployment-strategy/) | Decides how a new version of one deployable unit reaches production — rollout mechanism (recreate / rolling / blue-green / canary / feature-flag), environment progression, expand/contract schema discipline, the health signal that aborts a rollout, cadence. Produces an ADR. |
| [`Architecture/cloud-iam-boundary`](.claude/skills/Architecture/cloud-iam-boundary/) | Decides who/what gets access to a cloud resource and its network placement — principal, least-privilege permission set, trust boundary & credential lifetime (STS-assumed role vs long-lived keys), permissions-boundary/SCP ceiling, public vs private subnet. Produces an ADR. |
| [`Architecture/serverless-execution-model`](.claude/skills/Architecture/serverless-execution-model/) | Decides how one unit of work runs — compute primitive (FaaS / container task / long-running service), invocation model (sync / async / poll-based), orchestration vs choreography, and the per-invocation failure contract (Retry/Catch, DLQ, idempotency). Produces an ADR. |
| [`Architecture/access-control-modeling`](.claude/skills/Architecture/access-control-modeling/) | Decides how an application authorizes who may do what to which resource — authorization model (flat/hierarchical RBAC, ABAC, ACL, ReBAC), the actors/resources/actions, permission granularity, and tenant isolation. Produces an ADR. |
| [`Architecture/bff-gateway-placement`](.claude/skills/Architecture/bff-gateway-placement/) | Decides what sits between client applications and backend services — no intermediary, a shared API gateway, or a Backend-for-Frontend per client type — from client-type count, backend-surface count, and per-client divergence. Produces an ADR. |
| [`Architecture/service-mesh-adoption`](.claude/skills/Architecture/service-mesh-adoption/) | Decides whether a service mesh (Istio/Linkerd/Consul Connect) earns its operational cost versus a lighter alternative (orchestrator-native discovery, in-process resilience libraries), from service count, platform, and the specific mesh capability actually needed. Produces an ADR. |
| [`Architecture/config-and-secrets-management`](.claude/skills/Architecture/config-and-secrets-management/) | Decides where a config value or secret lives and how it reaches a running process — plain env vars, orchestrator-native secrets, or a dedicated secrets manager — and its rotation policy. Produces an ADR. |
| [`Architecture/change-surface-audit`](.claude/skills/Architecture/change-surface-audit/) | Pre-flight procedure (not a gate) for one proposed add/modify/remove change, or a "silent" change (dependency upgrade, config, infra) — walks six blast-radius surfaces (API, data, state, performance, security, observability), requires expand-contract for a breaking modify, and audits hidden dependents before a removal. |
| [`Architecture/disclosure-gap-audit`](.claude/skills/Architecture/disclosure-gap-audit/) | Pre-flight audit (procedure, gated on a data inventory) of a shipped product against its public commitments — a 15-probe policy-vs-practice pass (AI processing, subprocessors, retention, tracking, automated decisions, sale/share, …), a design-review security-anti-pattern pass, and a flag-only legal/compliance pass that names the regime and routes to counsel, never rules. Emits a ranked findings register (severity + who-confirms + handoff). Non-authoritative on legal questions by design. |
| [`Business/technical-cost-decision`](.claude/skills/Business/technical-cost-decision/) | Forces the cost arithmetic on any decision that carries a recurring price. |
| [`Business/ticket-evaluation`](.claude/skills/Business/ticket-evaluation/) | Separates what a ticket says from what it's missing from what can be judged; verdict last. |
| [`Business/explaining-my-work`](.claude/skills/Business/explaining-my-work/) | One evidence base rendered at three altitudes — plain summary, spoken script, public post. |
| [`Business/user-story-decomposition`](.claude/skills/Business/user-story-decomposition/) | Decides use-case vs. user-story format, then walks epic → user story → acceptance criteria against an INVEST-style quality bar and a Definition-of-Ready checklist. Downstream of `design-scoping`'s functional list, upstream of `ticket-evaluation`'s sprint verdict. |
| [`Business/software-carpentier-brand`](.claude/skills/Business/software-carpentier-brand/) | Represents the user professionally under their personal brand — LinkedIn headline/About and feed posts, resume bullets, cover letters, elevator pitches, interview self-intros — holding to a career-honesty checklist so copy doesn't overstate what actually happened. |
| [`Business/system-design-communication`](.claude/skills/Business/system-design-communication/) | Live coaching, not a decision gate — practice explaining a design (Design Walkthrough), a simulated system-design interview (Mock Interview), or defending one architectural choice over another under "what if?" pressure (Tradeoff Defense). Never supplies the "right" answer; exposes gaps and pressure-tests reasoning instead. |
| [`Business/delete-ai-words`](.claude/skills/Business/delete-ai-words/) | Audits and rewrites text so it stops reading like AI — bans negative-parallelism reframes, a fixed list of tell words, forced rule-of-three, fake-depth participles. General-purpose, and the prose-style pass that `software-carpentier-brand` and `learning-gate`'s `guided-walkthrough` defer to. |
| [`Git/commit-and-push`](.claude/skills/Git/commit-and-push/) | Stages, commits, and pushes with a message derived from the actual diff. |
| [`Git/history-integration-strategy`](.claude/skills/Git/history-integration-strategy/) | Gate: pick merge commit / fast-forward / squash / rebase for folding a branch in (or merge-in vs. rebase-onto for syncing), after five facts — shared history, a mandated strategy, commit quality, integrate-vs-sync, whether the team bisects. One recommendation, not a survey. `commit-and-push` hands the strategy choice here. |

## Agents

Skills are procedures inside one foreground conversation. Two pieces of actual unattended-agent infrastructure sit alongside them:

| What | Where | Does what |
|---|---|---|
| `spec-executor` subagent | [`.claude/agents/spec-executor.md`](.claude/agents/spec-executor.md) | Executes one slice of an already-approved `spec-drift-gate` spec in an isolated worktree — briefed with the spec, the precision instruction, and nothing else. Doesn't decide scope, doesn't merge or push; reports back what it did and what it flagged as outside the spec, for a human (or the calling session) to run through `spec-drift-gate`'s own Step 4 before anything lands. |
| Weekly Catalog Drift Audit | [`claude.ai/code/routines`](https://claude.ai/code/routines) (cloud, not local) | A scheduled cloud routine (Monday 9am America/New_York) that runs `catalog-drift-audit`'s procedure against `main`, fixes mechanical drift on a branch, and opens a PR — it does not push to `main` directly. Its durable audit trail lives in `.claude/_Prompts/catalog-audit-log.md` (created on first real finding), which each run reads first so it never re-flags something already resolved. |

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
