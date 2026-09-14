---
name: equity-investment-take
description: |-
  Gives Claude's own sourced, opinionated read on a specific public company — the business, the real numbers, competitive/bear-case evidence, and a bottom-line verdict with reasoning and a "what to consider" list — instead of gating the synthesis back to the user. Triggers: an explicit ask for Claude's own opinion — "what do you think about TICKER", "give me your take", "is TICKER a good investment", "should I buy TICKER", "give me the full verdict". Every figure is fetched live and cited, same tools and discipline as `equity-research-sourcing` — never fabricated from training knowledge, any gap flagged NOT VERIFIED. Not the default for "research TICKER" / "deep dive" — that stays `equity-research-writeup`'s gate; this only fires on an explicit ask for Claude's own opinion, a separate door, not that gate released under pressure. Not ETFs (not extended here yet), not a held-position re-check (`portfolio-thesis-audit`), not sizing or entering the trade (`equity-trade-decision`).
---

# Equity Investment Take

`equity-research-writeup` exists because a fluent, Claude-authored investment case feels like
research without being any — the user reads it, does nothing themselves, and risks capital on
figures nobody checked. That gate is correct and it should keep holding, including under
direct pressure ("just give me your take," "that's your job"). But refusing forever with no
real alternative just produces friction for a user who has genuinely decided they want
Claude's own opinion, sourced properly, rather than doing the section-by-section work
themselves. This skill is that alternative: a **separate, explicitly-invoked** door that does
the work and gives a real verdict — not the gate quietly caving, a different skill with
different rules that the user has to ask for directly.

Where it sits: parallel to `equity-research-writeup`, not inside it. Both start from "should I
own this stock" — which one answers depends entirely on whether the user asked for their own
gated process or for Claude's opinion.

## What this does not do

- **Become the default for "research TICKER" / "deep dive on X."** Those triggers still belong
  to `equity-research-writeup`. This skill fires only when the ask is unambiguously for
  Claude's own opinion — see the disambiguation table below. When in doubt, the gate wins;
  a Claude-authored verdict should never be the path of least resistance.
- **Release `equity-research-writeup`'s gate from inside that skill's own flow.** Pressure
  there ("just give me the analysis," "you already know this stuff") still does not release
  it — that skill's own red flags are unchanged by this one existing. What changes is that the
  refusal can now name a real, working alternative instead of a dead end: "if you want
  Claude's own take instead of doing this yourself, ask for it — that's a different skill,
  not this gate giving in." The user still has to ask for *this* skill on purpose.
- **Evaluate an ETF.** `etf-selection` stays a pure gate with no fast-take counterpart — a real
  gap, not silently absorbed here. Not extended yet.
- **Re-check a held position's thesis.** That's `portfolio-thesis-audit` — this skill is for a
  name not yet owned.
- **Size or enter a trade.** Once the verdict here leans toward buying, `equity-trade-decision`
  still does the position-size and entry-timing work; a verdict here satisfies its checklist
  item 1 the same way a completed `equity-research-writeup` does.
- **Skip real sourcing.** Same bar as `equity-research-sourcing`: every figure fetched live and
  cited, a gap flagged `NOT VERIFIED` rather than filled from training-data memory — the
  license to *interpret* is not a license to *fabricate*.

## When this fires vs. `equity-research-writeup`

| Ask | Skill |
|---|---|
| "Research TICKER," "deep dive on TICKER," a ticker about to be seriously worked through | `equity-research-writeup` — the gate, the default |
| "What do you think about TICKER," "give me your take," "is TICKER a good investment," "should I buy TICKER," "give me the full verdict" | **This skill** |
| Same phrasing, but ownership language — "my TICKER position," "should I still hold TICKER" | `portfolio-thesis-audit` — already owned, a different question than "should I buy" |
| Mid-`equity-research-writeup`, the user pushes back on writing a section themselves | Still `equity-research-writeup` — hold the gate, but name this skill by name as the real alternative if the user wants it |

A ticker named only as an example while the ask is still "research" stays with
`equity-research-writeup`. A bare "thoughts on TICKER" with no other context defaults to this
skill only once the user has made clear they want an opinion, not a walkthrough — if that's
unclear, ask which one, once, rather than guessing.

## The process

1. **Fetch.** Same tool set and sourcing discipline as `equity-research-sourcing`'s Fetch mode:
   business profile, income statement, balance sheet, cash flow, financial indicators, analyst
   ratings/targets, forecast EPS, peer positioning — each cited with source + as-of date.
2. **Search.** Targeted `WebSearch`/`WebFetch` for what structured data can't carry: what the
   company actually does in plain terms, competitive/bear-case evidence, any adverse reports
   (short-seller pieces, regulatory or consumer-complaint findings), IPO/lockup status if
   relevant, and anything recent enough to move the read.
3. **Synthesize.** Assemble the output block below. State a real verdict — buy-leaning,
   pass, or too-early-to-say — with explicit reasoning, not a hedge that avoids committing.
   Flag anything the sourcing couldn't verify rather than smoothing over the gap.

## Output block

```
Investment take — <TICKER>   ·   <date>   ·   screen cleared: <date | not run — flag, not a blocker>

Business:              <what it sells, to whom, how it earns money>        source(s): <...>
Key numbers:            <revenue growth, margin, FCF/OCF trend, balance sheet>  source(s): <...>
Valuation:              <multiple, vs guidance/history/peers>              source(s): <...>
Competitive position & bear case:  <evidence, incl. any adverse/short reports>  source(s): <...>
Structural risk factors: <float, beta/volatility, lockup status, technical extension vs analyst targets>

Consider / watch:
  - <specific factor to weigh>
  - <specific factor to weigh>
  [...]

Verdict:  <Claude's own opinion, stated plainly, with the reasoning — not just a rating>
What would change this read:  <specific events or data that would flip it>
```

## Red flags — the take isn't real

- A figure with no source name or as-of date — the same failure `equity-research-sourcing`
  exists to prevent, now with an opinion layered on top instead of nothing.
- A verdict delivered while a material input is `NOT VERIFIED`, without saying so plainly.
- This skill firing on a bare "research TICKER" with no explicit ask for an opinion — that's
  starvation of `equity-research-writeup`'s gate, the exact failure the disambiguation table
  exists to prevent.
- A verdict that's really a hedge ("could go either way, depends on the market") dressed up as
  an answer — the user asked for Claude's actual read, not a refusal wearing more words.
- The "consider/watch" list skipped — it's the point of this skill as much as the verdict is.

## Example invocations

> "What do you think about TICKER — I'm thinking about opening a position."

This skill, once it's clear the ask is for Claude's own opinion. Fetch, search, synthesize,
give a real verdict and a watch list.

> "Research TICKER for me — deep dive."

Not this skill — `equity-research-writeup`'s gate, the default for this phrasing.

> "I don't want to write out a business summary and a bear case, that's your job."

Inside an active `equity-research-writeup` conversation, this is pressure, not a release — the
gate holds. Name this skill directly as the real alternative; the user asking for it by name
or clear intent is what actually switches paths, not resistance to the section-by-section work.

> "Should I add to my TICKER position?"

Already held — `portfolio-thesis-audit`, not this skill.

> "TICKER looks good, size me a position."

The verdict conversation is over — `equity-trade-decision` for sizing and entry.

---

## Portability

Depends on the same tools as `equity-research-sourcing` (Webull's financial-data tools plus
`WebSearch`/`WebFetch`) — no portability story beyond what that skill already has. Writes
nothing to disk; the take is delivered in chat. Copy the `equity-investment-take/` directory
into another repo's `.claude/skills/`, alongside `equity-research-sourcing` and
`equity-research-writeup`.
