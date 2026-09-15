---
name: rebalancing-execution
description: |-
  Turns an already-flagged allocation drift into an actual trim/buy plan — the step `asset-allocation-policy` names but doesn't do, and `weekly-portfolio-review` flags but doesn't execute. Triggers: "how do I actually rebalance", "which positions do I trim to get back to target", "I'm over my ceiling, what do I do". Applies the already-set tax-aware order (new money first → tax-advantaged accounts → taxable only past the stated threshold) mechanically, computes real dollar/share amounts, and hands a confirmed taxable sale to `tax-lot-selection` for the lot. Never judges whether a thesis still holds — a drift on a thesis-intact winner is this skill; a drift from a broken thesis is `portfolio-thesis-audit`/`position-exit-rules` first. Not `asset-allocation-policy` (sets bands/order), not `weekly-portfolio-review` (flags the drift), not `tax-lot-selection` (picks the lot), not a brand-new name (`equity-trade-decision`/`watchlist-screener-criteria`).
---

# Rebalancing Execution

`asset-allocation-policy` sets the bands, the trigger, and the tax-aware order — then says so
itself: "Execute a rebalance... that follows the trigger and the tax-aware ordering this
policy *sets*." `weekly-portfolio-review` step 5 flags a breach and stops, by design — "a
guardrail check, not a rebalancing model." Nothing in the catalog actually turns a real,
flagged drift into "sell exactly this many shares of exactly this position, in this order."
Left there, a real breach either gets executed on a guess (wrong account order, no tax
awareness, an arbitrary trim size) or sits flagged and ignored because nobody translated the
flag into an action. This skill is that translation step — mechanical, not judgmental: given
a breach that's already real, apply the policy's own already-set rules and compute the actual
plan.

Where it sits: `asset-allocation-policy` (sets bands + order) → `weekly-portfolio-review` step
5 (flags the breach) → **this** (turns the flag into a plan) → `tax-lot-selection` (picks the
specific lot, only if a taxable sale is actually required).

## What this does not do

- **Set the bands, the trigger, or the tax-aware order.** Those are `asset-allocation-policy`
  area 5 — this skill reads and applies them, verbatim, never invents its own ordering.
- **Flag the drift.** `weekly-portfolio-review` step 5 (or `asset-allocation-policy`'s own
  consistency check) is where a breach first surfaces. If nothing has flagged a real breach
  yet, this skill has nothing to execute — check there first, don't eyeball a percentage.
- **Judge whether a position's thesis still holds.** This is the single most important
  boundary: a position that's overweight because it *won* and the thesis is still intact is a
  **rebalance** — this skill. A position that's overweight (or the trigger for looking at all)
  because something about the original thesis broke is a **thesis question** —
  `portfolio-thesis-audit` (held position, keep/exit) or `position-exit-rules` (no exit rule
  existed yet). Confirm the thesis is intact before treating a breach as a rebalance; if it
  isn't, redirect there instead of trimming.
- **Pick the specific tax lot.** Once this skill confirms a taxable sale is genuinely
  necessary and computes the share count, `tax-lot-selection` picks which lot(s) — this skill
  supplies its required input (the share count and the reason: "rebalance trim"), never the
  lot choice itself.
- **Buy a brand-new name to fill an underweight sleeve.** If closing a gap means adding to an
  existing core/fund holding, this skill directs the dollars there. If it actually requires
  picking a new individual stock, that's `watchlist-screener-criteria` →
  `equity-research-writeup` → `equity-trade-decision` — name the gap, don't invent a pick.
- **Sell from runway or near-term-need money.** Those dollars are never a rebalance source,
  same rule `asset-allocation-policy` states for itself.
- **Answer a bare conceptual question.** "What is rebalancing", "how often should I rebalance
  in general" with no real breach on the table is `learning-gate`.

---

## The precondition — a real breach, a confirmed thesis, and the policy's own rules

1. **The breach, sourced.** Current % vs. target vs. band, from `weekly-portfolio-review` step
   5's flag, `asset-allocation-policy`'s own consistency check, or a `portfolio-thesis-audit`
   HOLD verdict on a position that's also over its ceiling — not an eyeballed guess. Name
   which kind: a single-position ceiling breach (`position-exit-rules` rule 3 / policy area 3),
   or a broader asset-class/sector/theme/geography band breach (policy area 4).
2. **Thesis confirmation.** For a single-position breach specifically: is the thesis still
   intact? If yes, this is a rebalance. If no, or unclear, stop and route to
   `portfolio-thesis-audit` (held position) or `position-exit-rules` (no exit rule on file) —
   don't execute a trim on a position that actually needs a keep/exit call first.
3. **New-money availability.** Is there fresh cash or a pending contribution, and how much? The
   policy's own order puts this first, always — a rebalance that reaches for a sale before
   checking this is skipping a step.
4. **Account map for the breached exposure.** Which accounts hold it, and each one's tax
   status (taxable vs. tax-advantaged) — needed to apply the order correctly.
5. **The policy's own rebalancing rule (area 5), pasted, not re-derived** — the trigger, the
   order, and the taxable threshold ("only if a band is badly breached — name the threshold").
   No policy on file at all → gate to `asset-allocation-policy` first; there's nothing to
   execute against.

If any of 1, 2, or 5 is missing, stop and get it — a trim computed against an unsourced breach,
an unconfirmed thesis, or an invented order isn't an execution plan.

---

## Applying the order

1. **New money + dividends first.** Compute how much of the gap fresh cash alone would close.
   Route it to the most-underweight sleeve/position per the policy's own contribution-routing
   rule (area 6). If this fully resolves the breach, stop here — no sale needed.
2. **Tax-advantaged accounts next.** If new money isn't enough, trim the overweight exposure
   inside Roth/IRA/401(k) accounts first — no tax event. Compute the exact share/dollar amount
   needed to bring the position back to target (or to the policy's stated stopping point, if it
   specifies "back to the band edge" rather than "back to target" — ask if the policy doesn't
   say, and default to target, flagged, if it's genuinely silent).
3. **Taxable only past the stated threshold.** Only if the breach is still real after 1–2, and
   only if it clears the policy's own named taxable-threshold, compute the exact share count
   that needs to sell in the taxable account. Hand this off to `tax-lot-selection` as "rebalance
   trim, <TICKER>, <n> shares" — the specific lot is that skill's job, not this one's.

---

## Output — the execution plan

```
Rebalancing execution — <date>   ·   source: <weekly-portfolio-review flag | policy consistency check | portfolio-thesis-audit HOLD-over-ceiling>

Breach:              <TICKER or asset class>   ·   current <pct>%  vs  target <pct>%  (band <pct>–<pct>%)
Breach type:          <single-position ceiling | asset-class/sector/theme/geography band>
Thesis confirmed intact:  <yes — proceeding as a rebalance | NO — redirect to
                          portfolio-thesis-audit / position-exit-rules instead, stop here>

Policy's own rule (area 5), as stated:  <trigger> · <order> · taxable threshold: <...>

Step 1 — new money:      $<n> available → closes $<n> of the gap  (<fully resolved | gap remains: $<n>>)
Step 2 — tax-advantaged: <account> → trim <TICKER> by <n> shares / $<n>   (<resolved | still short: $<n>>)
Step 3 — taxable:        <TICKER> → <n> shares need to sell, threshold cleared: <yes/no>
                          → hand to tax-lot-selection: "rebalance trim, <TICKER>, <n> shares"

Never touched:  <runway / near-term-need money — confirmed untouched>

Result:  <breach resolved | partially resolved, remaining gap $<n> — <why: threshold not
         cleared / new money insufficient and no taxable sale warranted yet>>
```

---

## Red flags — the plan isn't real

- A trim executed on a position whose thesis was never confirmed intact — the breach might
  actually be a thesis problem wearing a rebalancing label.
- The order skipped — reaching for a taxable sale before checking new money and tax-advantaged
  accounts first.
- A specific tax lot picked here instead of handed to `tax-lot-selection`.
- A taxable sale executed below the policy's own stated threshold, or with no threshold named
  at all.
- Runway or near-term-need money used as a rebalance source.
- A vague "trim some AAPL" with no computed share/dollar amount — that's not an execution plan.
- No `asset-allocation-policy` on file, or its area 5 rule never actually read before
  proceeding.

---

## Example invocations

> "My weekly review flagged my tech position over its ceiling and my equity sleeve 8 points
> over target — what do I actually do about it?"

This skill. Confirm the thesis is intact, check new-money availability, apply the order,
compute the real amounts, hand off a taxable trim to `tax-lot-selection` if one is needed.

> "My AAPL position grew to 22% of my book but I still believe in the thesis — should I trim?"

Thesis intact + over the ceiling = a rebalance. This skill, not `portfolio-thesis-audit`.

> "My XYZ position is overweight, and the reason I bought it — margin expansion — never
> actually happened."

Thesis question, not a rebalance — `portfolio-thesis-audit` first. This skill only picks up
once that's resolved (if anything survives to be rebalanced at all).

> "How much of my portfolio should be in tech?"

That's the band itself — `asset-allocation-policy`, not this skill.

> "OK, I need to sell 15 shares of AAPL to rebalance — which lot?"

Downstream — `tax-lot-selection`, once this skill has produced the share count.

---

## Portability

Repo-agnostic. Writes nothing; produces the execution plan in chat. Copy the
`rebalancing-execution/` directory into another repo's `.claude/skills/`. Sits between
`asset-allocation-policy`/`weekly-portfolio-review` (upstream — set the rule, flag the breach)
and `tax-lot-selection` (downstream — picks the lot once a taxable sale is confirmed).
