---
name: watchlist-screen-sync
description: |-
  Run a candidate ticker through the user's committed watchlist screens and file the result into the matching Webull watchlist(s), OR discover new candidates itself via Webull's market-scan tools when a style watchlist is empty or thin. General screen routes to Screen Passed/Rejected; five style screens (Deep Value, Quality Compounder, Growth, Momentum, Dividend Income) each route to their own "AI [Style]" watchlist — a ticker can land on several. Use for "screen TICKER", "does TICKER pass, add it", "find me some [style] candidates", "run discovery", "run the style screens", "run the style-watchlist review". Discovery is the one case here where Claude sources tickers and fetches their values itself — every user-named screen still requires the user's own sourced values. Not the whole-account weekly walk — that's `weekly-portfolio-review`. Not for changing the criteria (needs sign-off), sizing/entering a trade (`equity-trade-decision`), or the full thesis writeup (`equity-research-writeup`).
---

# Watchlist Screen Sync

Bridges Joshua's committed screening criteria (general + five styles) with
his actual Webull watchlists, so a ticker that clears a screen shows up
somewhere real instead of just getting typed into a chat response he has to
remember to act on. A ticker that fails still gets logged, not silently
dropped, so it can be checked against "already screened" before being
re-litigated.

**This skill does not replace any downstream gate.** Landing on any watchlist
— general or style-specific — is not a buy signal. `equity-research-writeup`
still owns the thesis, `equity-trade-decision` still owns sizing and entry.
This skill only automates the filing step.

**This skill does not define or loosen the criteria.** The thresholds below
were committed by Joshua after an initial pass and a subsequent expert-
literature audit he explicitly approved. Don't adjust a number, add a
metric, or relax a disqualifier because a candidate is "close" or because it
seems reasonable in the moment — that's a Define-mode change, and it
requires Joshua's explicit sign-off in conversation, the same bar as any
other screen edit.

## Webull watchlist IDs

| Watchlist | ID |
|---|---|
| Screen Passed | `d478a39a042c4612aa3d57493121b3c1` |
| Screen Rejected | `ffe8dc1df7344497b040f76ecf461d2f` |
| AI Deep Value | `3157a89143694aefb8dba81fa50dcf33` |
| AI Quality Compounder | `4af991cc1719405686c10bef335e1e74` |
| AI Growth | `3a9ed36d4d71445f85534476c91abcd6` |
| AI Momentum | `115ceb562bf147c990effd9d1b6f6362` |
| AI Dividend Income | `1f248ceaf10b482d8375af7d4e3774c4` |

Specific to Joshua's Webull account. If copied to
another account, these IDs won't resolve — call `Webull:get_watchlists` to
find or recreate equivalents and update this table.

**"AI" in each name is a list-ownership marker, not a sector filter.** It means "Claude
created and files into this list" — nothing more. These watchlists are NOT scoped to AI or
tech companies; every style screen applies market-wide, across every sector, exactly as it
would for a healthcare, industrial, financial, energy, or consumer name. Never narrow
discovery's candidate pool to AI/tech/semiconductor names because of the list name — see the
cross-sector sampling requirement in Candidate discovery below.

## The five committed style screens

### Deep Value

| Criterion | Rule |
|---|---|
| Valuation metric | EV/EBITDA, judged relative to the company's own sector average (no fixed absolute number) |
| Cash-flow cross-check | EV/FCF or FCF yield, also judged relative to sector — required especially when the candidate is capital-intensive (capex/sales materially above its sector median) |
| Safety filter | Current ratio ≥ 2, AND long-term debt ≤ net current assets (Graham's classic check) |

A candidate must clear EV/EBITDA AND the FCF cross-check AND the safety
filter to pass.

### Quality Compounder

| Criterion | Rule |
|---|---|
| ROIC | ≥ 15% |
| Gross Profitability (gross profit ÷ total assets) | Top 30% of its industry peers |
| Valuation check | Sector-relative EV/EBIT or FCF yield |
| Piotroski F-Score | Disqualifier only — reject/flag if ≤ 3 or clearly deteriorating. NOT required to be ≥ 7 to pass |
| Disqualifier — accrual check | Reject if reported profit is significantly higher than actual operating cash flow (Sloan-ratio-style red flag) |
| Disqualifier — leverage cap | Reject if debt/EBITDA ≥ 3x |

A candidate must clear ROIC AND Gross Profitability AND the valuation check
to pass, and must not trip either disqualifier or the low F-Score tripwire.

### Growth

| Criterion | Rule |
|---|---|
| Annual EPS growth | ≥ 15% per year (3–5 year average) |
| Revenue growth | ≥ 10% per year |
| Valuation guardrail | PEG ratio ≤ 1.5 |

A candidate must clear all three.

### Momentum

| Criterion | Rule |
|---|---|
| Relative strength vs. S&P 500 | Top 30% of all stocks (RS rank ≥ 70) |
| 6-month price return | Top 30% of all stocks |
| Trend confirmation | Requires a recent golden cross (50-day MA just crossed above 200-day) |
| Regime gate for NEW adds only | Only add a new name if the S&P 500 itself is currently above its own 200-day moving average. If the broad market is below its 200-day average, do not add new Momentum names even if the ticker otherwise clears the screen — wait and re-check later |
| Crash-risk handling for existing holdings | Flag in the weekly summary if broad-market volatility looks elevated. Does NOT trigger removal of anything already on the list |

A candidate must clear RS rank AND 6-month return AND the golden cross AND
the regime gate to be newly added.

### Dividend Income

| Criterion | Rule |
|---|---|
| Dividend yield | ≥ 3% |
| Payout ratio (cash basis) | FCF payout ≤ 70% for regular companies; FFO/AFFO payout ≤ 90% for REITs; distributable-cash-flow payout ≤ 70% for midstream/BDCs |
| Yield-trap flag | Anything above 8% yield is flagged as a likely trap requiring extra scrutiny — not an automatic pass, regardless of payout ratio |

A candidate must clear yield AND the correct sector-appropriate cash payout
ratio to pass. An 8%+ yield does not auto-fail, but must be called out
explicitly as a trap risk in the result.

## Structural rules

- A ticker CAN land on more than one style watchlist if it independently
  clears more than one style's criteria. Styles are not mutually exclusive
  and are each checked separately.
- Position-sizing note: this account caps every position at one share by its
  existing collecting pattern, so multi-style tagging doesn't currently
  create dollar-level concentration risk. If that pattern ever changes,
  revisit whether an exposure cap independent of tag count is needed.
- Weekly review: if a ticker already on a style watchlist no longer clears
  that style's criteria on re-check, flag it in the weekly summary — do NOT
  remove it automatically. Removal is always Joshua's manual call.

## Steps

1. **Get the candidate inputs.** The ticker, plus each metric's value from a
   named real source (broker, data provider, filing) — never fetched,
   estimated, or reasoned out by Claude. A missing value is
   `not supplied — get it from <source>`. A value merely repeated from a
   video, tip, or headline — with no broker/data-provider/filing behind it —
   is not a named real source either; flag it
   `unverified — confirm against a real source before filing` rather than
   running it as if sourced. This matters more here than in chat-only Screen
   mode, because a pass here writes to a real, persistent watchlist. Also
   note how the candidate surfaced (screen run, video, tip, headline).

2. **Run the general screen** (per `watchlist-screener-criteria`, if Joshua
   has one defined and wants it checked) and/or **run each of the five style
   screens above independently** against the supplied values — whichever
   Joshua asked for. Produce a table per screen checked: each criterion, the
   supplied value, pass/fail, and the overall verdict. Don't skip or
   compress this — it's what makes the Webull action defensible later.

3. **Check for an existing entry first** — for every watchlist a verdict would file the
   ticker into (or out of, per the resurfaced-ticker case below), call
   `Webull:get_watchlist_instruments` on that watchlist and confirm the ticker isn't already
   sitting there before adding it. If it's already on the target list, say so and skip the
   redundant add; a ticker landing on more than one style list in the same run needs this
   check per list, not once overall.

4. **Route based on verdict(s):**

   | Result | Action |
   |---|---|
   | General screen: `ADD TO WATCHLIST` | Add to Screen Passed (`d478a39a042c4612aa3d57493121b3c1`) |
   | General screen: `REJECT` | Add to Screen Rejected (`ffe8dc1df7344497b040f76ecf461d2f`) |
   | Deep Value: clears all three | Add to AI Deep Value (`3157a89143694aefb8dba81fa50dcf33`) |
   | Quality Compounder: clears all, no disqualifier | Add to AI Quality Compounder (`4af991cc1719405686c10bef335e1e74`) |
   | Growth: clears all three | Add to AI Growth (`3a9ed36d4d71445f85534476c91abcd6`) |
   | Momentum: clears all four (incl. regime gate) | Add to AI Momentum (`115ceb562bf147c990effd9d1b6f6362`) |
   | Dividend Income: clears yield + payout | Add to AI Dividend Income (`1f248ceaf10b482d8375af7d4e3774c4`), flag separately if yield > 8% |
   | Any screen: `INCOMPLETE` (missing values) | No Webull action for that screen. Report exactly what's missing. |

   Use `Webull:add_watchlist_instruments` with `category: US_STOCK` and
   `symbols: [<TICKER>]` for each watchlist the ticker clears — a ticker can
   trigger multiple adds in the same run.

5. **Confirm every action taken** — name each watchlist the ticker landed
   on (or didn't) and why, so nothing is a silent side effect.

6. **Resurfaced tickers:** before re-running a full screen on a ticker
   already on Screen Rejected or lacking a style pass, check via
   `Webull:get_watchlist_instruments` first. Per `watchlist-screener-criteria`'s
   rule, don't re-litigate unless something material actually changed —
   say so directly if nothing has.

## Style-watchlist review pass

**Not the whole-account weekly review.** `weekly-portfolio-review` owns the whole-account
walk (positions vs. thesis, stops, options expiring, earnings/ex-div calendar, allocation
drift, watchlist names in range). This pass only re-checks tickers already sitting on a style
watchlist against that style's own criteria — a narrower, separate cadence.

Manually triggered by Joshua, or via a Claude Cowork Scheduled Task set up
separately (Claude cannot self-schedule from this chat). For every ticker
currently on any of the five style watchlists:

1. Re-pull current metric values (Joshua supplies, or confirms the source to
   check).
2. Re-run that ticker against its style's table.
3. If it still clears — no action needed.
4. If it no longer clears — flag it in the summary with which criterion it
   now fails. Do NOT remove it from the watchlist. Joshua decides.
5. For Momentum specifically, also report current S&P 500 vs. its 200-day
   average, since that gates whether *new* adds are allowed this week (it
   does not affect existing holdings).
6. Summarize: tickers flagged per style, tickers newly added this week (and
   which watchlists), any INCOMPLETE screens still pending data.

**The weekly unattended routine also runs Candidate discovery (below) after this re-check
pass**, one run per style, so the five watchlists don't stay empty between manual visits.
Same 10-candidates-per-style cap, same auto-file-on-pass behavior, same full-funnel report —
nothing about discovery loosens or shortcuts when it runs unattended instead of on request.

## Candidate discovery

**The one exception to "Joshua supplies the values."** Every other mode above assumes a
ticker already exists to screen — the whole catalog's house rule ("Claude does not fetch,
look up, or estimate a company's fundamentals," per `watchlist-screener-criteria`) exists to
stop Claude replacing Joshua's own sourcing. Discovery is different: there is no candidate to
bring yet, so this mode sources tickers from Webull's own real market-scan tools and fetches
their financials itself — the same real-data-not-memory standard the weekly review pass
already uses unattended, just run on demand instead of on a schedule.

Triggers: "find me some Growth candidates", "run discovery for Momentum", "scan for new Deep
Value names", "the watchlists are empty, find something", or the weekly routine's own
discovery phase (below).

### Per-style candidate sourcing — honest about tool coverage

Webull's scanners map cleanly onto three styles and only loosely onto two. Don't oversell the
weaker two as equally rigorous:

| Style | Scanner tool(s) used for the raw candidate pool | Coverage |
|---|---|---|
| Dividend Income | `Webull:get_high_dividend`, sorted by `YIELD` | **Strong** — near-direct match to the yield criterion |
| Growth | `Webull:get_gainers_losers` (`rank_type: MONTH_3` or `MONTH_1`, `sort_by: CHANGE_RATIO`, `direction: DESC`) | **Strong** — price momentum as a growth proxy, verified against real EPS/revenue growth after |
| Momentum | `Webull:get_gainers_losers` (`rank_type: MONTH_1` or `WEEK_52`, `sort_by: CHANGE_RATIO`) cross-checked against `Webull:get_most_active` for liquidity | **Strong** — this style's own criteria (RS rank, 6-month return, golden cross) are themselves price-momentum measures |
| Deep Value | `Webull:get_market_sectors_detail`, sorted by `PE_TTM` ascending, sampled across **every** sector `Webull:get_market_sectors` returns (see cross-sector requirement below) | **Weak proxy** — Webull has no EV/EBITDA or FCF-yield screener; a low trailing P/E is a rough stand-in, not the actual valuation metric this style uses. Lean harder on the real financial-data verification step below; expect a lower hit rate |
| Quality Compounder | `Webull:get_market_sectors_detail`, sorted by `MARKET_VALUE` descending, sampled across **every** sector `Webull:get_market_sectors` returns (see cross-sector requirement below) | **Weak proxy** — no ROIC or gross-profitability screener exists; this only produces a plausible-quality universe, the real criteria table does the actual filtering |

**Cross-sector requirement for Deep Value and Quality Compounder — the only two styles that
source from sectors.** Call `Webull:get_market_sectors` once to get the full sector list, then
pull `Webull:get_market_sectors_detail` for **every** sector returned (small page size, ~3–5
per sector), not just the one or two largest by market value. Semiconductors and Software &
IT Services are usually the biggest sectors by aggregate market cap in the current market —
if the pool only ever samples the top sector(s), Deep Value and Quality Compounder discovery
silently turns into an AI/semiconductor screener every single run, which is exactly the
outcome the "AI" list-name note above says these watchlists are NOT supposed to be. Combine
the per-sector pulls into one raw pool spanning healthcare, industrials, financials, energy,
consumer, materials, utilities, communication services, real estate, and tech/software alike,
*then* apply the pre-filter and the 10-candidate cap below.

### Steps

1. **Pull a raw candidate pool per style requested** — one scanner call (page size ~20–30)
   per the table above, except Deep Value and Quality Compounder, which pull across every
   sector per the cross-sector requirement above (one `get_market_sectors_detail` call per
   sector, not one call total). If no style is named, ask which, or run all five if Joshua
   says so explicitly.

2. **Pre-filter before spending real financial-data calls:**
   - Drop any ticker already on that style's watchlist, on Screen Rejected, or already
     evaluated this run for a different style's discovery pass.
   - Drop anything below a basic liquidity floor (near-zero volume, a penny-stock price) —
     this is a sanity filter, not a criterion; it doesn't replace the style's own table.
   - Cap the survivors at **10 candidates per style per run**. More than that turns one
     discovery run into a market-wide scan and burns an unbounded number of tool calls; if
     the raw pool has more plausible names than that, take the top few from each scanner
     page (or, for Deep Value/Quality Compounder, from each sector) rather than re-sorting
     the whole combined pool by raw value and truncating — for Quality Compounder
     specifically, a straight market-value-descending cut across all sectors combined would
     just re-collapse the pool onto the largest global companies (which are AI/tech mega-caps
     right now), undoing the cross-sector sampling above.

3. **Pull real financials for each survivor** via Webull's data tools
   (`get_financial_indicators`, `get_income_statement`, `get_balance_sheet`, `get_cash_flow`,
   `get_stock_quotes`, `get_52_week_high_low`, `get_stock_bars_single`, or similar) — fetched,
   never estimated or reasoned out. A value that genuinely isn't available is
   `data not available`, not a guess.

4. **Run each survivor through its style's criteria table** exactly as written above —
   same bar as a user-named candidate, no loosened threshold because it came from a scan.

5. **File passers** using the same duplicate-check-then-add steps as the main flow (Steps 3–4
   above): confirm not already present, then `Webull:add_watchlist_instruments` into that
   style's watchlist.

6. **Report the whole funnel, not just the winners** — raw pool size, how many were
   pre-filtered out and why, how many got full financials pulled, pass/fail per evaluated
   candidate with the failing criterion named, and which were filed. A discovery run that
   found nothing is a valid, reportable outcome — don't pad it.

A request to skip the financials pull, or file a survivor before it's actually run through
the criteria table, is the same class of override as loosening a threshold — it doesn't get a
pass because the candidate came from a scan instead of Joshua. "Just add the first one that
looks decent" is a reason to want Steps 3–4 skipped, not a release of them.

## What this does not do

- Does not define, loosen, or reinterpret any criterion — see the Define-mode
  note at the top, and note discovery evaluates candidates against the same tables, not a
  looser bar.
- Does not pull metric values itself for a user-named screen — Joshua supplies
  them there, or names the source to check. Discovery (above) and the unattended weekly
  routine are the two named exceptions, and only for sourcing/fetching, never for loosening
  the pass bar.
- Does not size, price, or execute a trade on any passed name.
- Does not write the thesis for a passed name (`equity-research-writeup`).
- Does not backtest a filed candidate — that's `strategy-backtest-design`, once a specific
  entry/exit rule is named.
- Does not remove a name from any watchlist automatically — every removal is
  a manual `Webull:remove_watchlist_instruments` call after Joshua confirms.