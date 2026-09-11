---
name: equity-research-writeup
description: |-
  Research a single public company before deciding to own it. Triggers: "research TICKER", "deep dive on X", "analyse the fundamentals", "help me build my thesis". A gate: no finished writeup until the user fills each section in their own words with specific figures, each tied to a filing or earnings call. Eight sections are the process: the business; unit economics; competitive position (evidence, not "moat"); 3–5yr financial trend; valuation reasoning; the bear case (user writes it); a falsifiable thesis; what would change my mind. Claude supplies structure and checks every claim has a figure and a source; it does not author content or fetch data. Sections 7–8 feed `equity-trade-decision` and `position-exit-rules`. Not `watchlist-screener-criteria` (the numeric pre-filter first), not `equity-trade-decision` (sizes the trade after), not `portfolio-thesis-audit` (a held position), not ETFs (`etf-selection`), not a private-company buy (`seller-financing-evaluation`).
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
  should clear it before a full writeup is worth the time; this skill assumes that happened. A
  writeup on an unscreened name is still legitimate — flag that the screen wasn't run; the
  pre-filter just exists to reserve writeup effort for names worth it.
- **Size or time the trade.** `equity-trade-decision` does that, *after* this. Its pre-trade
  checklist item 1 ("fundamentals reviewed") is satisfied by a completed writeup here.
- **Re-check a held position's thesis.** `portfolio-thesis-audit` does that. "Should I still
  own X" starts there; it routes back here when the answer needs a fresh writeup.
- **Evaluate an ETF or fund.** A rules-based basket is judged on expense ratio, index
  methodology, AUM/liquidity, tracking error, and holdings overlap — not a business, moat,
  and bear case. That's `etf-selection` — the funds counterpart to this skill.
- **Build a DCF model.** This forces the valuation *reasoning* — the multiple against history
  and peers, the growth and margin the price implies, the yield you're paid to wait — not a
  cell-by-cell spreadsheet.
- **Analyse a private-company acquisition.** That's `seller-financing-evaluation` territory —
  no public filings, a different diligence process.
- **Answer a bare conceptual question.** "How do I read a 10-K", "what is FCF", "how does a
  DCF work", "help me get better at analysing companies" with no company on the table is
  `learning-gate`.
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

"Just give me the analysis", "no time to read the 10-K", "you already know this stuff" are
reasons to want the gate skipped, not a release of it — Claude still authors no section,
supplies no figure, and runs no valuation; prior knowledge is offered only as unverified
pointers to check against the filing.

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
Equity research writeup — <TICKER>   ·   <date>   ·   screen cleared: <date | not run — flag, not a blocker>

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
