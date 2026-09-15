---
name: lump-sum-vs-dca
description: |-
  For a real, consequential one-time sum (bonus, inheritance, sale proceeds) already destined for an existing allocation — decides the entry schedule using real historical price data, not a recited "studies show" claim. Triggers: "should I invest this all at once or spread it out", "lump sum vs DCA", "I got a windfall, how should I invest it". Pulls real bars via Webull for the destination benchmark, computes the actual historical win rate and magnitude of lump sum vs. a staged schedule across real rolling windows, then presents options against the user's own stated regret-risk tolerance — Claude states what the evidence favors, the user picks the schedule. Not `asset-allocation-policy` (sets the destination and the generic day-to-day contribution cadence — this is for one sum big enough to warrant a real look, not routine small deposits), not a market-timing call (`macro-cycle-read` is the cycle-stage skill, if invoked at all), not which fund/stock to buy.
---

# Lump Sum vs. Dollar-Cost-Averaging

"Lump sum wins about two-thirds of the time" is the kind of claim that gets repeated from
memory, never actually checked against real prices, on a decision that's often a genuine
five- or six-figure sum. `strategy-backtest-design` already refuses to let a trading rule get
tested on anything but real historical bars; this is the same discipline applied to a
different, common question — not a trading rule, a one-time contribution schedule. This
skill pulls real price history for the actual destination benchmark and computes the actual
numbers for *this* run, then treats the result as one input to a decision that also depends
on the user's own stated tolerance for a bad first month — never as the whole decision.

Where it sits: assumes `asset-allocation-policy` already exists (the money's destination is
decided) — this only answers *when*, not *where*. The policy's own area 6 sets a generic
cadence default for routine contributions; this skill is for a specific sum big enough, or a
regret-risk stated strongly enough, that the generic default isn't a satisfying answer on its
own.

## What this does not do

- **Set the destination allocation.** `asset-allocation-policy` decides where the money goes
  (asset class, sleeve). If no policy exists yet, gate there first — there's nothing to
  schedule an entry into.
- **Set the generic day-to-day contribution cadence.** Policy area 6 already states a default
  ("lump sum on arrival" or "spread over N weeks") for routine paycheck-sized contributions.
  This skill is not re-run for every regular deposit — it's for a real one-time sum, or when
  the user's stated regret-risk makes the generic default worth checking against real evidence.
- **Make a market-timing call.** The historical win-rate computation is not a prediction and
  never becomes "the market's about to drop, wait." `macro-cycle-read` is the one skill in this
  catalog that calls a cycle stage from real evidence, and even it never picks a top or bottom —
  citing it here, if at all, is context, not a reason to delay.
- **Resolve debt-vs-invest.** If the sum could instead pay down high-APR debt,
  `debt-credit-management` and `asset-allocation-policy` both name that tension without
  resolving it — this skill assumes the money is already destined for investing, not still
  contested with a payoff decision.
- **Pick the fund or stock.** Once a schedule is chosen, what specifically gets bought is
  `watchlist-screener-criteria` / `equity-research-writeup` / `etf-selection` territory, or a
  simple add to an existing core holding already inside the policy's targets.
- **Fabricate or recall historical statistics.** Every number in the output comes from a real
  Webull bar pull for this run. A "studies generally show" line with no fetched data behind it
  is not an answer here — same standard `strategy-backtest-design` holds itself to.
- **Answer a bare conceptual question.** "What's dollar-cost averaging" with no real sum on the
  table is `learning-gate`.

---

## The precondition

1. **Destination confirmed.** The `asset-allocation-policy` sleeve(s) this money is going into.
   No policy on file → gate there first.
2. **The sum**, and that it's genuinely a one-time, consequential amount — not a routine
   recurring deposit already covered by the policy's own cadence default.
3. **The benchmark.** Default to whatever the destination sleeve's core holding actually is
   (e.g. the broad index fund the equity sleeve is built around); the user can name a different
   one.
4. **Staged-schedule length**, if a comparison is wanted — how many months a "spread it out"
   option would run (a common default is 6 or 12; ask rather than assume).
5. **Regret-risk tolerance, stated plainly.** How the user would actually feel investing the
   full sum today and watching it drop 15–20% over the following month or two — this is the
   input the historical win-rate alone can't supply, and it's what actually decides between two
   options with different expected value and different downside-regret profiles.

If 1–5 are missing — especially 5 — ask and **stop**. A recommendation with no stated
regret-risk tolerance is not this skill's answer, the same standard `asset-allocation-policy`
holds for its own five inputs.

---

## Computing the real evidence

1. Pull real daily bars for the benchmark via `get_stock_bars_single` (as much history as the
   tool returns, same source and honesty standard as `strategy-backtest-design`).
2. For every available rolling start date, compare: invest 100% on day 1, vs. invest evenly
   across the stated staged-schedule length starting the same day. Compute each path's ending
   value at the same horizon.
3. Report: how many of the rolling windows lump sum won, by how much on average, and the
   single worst outcome for lump sum in the window set (dated) — the scenario the regret-risk
   question is actually about.
4. State the caveats plainly: one benchmark, the data window's actual depth (say it if it's
   thin), a market with a long-run upward drift will structurally favor lump sum more often —
   this is a description of *this* history, not a guarantee about the next period.

---

## Output — the decision block

```
Lump sum vs. DCA — $<amount>   ·   destination: <policy sleeve(s)>   ·   benchmark: <ticker>

Historical evidence (real bars, <date range>, <n> rolling <M>-month windows):
  Lump sum beat staged entry in <n>/<n> windows (<pct>%)
  Average ending-value difference: lump sum $<n> vs. staged $<n>
  Worst case for lump sum in this window set: <the specific dated drawdown scenario>

Stated regret-risk tolerance: <user's own words>

Options:
  A — 100% lump sum now
  B — Staged over <n> months (<pct>/<pct>/... schedule)
  C — Hybrid: <pct>% now, remainder staged over <n> months

Evidence favors:  <A | B/C, and by how much>  — the schedule itself is your call, not
                  Claude's; this is one input, not the whole decision.

Feeds forward: chosen schedule → routed per asset-allocation-policy area 6's contribution rule;
what specifically gets bought is a separate `watchlist-screener-criteria` / `etf-selection` /
existing-core-holding question.
```

---

## Red flags — the evidence isn't real

- A win-rate or "studies show" claim with no actual Webull bar pull behind it for this run.
- No destination allocation on file — there's nowhere for either schedule to route into yet.
- The regret-risk question skipped, so "evidence favors lump sum" stands in as the whole
  decision instead of one input the user still weighs.
- This run triggered for a routine small recurring deposit instead of a genuine one-time sum.
- A market-timing call smuggled in ("wait, we're near a top") dressed up as historical evidence.
- The worst-case scenario for lump sum omitted — the number the regret-risk question is
  actually about.

---

## Example invocations

> "I just got a $60k inheritance — should I put it all in at once or spread it out?"

This skill. Confirm the destination policy exists, pull real bars for the core benchmark,
compute the rolling-window comparison, ask the regret-risk question, present the three options.

> "I get $500/paycheck into my brokerage — lump sum or spread it?"

Too small and routine — that's the policy's own area 6 cadence default, already set once, not
a fresh run of this skill every paycheck.

> "Where should this money actually go — stocks, bonds, cash?"

That's the allocation itself — `asset-allocation-policy`, not this (this only answers *when*).

> "Is now a good time to invest?"

Too vague for a real sum on the table — if there's no actual amount, `learning-gate`; if there
is, this skill still answers with historical entry-schedule statistics, never a market call.

---

## Portability

Repo-agnostic logic; the data pull is Webull-tool-specific (`get_stock_bars_single`, same as
`strategy-backtest-design`) — a port to another repo needs an equivalent real-bars source.
Writes nothing; produces the decision block in chat. Assumes `asset-allocation-policy` already
exists upstream.
