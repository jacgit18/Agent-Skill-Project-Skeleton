---
name: macro-cycle-read
description: |-
  Call which economic-cycle stage we're in — post-recession recovery, recovery momentum, mid-cycle expansion, late-cycle/peak, or recession/contraction (`equity-trade-decision`'s stage names) — from real, sourced values, not vibes. Triggers: "what stage of the cycle are we in", "should I tilt toward X sector", "read the macro picture", or an unsourced `equity-trade-decision` cycle-stage step. A gate: pulls current values via search/fetch (never memory) across yield curve (2s10s/3m10y), labor (unemployment + claims trend), leading activity (ISM/PMI + 3-month trend), credit (HY spread), and inflation trajectory (CPI/PCE direction) — names a stage only on ≥3 of these 5, never one indicator, flags conflicts. Not a stock/sector/ETF pick (`equity-trade-decision`'s tilt table, `etf-selection`), not a broad-market timing call or license to exceed allocation bands (`asset-allocation-policy`), not a macro-regime backtest (`strategy-backtest-design`, no regime mode), not a recession-timing forecast — current state only.
---

# Macro Cycle Read

"The market feels toppy" or "we're clearly late-cycle" is a stage call with no evidence behind
it — the exact failure `equity-trade-decision`'s own cycle-stage step exists to catch, and the
one this skill is built to satisfy instead of leaving to a vibe. This skill withholds a stage
name until real, current values exist for a minimum spread of independent categories, states the
call as a hypothesis rather than a fact, and hands the stage plus its evidence to whatever asked
for it.

## What this does not do

- **Pick a stock, sector, or ETF.** Naming the stage is the input; turning it into a sector tilt
  is `equity-trade-decision`'s cycle-stage sector-tilt table, and fund selection against a
  stage-informed sleeve is `etf-selection`. This skill hands off the stage and stops.
- **Call a broad-market top or bottom, or license moving outside allocation bands.** A cycle
  stage informs a tilt *within* the bands `asset-allocation-policy` already set — it never
  overrides them, and it's not a signal to raise or lower overall equity exposure.
- **Backtest how a stage historically resolved.** `strategy-backtest-design` backtests
  rule-based entry/exit logic on price data; it has no macro-regime mode today. If asked to
  backtest "what happens after late-cycle," name that gap rather than improvising a regime
  study here.
- **Forecast recession timing or duration.** Describes the current read only — never "a
  recession is coming in Q2" or "this expansion has 18 months left."
- **Invent an indicator value.** If search/fetch can't turn up a current number for a category,
  that category is unavailable — count it out of the ≥3, don't estimate or recall a plausible
  one from memory/training data.

---

## The gate — real current values across ≥3 of 5 categories

| # | Category | What to pull | Source shape |
|---|---|---|---|
| 1 | Yield curve | 2s10s or 3m10y spread — current value and direction (steepening/flattening/inverted) | Treasury / FRED |
| 2 | Labor market | Unemployment rate trend + initial-claims trend | BLS |
| 3 | Leading activity | ISM/S&P Global PMI manufacturing and services — current print and 3-month trend | ISM / S&P Global |
| 4 | Credit conditions | High-yield spread level and direction | FRED (ICE BofA HY OAS) |
| 5 | Inflation trajectory | CPI or PCE — direction, not just the latest level | BLS / BEA |

Pull each via search/fetch against a primary or clearly-attributed source — never from memory or
training-data recall, which goes stale the moment a print updates. A category with no findable
current value is simply unavailable; it does not get filled in with a plausible guess.

**No stage call below 3 of these 5.** A read on 1–2 categories is "here's what I could source,
not enough for a stage call" — say that and stop, don't round up to a verdict. A single
indicator ("the NASDAQ dropped 3%," "unemployment ticked up one-tenth") is never a cycle read on
its own, regardless of how dramatic it looks.

---

## Stage signatures — for classification, not for a sector tilt

Use this only to match sourced values to a stage name. It is deliberately not a "what to buy"
table — that table already exists, in `equity-trade-decision`, and this skill doesn't duplicate
it.

| Stage | Yield curve | Labor market | Leading activity | Credit spreads | Inflation |
|---|---|---|---|---|---|
| Post-recession recovery | Steepening off inverted/flat | Unemployment still elevated, claims falling | PMI rising, crossing back above 50 | Narrowing sharply | Falling or bottoming |
| Recovery momentum | Steep and positive | Unemployment falling, claims low | PMI solidly above 50, still rising | Tight and stable | Stable, moderate |
| Mid-cycle expansion | Positive, flattening slowly | Unemployment near cycle lows | PMI above 50, off its peak | Tight | Firming |
| Late-cycle / peak | Flattening or inverting | Unemployment at cycle lows, starting to tick up | PMI rolling over toward 50 | Starting to widen | Elevated, sticky |
| Recession / contraction | Inverted or freshly dis-inverting | Unemployment rising, claims spiking | PMI below 50, falling | Widening sharply | Falling (demand destruction) |

Real data rarely lines up cleanly with one row — that's expected, not a bug in the framework.

---

## Process

1. Pull current values for as many of the 5 categories as findable via search/fetch. Stop and
   report a partial read if fewer than 3 come back.
2. Match the sourced values against the stage-signature table. Name the **closest-fitting
   stage as a hypothesis** — "the evidence points to X" — not a flat assertion. Cycle calls are
   contested in real time; this skill's own confidence is bounded by how many categories agree.
3. List which categories support the named stage and which conflict. If two categories point to
   adjacent stages (e.g., labor still strong while PMI has rolled over — a common late-cycle
   pattern), say so explicitly rather than silently picking the more dramatic-sounding read.
4. Hand off the stage name plus the evidence table to whatever requested it — most often
   `equity-trade-decision`'s own cycle-stage step, which owns the resulting sector tilt, or
   answer a standalone "where are we in the cycle" question directly with the same evidence
   table.

---

## Red flags — the read isn't done

- A stage named on fewer than 3 sourced categories.
- A stage named from a single indicator, however dramatic ("the market dropped 3%," "jobs report
  missed").
- Any indicator value recalled from memory/training data rather than pulled live via
  search/fetch.
- A stage call delivered as settled fact rather than a hypothesis, with no mention of which
  categories agree or conflict.
- A sector, stock, or ETF recommendation issued from inside this skill instead of handed to
  `equity-trade-decision` / `etf-selection`.
- The stage read used to justify moving outside `asset-allocation-policy`'s bands rather than
  tilting within them.
- A recession-timing or -duration forecast issued instead of a current-state description.

---

## Portability

Repo-agnostic; the data pull is source-agnostic (FRED, BLS, ISM/S&P Global, Treasury) via
whatever search/fetch tooling is available — no dedicated MCP data tool required. Writes
nothing on its own; produces the stage call and evidence table in chat. Chains into
`equity-trade-decision`'s cycle-stage step (stage in, sector tilt out) and can answer a
standalone macro question with no downstream trade in view.
