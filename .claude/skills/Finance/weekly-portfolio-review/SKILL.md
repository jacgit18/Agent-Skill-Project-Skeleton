---
name: weekly-portfolio-review
description: Use for the recurring, structured operational pass over a brokerage account — "do my weekly review", "run the portfolio check", "what do I need to look at this week", "weekly portfolio review" — not the one-off "should I sell this" question. Also fires on a diagnostic framing — "I keep skipping my review", "things fall through the cracks", "my weekly process isn't working" — by walking the seven steps and the red-flags list to find where the process is breaking. It is a procedure, not a gate: it needs concrete inputs (the current holdings with cost basis / price / % of book; each position's written thesis and exit rules on file, or a flag that they're missing; any covered calls written, with strike and expiration; a forward calendar of earnings, ex-dividend, and option-expiration dates; the date of the last review) and then runs a fixed seven-step walk — positions vs. thesis, stops still valid, options expiring, earnings and events ahead, allocation drift vs. each position's size ceiling and vs. the `asset-allocation-policy` bands (asset-class, sector, theme, geography) when a policy exists, watchlist names in range, and what changed since last review. It does not make the decisions: every finding is surfaced and tagged with the skill that owns the follow-up — `portfolio-thesis-audit` for a shaky thesis, `position-exit-rules` for a missing or stale stop, `covered-call-decision` for an expiring call, `equity-trade-decision` for a watchlist name that's ready, a trim flag for a position over its ceiling. It runs on a calendar cadence on purpose — so the review happens when the user is calm, not only when a position drops and disposition-effect bias is strongest. Not `portfolio-thesis-audit` — that is the full per-position keep/sell audit this review flags positions *for*; "which of these should I sell" routes there, "run my weekly check" stays here. A bare "review my portfolio" / "tell me what to do with my holdings" with no cadence signal is `portfolio-thesis-audit` (or `ambiguity-gate` if the intent itself is unsettled); this skill needs a recurring / periodic / weekly framing to fire. Not portfolio construction or target-allocation design — that's `asset-allocation-policy`; step 5 checks drift against its bands and routes there when no policy exists. Not the scheduling/automation infrastructure itself — this defines the content of the review; a Python/yfinance script produces the raw data it consumes. Not a bare conceptual question — "how should I review a portfolio" with no holdings is `learning-gate`. Not a substitute for a financial advisor.
---

# Weekly Portfolio Review

Portfolio review usually happens on a *fear* cadence — you look when something is down a lot,
which is exactly when loss-aversion bias is loudest — or it doesn't happen at all, and an
option expires unmanaged, earnings hit a position you forgot was reporting, a stop goes stale
after the thesis changed, a broken thesis just sits there for months. This skill is a
**procedure**: a fixed weekly walk that catches those on a calendar, and routes each finding
to the skill that owns the decision. It does not make the calls itself.

## Inputs the walk needs

Ask for what's missing and note it; the walk can run partially, but gaps get flagged loudly.

1. **Holdings** — per position: ticker, shares, cost basis, current price, unrealized P&L,
   % of the portfolio. (This is the "portfolio dashboard" data — a script can produce it.)
2. **Thesis + exit rules on file** — for each position, the written thesis (built via
   `equity-research-writeup`, audited by `portfolio-thesis-audit`) and the exit rules
   (`position-exit-rules`: hard stop, thesis-invalidating events, size ceiling, upside review
   trigger). If a position has neither, that is finding #1 for it.
3. **Option positions** — any covered calls written: underlying, strike, expiration,
   contracts, currently ITM or OTM.
4. **Forward calendar** — earnings dates, ex-dividend dates, and option-expiration dates for
   the held names, out to at least the next review; any macro event the user tracks.
5. **Last review date** — to scope "what changed since".

---

## The walk — seven steps, every time

### 1. Positions vs. thesis

For each holding, a *quick* check (not a full audit): is the thesis still plausibly intact?
Price against the upside review trigger and against the hard stop. Anything that has hit a
trigger, or whose thesis looks shaky on a quick read, or that has no thesis on file →
**flag for `portfolio-thesis-audit`**.

### 2. Stops still valid

For each position: is the hard stop still where the exit rules say? Has the thesis or the
position size changed in a way that makes the stop stale (e.g. the thesis-invalidating event
already partly fired, but the price stop was never revisited)? No stop on file →
**flag for `position-exit-rules`**. A stop that was quietly loosened after a drawdown is its
own flag — that is the disposition effect editing the rule.

### 3. Options expiring

Covered calls expiring before the *next* review:

- **ITM** (likely assignment) → decide roll vs. let assign → **`covered-call-decision`**.
- **OTM** → decide re-write vs. stop writing → **`covered-call-decision`**.
- **Ex-dividend date before expiration on an ITM call** → early-assignment watch, note it.

### 4. Earnings and events ahead

Positions reporting earnings before the next review; ex-dividend dates; any covered call that
would be held *through* an earnings date. List the names with event risk in the coming week —
this is information for steps 1–3, not an action on its own.

### 5. Allocation drift

Any position now above its size ceiling (from its exit rules) → **trim flag**. Current cash
%. Largest position as a share of the book. This is a guardrail check, not a rebalancing
model — it flags the breach and stops.

Book vs. the `asset-allocation-policy` bands — asset-class targets, per-sector, per-theme,
geography: any band breached → **flag for `asset-allocation-policy`**. No allocation policy
on file at all → **flag for `asset-allocation-policy`** to build one; until then drift has
nothing to measure against.

### 6. Watchlist

Names that cleared `watchlist-screener-criteria` and are waiting: any that have moved into or
out of the entry range. One that's ready and that the user has capital for →
**`equity-trade-decision`**.

### 7. Since last review

What changed: realized trades, assignments, new positions, thesis updates, stop changes.
Keeps a running log so the review has memory.

---

## Output — the review report

```
Weekly portfolio review — <date>   (last review <date>)

Positions: <n>   ·   Cash: <pct>   ·   Largest: <ticker> <pct>   ·   Over ceiling: <n>
Thesis/exit rules on file: <n>/<n> positions   ← the number to drive to <n>/<n>

Action items — each tagged with the skill that owns the follow-up:
  [portfolio-thesis-audit]  <TICKER> — <what looks off: hit review trigger / thesis shaky /
                            nothing on file>
  [position-exit-rules]     <TICKER> — <no stop on file | stop stale because <...>>
  [covered-call-decision]   <TICKER> — $<K> call expires <date>, <ITM|OTM> → <roll vs assign
                            | re-write vs stop>
  [equity-trade-decision]   <TICKER> — cleared the screen <date>, in range, capital available
  [trim]                    <TICKER> — <pct>% of book, over the <pct>% ceiling
  [asset-allocation-policy]  <which band drifted: asset-class / sector / theme / geography |
                            no allocation policy on file>

Event calendar — through <next review date>:
  <date> <TICKER> earnings   ·   <date> <TICKER> ex-div   ·   <date> <exp> option expiration

Clean — no action: <TICKERS that checked out on all seven steps>

Since last review: <realized trades / assignments / new positions / thesis + stop updates>
```

Every section appears even when empty (`none`), so a light week is visibly a light week and
not a skipped step.

---

## Automation boundary

The review is structured so a script does the data, a human does the judgment. Mirrors the
user's own Automate / Don't-automate split.

| A Python/yfinance script produces | Stays a human (or gated-skill) decision |
|---|---|
| Holdings table: shares, cost basis, price, P&L, % of book | Whether a thesis is still intact (step 1) |
| Price vs. stop / vs. review trigger — the arithmetic | Roll vs. let assign; re-write vs. stop (step 3) |
| Earnings / ex-div / expiration calendar pull | Whether to trim a ceiling breach now or wait |
| Covered-call ITM/OTM status, days to expiry | Sizing any new entry (step 6) |
| "Over ceiling" and cash-% flags | Editing an exit rule (that's `position-exit-rules`) |
| Position / sector / asset-class % vs. the `asset-allocation-policy` bands | Whether to act on a band breach (`asset-allocation-policy` owns the rule) |
| The since-last-review diff of the holdings table | — |

A script that starts *making* the step-1/3/5 decisions has crossed the line — the review
surfaces and routes, it doesn't decide.

---

## Red flags — the review isn't real

- Action items that resolve the decision inline instead of routing it (e.g. "sell TICKER"
  rather than "`portfolio-thesis-audit` TICKER — thesis broke on <X>").
- Steps skipped silently rather than shown as `none`.
- The review run only because a position dropped — the cadence is the point; a fear-driven
  look is not this.
- Missing theses / stops noted once and then never counted again — the `<n>/<n> on file`
  line exists to make the gap visible every week until it's closed.
- A stop shown as "still valid" when the thesis-invalidating event has already partly fired.
- Automation that has drifted into making the judgment calls, not just the data.

---

## Example invocations

> "Do my weekly portfolio review."

Run the walk. Ask for the holdings table, the thesis/exit-rules status per position, any
covered calls, the forward calendar, and the last review date. Produce the report.

> "Which of my positions should I actually sell?"

That's the full keep/sell audit — `portfolio-thesis-audit`, not this. This review might
*flag* three positions for that audit; it doesn't run it.

> "Help me set up a weekly review process — what should it cover?"

If they have real holdings, walk the seven steps against them. If it's a general "how should
this work" with nothing concrete, that's `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing by itself; produces the review report in chat. The seven-step
structure and the input list are deliberately mechanical so a Python/yfinance script can feed
it (see Automation boundary). Copy the `weekly-portfolio-review/` directory into another
repo's `.claude/skills/`. It is the recurring integration pass over the other `Finance/`
skills — `portfolio-thesis-audit`, `position-exit-rules`, `covered-call-decision`,
`equity-trade-decision`, `watchlist-screener-criteria` — and routes to each. If a session is
ending and the user wants the review carried forward, run or confirm it first, then persist
the report via `session-handoff`.
