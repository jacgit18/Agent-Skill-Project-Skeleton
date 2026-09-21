---
name: watchlist-screen-sync
description: "Screen named stocks, discover candidates, maintain Webull AI style watchlists, and sync AI Shortlist for Deep Value, Quality Compounder, Growth, Momentum, and Dividend Income. Use for 'screen TICKER', 'find [style] candidates', 'run discovery', 'sync the shortlist', and 'check TICKER for day trade'. Supports unattended Webull sync with exact derivations, progressive retrieval, early exits, a 5-new-candidate/style cap, and rotating 9-sector Deep Value/Quality discovery. Not for portfolio reviews (weekly-portfolio-review), trade sizing/entry (equity-trade-decision), or full thesis research (equity-research-writeup). Never auto-removes names or trades."
---

# Watchlist Screen Sync

> Updated for Webull unattended screening: 5-new-candidate cap,
> deterministic metric derivation, progressive retrieval, and early-exit
> call-budget safety.

Bridges Joshua’s committed screening criteria (general + five styles)
with his actual Webull watchlists, so a ticker that clears a screen
shows up somewhere real instead of just getting typed into a chat
response he has to remember to act on. A ticker that fails still gets
logged, not silently dropped, so it can be checked against “already
screened” before being re-litigated.

**This skill does not replace any downstream gate.** Landing on any
watchlist — general or style-specific — is not a buy signal.
`equity-research-writeup` still owns the thesis, `equity-trade-decision`
still owns sizing and entry. This skill only automates the filing step.

**This skill does not define or loosen the criteria.** The thresholds below are Joshua's committed rules. Changes to thresholds, formulas, disqualifiers, discovery cadence, or write authority require Joshua's explicit sign-off. Don’t adjust a number,
add a metric, or relax a disqualifier because a candidate is “close” or
because it seems reasonable in the moment — that’s a Define-mode change,
and it requires Joshua’s explicit sign-off in conversation, the same bar
as any other screen edit.

## Webull watchlist IDs

| Watchlist             | ID                                 |
|:----------------------|:-----------------------------------|
| Screen Passed         | `d478a39a042c4612aa3d57493121b3c1` |
| Screen Rejected       | `ffe8dc1df7344497b040f76ecf461d2f` |
| AI Deep Value         | `3157a89143694aefb8dba81fa50dcf33` |
| AI Quality Compounder | `4af991cc1719405686c10bef335e1e74` |
| AI Growth             | `3a9ed36d4d71445f85534476c91abcd6` |
| AI Momentum           | `115ceb562bf147c990effd9d1b6f6362` |
| AI Dividend Income    | `1f248ceaf10b482d8375af7d4e3774c4` |
| AI Shortlist          | `73b222507bd84d3b84a16e14c0d2ed72` |
| AI Day Trade          | `e1d3094ed02842d583034ee9a23f801e` |

Specific to Joshua’s Webull account. If copied to another account, these
IDs won’t resolve — call `Webull:get_watchlists` to find or recreate
equivalents and update this table.

**“AI” in each name is a list-ownership marker, not a sector filter.**
It means “Claude created and files into this list” — nothing more. These
watchlists are NOT scoped to AI or tech companies; every style screen,
the Day Trade screen, and Shortlist’s aggregation apply market-wide,
across every sector, exactly as they would for a healthcare, industrial,
financial, energy, or consumer name. Never narrow discovery’s candidate
pool to AI/tech/semiconductor names because of the list name — see the
cross-sector sampling requirement in Candidate discovery below.

## The five committed style screens

### Deep Value

| Criterion             | Rule                                                                                                                                                               |
|:----------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Valuation metric      | EV/EBITDA, judged relative to the company’s own sector average (no fixed absolute number)                                                                          |
| Cash-flow cross-check | EV/FCF or FCF yield, also judged relative to sector — required especially when the candidate is capital-intensive (capex/sales materially above its sector median) |
| Safety filter         | Current ratio ≥ 2, AND long-term debt ≤ net current assets (Graham’s classic check)                                                                                |

A candidate must clear EV/EBITDA AND the FCF cross-check AND the safety
filter to pass.

### Quality Compounder

| Criterion                                         | Rule                                                                                                           |
|:--------------------------------------------------|:---------------------------------------------------------------------------------------------------------------|
| ROIC                                              | ≥ 15%                                                                                                          |
| Gross Profitability (gross profit ÷ total assets) | Top 30% of its industry peers                                                                                  |
| Valuation check                                   | Sector-relative EV/EBIT or FCF yield                                                                           |
| Piotroski F-Score                                 | Disqualifier only — reject/flag if ≤ 3 or clearly deteriorating. NOT required to be ≥ 7 to pass                |
| Disqualifier — accrual check                      | For non-financial companies, reject if the latest completed annual simplified Sloan accrual ratio `(net income - operating cash flow) / average total assets` is > +10%. Financial companies: `not applicable`. |
| Disqualifier — leverage cap                       | Reject if debt/EBITDA ≥ 3x                                                                                     |

A candidate must clear ROIC AND Gross Profitability AND the valuation
check to pass, and must not trip either disqualifier or the low F-Score
tripwire.

### Growth

| Criterion           | Rule                              |
|:--------------------|:----------------------------------|
| EPS growth          | 3–5 year EPS CAGR ≥ 15%; use the longest valid comparable span available |
| Revenue growth      | 3–5 year revenue CAGR ≥ 10%; use the longest valid comparable span available |
| Valuation guardrail | PEG ratio ≤ 1.5                   |

A candidate must clear all three.

### Momentum

| Criterion                                 | Rule                                                                                                                                                                                                                                                  |
|:------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Relative strength vs. S&P 500             | Top 30% of all stocks (RS rank ≥ 70)                                                                                                                                                                                                                  |
| 6-month price return                      | Top 30% of all stocks                                                                                                                                                                                                                                 |
| Trend confirmation                        | Requires a recent golden cross (50-day MA just crossed above 200-day)                                                                                                                                                                                 |
| Regime gate for NEW adds only             | Only add a new name if the S&P 500 itself is currently above its own 200-day moving average. If the broad market is below its 200-day average, do not add new Momentum names even if the ticker otherwise clears the screen — wait and re-check later |
| Crash-risk handling for existing holdings | Flag in the weekly summary if broad-market volatility looks elevated. Does NOT trigger removal of anything already on the list                                                                                                                        |

A candidate must clear RS rank AND 6-month return AND the golden cross
AND the regime gate to be newly added.

### Dividend Income

| Criterion                 | Rule                                                                                                                             |
|:--------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| Dividend yield            | ≥ 3%                                                                                                                             |
| Payout ratio (cash basis) | FCF payout ≤ 70% for regular companies; FFO/AFFO payout ≤ 90% for REITs; distributable-cash-flow payout ≤ 70% for midstream/BDCs |
| Yield-trap flag           | Anything above 8% yield is flagged as a likely trap requiring extra scrutiny — not an automatic pass, regardless of payout ratio |

A candidate must clear yield AND the correct sector-appropriate cash
payout ratio to pass. An 8%+ yield does not auto-fail, but must be
called out explicitly as a trap risk in the result.

## AI Shortlist — cross-style aggregator

No independent criteria of its own. A ticker only ever reaches AI
Shortlist by first clearing one of the five style tables above and
holding a spot on that style’s own watchlist — Shortlist never files a
name that hasn’t already earned one elsewhere.

**Ranking metric per style** (used only to pick which passers are “top,”
never to change who passes):

| Style              | Rank by (higher/better unless noted)                                                |
|:-------------------|:------------------------------------------------------------------------------------|
| Deep Value         | Discount to sector-average EV/EBITDA — bigger discount ranks higher                 |
| Quality Compounder | ROIC                                                                                |
| Growth             | Revenue growth rate; PEG (lower is better) breaks ties                              |
| Momentum           | RS rank, then 6-month return breaks ties                                            |
| Dividend Income    | Yield among names NOT flagged as a yield trap; lowest cash payout ratio breaks ties |

**Membership rule:** at every style-watchlist review pass (manual or the
weekly routine), after re-checking the five style lists, rank each
style’s currently-clearing tickers by that style’s metric above and take
the top 2. AI Shortlist’s membership is the union of those five top-2
sets (up to 10 tickers, fewer if a style has under 2 passers). A ticker
earns its spot via any style it’s top-2 in — being top-2 for two styles
at once still earns only one slot.

**Adds are automatic, removals are flagged only** — same asymmetry as
every style list above. A newly top-2 ticker is added via
`Webull:add_watchlist_instruments` (after the usual duplicate check) in
the same run that promotes it. A ticker that falls out of the top 2 for
every style it qualified through is flagged in the summary as `no longer top-ranked for [style]` — it is NOT removed automatically. Joshua decides whether to drop it
via `Webull:remove_watchlist_instruments`.

Watchlist ID: `73b222507bd84d3b84a16e14c0d2ed72`.

## AI Day Trade — manual-only liquidity/volatility screen

**Never part of the unattended weekly routine.** Intraday setups are
stale within hours; a Sunday-night batch re-check can’t track something
that trades on same-session volume and range. This screen and its
Discovery mode below only run when Joshua invokes them himself,
in-session.

| Criterion                                                  | Rule                                                                                                                       |
|:-----------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------|
| Price floor                                                | ≥ $5 — avoids penny-stock/manipulation-prone names                                                                        |
| Average dollar volume (20-day ADV × price)                 | ≥ $20M/day — ensures fills at day-trade size without excessive slippage                                                   |
| Relative volume (RVOL) — today’s volume vs. 20-day average | ≥ 1.5x — the actual same-session-interest trigger for a day-trade setup                                                    |
| Intraday volatility — 14-day ATR ÷ price                   | ≥ 3% — enough range to clear commissions/slippage and hit a meaningful target                                              |
| Float (shares outstanding available to trade)              | Flag, don’t disqualify, if < 20M shares — bigger gaps and reversals, tighter risk control needed, not a reason to exclude |

A candidate must clear the price floor AND ADV AND RVOL AND ATR% to
pass. A small float is a flag, not a disqualifier, in the result.

**No automated re-check exists for this list** (see above) — a ticker is
only re-evaluated when Joshua names it again. If RVOL and ATR% have both
fallen back toward baseline (RVOL < 1.2x, ATR% < 2%) on a re-check,
flag it as cooled off; removal is still Joshua’s manual call via
`Webull:remove_watchlist_instruments`, same as every other list.

Watchlist ID: `e1d3094ed02842d583034ee9a23f801e`.

### Day Trade discovery (manual-only)

Same sourcing exception as Candidate discovery below, scoped to this one
screen and never triggered by the weekly routine. Sourcing:
`Webull:get_gainers_losers` (`rank_type: DAY`, `sort_by: CHANGE_RATIO`
or `VOLUME`, `direction: DESC`) cross-checked against
`Webull:get_most_active` for the raw pool; `Webull:get_stock_quotes` /
`Webull:get_stock_snapshot` for current price and volume (the RVOL
numerator); `Webull:get_stock_bars` for the 14-day range needed to
compute ATR%. Pre-filter, cap at 10 survivors, pull real quote/bar data
for each, run the table above, file passers the same way as any other
discovery mode (duplicate check, then add). Report the full funnel — raw
pool size, pre-filtered-out count, evaluated count, pass/fail per
candidate, filed tickers — same as every other discovery report.

## Structural rules

- A ticker CAN land on more than one style watchlist if it independently
  clears more than one style’s criteria. Styles are not mutually
  exclusive and are each checked separately.
- Weekly review: if a ticker already on a style watchlist no longer
  clears that style’s criteria on re-check, flag it in the weekly
  summary — do NOT remove it automatically. Removal is always Joshua’s
  manual call.
- AI Shortlist is not an independent style — a ticker cannot land there
  without first clearing (and currently holding a spot on) one of the
  five style lists. See its own section above for the ranking/promotion
  mechanic.
- AI Day Trade is excluded from every unattended pass (weekly routine,
  style-watchlist review). It only runs when invoked directly — see its
  own section above.

## Steps

1.  **Get the candidate inputs.** For a named ticker, use values Joshua supplies or fetch exact values from an available named real source such as Webull, another broker/data provider, or a filing when the mode allows tool use. Never estimate, infer, or fill a missing fundamental from model knowledge. A value repeated only from a video, tip, or headline is `unverified` until confirmed against a real source. Also note how the candidate surfaced.

2.  **Run the general screen** (per `watchlist-screener-criteria`, if
    Joshua has one defined and wants it checked) and/or **run each of
    the five style screens above independently**, and/or **the Day Trade
    screen** if Joshua asked for it specifically, against the supplied
    values — whichever Joshua asked for. Produce a table per screen
    checked: each criterion, the supplied value, pass/fail, and the
    overall verdict. Don’t skip or compress this — it’s what makes the
    Webull action defensible later.

3.  **Check for an existing entry first** — for every watchlist a
    verdict would file the ticker into (or out of, per the
    resurfaced-ticker case below), call
    `Webull:get_watchlist_instruments` on that watchlist and confirm the
    ticker isn’t already sitting there before adding it. If it’s already
    on the target list, say so and skip the redundant add; a ticker
    landing on more than one style list in the same run needs this check
    per list, not once overall.

4.  **Route based on verdict(s):**

    | Result                                            | Action                                                                                           |
    |:--------------------------------------------------|:-------------------------------------------------------------------------------------------------|
    | General screen: `ADD TO WATCHLIST`                | Add to Screen Passed (`d478a39a042c4612aa3d57493121b3c1`)                                        |
    | General screen: `REJECT`                          | Add to Screen Rejected (`ffe8dc1df7344497b040f76ecf461d2f`)                                      |
    | Deep Value: clears all three                      | Add to AI Deep Value (`3157a89143694aefb8dba81fa50dcf33`)                                        |
    | Quality Compounder: clears all, no disqualifier   | Add to AI Quality Compounder (`4af991cc1719405686c10bef335e1e74`)                                |
    | Growth: clears all three                          | Add to AI Growth (`3a9ed36d4d71445f85534476c91abcd6`)                                            |
    | Momentum: clears all four (incl. regime gate)     | Add to AI Momentum (`115ceb562bf147c990effd9d1b6f6362`)                                          |
    | Dividend Income: clears yield + payout            | Add to AI Dividend Income (`1f248ceaf10b482d8375af7d4e3774c4`), flag separately if yield > 8%   |
    | Day Trade: clears price floor + ADV + RVOL + ATR% | Add to AI Day Trade (`e1d3094ed02842d583034ee9a23f801e`), flag separately if float < 20M shares |
    | Any screen: `INCOMPLETE` (missing values)         | No Webull action for that screen. Report exactly what’s missing.                                 |

    AI Shortlist has no row here — it is never filed to directly from a
    per-ticker screen. It is synced only through the style-watchlist
    review pass below.

    Use `Webull:add_watchlist_instruments` with `category: US_STOCK` and
    `symbols: [<TICKER>]` for each watchlist the ticker clears — a
    ticker can trigger multiple adds in the same run.

5.  **Confirm every action taken** — name each watchlist the ticker
    landed on (or didn’t) and why, so nothing is a silent side effect.

6.  **Resurfaced tickers:** before re-running a full screen on a ticker
    already on Screen Rejected or lacking a style pass, check via
    `Webull:get_watchlist_instruments` first. Per
    `watchlist-screener-criteria`’s rule, don’t re-litigate unless
    something material actually changed — say so directly if nothing
    has.

## Style-watchlist review pass

**Not the whole-account weekly review.** `weekly-portfolio-review` owns
the whole-account walk (positions vs. thesis, stops, options expiring,
earnings/ex-div calendar, allocation drift, watchlist names in range).
This pass only re-checks tickers already sitting on a style watchlist
against that style’s own criteria — a narrower, separate cadence.

AI Day Trade is never part of this pass — see its own section above. AI
Shortlist has no re-check of its own; it’s resynced as the final step
below from the five styles’ fresh results.

Manually triggered by Joshua, or via a Claude Cowork Scheduled Task set
up separately (Claude cannot self-schedule from this chat). For every
ticker currently on any of the five style watchlists:

1.  Re-pull current metric values from Webull for unattended runs. For manual runs, use Joshua-supplied values or an explicitly named source/tool.
2.  Re-run that ticker against its style’s table.
3.  If it still clears — no action needed.
4.  If it no longer clears — flag it in the summary with which criterion
    it now fails. Do NOT remove it from the watchlist. Joshua decides.
5.  For Momentum specifically, also report current S&P 500 vs. its
    200-day average, since that gates whether *new* adds are allowed
    this week (it does not affect existing holdings).
6.  Summarize: tickers flagged per style, tickers newly added this week
    (and which watchlists), any INCOMPLETE screens still pending data.
7.  **Sync AI Shortlist** from this run’s fresh per-style verdicts:
    recompute each style’s top 2 by its ranking metric (see the AI
    Shortlist section above), add any newly-promoted ticker, and flag —
    never remove — any ticker that fell out of every style’s top
    2.  

**The weekly unattended routine also runs Candidate discovery (below)
after this re-check pass**, one run per style, so the five watchlists
don’t stay empty between manual visits. Same 5-candidates-per-style cap,
same auto-file-on-pass behavior, same full-funnel report — nothing about
discovery loosens or shortcuts when it runs unattended instead of on
request. The Shortlist sync (step 7 above) also runs automatically as
part of the unattended routine, since it only reuses data the re-check
pass already pulled — no extra Webull calls beyond its own
add/duplicate-check. AI Day Trade discovery is never run by the
unattended routine — see its own section above.

## Candidate discovery

**Discovery and unattended review are Webull-sourced modes.** They source tickers and required values from Webull tools directly. Manual named-ticker screens may use Joshua-supplied values or exact values fetched from an explicitly named source. In every mode, missing fundamentals stay missing; never replace them with model knowledge or estimates.

Triggers: “find me some Growth candidates”, “run discovery for
Momentum”, “scan for new Deep Value names”, “the watchlists are empty,
find something”, or the weekly routine’s own discovery phase (below).
This section covers the five style lists only — Day Trade discovery has
its own section above and is never part of the weekly routine.

### Per-style candidate sourcing — honest about tool coverage

Webull’s scanners map cleanly onto three styles and only loosely onto
two. Don’t oversell the weaker two as equally rigorous:

| Style              | Scanner tool(s) used for the raw candidate pool                                                                                                                                                      | Coverage                                                                                                                                                                                                                                         |
|:-------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Dividend Income    | `Webull:get_high_dividend`, sorted by `YIELD`                                                                                                                                                        | **Strong** — near-direct match to the yield criterion                                                                                                                                                                                            |
| Growth             | `Webull:get_gainers_losers` (`rank_type: MONTH_3` or `MONTH_1`, `sort_by: CHANGE_RATIO`, `direction: DESC`)                                                                                          | **Strong** — price momentum as a growth proxy, verified against real EPS/revenue growth after                                                                                                                                                    |
| Momentum           | `Webull:get_gainers_losers` (`rank_type: MONTH_1` or `WEEK_52`, `sort_by: CHANGE_RATIO`) cross-checked against `Webull:get_most_active` for liquidity                                                | **Strong** — this style’s own criteria (RS rank, 6-month return, golden cross) are themselves price-momentum measures                                                                                                                            |
| Deep Value         | `Webull:get_market_sectors_detail`, sorted by `PE_TTM` ascending, sampled across the **selected rotating sector batch** from `Webull:get_market_sectors` (see cross-sector requirement below)        | **Weak proxy** — Webull has no EV/EBITDA or FCF-yield screener; a low trailing P/E is a rough stand-in, not the actual valuation metric this style uses. Lean harder on the real financial-data verification step below; expect a lower hit rate |
| Quality Compounder | `Webull:get_market_sectors_detail`, sorted by `MARKET_VALUE` descending, sampled across the **selected rotating sector batch** from `Webull:get_market_sectors` (see cross-sector requirement below) | **Weak proxy** — no ROIC or gross-profitability screener exists; this only produces a plausible-quality universe, the real criteria table does the actual filtering                                                                              |

**Rotating cross-sector requirement for Deep Value and Quality
Compounder — the only two styles that source from sectors.** The
objective remains market-wide discovery: never narrow the candidate pool
to AI, technology, software, or semiconductors merely because those
sectors are large or because the watchlist names begin with “AI.”

For unattended runs, do **not** query every sector in the same run. That
can exhaust the available Webull tool-call budget before candidates
receive full financial verification. Instead:

1.  Call `Webull:get_market_sectors` **once** to obtain the full sector
    universe.
2.  Sort the returned sectors deterministically by stable sector ID
    ascending.
3.  Partition that ordered universe into sequential batches of **9
    sectors**. The final batch may contain fewer than 9.
4.  Let `batch_count = ceil(total_sectors / 9)`.
5.  Select the unattended run’s batch statelessly with
    `batch_index = ISO_week_number modulo batch_count`, using zero-based
    indexing.
6.  Use the **same selected sector batch** for Deep Value and Quality
    Compounder.
7.  Over successive weeks, this rotation covers the full sector universe
    before repeating when the sector universe and batch count remain
    unchanged.

The ISO-week rule is deliberately stateless: an unattended run does not
need memory of the previous week’s batch, and a missed or failed run
does not corrupt rotation state.

For each selected sector, pull approximately **2 raw candidates per
style per sector**: Deep Value prioritizes `PE_TTM` ascending as its
discovery proxy; Quality Compounder prioritizes `MARKET_VALUE`
descending. If one sector-detail response contains enough
information/orderings to derive both candidate sets, reuse it. Otherwise
make the minimum additional sector-detail call required.

Preserve cross-sector representation when reducing the raw pool. Do not
globally sort the combined pool and truncate it in a way that allows one
sector to dominate. The rotating batch changes only candidate sourcing;
**the committed Deep Value and Quality Compounder criteria and
thresholds remain unchanged**.

Manual discovery may still scan a broader sector universe when Joshua
explicitly requests it and the available tool budget supports it. The
unattended routine defaults to the rotating batch process above.

### Steps

1.  **Pull a raw candidate pool per style requested.** For unattended
    all-style runs, process discovery in this order: **Dividend Income →
    Growth → Momentum → Deep Value → Quality Compounder**. Dividend,
    Growth, and Momentum use the scanner calls in the table above. Deep
    Value and Quality Compounder use the rotating sector batch above. If
    Joshua manually requests only one style, run only that style.

2.  **Pre-filter before spending real financial-data calls:**

    - Fetch the relevant watchlist memberships once near the start of
      the run and cache them for filtering. Re-fetch a target watchlist
      immediately before an allowed add so the duplicate check is still
      current.
    - Maintain an `evaluated_this_run` set across style discovery
      passes. Drop any ticker already evaluated for another style’s
      discovery pass in the same run.
    - Drop any ticker already on that style’s watchlist or on Screen
      Rejected.
    - Drop anything below a basic liquidity floor (near-zero volume, a
      penny-stock price). This is a sanity filter, not a replacement for
      the style’s committed table.
    - Cap **full financial evaluation at 5 candidates per style per
      run**. This is a maximum, not a target that requires extra calls
      after the plausible discovery pool is exhausted.
    - For Deep Value and Quality Compounder, preserve cross-sector
      representation when selecting those survivors rather than globally
      sorting the combined raw pool.
    - Do not pull financial statements for candidates eliminated by the
      pre-filter.

3.  **Pull real financials for each survivor** via Webull’s data tools
    (`get_financial_indicators`, `get_income_statement`,
    `get_balance_sheet`, `get_cash_flow`, `get_stock_quotes`,
    `get_52_week_high_low`, `get_stock_bars_single`, or similar) —
    fetched, never estimated or reasoned out. A value that genuinely
    isn’t available is `data not available`, not a guess.

4.  **Run each survivor through its style’s criteria table** exactly as
    written above — same bar as a user-named candidate, no loosened
    threshold because it came from a scan.

5.  **File passers** using the same duplicate-check-then-add steps as
    the main flow (Steps 3–4 above): confirm not already present, then
    `Webull:add_watchlist_instruments` into that style’s watchlist.

6.  **Report the whole funnel, not just the winners** — raw pool size,
    how many were pre-filtered out and why, how many got full financials
    pulled, pass/fail per evaluated candidate with the failing criterion
    named, and which were filed. A discovery run that found nothing is a
    valid, reportable outcome — don’t pad it.

A request to skip the financials pull, or file a survivor before it’s
actually run through the criteria table, is the same class of override
as loosening a threshold — it doesn’t get a pass because the candidate
came from a scan instead of Joshua. “Just add the first one that looks
decent” is a reason to want Steps 3–4 skipped, not a release of them.

## Unattended call-efficiency rules

These rules optimize connector usage only; they do **not** change a
screen’s pass/fail bar.

- Reuse market, sector, quote, bar, and financial data already fetched
  during the same run instead of calling Webull again for the same
  ticker/sector/period.
- Fetch style-watchlist memberships and Screen Rejected once near the
  start and cache them for filtering. Immediately before an allowed add,
  re-check the target watchlist with `Webull:get_watchlist_instruments`;
  skip the add if the ticker is already present.
- Stop evaluating a candidate once a required hard criterion
  definitively fails unless another field is needed to produce the
  required report.
- Prefer a combined financial-indicator or statement response when it
  supplies multiple required metrics.
- Never infer a missing fundamental. Record `data not available`; a
  required unavailable value prevents a pass.
- Candidate discovery order for an unattended all-style run is Dividend
  Income, Growth, Momentum, Deep Value, then Quality Compounder so the
  shared `evaluated_this_run` set can eliminate duplicate work before
  the sector-based screens.
- The 5-candidate-per-style evaluation cap remains unchanged.

## Metric derivation contract for unattended runs

This contract applies before declaring a required metric
`data not available`. Use **Webull-sourced data only**. Never use model
memory, web estimates, analyst-site values, or guessed substitutes.
Reuse same-run data. Prefer `get_financial_indicators` when it directly
exposes the exact required metric; otherwise fetch only the necessary
`get_income_statement`, `get_balance_sheet`, `get_cash_flow`,
`get_company_profile`, market/sector payload, or price bars.

### Period alignment

- Use the latest completed **ANNUAL** fiscal period for fundamental
  tests, unless the style explicitly requires current market data.
- Match income statement, balance sheet, and cash flow by fiscal
  year/end date.
- For multi-year growth, use comparable annual periods and prefer the
  longest valid span from 3–5 years.
- Do not mix currencies inside an absolute-value company or peer
  calculation. Ratio-based peer metrics are acceptable when each ratio
  is internally same-currency.
- Webull commonly reports capex as a negative cash-flow value. Use
  `ABS(capex)` in the formulas below.

### Deterministic formulas

- Revenue CAGR = `(latest revenue / revenue N years earlier)^(1/N) - 1`,
  where N is 3, 4, or 5 and both endpoints are positive/comparable.
- EPS CAGR =
  `(latest diluted EPS / diluted EPS N years earlier)^(1/N) - 1` only
  when both endpoint EPS values are positive. If either endpoint is
  `<= 0`, do not manufacture a CAGR.
- PEG = current Webull P/E divided by EPS growth expressed as a
  whole-number percent, e.g. P/E 30 / growth 20 = PEG 1.5.
- Current ratio = `total_cur_assets / total_cur_liab`.
- Net current assets = `total_cur_assets - total_cur_liab`.
- Long-term debt = prefer `lt_debt`; do not substitute total debt.
- FCF = `CFO - ABS(capex)`.
- FCF yield = `FCF / current market capitalization`.
- EBIT = operating income (`op_income` or exact equivalent).
- EBITDA = `EBIT + D&A`, using same-period D&A. Never substitute CFO.
- Enterprise value = `market cap + total debt - cash_st_invest`. If
  `cash_st_invest` is unavailable, use `cash_equiv + st_invest` only
  when both exact fields exist.
- EV/EBITDA = `EV / EBITDA`, only when EBITDA > 0.
- EV/EBIT = `EV / EBIT`, only when EBIT > 0.
- EV/FCF = `EV / FCF`, only when FCF > 0.
- Debt/EBITDA = `total debt / EBITDA`, only when EBITDA > 0.
- Gross-profit/assets = `gross_profit / total_assets`.
- Capex/sales = `ABS(capex) / revenue`.

Current market cap should come from an exact Webull market/sector
payload or another exact Webull field. Only derive shares × price when
both values are current Webull values from the same run and no direct
market-cap value is available.

### Deep Value peer rules

Use the candidate’s exact Webull sector/industry. Exclude the candidate
from its peer comparison set. Use only peers with the exact inputs
required for a metric.

- Sector-average EV/EBITDA = arithmetic mean of valid peer EV/EBITDA.
- Sector-median capex/sales = median of valid peer capex/sales.
- FCF valuation must be like-for-like: company FCF yield vs peer
  FCF-yield average/distribution, or company EV/FCF vs peer EV/FCF
  average/distribution.
- `Favorable vs sector` means higher FCF yield than sector average, or
  lower EV/FCF than sector average.
- If peer coverage is too sparse to represent the sector defensibly, use
  `data not available`; never substitute PE_TTM for an EV metric.
- Balance-sheet gate remains exact: current ratio >= 2 **and**
  long-term debt <= net current assets.

### Quality derivation rules

ROIC must never be replaced by ROE or ROA. Derive only as:

- NOPAT = `EBIT * (1 - effective tax rate)`.
- Effective tax rate = `income_tax / EBT` when EBT > 0 and the
  resulting tax rate is between 0 and 1.
- Invested capital =
  `total debt + total shareholder equity - cash_st_invest`.
- Average invested capital = average of current- and prior-year invested
  capital.
- ROIC = `NOPAT / average invested capital`.

If any component is unavailable or the tax rate is invalid, ROIC is
`data not available`.

For gross-profit/assets top-30%, calculate the ratio for the candidate
and valid peers in the same Webull peer set and rank descending. Pass
only if the candidate is unambiguously in the top 30%; sparse peer
coverage means `data not available`.

For Quality’s valuation check, favorable means EV/EBIT below sector
average or FCF yield above sector average.

Piotroski F-score may be derived only when all nine standard components
can be computed from exact Webull annual statements: positive ROA;
positive CFO; ROA improvement; CFO > net income; lower
long-term-debt/assets; higher current ratio; no increase in shares
outstanding; higher gross margin; higher asset turnover. Score one point
each. If any component is unavailable, do not create a partial F-score.
Exact F-score <= 3 disqualifies.

For non-financial companies, derive the simplified Sloan accrual ratio
from the latest completed annual fiscal year:

`(net income - operating cash flow) / average total assets`

where average total assets is the average of current- and prior-year
total assets. A ratio **> +10%** is a Quality disqualifier; a ratio
`<= +10%` clears this sub-test. Financial companies (including banks and
insurers) are `not applicable` for this test rather than pass/fail. If
net income, operating cash flow, or either annual total-assets input is
unavailable, report `data not available`; do not substitute an alert,
proxy, or different accrual formula.

### Dividend payout rules

Classify the candidate using Webull company-profile/industry data.

- Regular company: use an exact Webull cash-dividend payout ratio when
  available; otherwise derive only from exact total common cash
  dividends and the appropriate committed numerator.
- REIT: require Webull FFO/AFFO plus distributions. Never substitute EPS
  payout.
- Midstream/BDC: require Webull distributable cash flow plus
  distributions. Never substitute CFO or EPS payout.
- Missing category-specific numerator => `data not available`.
- Yield > 8% is a yield-trap scrutiny flag, not an automatic failure if
  the appropriate payout test clears.

### Momentum derivation rules

Use consistent completed Webull daily bars.

- Six-month return = latest completed close divided by the close
  approximately six calendar months earlier (nearest prior trading
  session), minus 1.
- 50DMA and 200DMA are simple averages of the latest 50/200 completed
  daily closes.
- A recent golden cross requires evidence in fetched history that 50DMA
  moved from `<= 200DMA` to `> 200DMA`. Merely being above the 200DMA is
  not enough.
- RS rank >= 70/top 30% and six-month-return top 30% are
  cross-sectional. Use a Webull-sourced comparison universe from the
  discovery/ranking universe. If the universe is too narrow to establish
  the percentile defensibly, use `data not available`; never infer
  percentile from absolute return.
- S&P 500 regime uses SPY: latest completed close > its 200DMA.

For every derived value, the unattended report should identify it as
`derived from Webull statements`, include the formula result/fiscal
period, and report peer sample size for peer-relative tests.

## Progressive retrieval / early-exit execution contract

This execution contract changes call order only. It does **not** change
any criterion, threshold, ranking rule, or watchlist-write restriction.

### Global rule

Never prefetch every statement for every ticker. Start with the
cheapest, highest-yield endpoint needed for that style. Fetch another
endpoint only when the ticker can still pass and the next unresolved
criterion requires it. Cache every response for the full run and reuse
it across styles, peer calculations, and Shortlist ranking.

The moment a required hard criterion definitively fails, stop candidate-
specific retrieval unless one already-cheap value is needed for the
report. `data not available` is not permission to substitute another
metric.

Every existing ticker on the five style watchlists must still be
reviewed before discovery. If connector limits prevent completion of
that existing-list review, stop before discovery, make no
discovery-based additions, and report where the run stopped.

### Growth pipeline

1.  Fetch ANNUAL income statement, count 5.
2.  Derive longest valid 3–5y revenue CAGR and EPS CAGR.
3.  Revenue CAGR < 10% or valid EPS CAGR < 15% => immediate FAIL; do
    not fetch PEG inputs.
4.  If EPS CAGR is unavailable because positive endpoints do not exist,
    mark that criterion unavailable and stop unless cached financial
    indicators directly resolve it.
5.  Only when both growth hurdles pass, fetch/reuse financial indicators
    for current Webull P/E. If P/E is absent there, check cached Webull
    market, ranking, or sector-detail payloads for an exact current
    `pe_ttm` value before making another call. If no cached payload
    contains P/E, make at most one cheap Webull market/valuation request
    capable of returning current P/E. Derive PEG only from an exact
    Webull P/E and the valid EPS CAGR. PEG must be <= 1.5. If P/E remains
    unavailable after that fallback, PEG=`data not available` and stop.
6.  Do not fetch balance sheet, cash flow, or profile for Growth unless
    already cached for another reason.

### Dividend pipeline

1.  Use cached discovery/current Webull yield first. Yield < 3% =>
    immediate FAIL.
2.  Fetch/reuse company profile only when classification is not already
    known.
3.  Yield > 8% => attach yield-trap scrutiny flag and continue.
4.  Check financial indicators first for the exact category-appropriate
    payout metric.
5.  Regular companies: if an exact cash payout metric is not directly
    available, fetch only the statement(s) required to derive the
    committed cash payout ratio.
6.  REITs: require exact Webull FFO/AFFO plus distributions. Once the
    relevant Webull financial data establish that FFO/AFFO is not
    exposed, do not fetch unrelated income, balance-sheet, or cash-flow
    statements in an attempt to substitute another numerator. Mark the
    payout criterion `data not available` and stop.
7.  Midstream/BDCs: require exact Webull distributable cash flow plus
    distributions. Once the relevant Webull financial data establish
    that DCF is not exposed, do not fetch unrelated statements or
    substitute CFO, EPS, or net investment income. Mark the payout
    criterion `data not available` and stop.

### Deep Value pipeline

1.  Fetch ANNUAL balance sheet, count 2.
2.  Derive current ratio, net current assets, and long-term debt.
3.  Current ratio < 2 or long-term debt > net current assets =>
    immediate FAIL; do not fetch income/cash flow/peer valuation data.
4.  Only survivors fetch/reuse annual income statement + cash flow for
    EBITDA, FCF, and capex/sales.
5.  Reuse cached current market cap when possible.
6.  If company EV/EBITDA or FCF valuation is unavailable/nonpositive
    where the screen requires a valid value, stop before peer expansion.
7.  Only survivors trigger incremental peer-relative work. Reuse
    sector-detail payloads and stop peer expansion once the comparison
    is unambiguous or cannot become defensible within available Webull
    data/call budget.

### Quality pipeline

1.  Fetch/reuse ANNUAL income statement + balance sheet, count 2. Before
    declaring a prior-period input unavailable, verify that the response
    contains the required number of distinct comparable fiscal years.
    If duplicate currency/reporting representations cause count 2 to
    return only one distinct fiscal year, make one adaptive escalation
    to count 3 and, only if still necessary, count 4. Deduplicate by
    symbol + fiscal year + end date and use one consistent reporting
    currency for absolute-value calculations. Fetch cash flow only when
    needed for CFO, D&A, F-score, FCF, or Sloan review.
2.  Derive ROIC. ROIC < 15% => immediate FAIL; do not perform peer
    ranking or valuation.
3.  Derive debt/EBITDA as soon as inputs exist. Debt/EBITDA >= 3x =>
    immediate FAIL.
4.  Derive Piotroski F-score only when all nine components are
    available. F-score <= 3 => immediate FAIL. Never partial-score.
5.  For non-financial companies still capable of passing, derive the
    latest-fiscal-year simplified Sloan accrual ratio from annual net
    income, operating cash flow, and current/prior total assets. Ratio
    > +10% => immediate FAIL. Financial companies are `not applicable`.
    Do not call `get_financial_alert` as a substitute for this formula.
6.  Finish the company-level gates for all existing Quality names before
    starting expensive peer expansion. Group surviving names by Webull
    sector/industry and build each peer universe once per sector, not once
    per ticker. Reuse the same peer set for every surviving existing name
    in that sector.
7.  Only after ROIC and hard disqualifiers clear, perform
    gross-profit/assets peer ranking and sector-relative EV/EBIT or
    FCF-yield valuation. Expand peer statements incrementally. Stop peer
    expansion as soon as the candidate's top-30% ranking or valuation
    comparison is unambiguous, or as soon as the available Webull data
    cannot become defensible within the call budget. Report peer sample
    size for each resolved or unresolved comparison.

### Momentum pipeline

1.  Fetch/reuse SPY bars once per run and calculate the market 200DMA
    regime once.
2.  If SPY is not above its 200DMA, no new Momentum candidate can pass.
    Skip candidate-specific bar calls for new adds. Existing Momentum
    retention remains independent of this broad-market gate.
3.  Use discovery ranking payloads first. If the Webull universe cannot
    support the mandatory top-30% cross-sectional tests, mark them
    unavailable; do not fetch bars to replace a missing percentile.
4.  Only candidates clearing the cross-sectional tests receive enough
    daily bars for 200DMA plus cross history.
5.  No recent golden cross => immediate FAIL.

### Call-budget safety and peer sharing

- Maintain a sector cache keyed by Webull sector ID and a statement
  cache keyed by symbol + period + endpoint. Treat duplicate annual
  rows that represent the same fiscal year/end date in different
  currencies as one fiscal period for period-count purposes.
- Complete company-level Quality gates across existing names first, then
  group surviving names by sector and perform peer work sector-by-sector
  so a peer universe is constructed once and reused across all relevant
  survivors.
- If a peer was fetched for Deep Value, reuse it for Quality and vice
  versa. Prefer peers whose market cap, P/E, and sector metadata are
  already present in cached sector-detail payloads before issuing new
  statement calls.
- The 5-new-candidates-per-style cap applies to candidate full
  evaluations, not supporting peer calculations.
- If connector limits are approached, **stop rather than weaken
  criteria**. Finish mandatory existing-list review if possible;
  otherwise stop before discovery. During discovery, complete styles in
  the committed order and stop before starting the next style if needed.
- Never promote a partially evaluated ticker and never add a ticker with
  a required `data not available` criterion.
- Report an `early-exit reason` and concise endpoints used for every
  evaluated ticker so call savings are auditable.
- Do not begin the rotating 9-sector Deep Value/Quality discovery batch
  until every mandatory existing-list review has completed. Once
  discovery begins, calculate the actual ISO week at run time, select the
  committed 9-sector batch, cache its constituent payloads once, and use
  that same selected batch for both Deep Value and Quality.

## Unattended report additions

For Deep Value and Quality Compounder, report all of the following in
addition to the existing full discovery funnel:

- total Webull sector-universe size;
- selected batch number, human-readable as 1..N;
- the ISO week number used to select the batch;
- names of sectors scanned this run;
- `sectors scanned this run: X / total`;
- total rotation batch count and expected full-rotation length in weeks.

Do not claim historical cumulative coverage unless it can be derived
reliably from the current unchanged sector universe. Report the
deterministic current batch and expected rotation length instead.

## Unattended write authority

The unattended weekly routine may write only to the five AI style watchlists and AI Shortlist, and only by adding a ticker after a fresh duplicate check. It must never write to **Screen Passed**, **Screen Rejected**, or **AI Day Trade**. It must never remove a ticker, create/delete/rename a watchlist, or place/change/cancel an order. Existing names that fail or become incomplete are report-only flags. Every unattended report ends with `Removed: none`.

## What this does not do

- Does not define, loosen, or reinterpret any criterion — see the
  Define-mode note at the top, and note discovery evaluates candidates
  against the same tables, not a looser bar.
- Does not invent, estimate, or silently substitute missing metric
  values. For a user-named screen, use values Joshua supplies or fetch
  the required values from an available named/connected source such as
  Webull. Missing required data remains `data not available`; sourcing
  data never loosens the pass bar.
- Does not size, price, or execute a trade on any passed name.
- Does not write the thesis for a passed name
  (`equity-research-writeup`).
- Does not backtest a filed candidate — that’s
  `strategy-backtest-design`, once a specific entry/exit rule is named.
- Does not remove a name from any watchlist automatically — every
  removal is a manual `Webull:remove_watchlist_instruments` call after
  Joshua confirms.
- Does not give AI Shortlist independent criteria — every member must
  already be clearing (and holding a spot on) a style list; see its own
  section above.
- Does not run AI Day Trade screening or discovery unattended —
  manual-only, invoked in-session, never part of the weekly routine.