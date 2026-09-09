---
name: equity-research-writeup
description: Use when someone wants to actually research a single public company before deciding to own it — "research TICKER", "do a deep dive on X", "analyse the fundamentals of X", "help me build my thesis on X", "is this a good business at this price", "I want a real analysis, not a headline take". It is a gate: it withholds a finished research writeup — and refuses to author the analysis — until the user has filled each section in their own words with the specific figures, each tied to a named source (10-K, 10-Q, an earnings call, the company's IR materials). The eight sections are the research process: (1) the business — what it sells, to whom, how it makes money, in plain terms; (2) unit economics — the two or three numbers that actually move the P&L, with current values; (3) competitive position — who competes and the *evidence* of pricing power / retention / share, not the word "moat"; (4) financial trend — 3–5 years of revenue growth, margin direction, FCF and whether it's funded by dilution or debt, share count, balance-sheet leverage, from the filings; (5) valuation — the multiple vs. the company's own history and peers, what growth and margin the current price implies, what you get paid to wait; (6) the bear case — the user writes the strongest argument *against* owning it; (7) the thesis — three or more sentences: why own it, what has to be true, over what horizon; (8) what would change my mind — the specific observable events or metrics that invalidate each thesis clause. Claude's job is to supply the structure, check every claim has a figure and a source behind it, flag a section that is thin or all-bull or circular, pressure-test the bear case, and confirm the thesis is falsifiable — it does not write a section, supply a financial figure, run a valuation, or fetch data. Sections 7 and 8 feed forward: the thesis satisfies `equity-trade-decision`'s fundamentals checklist item, and "what would change my mind" becomes `position-exit-rules`' thesis-invalidating events. Not `watchlist-screener-criteria` — that is the numeric pre-filter that runs *before* this; a name should clear the screen before you sink time into a full writeup. Not `equity-trade-decision` — that sizes and times the trade *after* this produces the thesis. Not `portfolio-thesis-audit` — that re-checks the thesis on a position already held; for "should I still own this", start there (it may route back here for a fresh writeup). Not for ETFs or funds — a rules-based basket gets evaluated on expense ratio, methodology, and tracking, not a business-and-moat writeup. Not a full DCF model build — it forces the valuation *reasoning*, not a spreadsheet. Not a private-company acquisition analysis (`seller-financing-evaluation` territory). Not a bare conceptual question — "how do I read a 10-K", "what is free cash flow", "how does a DCF work" with no company on the table is `learning-gate`. Not a substitute for a financial advisor, and Claude's own knowledge of any company's financials is a starting point to verify against the filings, never the source.
---

# Equity Research Writeup

Asked to "research TICKER", Claude will write a fluent, balanced-looking equity note from its
own knowledge — segments, growth drivers, a moat story, a bull and bear case, "fairly valued
here." The user reads it and feels researched, having done nothing, on figures that may be a
year stale. That is the "informal input treated as research" failure one level up: the
narrative is now Claude's instead of a video's. This skill is a **gate**: the user does the
reading and writes each section; Claude supplies the structure and stress-tests what comes
back. It does not author the analysis and does not provide the numbers.

Where it sits: `watchlist-screener-criteria` (numeric filter) → **this** (the thesis) →
`position-exit-rules` (the exits) → `equity-trade-decision` (size and enter).

## What this does not do

- **Screen for candidates.** `watchlist-screener-criteria` is the numeric pre-filter. A name
  should clear it before a full writeup is worth the time; this skill assumes that happened.
- **Size or time the trade.** `equity-trade-decision` does that, *after* this. Its pre-trade
  checklist item 1 ("fundamentals reviewed") is satisfied by a completed writeup here.
- **Re-check a held position's thesis.** `portfolio-thesis-audit` does that. "Should I still
  own X" starts there; it routes back here when the answer needs a fresh writeup.
- **Evaluate an ETF or fund.** A rules-based basket is judged on expense ratio, index
  methodology, AUM/liquidity, tracking error, and holdings overlap — not a business, moat,
  and bear case. Different evaluation entirely.
- **Build a DCF model.** This forces the valuation *reasoning* — the multiple against history
  and peers, the growth and margin the price implies, the yield you're paid to wait — not a
  cell-by-cell spreadsheet.
- **Analyse a private-company acquisition.** That's `seller-financing-evaluation` territory —
  no public filings, a different diligence process.
- **Answer a bare conceptual question.** "How do I read a 10-K", "what is FCF", "how does a
  DCF work" with no company on the table is `learning-gate`.
- **Provide the financials or the analysis.** Claude's knowledge of a company is a prompt to
  go verify against the latest filing, never the source. It does not fetch data, fill in a
  figure, or write a section's content.

---

## The precondition — the user fills the eight sections

Claude provides the skeleton and works one section at a time. A section is not done until it
has the user's own words **and** the specific figures, each with a named source (10-K, 10-Q,
earnings call transcript, IR deck, a data provider — named, not "I read somewhere").

If the user brings a partial draft, gap-check it against the eight sections rather than
starting over. If they bring nothing, build it section by section — but the content is
theirs.

### 1. The business

What it sells, to whom, and how it makes money — revenue mix in plain terms, 3–4 sentences.
If the user cannot explain the money plainly, stop here: that is disqualifying at the
research stage, same bar as the screener's "can't explain it in two sentences".

### 2. Unit economics

The two or three numbers that actually move the P&L, with current values and where they came
from — e.g. subscribers × ARPU × contribution margin; stores × sales-per-store × store
margin; take-rate × GMV; seats × price × net revenue retention.

### 3. Competitive position

Who competes, why customers stay or leave, and the **evidence**: pricing power shown in a
margin or take-rate trend; retention/churn numbers; market-share direction. "Wide moat" with
no number behind it is not an answer.

### 4. Financial trend

From the filings, 3–5 years: revenue growth (and whether it's decelerating), gross and
operating margin direction, free cash flow (positive? or funded by dilution / debt?), share
count trend, and balance-sheet leverage (net debt / EBITDA, interest coverage). Each figure
sourced.

### 5. Valuation

The multiple that fits the style (P/FCF, EV/EBIT, P/E, EV/Sales) against **the company's own
history** and against peers; what revenue growth and margin the current price implies if you
work backwards; and what you're paid to wait (FCF yield, dividend yield, buyback). Any price
target states its assumptions — no number pulled from air.

### 6. The bear case

The user writes the **strongest** argument against owning it — what breaks the thesis, what
the market may be seeing that they aren't, the plausible way this is a value trap or a
popped-multiple story. A thin or strawman bear case is a red flag: it means the writeup is
confirmation-seeking.

### 7. The thesis

Three or more sentences: why own it, what specifically has to be true for it to work, and
over what horizon. This is the artifact that feeds forward — `equity-trade-decision` checklist
item 1, and the clauses `position-exit-rules` turns into thesis-invalidating events.

### 8. What would change my mind

For each thesis clause in section 7, the specific observable event or metric that would prove
it wrong (e.g. "net revenue retention below 105% for two quarters", "the lead product loses
its top-3 customer", "gross margin below 60%"). This list is handed to `position-exit-rules`
verbatim.

---

## Claude's contribution — deliberately narrow

- Supply the section skeleton; take one section at a time.
- For every claim, check there is a **figure** and a **named source**. Flag "needs a source"
  rather than supplying one.
- Flag a section that is thin, entirely bullish, or circular ("it will grow because it's a
  growth company").
- Pressure-test section 6: "is that the strongest version of the bear case, or the easiest to
  dismiss?"
- Check the section 7 thesis is falsifiable and that section 8 actually maps to it.
- Where Claude has prior knowledge of the company, offer it explicitly labelled as
  *unverified, check the latest filing* — never as the figure of record.

Then assemble the writeup as the user's document and call out the two feed-forward pieces.

---

## Output — the writeup

```
Equity research writeup — <TICKER>   ·   <date>   ·   screen cleared: <date | not run — do that first>

1. Business:            <user's summary>            source(s): <...>
2. Unit economics:      <the 2–3 drivers + values>  source(s): <...>
3. Competitive position:<who / why / the evidence>  source(s): <...>
4. Financial trend:     <5y revenue / margin / FCF / share count / leverage>  source(s): <...>
5. Valuation:           <multiple vs history + peers · implied expectations · yield>  source(s): <...>
6. Bear case:           <the strongest argument against>
7. Thesis:              <≥3 sentences — why / what must be true / horizon>
8. What would change my mind:
     - <clause A> → <observable invalidating event>
     - <clause B> → <...>

Section check:          <1–8 each: OK | THIN — <what's missing> | UNSOURCED — <which claim> |
                        ALL-BULL — <section 6 needs a real bear case>>
Completeness:           <n>/8 sections trade-ready

Feeds forward:
  → equity-trade-decision : thesis (section 7) satisfies pre-trade checklist item 1
  → position-exit-rules   : section 8 list = the thesis-invalidating events (rule 2)
```

---

## Red flags — the writeup isn't real

- Claude wrote any section's content, supplied a financial figure, or produced a valuation
  number.
- Claims with no figure, or figures with no named source ("I read that revenue was up a
  lot").
- Financials taken from Claude's training knowledge instead of the current filing.
- A bear case (section 6) that is a strawman, or shorter than the bull case.
- A thesis that isn't falsifiable ("great company, long-term hold"), or a section 8 that
  doesn't line up clause-for-clause with section 7.
- The writeup treated as complete while sections are still `THIN` or `UNSOURCED`.
- A full writeup built on a name that never cleared `watchlist-screener-criteria`.

---

## Example invocations

> "Research NVDA for me — I want a real fundamental analysis before I decide to buy."

Give the eight-section skeleton. Ask the user to write section 1 in their own words and pull
the section 4 figures from the latest 10-K / 10-Q. Do not produce the analysis. Work down the
sections, checking sources and pushing on the bear case, then assemble.

> "Here's my writeup on COST — can you check it?"

Gap-check the draft against the eight sections. Flag unsourced claims, a thin bear case, a
non-falsifiable thesis. Don't rewrite it.

> "Should I still hold my ELF position?"

That's `portfolio-thesis-audit` — a held-position thesis check. It may send you back here for
a fresh writeup if the original thesis was never written down.

> "How do I actually read a cash flow statement?"

No company on the table — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing to disk by itself; produces the writeup in chat as the user's
document (they keep it — `position-exit-rules` and `portfolio-thesis-audit` both read from
it later). Copy the `equity-research-writeup/` directory into another repo's
`.claude/skills/`. Sits between `watchlist-screener-criteria` and
`position-exit-rules` / `equity-trade-decision` in the `Finance/` pipeline.
