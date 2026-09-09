---
name: watchlist-screener-criteria
description: Use when someone wants to decide, in advance and as numbers, which stocks are even worth researching — the filter that runs before a name reaches `equity-trade-decision` — or wants to run a specific candidate through that filter. Triggers include "help me set up screening criteria", "what filters should I use to find stocks", "I keep hearing about names from YouTube and want a real process", "does TICKER pass my screen", "should this stock make my watchlist", or a stated candidate whose only backing is a video, a tip, or product familiarity. Two modes. **Define** — the user commits to a screen: a stated investing style (value / quality-compounder / growth / momentum / dividend), then a small set of criteria, each a metric + a numeric threshold + a direction + one line on why the user believes it predicts returns, plus a hard-disqualifier list. Claude checks each criterion is numeric and checkable, that they cohere around the stated style, and that there are enough to actually filter — it does not hand the user a screen. **Screen** — a specific ticker is run against an existing screen: the user brings the metric values from a real data source (Claude does not fetch or estimate fundamentals), and gets pass/fail per line, an overall verdict (add to watchlist / proceed to `equity-trade-decision` / reject), and an explicit flag when a narrative-sourced candidate is failing the filters — the exact pattern the screen exists to stop. If no screen exists yet, Screen mode gates back to Define. Not `equity-trade-decision` — that is the next stage, a specific trade with a real entry, stop, and capital; this decides whether a name earns that work at all. Not `portfolio-thesis-audit` (positions already held) or `position-exit-rules` (exits). Not a stock-picking service — it does not run the screen against the market and return names; the user screens in their own tool and brings candidates. Not backtesting — whether these criteria historically produced returns is a separate quantitative exercise; name it, don't fake it. Not portfolio construction or diversification policy. Not a bare conceptual question — "what is the F-score", "what P/E is considered cheap" with no screen being built is `learning-gate`. Not a substitute for a financial advisor.
---

# Watchlist Screener Criteria

Stocks enter a consideration set through narrative — a video, a friend, a headline, "I use
the product." Then the full trade evaluation runs on a name that was never filtered on
anything, so the research is really post-hoc justification of a pick that arrived by vibes.
There is no repeatable process generating candidates, so there is no edge to measure. This
skill is a **gate**: it withholds the "this name is worth researching" verdict until a
written, numeric screen exists and the candidate has been run through it. It is the gate
before `equity-trade-decision`'s gate.

## Two modes

| Ask | Mode |
|---|---|
| "help me set up screening criteria", "what should my filters be", "I want a real process instead of YouTube" | **Define** — build the written screen |
| "does TICKER pass my screen", "should this make my watchlist", a specific candidate to vet | **Screen** — run one candidate against the existing screen |

If a candidate is brought for **Screen** mode and no written screen exists yet, gate back to
**Define** first — running a name against a screen that only exists in someone's head is the
same vibes problem with an extra step.

## What this does not do

- **Evaluate or size a specific trade.** Entry price, stop, capital, share count — that's
  `equity-trade-decision`, the stage *after* this one. This skill decides whether a name
  earns that work; it does not do it.
- **Audit a held position** (`portfolio-thesis-audit`) or **define exits**
  (`position-exit-rules`). This is entirely about names not yet owned.
- **Screen the market and return names.** The user runs the screen in their own tool (a
  broker screener, Finviz, a data provider) and brings candidates. Claude defines the
  criteria structure and vets a candidate's stated numbers — it does not fetch, look up, or
  estimate a company's fundamentals.
- **Backtest the screen.** Whether these thresholds historically produced returns is a
  separate quantitative exercise. Name it as a follow-up; do not assert a screen "works"
  without it.
- **Portfolio construction.** How many names, sector limits, position sizing — not here.
- **Answer a bare conceptual question.** "What's a good ROIC threshold", "how does the
  Piotroski F-score work" with no screen being built is `learning-gate`.

---

## Define mode — the precondition

The user commits, in their own words and numbers:

1. **The style.** One of: deep value / quality compounder / growth / momentum / dividend
   income — or a stated blend, but named. Criteria that don't cohere around a style ("low
   P/E *and* high growth *and* high momentum *and* high yield") describe no real company and
   filter nothing.
2. **The criteria** — a small set (roughly 4–8; fewer filters nothing, more filters
   everything out and can't be maintained). Each one is:
   - a **metric** (see the menu below),
   - a **numeric threshold**,
   - a **direction** (above / below / within),
   - one line: **why the user believes this predicts forward returns or screens out
     losers** — not "it's good", an actual mechanism ("FCF-positive means growth isn't
     funded by dilution or debt").
3. **Hard disqualifiers** — the automatic nos regardless of everything else (e.g. going-
   concern language in the latest filing; a restatement in the last N years; negative
   operating cash flow with no stated path; below a chosen Altman-Z or Piotroski-F floor;
   below a liquidity minimum — average daily dollar volume, market cap).
4. **Review cadence** — when the screen itself gets re-examined (quarterly, annually), so it
   is a living methodology, not a one-time list.

Claude's contribution:

- Check every criterion has a **number and a direction** and is **checkable from public
  data** — reject "strong management", "wide moat", "good industry position" as screen
  lines (they belong in `equity-trade-decision`'s qualitative checklist, not a numeric
  pre-filter).
- Check the set **coheres around the stated style**.
- Check there is a disqualifier list and a review cadence.
- Produce the written screen block. Do **not** supply the thresholds — if the user has no
  view on a threshold, that is a gap to close (via `learning-gate`), not for Claude to fill.

### Metric menu (pick from these, set your own thresholds)

| Dimension | Common metrics |
|---|---|
| Valuation | P/E, P/FCF, EV/EBIT, EV/Sales, P/B, earnings yield, PEG |
| Quality / returns | ROIC, ROE, ROA, gross margin, operating margin, margin trend |
| Growth | revenue CAGR (3–5y), EPS CAGR, forward revenue growth, same-store/organic growth |
| Financial health | net debt / EBITDA, interest coverage, current ratio, Altman Z, Piotroski F, FCF positive |
| Capital discipline | share count trend (buybacks vs dilution), dividend history, FCF conversion, accruals |
| Momentum / technical | price vs 200-day MA, 6–12 month relative strength, distance from 52-week high |
| Size / liquidity | market cap floor, average daily dollar volume, spread |

---

## Screen mode — running a candidate

The user brings:

1. **The ticker.**
2. **The value of each screen metric** for that company, from a named real source (their
   broker, a data provider, the filing). If a value is "not looked up yet", that line is
   `not supplied — get it from <source>`, never estimated by Claude.
3. **How the candidate surfaced** — a screen run, a video, a tip, product familiarity, a
   news headline. Stated plainly.

Output:

```
Screen result — <TICKER>   ·   screen: <style>, defined <date>, last reviewed <date>

How it surfaced:      <screen run | YouTube / tip / product familiarity / headline>

Criterion            Threshold        Candidate value     Pass?
<metric 1>           <dir> <n>        <value | not supplied>   <✓ | ✗ | unknown>
<metric 2>           ...              ...                      ...
[all criteria]

Hard disqualifiers:   <none triggered | TRIGGERED: <which> → automatic reject>

Passed:  <k> / <n> criteria   ·   Disqualifiers: <clear | triggered>

Verdict:  <ADD TO WATCHLIST — clears the screen, proceed to `equity-trade-decision` when
          ready | REJECT — fails <k> criteria / a disqualifier | INCOMPLETE — <m> metric
          values not supplied, get them first>

Informal-input flag:  <none | the only reason this name is here is a video / tip / product
                      familiarity, AND it fails the screen — this is the exact pattern the
                      screen exists to stop; a narrative is not a reason to override a
                      failed filter>
```

A candidate that surfaced from a narrative **and** passes the screen is fine — the screen
did its job. A candidate that fails and whose only backing is narrative is a reject, and the
skill says so directly.

---

## Red flags — the screen isn't real

- Criteria with no number ("cheap", "high quality", "growing") — that is a vibe with a
  metric's name on it.
- Claude having supplied the thresholds. The user owns the screen or it isn't theirs to
  trust.
- A screen whose lines don't cohere around any single style — it will pass nothing or
  everything.
- No hard-disqualifier list.
- Screen mode run with metric values Claude estimated or "reasoned out" instead of the user
  pulling them from a real source.
- A failing, narrative-sourced candidate waved through because "the guy who called it has a
  good track record" — that is the informal-input pattern, not a screen result.
- The screen treated as a permanent artifact with no review date.

---

## Example invocations

> "Help me set up screening criteria — I want to stop picking stocks off YouTube."

Define mode. Ask for the style first, then make the user commit each criterion (metric +
threshold + direction + why) and a disqualifier list. Offer the metric menu to choose from;
don't fill in the thresholds.

> "Does PLTR pass my screen?" (screen already defined)

Screen mode. Ask for the metric values from a real source and how PLTR came to their
attention, then run the block.

> "Does PLTR pass my screen?" (no screen defined yet)

Gate to Define mode — there's nothing to run it against.

> "What P/E ratio counts as undervalued?"

No screen being built — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the screen definition or the screen-result block in
chat. Copy the `watchlist-screener-criteria/` directory into another repo's `.claude/skills/`.
Feeds `equity-trade-decision` — a name that clears the screen is a candidate worth that
skill's full checklist.
