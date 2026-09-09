# Project 3: AI Investment Advisor (Finance-Skill Operationalizer)

## Goal
Build a personal AI investment advisor that runs my own written decision frameworks — the
`.claude/skills/Finance/` gates — against my real holdings. The system stores the portfolio,
theses, exit plans, and allocation policy; Claude does the tedious part (gathering each
gate's required inputs, checking them against sources, tracking them over time); and the
gate's discipline is preserved end to end — **the app never emits a buy / sell / size
verdict on its own.** I make the call; the system records the call and the reasoning.

This is the "real utility" counterpart to Project 1 (the financial dashboard), which stays a
skills-practice sandbox. Project 3 reuses every production-AI pattern learned in the
dashboard arc (chat, structured output, tool-calling, RAG) but points them at a portfolio I
actually manage.

## Architecture

### High-Level

The advisor wraps the existing Finance skill catalog. Each skill is a decision **gate** that
withholds its answer until real, sourced inputs are supplied; the app's job is to make those
inputs cheap to assemble and keep them current, not to replace the gate.

- **Portfolio store** — `Account` (taxable / Roth / IRA / 401k), `Holding` (ticker, shares,
  cost basis, account, % of book), `AllocationPolicy` (asset-class targets + tolerance
  bands, position-sizing bands, diversification limits, rebalancing trigger), `Thesis`
  (per holding: written thesis, date, explicit falsifiers, current-validity note),
  `ExitPlan` (hard price stop, thesis-break condition, trim rules, time stop), `Fact`
  (a single fundamental or fact-sheet figure with a `source` tag and `as_of` date),
  `GateRun` (which skill, inputs gathered, the checklist answers, the verdict *the user*
  recorded, timestamp), `ReviewRun` (a weekly-review pass: the seven steps, red flags,
  follow-ups).

- **Advisor engine** — one workflow per Finance gate. A workflow has three strictly
  separated phases: (1) **gather** — Claude pulls what the gate needs from the portfolio
  store and from documents the user pastes/uploads (10-K, 10-Q, earnings call, issuer fact
  sheet), and drafts nothing as fact without a source tag the user confirms; (2) **run** —
  Claude walks the gate's structured checklist as an interview, surfacing what is missing or
  stale; (3) **record** — the user types the decision and rationale, which is stored as a
  `GateRun`. The verdict field is never model-populated.

- **Routing** — an explicit state machine, not prompt glue: a new name goes
  `watchlist-screener-criteria` → `equity-research-writeup` → `equity-trade-decision` →
  `position-exit-rules`; a held name in question goes `portfolio-thesis-audit` (which may
  route into `equity-research-writeup`); `asset-allocation-policy` is the frame every
  single-position workflow reads first; `weekly-portfolio-review` is the recurring pass that
  reads all of the above and flags holdings with no thesis or no exit plan.

- **Market data** — delayed quotes from a free API for prices and drift math; fundamentals
  and fund facts are always user-supplied with a source (this matches how the skills already
  behave — they refuse memory-sourced numbers).

- **Interface** — CLI first (fast to build, matches the interview-story projects), a thin
  React view later for the portfolio table, drift report, and review history.

### Technical Decisions

| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Stack | Same as the dashboard: FastAPI + SQLAlchemy + Postgres + Anthropic SDK | Deliberate reuse — Project 1 already paid the setup cost and taught the patterns; Project 3 is about the domain logic, not re-learning the plumbing | A new stack (learn something else) — wrong trade-off here; the point is to apply, not restart |
| Verdict handling | The app has **no** recommendation/verdict output. Every workflow ends by storing a user-authored decision + rationale. A test asserts no endpoint or CLI command returns a hold/buy/sell/trim/size field. | The entire value of these skills is that they *withhold* the answer until inputs are real. An "advisor" app is the easiest place to accidentally collapse that discipline (autofilled thesis, guessed stop). Keeping gather / run / record separate is the core design constraint. | Let Claude produce a "suggested" verdict the user edits — defeats the gate; anchoring bias makes the "edit" cosmetic |
| Fact provenance | Every `Fact` row carries `source` (10-K / 10-Q / earnings call / issuer fact sheet / filing) and `as_of`. A gate run is **blocked** when a required figure is missing a source or is older than a per-figure staleness window. | `etf-selection` and `equity-research-writeup` explicitly refuse figures pulled from memory; the store has to enforce the same rule or the skill is worthless through the app | Trust Claude to fetch/recall numbers — hallucinated fundamentals are the classic failure and exactly what the skills guard against |
| One canonical portfolio | `asset-allocation-policy`, `position-exit-rules`, `portfolio-thesis-audit`, and `weekly-portfolio-review` all read the same `Holding` / `Thesis` / `ExitPlan` rows. Routing between gates is a modeled state machine. | These gates are designed to compose (allocation is the frame; the weekly review reads theses and exit plans). Prompt glue between them drifts; a state machine is testable. | Independent per-gate context assembled ad hoc — gates disagree about the same position, no single source of truth |
| Claude models | Sonnet 5 for gather + run (long, low-volume, high-reasoning). Opus 5 only for the final `equity-research-writeup` narrative. No Haiku tier — there is no high-volume classification workload here. | Cost profile is the inverse of the dashboard: few calls, each large and reasoning-heavy. The lever is prompt caching, not a cheap tier. | Haiku for everything — under-powered for gate reasoning; the volume that would justify it doesn't exist |
| Caching | Prompt-cache the skill text (the gate's `SKILL.md` + companion reference) — it is large and stable. Do not re-send the full portfolio every turn; send a compact holdings digest + only the rows the current workflow touches. | Skill files are the expensive stable prefix; re-paying for them each turn dominates cost. Portfolio context is small but grows — scope it to the workflow. | No caching, full portfolio every turn — needless token spend on a stable prefix and irrelevant rows |
| Deployment | Local-first (SQLite ok). Optional Render + managed Postgres if a hosted view is wanted. No public multi-user surface. | It holds my real financial positions — single-user, local, no reason to expose it | Deploy multi-user like Projects 1–2 — adds auth-isolation and hosting risk for zero benefit on a personal tool |

### Non-Trivial Challenges

1. **Preserving the gate discipline through an app.** The skills are valuable *because* they
   refuse to answer until the inputs are real; software that "helps" tends to short-circuit
   that (pre-fill a thesis, infer a stop, offer a verdict the user rubber-stamps). Approach:
   the advisor engine hard-separates **gather** (Claude may draft, user must confirm each
   figure with a source tag) from **run** (the gate's checklist, missing items surfaced,
   nothing hidden) from **record** (verdict is user-typed, stored, never model-populated).
   Test: assert no code path returns a buy/sell/trim/size recommendation; assert a workflow
   cannot reach `recorded` state with an unconfirmed or unsourced required figure.

2. **Fact provenance and staleness.** A gate run needs specific figures (expense ratio,
   revenue, the index a fund actually tracks, cost basis, current price) and every one has a
   source and an age. Approach: `Fact` rows are append-only with `source` + `as_of`;
   a staleness window per figure type; the workflow blocks and lists what to refresh before
   it will run the checklist. Test: gate run blocked when a required `Fact` is unsourced or
   past its window; unblocked once the user pastes the current filing/fact sheet.

3. **Keeping many gates coherent against one portfolio.** `asset-allocation-policy` sets the
   frame every position decision runs inside; the weekly review reads theses and exit plans;
   a losing position routes thesis-audit → maybe research-writeup. Approach: one canonical
   store; routing as an explicit state machine with named transitions; a holding with no
   `Thesis` and no `ExitPlan` is flagged by `weekly-portfolio-review` and is blocked from a
   "trade plan complete" state. Test: add a bare holding → it appears in the weekly-review
   red flags → completing its thesis + exit plan clears the flag.

4. **Cost/latency shape is the opposite of the dashboard.** Few calls, each long and
   reasoning-heavy, so the dashboard's batching/cheap-tier levers don't apply. Approach:
   prompt-cache the (large, stable) skill text; send a compact portfolio digest plus only
   the rows the current workflow touches, not the whole book each turn; log token counts per
   workflow run. Test: second run of the same workflow within the cache window is materially
   cheaper; portfolio growth doesn't linearly inflate per-turn tokens.

## Success Criteria
- [ ] Portfolio store holds real accounts, holdings, allocation policy, theses, exit plans,
      and gate-run history; CSV import + manual entry both work
- [ ] At least four Finance gates operationalized end to end: `asset-allocation-policy`,
      `position-exit-rules`, `portfolio-thesis-audit`, `weekly-portfolio-review`
      (stretch: `equity-research-writeup`, `etf-selection`, `watchlist-screener-criteria`,
      `equity-trade-decision`, `covered-call-decision`)
- [ ] The gate discipline is provably intact: no verdict is ever system-generated; a
      workflow cannot complete on unsourced or stale required figures (tests assert both)
- [ ] Routing between gates is a modeled state machine with tests, not prompt glue
- [ ] `weekly-portfolio-review` reads the whole store and flags missing theses / exit plans
- [ ] RAG (Months 7–9 pattern): a review can retrieve prior theses and past review runs and
      answer "what changed since last review" / "you flagged this same concentration before"
- [ ] Clean, testable: advisor engine decoupled from Claude calls; gate workflows unit-
      tested with mocked model responses; fact-provenance and no-verdict rules covered
- [ ] Can explain the design: why gates withhold answers, why gather/run/record are
      separated, why one canonical portfolio, why caching (not a cheap tier) is the cost lever

## Timeline

Sequenced **beside the dashboard, Months 6–9** — it starts once the tool-calling pattern is
learned (Month 5–6) and folds in RAG during Months 7–9, reusing the dashboard's stack and
patterns rather than standing up new infrastructure.

- **Week 1** — Portfolio store + import. Schema (`Account`, `Holding`, `AllocationPolicy`,
  `Thesis`, `ExitPlan`, `Fact`, `GateRun`, `ReviewRun`); CSV import + manual entry; delayed-
  quote price fetch; tests for the store.
- **Week 2** — Advisor engine skeleton + first gate. The gather / run / record phase split;
  prompt-cache the skill text; implement `asset-allocation-policy` end to end (policy
  capture, drift math, contribution routing); no-verdict and provenance tests.
- **Week 3** — `position-exit-rules` + `portfolio-thesis-audit`. Shared reads of the
  canonical store; the routing state machine (thesis-audit → research-writeup); block a
  "trade plan complete" state on a missing exit plan.
- **Week 4** — `weekly-portfolio-review`. The seven-step pass over the whole store; red-flag
  list (no thesis / no exit plan / policy drift / stale facts); follow-up tracking;
  `ReviewRun` history.
- **Week 5** — RAG integration. Embed prior theses + past `ReviewRun`s + relevant notes;
  retrieval into the review ("what changed since last review", repeat-flag detection);
  retrieval-quality iteration.
- **Week 6** (optional) — Thin React view (portfolio table, drift report, review history),
  token-cost logging pass, README + architecture write-up, interview-story polish.

*Compressed standalone option (~4 weeks): Weeks 1–4 only — store + the four core gates,
CLI-only, RAG deferred. Extend with the stretch gates and RAG later.*

## Interview Story (Draft)

"I keep a personal library of written investing decision frameworks — each one is a *gate*:
it deliberately refuses to give you an answer until you've supplied real, sourced inputs (an
actual stop price, a falsifiable thesis, figures pulled from a filing rather than memory).
They work, but running them by hand every week is tedious, so I built an AI advisor that
runs them against my real portfolio.

The interesting engineering constraint was that the value of the frameworks is precisely the
part software tends to destroy. An 'advisor' app wants to be helpful — pre-fill the thesis,
infer the stop, suggest a verdict you rubber-stamp — and every one of those collapses the
discipline. So I split each workflow into three phases that can't bleed into each other:
*gather* (Claude assembles the inputs and drafts nothing as fact without a source tag I
confirm), *run* (Claude walks the gate's checklist and surfaces what's missing), and
*record* (I type the decision and the reasoning — the system never populates a verdict
field). There's a test that asserts no code path returns a buy/sell/size recommendation, and
another that a workflow can't complete on an unsourced or stale figure.

The other real problem was coherence: I have maybe eight of these gates and they're designed
to compose — an allocation policy is the frame every position decision runs inside, the
weekly review reads every position's thesis and exit plan. I put everything in one canonical
store and made the routing between gates an explicit state machine instead of prompt glue,
so it's testable — add a bare holding and it shows up in the weekly review's red flags until
its thesis and exit plan exist.

What I learned: 'add AI to it' is often the wrong framing. The skill here was figuring out
which part of the human process to speed up (gathering and tracking inputs) and which part
to protect from automation (the judgment the frameworks exist to force)."

---

*Once shipped, add a "Final Interview Story" section here reflecting what actually happened
during the build.*
