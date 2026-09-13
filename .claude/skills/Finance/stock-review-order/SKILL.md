---
name: stock-review-order
description: |-
  Quick reference: the order to look at a stock in, when no ticker is on the table yet. Triggers: "what order should I look at this stuff in", "walk me through examining a stock", "how do I examine a stock", "what's the process for researching a ticker", "what should I check first on Webull". Not a gate — returns the eight-step numbered checklist directly, one line per step, no forcing sections and no blocking on sourced figures. Steps: numeric pre-screen, the business in plain terms, unit economics, competitive position, 3-5yr financial trend, valuation (last, not first), the bear case, thesis + invalidation events. Step 1 defers to `watchlist-screener-criteria` (owns the real numeric screen); the deep steps mirror `equity-research-writeup`'s eight sections (owns the gated writeup with sourced figures) — this skill names the sequence, that one does the work. If a specific ticker is named and the user clearly wants to research it now, hand off to `equity-research-writeup` instead of answering inline.
---

# Stock Review Order

The failure this prevents is small but real: asked "what order should I look at a stock in",
Claude free-associates a plausible-sounding list from memory — sometimes leading with
valuation, sometimes skipping the bear case entirely — and the sequence is different every
time it's asked. This skill is **not a gate**. It exists so the answer to "what's the order"
is the same fixed sequence every time, handed over immediately, with no section-filling
required. Filling any section in with real, sourced content is `equity-research-writeup`'s
job, not this one's.

## When this fires vs. when it doesn't

| Ask | Skill |
|---|---|
| "What order should I look at a stock in?" / "walk me through how to examine a stock" / no ticker named | **This skill.** Return the checklist below. Nothing to fill in. |
| "Research TICKER" / "deep dive on X" / a specific ticker the user is about to seriously work through | `equity-research-writeup`. Say so and hand off — don't run the checklist inline as a substitute for the gated writeup. |
| "What should my screen criteria be?" / "does TICKER pass my screen?" | `watchlist-screener-criteria` owns the actual numeric screen (thresholds, disqualifiers). This skill's step 1 just names that it comes first. |
| "What's a good ROIC threshold" / "how does a DCF work" with no stock in view | `learning-gate` — a bare concept question, not a process reminder. |

A ticker mentioned only as an example ("like, say, AAPL") while the ask is still "what's the
order" stays here — answer the checklist, don't pivot into researching AAPL.

## The checklist

```
Stock review order

1. Numeric pre-screen        Does it clear your written screen criteria (style,
                              thresholds, disqualifiers)? → watchlist-screener-criteria
2. The business, plainly     What it sells, to whom, and how it makes money.
3. Unit economics            The 2-3 numbers that actually move the P&L.
4. Competitive position      Evidence it can defend pricing/share — not "moat".
5. Financial trend (3-5y)    Revenue, margin, FCF, share count, leverage.
6. Valuation                 Multiple vs. history and peers — last, not first.
7. The bear case             The strongest argument against, written by you.
8. Thesis + invalidation     What has to stay true; what would prove it wrong.
```

Hand back this block as-is (or lightly reworded to fit the conversation) — don't expand any
line into a worked section, don't ask the user to fill anything in, don't request sourced
figures. That's the point of the disambiguation above: this is the map, not the hike.

## Why this order

- **Pre-screen first** so time isn't spent on a name that was never going to clear the
  user's own bar.
- **Business and unit economics before competitive position** — you can't judge whether an
  edge is defensible until you know what's actually being defended.
- **Financial trend before valuation** — a multiple means nothing without the trend it's
  being paid for.
- **Valuation before the bear case, not first** — pricing the stock before stress-testing the
  thesis anchors the bear case to "why isn't this cheaper" instead of "what actually breaks
  this".
- **Bear case before the thesis** — a thesis written before the strongest counter-argument is
  confirmation-seeking; this order forces the counter-argument onto the table first.

## Example invocations

> "What order should I look at this stuff in before I research a stock?"

Return the eight-step block. No ticker in view, nothing to gate.

> "Walk me through examining a stock — I don't have one in mind yet, just want the process."

Same — the checklist, as-is.

> "What order should I check NVDA in?"

A specific ticker with clear research intent — hand off to `equity-research-writeup` for the
gated eight-section writeup rather than running this lighter checklist as a substitute.

> "Does PLTR pass my screen?"

Not this skill — `watchlist-screener-criteria` Screen mode.

---

## Portability

Repo-agnostic. Writes nothing; returns the checklist in chat. Copy the
`stock-review-order/` directory into another repo's `.claude/skills/`. Sits in front of the
`Finance/` equity pipeline as a memory aid, not a pipeline stage itself — it points at
`watchlist-screener-criteria` (step 1) and `equity-research-writeup` (steps 2-8, done for
real) rather than replacing either.
