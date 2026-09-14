---
name: performance-benchmarking
description: |-
  Compares whole-account realized return to a real benchmark (SPY/total market) so a lucky winner never passes as skill. Triggers: "how am I doing vs the market", "am I beating the S&P", "run my Sharpe ratio". A procedure: withholds a verdict until start/end value+date and every cash flow between them are supplied, never estimated. Computes return via Modified Dietz, fetches the benchmark's real price for the same window via Webull, reports the delta in percentage points. Sharpe/Sortino only with ≥3 snapshots; skips and says so otherwise. Appends each run to a running log to build a real return series over time. Not `weekly-portfolio-review` (process, not results), not `strategy-backtest-design` (hypothetical rule vs. real history), not one stock's return vs. benchmark (`equity-trade-decision`'s checklist line), not tax liability.
---

# Performance Benchmarking

Nothing else in this catalog ever asks the one question that actually tells you whether any
of this is worth doing: **did the account beat a plain index fund, on a risk-adjusted basis,
over real time?** Every other Finance skill either prices a single decision (buy this, sell
that, size this) or audits process (is the thesis still valid, was the stop honored). None of
them look back at realized results and compare them to the honest alternative — buying VOO and
doing nothing. This skill is that comparison, and only that comparison. It doesn't decide
anything; it reports a number and a delta.

A procedure, not a gate on judgment — but it withholds any verdict until the inputs below are
actually supplied. A single lucky winner inflating the whole-account return, with no benchmark
next to it, is exactly the failure this skill exists to prevent — so it never reports a
portfolio return alone.

## Inputs required before any computation

1. **Period start** — a date, and the total portfolio value on that date (priced holdings,
   not a remembered figure).
2. **Period end** — a date, and the total portfolio value on that date.
3. **Every external cash flow in between** — each contribution or withdrawal, with its date
   and signed amount. "No cash flows this period" is a valid answer, but must be stated, not
   assumed silently — a contribution mistaken for investment return is the single most common
   way retail performance tracking lies to itself.
4. **Benchmark choice** — SPY, VOO, a named total-market fund, or "no preference" (defaults to
   SPY, named explicitly either way so it's never a silent choice).
5. **Optional — periodic snapshots.** Monthly (or more frequent) account values between start
   and end, if the user has them. Not required for the base return comparison; required for
   the Sharpe/Sortino step below. Their absence is fine and common — say so plainly rather than
   asking the user to reconstruct history they don't have.

Missing 1–4: state exactly what's missing and stop. Don't estimate a start value from a vague
"around $X" — that number is the whole basis for everything downstream.

## Steps

1. **Compute the portfolio's return using the Modified Dietz method** — the standard
   practitioner approximation for a return series with interim cash flows but no daily
   valuations:

   ```
   R = (EndValue − StartValue − NetCashFlow) / (StartValue + Σ(CF_i × W_i))

   where W_i = (days remaining in the period after CF_i) / (total days in the period)
   ```

   Show the formula filled in with the user's actual numbers, not just the final percentage —
   this is what makes the number auditable instead of a black box.

2. **Fetch the benchmark's real price for the identical window** via
   `Webull:get_stock_bars_single` (or `get_stock_bars`) for the chosen ticker at the start and
   end dates — fetched, never estimated. Compute the benchmark's simple return over the same
   window. Name explicitly that Webull's bars are price-only: a benchmark held with dividends
   reinvested would have returned slightly more than this figure shows — state this as a known
   understatement of the true total-return benchmark, don't silently treat price return as
   total return.

3. **Report the comparison** — portfolio return %, benchmark return % (with the dividend
   caveat from step 2 attached), the delta in percentage points, and the dollar difference if
   useful. The delta is the actual point of the skill; never present the portfolio return in
   isolation as if it answers the question on its own.

4. **Risk-adjusted metrics — only with ≥3 periodic snapshots.** If step 5 of the inputs was
   supplied with at least 3 data points, build a return series from consecutive snapshots and
   compute:
   - **Sharpe ratio**: (mean period return − risk-free rate) ÷ standard deviation of period
     returns, annualized. Ask the user for a risk-free-rate figure (current 3-month T-bill
     yield is the standard proxy) or name that it needs sourcing — never assume a rate.
   - **Sortino ratio**: same numerator, denominator is downside deviation only (periods below
     the target/zero return), annualized.

   With fewer than 3 snapshots, say plainly that there isn't enough data for a meaningful
   volatility estimate and skip both — do not compute a ratio from one or two points and
   present it as real; that's statistically meaningless and worse than saying nothing.

5. **Append this run to the running log** at `Finance/Investment/Performance Log.md` in the
   vault (not this repo) — date, portfolio value, cash flows since the last entry, computed
   return, benchmark used and its return, and the Sharpe/Sortino figures if computed. Create
   the file with a simple dated-table format if it doesn't exist yet. This is what turns a
   one-off comparison into a real return series over time, the same way `problem-journal`'s
   Capture mode turns individual errors into a corpus its Journal mode can later search.

## Output format

```
PERFORMANCE REVIEW — <start date> to <end date>

Portfolio:  Start $<n>  →  End $<n>   Net cash flow: $<n> (<k> contributions/withdrawals)
            Modified Dietz return: <pct>%

Benchmark:  <TICKER>   Start $<price>  →  End $<price>   Return: <pct>% (price only — total
            return with dividends reinvested would be modestly higher)

Delta:      <pct>pp <ahead of/behind> <TICKER>   ($<n> in dollar terms)

Risk-adjusted: <Sharpe: n.nn | Sortino: n.nn — computed from <k> snapshots>
               OR
               <Not computed — fewer than 3 periodic snapshots on file>

Logged to Finance/Investment/Performance Log.md.
```

## What this does not do

- Does not recommend buying, selling, or resizing anything based on the result — a bad number
  is information, not a trade signal. That verdict, if any, is the user's, possibly routed
  through `portfolio-thesis-audit` or `asset-allocation-policy`.
- Does not replace `weekly-portfolio-review` — that walk is about process and positions on a
  weekly cadence; this is about realized, whole-account results, meant for a much slower
  cadence (monthly/quarterly at soonest — weekly noise is too high to say anything about
  Sharpe or benchmark drift).
- Does not replace `strategy-backtest-design` — that tests a hypothetical rule against
  historical bars before capital is risked; this measures what the real account, with real
  decisions already made, actually did.
- Does not evaluate a single position's return against a benchmark — that's already
  `equity-trade-decision`'s pre-trade "relative performance" checklist line, a different,
  narrower, single-trade question. This skill is whole-account or nothing.
- Does not compute tax liability on the period's gains — `tax-lot-selection` and a CPA own
  that.
- Does not treat a benchmark's price-only return as its true total return — see step 2's
  dividend caveat, restated every time, not just the first.

## Red flags — the review isn't real

- A portfolio return reported with no benchmark comparison next to it.
- Sharpe or Sortino computed from fewer than 3 data points.
- Start or end value estimated from memory rather than supplied as an actual priced figure.
- A cash flow omitted or assumed zero without the user confirming there were none.
- A single large winner's return presented as if it represents the whole account's skill,
  with no benchmark delta shown alongside it.
- The benchmark's price-only return treated silently as if it already includes dividends.

## Example invocations

> "How am I actually doing compared to just holding the S&P this year?"

> "Run my Sharpe ratio for the last four quarters — I have month-end statements for all of
> them."

> "Quick check: is this year's return real, or is it just NVDA carrying the whole account?"
