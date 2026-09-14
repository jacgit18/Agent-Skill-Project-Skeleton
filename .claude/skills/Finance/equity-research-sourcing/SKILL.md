---
name: equity-research-sourcing
description: |-
  Fetches and cites real figures `equity-research-writeup`'s numeric sections need — unit-economics drivers, 3–5yr financial trend, valuation inputs — via Webull financial-data tools and named filings, each dated and sourced. Triggers: "pull the financials for TICKER", "get me the numbers for my writeup", "source section 4/5". Two modes: Fetch — pulls and cites the figure, flagging gaps NOT VERIFIED rather than estimating. Lookup — points to where to find/verify a figure yourself, for anything not available live. Never interprets a section — business, competitive evidence, bear case, thesis, invalidation events (sections 1, 3, 6, 7, 8) stay the user's own synthesis; supplies sourced inputs to sections 2, 4, 5 only. Not `watchlist-screener-criteria` Screen mode — values stay user-supplied by design even for a fetchable metric; reserved for names past the screen. Not `reddit-researcher` (sentiment, not filings). Not ETF fact-sheet data — `etf-selection` stays user-pulled, not extended here yet.
---

# Equity Research Sourcing

`equity-research-writeup` refuses to author a company's fundamentals from memory, on purpose
— that gate is what forces real verification instead of a fluent-sounding narrative the user
never checked. But three of its eight sections (2, 4, 5) are mostly *objective, tabular*
figures — revenue, margin, free cash flow, share count, a P/E multiple — not interpretation.
Making the user hand-copy those out of a filing one field at a time doesn't protect them the
way writing their own bear case does; it's just retyping. This skill is the fetch-and-cite
companion: it pulls those figures live, names the source and as-of date for each, and flags
anything it can't verify — so the user's effort stays on the parts that actually require
judgment.

Where it sits: inside `equity-research-writeup`, feeding sections 2 / 4 / 5 only. Sections 1,
3, 6, 7, 8 are untouched — same gate, same bar, as before this skill existed.

## What this does not do

- **Write or interpret a section.** The business in plain terms (1), the competitive-position
  *evidence and argument* (3), the bear case (6), the thesis (7), and invalidation events (8)
  are the user's own synthesis. This skill can hand over the raw margin/retention/revenue
  numbers those sections might reference, but never the sentence arguing what they mean.
  "Also just write me the bull case while you're in there" is declined — that's
  `equity-research-writeup`'s gate, not something this skill has authority to relax.
- **Run a valuation or produce a price target.** It fetches the multiple, the peer comps, and
  the analyst targets others have published — it does not compute a DCF or assert a fair
  value itself. `equity-research-writeup` section 5 still requires the user's own reasoning
  from those inputs.
- **Supply Screen-mode values.** `watchlist-screener-criteria` Screen mode requires the user
  bring metric values from a real source themselves — deliberately, so the screen stays cheap
  triage rather than full research spent on every video tip. A candidate that hasn't cleared
  the screen doesn't get this skill's effort; redirect to Screen mode's own rule instead of
  fetching for it. Once a name clears the screen and moves into a real writeup, this skill
  applies.
- **Source ETF/fund facts.** Expense ratio, tracking difference, AUM, holdings overlap are
  `etf-selection`'s domain, and that skill still requires the user pull them from the issuer
  fact sheet — this skill's tool set is company financials, not fund data. Not extended there
  yet; a real future gap, not a silent scope grab.
- **Do current-awareness or sentiment research.** "What's Reddit saying about TICKER", "any
  recent news" is `reddit-researcher` — a different source set (social/web, ~30-day window),
  a different kind of evidence (chatter, not filed numbers).
- **Screen the market for candidates.** Sourcing here starts from a named ticker already past
  the screen, not "find me some names" — that's `watchlist-screen-sync`'s Discovery mode.
- **Answer a bare conceptual question.** "What's free cash flow", "how do I read a 10-K" with
  no ticker in view is `learning-gate`.

---

## Two modes

| Ask | Mode |
|---|---|
| "Pull TICKER's numbers for section 4", "get me the financials", "source this for me" | **Fetch** — Claude pulls and cites |
| "Where do I find TICKER's segment revenue myself", "how do I check this number", "I'll pull it, just tell me where" | **Lookup** — Claude points, user pulls |

Default to **Fetch** when the ask is to get the numbers; switch to **Lookup** when the user
says they want to pull it themselves, or when a figure isn't available through the tools this
skill has and has to come from the filing directly anyway.

### Fetch mode

For each figure: pull it via the tool table below, state the **value**, the **source**
(named tool/filing/provider), and the **as-of date or fiscal period**. A figure the tools
don't carry (a segment breakout, an MD&A qualitative disclosure, a footnote detail) is
**not estimated** — `WebFetch` the actual SEC EDGAR filing for that section and cite the
filing type + date, or, if that's also not practical mid-conversation, flag
`NOT VERIFIED — pull from <specific filing/section> yourself` and switch that line to Lookup.

| equity-research-writeup section | What's fetched | Primary tool(s) |
|---|---|---|
| 2. Unit economics | Revenue, gross profit, shares outstanding, market cap, the named driver metrics (ARPU, take-rate, etc. where disclosed) | `get_income_statement`, `get_financial_indicators`, `get_stock_snapshot` |
| 4. Financial trend (3–5y) | Revenue growth, gross/operating margin, free cash flow, share count trend, net debt/EBITDA, interest coverage | `get_income_statement`, `get_balance_sheet`, `get_cash_flow`, `get_financial_indicators` (each across every period the tool returns — if that's fewer than 3–5 years, say so explicitly rather than padding the gap) |
| 5. Valuation | Current multiple (P/E, P/FCF, EV/EBIT, EV/Sales), peer comps, analyst target price/rating, forward EPS, FCF/dividend yield, 52-week range | `get_financial_indicators`, `get_stock_industry_comparison`, `get_analyst_rating`, `get_analyst_target_price`, `get_stock_forecast_eps`, `get_52_week_high_low`, `get_stock_dividend_calendar` |
| Any section — primary-source excerpt or filing list | Recent filing list, or a specific disclosure not in structured data | `get_stock_filings`, then `WebFetch` the filing itself for the exact section, cited by filing type + date |

**Honesty requirement, same standard as `performance-benchmarking`'s Webull-data caveats:**
state plainly when a tool's history is shallower than the 3–5 years section 4 wants, when a
"peer comp" is really just whatever `get_stock_industry_comparison` returns rather than a
hand-picked competitor set, and when an analyst target is a consensus figure the user should
weight accordingly, not a fact. Never silently pad a thin data return to look complete.

### Lookup mode

For a figure this skill can't fetch live, or when the user wants to pull it themselves: name
the specific source (10-K item / note number if known, 10-Q, latest earnings call transcript,
investor-relations page, IR deck) and what to check the number against once pulled (does it
match a subsequent quarter's restated figure, is it GAAP or non-GAAP, does it net out a
one-time charge). This mirrors `equity-research-writeup`'s own sourcing bar — a number "from
memory" or "roughly" is not good enough there either.

---

## Output — Fetch mode

```
Sourced figures — <TICKER>   ·   for equity-research-writeup section(s) <2 | 4 | 5>

<metric>:   <value>   ·   source: <tool/filing>   ·   as of: <date/period>
<metric>:   <value>   ·   source: <tool/filing>   ·   as of: <date/period>
[...]

Not verified (pull yourself):
  <metric>  →  <specific filing/section to check>

Data-depth note:  <e.g. "get_income_statement returned 3 fiscal years, not 5 — the other two
                  would need EDGAR's full 10-K archive" | none>

Hand back to equity-research-writeup: paste these into section <n> with the sources above —
Claude still does not write the sentence arguing what they mean.
```

---

## Red flags — the sourcing isn't real

- A figure presented with no source name or no as-of date/period — indistinguishable from a
  number pulled from memory, the exact failure `equity-research-writeup` exists to prevent.
- A gap in the tool's data silently padded or estimated instead of flagged `NOT VERIFIED`.
- This skill asked to write, argue, or interpret — a business summary, a bear case, a thesis
  sentence — and doing it instead of declining back to `equity-research-writeup`'s own gate.
- Screen-mode metric values fetched for a candidate that hasn't cleared the screen yet, quietly
  doing `watchlist-screener-criteria`'s user-supplied step for it.
- A peer "comp" or analyst "target" handed over as settled fact rather than what it actually
  is — one data provider's industry grouping, one consensus number.

---

## Example invocations

> "I'm working through the equity-research-writeup on LIFE — can you pull the numbers for
> sections 4 and 5?"

Fetch mode. Pull income statement / balance sheet / cash flow / financial-indicator history,
the current valuation multiple, peer comps, and analyst target — each cited and dated. Hand
the block back for the user to paste in; do not draft the trend or valuation narrative.

> "Where would I even find LIFE's segment revenue breakdown myself?"

Lookup mode. Name the 10-K note or 10-Q MD&A section, and what to cross-check it against.

> "Great, now just write me the bull case from those numbers."

Declined — that's `equity-research-writeup` section 7's territory, and it's gated on the
user's own synthesis. Offer the sourced figures again as raw input, not a drafted case.

> "Does TICKER pass my screen — can you pull the P/E and margins for me?"

Not this skill while TICKER hasn't cleared `watchlist-screener-criteria` yet — Screen mode's
values stay user-supplied by design. Redirect there.

> "What's VOO's expense ratio and tracking difference?"

Fund data, not company financials — `etf-selection`, which still requires the user pull it
from the issuer fact sheet; not covered here.

> "What is free cash flow, actually?"

No ticker on the table — answered directly. `learning-gate`.

---

## Portability

Depends on Webull's financial-data tools (`get_income_statement`, `get_balance_sheet`,
`get_cash_flow`, `get_financial_indicators`, `get_analyst_rating`, `get_analyst_target_price`,
`get_stock_forecast_eps`, `get_stock_filings`, `get_stock_industry_comparison`,
`get_52_week_high_low`, `get_stock_snapshot`, `get_stock_dividend_calendar`) plus `WebFetch`
for primary-filing excerpts; Lookup mode needs neither and is fully repo-agnostic. In a repo
without Webull's tools, Lookup mode still works as a standalone sourcing-methodology guide —
drop the tool table's Fetch column and point everything at EDGAR / IR / transcripts instead.
Writes nothing to disk; hands the sourced block back in chat for the user to paste into their
`equity-research-writeup` document. Copy the `equity-research-sourcing/` directory into
another repo's `.claude/skills/`.
