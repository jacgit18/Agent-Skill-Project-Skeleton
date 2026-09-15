---
name: etf-investment-take
description: |-
  The funds counterpart to `equity-investment-take` — Claude's own sourced, opinionated read on a specific ETF: expense ratio, tracking, holdings/overlap, structure, a tilt thesis where relevant, and a verdict with reasoning plus a consider/watch list. Triggers: an explicit ask for Claude's own opinion on a fund — "what do you think of TICKER", "give me your take on this ETF", "should I buy this fund". Every fact fetched live and cited via Webull fund-data tools plus the issuer fact sheet, never estimated; gaps flagged NOT VERIFIED. Not the default for `etf-selection`'s own evaluate asks ("SPY or VOO", "check the ETFs I own") — that stays the gate; fires only on an explicit opinion ask, not that gate released under pressure. Not stocks (`equity-investment-take`), not the sleeve decision (`asset-allocation-policy`), not sizing/entering (`equity-trade-decision`), not options on a held fund (`covered-call-decision`).
---

# ETF Investment Take

`etf-selection` exists because a fund bought on ticker recognition or a headline yield, with
nobody checking the expense ratio, the real holdings, or the overlap with what's already
owned, isn't a decision — it's a guess with a ticker attached. That gate is correct and stays
exactly as it is, including under pressure ("just tell me if VOO beats SPY," "I don't want to
pull fact sheets"). This skill is the same resolution `equity-investment-take` already applies
on the stock side: a **separate, explicitly-invoked** door for when the user has genuinely
decided they want Claude's own opinion instead of assigning the fund a role and pulling its
own facts. Not the gate caving — a different skill, different rules, asked for on purpose.

Where it sits: parallel to `etf-selection`, the same relationship `equity-investment-take` has
to `equity-research-writeup`. Both answer "should I own this fund"; which one responds depends
on whether the user wants their own process or Claude's opinion.

## What this does not do

- **Become the default for an evaluate-this-fund ask.** "SPY or VOO," "is this thematic ETF
  worth adding," "check the ETFs I own" still belong to `etf-selection`. This skill fires only
  on an unambiguous ask for Claude's own opinion — see the disambiguation table below.
- **Release `etf-selection`'s gate from inside that skill's own flow.** Pressure there ("just
  tell me if VOO beats SPY," "you already know the expense ratios") still does not release
  it — name this skill as the real alternative instead of a dead end; the user still has to
  ask for *this* skill on purpose.
- **Evaluate an individual stock.** `equity-investment-take` is the equity counterpart — a
  business/competitive/bear-case shape, not a cost/tracking/holdings shape. Different fact set
  entirely.
- **Set the allocation or the sleeve.** Whether a bond/commodity/sector sleeve should exist and
  its target % is `asset-allocation-policy`. This skill can name what role a fund *looks like*
  it fills (broad core, factor tilt, bond, commodity, income) from its own holdings and
  structure, but assigning it a slot in the user's actual policy stays theirs.
- **Size or enter the trade.** A BUY-leaning verdict here satisfies `equity-trade-decision`'s
  checklist item 1 the same way a completed `etf-selection` review does; it does not size or
  time the purchase.
- **Write options on a fund already held.** `covered-call-decision` owns that, downstream.
- **Skip real sourcing.** Same bar as `equity-research-sourcing`/`equity-investment-take`:
  every fact fetched live and cited, a gap flagged `NOT VERIFIED` rather than estimated — the
  license to opine is not a license to guess a number.

## When this fires vs. `etf-selection`

| Ask | Skill |
|---|---|
| "SPY or VOO," "is this thematic ETF worth adding," "which bond ETF for my sleeve," "check the ETFs I own" | `etf-selection` — the gate, the default |
| "What do you think of TICKER," "give me your take on this ETF," "is TICKER worth adding," "should I buy this fund" | **This skill** |
| Mid-`etf-selection`, the user pushes back on pulling fact-sheet data themselves | Still `etf-selection` — hold the gate, but name this skill by name as the real alternative |

A fund named only as an example inside a broader allocation question stays with whichever
skill owns that question (usually `asset-allocation-policy`), not this one. If it's unclear
whether the user wants the gated comparison or Claude's opinion, ask once rather than guessing.

## The process

1. **Fetch.** Webull's fund-data tools (`get_fund_brief`, `get_fund_holdings`,
   `get_fund_performance`, `get_fund_net_value`, `get_fund_allocation`, `get_fund_dividends`,
   `get_fund_splits`, `get_fund_rating`) plus `get_stock_snapshot` (`US_ETF`) for price/volume
   — each fact cited with source + as-of date.
2. **Search.** `WebSearch`/`WebFetch` the issuer's own fact sheet or prospectus for whatever
   the structured tools don't carry precisely — multi-year tracking difference, in-kind
   creation/redemption structure, domicile, whether a distribution includes return of capital,
   physical-vs-futures for a commodity fund, duration/credit/YTM for a bond fund.
3. **Synthesize.** Assemble the output block below. Name what role the fund appears to fill
   (broad core / factor or sector tilt / bond / commodity / income), state the holdings-overlap
   picture if the user has named what else they hold (ask once if they haven't), author the
   tilt thesis and its decay check for a non-core fund instead of requiring the user to write
   it, and commit to a real verdict — not a hedge.

## Output block

```
ETF take — <TICKER>   ·   <date>   ·   apparent role: <broad core | factor/sector tilt | bond | commodity | income>

Facts (each sourced):
  Expense ratio:        <n>%                              source: <...>
  Tracks:                <index>  ·  <n> holdings  ·  top-10 = <n>%  ·  <sector/geo note>  source: <...>
  AUM / ADV:             $<n> / $<n>/day                   source: <...>
  Tracking difference:   <n>% 1y / <n>% 3y / <n>% 5y       source: <...>
  Structure:              <physical | synthetic>  ·  in-kind <y/n>  ·  domicile <...>  source: <...>
  Yield:                 <n>%  (<qualified | includes ROC | YTM for bond>)  source: <...>
  Age:                   <n> years
  [bond] duration <n>y · credit <avg> · YTM <n>%
  [commodity] <physically backed | futures-based> · tax <treatment>

Overlap:  <vs named holdings, if supplied | not supplied — ask once before finishing>

Tilt thesis (non-core only):  <Claude's own why-this/why-now, sourced>
  Decay check:  <durable structural exposure | narrow, new, launched near a hype peak>

Consider / watch:
  - <specific factor to weigh>
  - <specific factor to weigh>
  [...]

Verdict:  <BUY/HOLD — fills a real role, cost + tracking fine | SWAP — name the cheaper/better
          alternative | PASS — <reason> | RESEARCH — <what's still NOT VERIFIED>>, with
          explicit reasoning, not just the label.
What would change this read:  <specific events or data that would flip it>
```

## Red flags — the take isn't real

- A fact with no source name or as-of date — indistinguishable from a guess.
- A verdict delivered while a material fact is `NOT VERIFIED`, without saying so plainly.
- This skill firing on a bare fund-evaluation ask with no explicit request for Claude's own
  opinion — starvation of `etf-selection`'s gate.
- Overlap skipped entirely instead of asked for once when not already supplied.
- A thematic/tilt fund's decay check skipped, or a hedge ("could go either way") standing in
  for a real verdict.

## Example invocations

> "What do you think of QQQM — worth adding for tech exposure?"

This skill. Fetch the facts, ask what else is held if overlap matters, author the tilt thesis
and decay check, give a real verdict.

> "Is this thematic ETF worth adding?" (no prior opinion request, just an evaluate-this ask)

Not this skill by default — `etf-selection`'s gate, unless the user makes clear they want
Claude's own take instead of doing the fact-pulling themselves.

> "I don't want to pull fact sheets, just tell me if VOO beats SPY."

Inside an active `etf-selection` conversation, this is pressure, not a release — the gate
holds. Name this skill as the real alternative.

> "TICKER looks good, buy me some."

The verdict conversation is over — `equity-trade-decision` for sizing and entry.

> "What do you think about NVDA?"

An individual stock — `equity-investment-take`, not this skill.

---

## Portability

Depends on Webull's fund-data tools (`get_fund_brief`, `get_fund_holdings`,
`get_fund_performance`, `get_fund_net_value`, `get_fund_allocation`, `get_fund_dividends`,
`get_fund_splits`, `get_fund_rating`) plus `get_stock_snapshot` and `WebSearch`/`WebFetch` for
fact-sheet detail. Writes nothing to disk; the take is delivered in chat. Copy the
`etf-investment-take/` directory into another repo's `.claude/skills/`, alongside
`etf-selection` and `equity-investment-take`.
