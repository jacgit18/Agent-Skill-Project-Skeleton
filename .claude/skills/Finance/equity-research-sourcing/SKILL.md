---
name: equity-research-sourcing
description: |-
  Fetches and cites real figures `equity-research-writeup` sections 2/4/5 and `portfolio-thesis-audit`'s validity check need, and narrows open-ended qualitative research (sections 3/6) to one checkable claim before anything runs. Triggers: "pull the financials for TICKER", "source section 4/5", "find evidence for the bear case". Three modes: Fetch — pulls and cites a figure, flagging gaps NOT VERIFIED. Lookup — points to where to find/verify a figure. Scope — asks which claim, what window, who runs the search (here, or the user via ChatGPT/elsewhere), then vets pasted-back research for a named source. Never interprets a section — business, competitive argument, bear case, thesis, invalidation events (1,3,6,7,8) stay the user's synthesis; supplies raw sourced inputs only. Not Screen mode (`watchlist-screener-criteria`, user-supplied). Not `reddit-researcher` (broad sentiment sweep vs. one verified claim). Not ETF fact-sheet data (`etf-selection`, user-pulled).
---

# Equity Research Sourcing

`equity-research-writeup` refuses to author a company's fundamentals from memory, on purpose
— that gate is what forces real verification instead of a fluent-sounding narrative the user
never checked. But three of its eight sections (2, 4, 5) are mostly *objective, tabular*
figures — revenue, margin, free cash flow, share count, a P/E multiple — not interpretation.
Making the user hand-copy those out of a filing one field at a time doesn't protect them the
way writing their own bear case does; it's just retyping. And the qualitative sections (3, 6)
have their own opposite failure: "research the competitive position" invites an unfocused,
token-expensive sweep that comes back as generic narrative instead of one checkable claim.
This skill covers both: it fetches and cites the objective figures live (Fetch), points to
where a figure lives when the user wants to pull it themselves (Lookup), and narrows a broad
research ask to one specific claim before anything runs — whether Claude executes that search
or the user takes a precisely-scoped query to another tool and pastes the result back (Scope).
The user's effort stays on the parts that actually require judgment.

Where it sits: inside `equity-research-writeup`, feeding sections 2 / 4 / 5 directly and
sourcing (never writing) evidence for sections 3 / 6; also feeds `portfolio-thesis-audit`'s
current-validity check the same way. Sections 1, 3, 6, 7, 8 are never authored by this skill
— same gate, same bar, as before this skill existed. Only the effort of *finding* the raw
material changes; the effort of *arguing from it* does not.

## What this does not do

- **Write or interpret a section.** The business in plain terms (1), the competitive-position
  *evidence and argument* (3), the bear case (6), the thesis (7), and invalidation events (8)
  are the user's own synthesis. This skill can hand over the raw margin/retention/revenue
  numbers those sections might reference, but never the sentence arguing what they mean —
  Scope mode holds the same line: a scoped, sourced finding is not an argument, however
  narrowly it was targeted. "Also just write me the bull case while you're in there" is
  declined — that's `equity-research-writeup`'s gate, not something this skill can relax.
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
  recent news", "what's the buzz" is `reddit-researcher` — a broad multi-source sweep for
  chatter across ~30 days, not this skill's narrow single-claim verification. If the ask
  names one specific, checkable claim ("does TICKER actually have pricing power"), that's
  Scope mode; if it's an open-ended "what's going on with TICKER," that's `reddit-researcher`.
- **Answer a bare "research TICKER" / "deep dive on X."** That trigger belongs to
  `equity-research-writeup` itself — the full eight-section gate, not this skill. Scope mode
  only fires once the ask names a specific claim to source evidence for (section 3 or 6,
  often inside an already-open writeup), not a bare research request that hasn't been broken
  into sections yet.
- **Screen the market for candidates.** Sourcing here starts from a named ticker already past
  the screen, not "find me some names" — that's `watchlist-screen-sync`'s Discovery mode.
- **Produce an opinion or verdict from the figures it sources.** `equity-investment-take`
  reuses this skill's tool set and sourcing bar to do exactly that, on explicit request — a
  separate skill with different rules, not this one quietly gaining an interpretation mode.
- **Answer a bare conceptual question.** "What's free cash flow", "how do I read a 10-K" with
  no ticker in view is `learning-gate`.

---

## Three modes

| Ask | Mode |
|---|---|
| "Pull TICKER's numbers for section 4", "get me the financials", "source this for me" | **Fetch** — Claude pulls and cites |
| "Where do I find TICKER's segment revenue myself", "how do I check this number", "I'll pull it, just tell me where" | **Lookup** — Claude points, user pulls |
| "Research TICKER's competitive position", "find evidence for the bear case", "dig into whether TICKER has pricing power", "what's TICKER's moat like", "does TICKER actually have a moat" | **Scope** — narrow the claim first, then research or hand off |

Default to **Fetch** when the ask is to get numeric figures; switch to **Lookup** when the
user wants to pull one themselves, or a figure isn't available through this skill's tools and
has to come from the filing directly. Use **Scope** whenever the ask is open-ended qualitative
research rather than a specific figure — that's the one most likely to burn tokens on an
unfocused sweep if it isn't narrowed first.

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

### Scope mode

Open-ended qualitative research — section 3's competitive evidence, section 6's bear case —
is where cost and focus both go wrong at once: "research TICKER's competitive position"
invites either a broad, token-expensive sweep or a generic narrative that never becomes a
checkable claim. Scope mode narrows the ask before anything runs. Ask, in order, only what
isn't already answered:

1. **The specific claim.** One dimension, not "everything about the competition": pricing
   power, retention/churn, market-share direction, customer concentration, regulatory/legal
   exposure, supply-chain dependency, insider activity. If the user already named one
   ("does TICKER actually have pricing power"), this step is already done — don't re-ask. A
   bare "what's TICKER's moat like" routes here too — "moat" is not itself a claim
   (`equity-research-writeup` section 3 already treats "wide moat" with no number as a
   non-answer), so this step's job is narrowing it into one of the dimensions above.
2. **The window.** Most recent quarter/fiscal year, or a stated period — recency matters for
   evidence the same way it does for a filing.
3. **Who runs it.** Claude executes one narrow, scoped `WebSearch`/`WebFetch` here and returns
   sourced findings — or Claude hands back the precise query text for the user to run
   elsewhere (ChatGPT, a browser, a data provider) and paste the results back. Ask; don't
   default silently either way, since the whole point is the user's own token/cost tradeoff.

**If Claude runs it:** one targeted search, not a sweep — return findings with source name
and date, the same sourcing bar as Fetch mode. Still no interpretation: "here's what the
sources say" stops short of "and that means the moat is wide."

**If the user pastes back external research** (from ChatGPT or anywhere else): check every
claim for a named, checkable source before it counts as evidence — an unsourced claim is
`NOT VERIFIED` regardless of how fluently it reads or which model produced it. "Named" means
a specific person, firm, publication, or filing **plus a date** — a soft attribution like
"analysts say" or "a recent report found" names neither and is `NOT VERIFIED`, not a pass,
even though it reads like a citation. Flag it, don't wave it through just because it arrived
pre-written and superficially sourced-looking.

Either path, the result feeds section 3 or 6 as **raw sourced evidence**, never the argument
itself — the user still writes why it matters.

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
Claude still does not write the sentence arguing what they mean. These are sourced inputs,
not a verdict — a completed thesis still needs sections 1, 3, 6, 7, 8, whether or not a
writeup is already open.
```

## Output — Scope mode

```
Research scope — <TICKER>   ·   claim: <the one named claim>   ·   window: <period>

<if Claude ran it>
Findings:
  <finding>   ·   source: <name>   ·   as of: <date>
  [...]
  Not verified: <anything the search didn't turn up a checkable source for>

<if handed to the user>
Query to run elsewhere:  "<the precise, pasteable search text>"
What to look for:        <the claim, the window, what would count as evidence either way>
Paste the results back here to vet before they go into section <3 | 6>.

<if vetting a paste>
Vetted findings:
  <claim>   ·   source: <named, checkable | NOT VERIFIED — no source given>
  [...]

Hand back to equity-research-writeup section <3 | 6>: these are raw evidence, not the
argument — the user still writes what it means.
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
- A Scope-mode research ask run as a broad, unscoped sweep instead of narrowing to one claim
  first — defeats the point (token cost and unfocused results both rise together).
- An externally-sourced claim (ChatGPT or otherwise) treated as evidence with no checkable
  source, just because it reads fluently and arrived pre-written.

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

> "Can you dig into TICKER's competitive position — is the pricing power real?"

Scope mode. The claim is already named (pricing power); confirm the window and ask who runs
the search. Either run one narrow search and cite what comes back, or hand back a precise
query for the user to run in ChatGPT or elsewhere.

> "I ran that in ChatGPT — here's what it said about TICKER's competitors. Can you check it?"

Vet the pasted content: does each claim carry a named, checkable source? Flag anything that
doesn't. Hand back the sourced remainder as raw input for section 3 — still no interpretation.

> "Research TICKER for me — deep dive."

Bare research trigger, not a specific claim — `equity-research-writeup` itself, not this
skill's Scope mode.

> "What is free cash flow, actually?"

No ticker on the table — answered directly. `learning-gate`.

---

## Portability

Fetch mode depends on Webull's financial-data tools (`get_income_statement`,
`get_balance_sheet`, `get_cash_flow`, `get_financial_indicators`, `get_analyst_rating`,
`get_analyst_target_price`, `get_stock_forecast_eps`, `get_stock_filings`,
`get_stock_industry_comparison`, `get_52_week_high_low`, `get_stock_snapshot`,
`get_stock_dividend_calendar`) plus `WebFetch` for primary-filing excerpts. Scope mode's
self-run path depends on `WebSearch` + `WebFetch` only, not Webull. Lookup mode needs neither
and is fully repo-agnostic, as does Scope mode's hand-off path (the user runs the search
externally; this skill only scopes the query and vets what comes back). In a repo without
Webull's tools, Fetch mode's tool table doesn't apply, but Lookup and Scope still work.
Writes nothing to disk; hands the sourced block back in chat for the user to paste into their
`equity-research-writeup` document. Copy the `equity-research-sourcing/` directory into
another repo's `.claude/skills/`.
