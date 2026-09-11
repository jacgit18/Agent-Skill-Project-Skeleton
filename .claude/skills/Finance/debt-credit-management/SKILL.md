---
name: debt-credit-management
description: |-
  Decide a real credit-card action — not a general credit question: "should I close this card", "which card do I pay off first", "help me clean up my cards". A gate: no close/consolidate/keep verdict until the user supplies, per card, APR, balance, limit, annual fee, and rewards category — plus utilization across ALL cards combined (total balances ÷ total limits), the number that moves the score. Before any close/consolidate call: closing a card lowers total limit while balances stay the same — raising combined utilization — and shortens average account age; both can hurt the score the cleanup was meant to protect. Payoff order (highest APR first) reads off the same table. Not `asset-allocation-policy` — a high-APR balance competing with the emergency-fund target is named here, not solved there. Not a bare concept question ("what is utilization", "how does APR work") with no real cards — that's `learning-gate`. Not a substitute for a financial advisor or credit counselor.
---

# Debt & Credit Management

"Clean up my cards" feels like tidying — close the ones you don't use, pay off the smallest
balance first, done. Both instincts can backfire: closing a card removes its limit from the
denominator of your utilization ratio while your balances stay the same, so utilization can
go *up* right when you thought you were improving it; and it shortens your average account
age, another scoring factor. Paying the smallest balance first ("snowball") feels like
progress but costs more in interest than paying the highest-APR balance first ("avalanche")
— a legitimate choice if it's the one that actually keeps someone paying, but a choice, not
something to hand out as the objectively right answer without naming the trade.

This skill is a **gate**: no close/consolidate/pay-off-order verdict until every card on the
table has real numbers behind it, and the combined-utilization and account-age effects of any
proposed close are computed, not assumed.

## What this does not do

- **Installment debt.** Mortgages, auto loans, student loans, personal loans — fixed
  amortization schedules with no utilization concept and no "close the account" lever. Name
  the gap; this skill is revolving (credit-card) debt only.
- **Route capital between debt paydown and investing.** A high-APR balance competing with the
  emergency-fund target — or with a retirement contribution — for the next dollar is a real
  tension this skill names (an APR above what the portfolio can reliably earn after tax is
  usually the stronger claim on the dollar) but does not resolve against the investable pool;
  that's `asset-allocation-policy`'s capital map.
- **Debt consolidation loan or balance-transfer mechanics in depth.** It flags the shape (a
  lower blended APR vs. a transfer fee and a promotional-rate cliff) and stops; it does not
  underwrite a specific loan or card offer.
- **Dispute inaccurate credit reporting.** A wrong balance or a fraudulent account on a report
  is a dispute with the bureau or issuer, not a decision this skill models. Name it and stop.
- **Answer a bare conceptual question.** "What is credit utilization", "how does APR work",
  "how is a credit score calculated" with no real cards on the table is `learning-gate`.
- **Replace a financial advisor or a nonprofit credit counselor.** Named and deferred for debt
  loads that need a structured repayment plan or hardship program, not computed here.

---

## The precondition — every card, real numbers, one goal named

For **each** card the user holds:

| Field | Why it matters |
|---|---|
| Issuer / card name | So the table is unambiguous when there are several |
| APR | Drives both the interest cost and the payoff-order math |
| Current balance | Half of both the per-card and combined utilization ratio |
| Credit limit | The other half; also what closing the card removes |
| Annual fee | A fixed cost the rewards need to actually clear |
| Rewards category / value | So "I keep it for the points" is a number, not a feeling |
| Account age (opened date, or years) | What a closure would remove from the average |

Then, **combined utilization** — total balances ÷ total limits across every card, not any
single card's ratio, since that combined number is what scoring models weight most. A card
sitting at 90% alone is a different problem if the other four are empty than if they're all
similarly loaded.

Finally, the user names **the goal**, because these can conflict and the skill will not pick
for them:

- **Pay down fastest / cheapest** — avalanche order, highest APR first, regardless of score
  effects along the way.
- **Protect or improve the credit score** — utilization and account age become the binding
  constraints; a close is now a candidate action to screen, not a default.
- **Simplify — fewer cards to track** — a real goal on its own, but named explicitly so it
  isn't reached by accident while chasing a payoff or a score, and its cost (the utilization
  and age effects below) is priced in on purpose.

A card missing any field is `not yet known — ask: <the question>`, never assumed favorable. A
verdict given with no goal named is a guess at what the user actually wants.

---

## The decision block

Goes **before** any "close this one" / "pay this one first" answer.

```
Debt & Credit table — <date>

Card              APR    Balance   Limit   Ann.fee  Rewards value   Age
<name 1>          <pct>  $<n>      $<n>    $<n>     $<n>/yr or n/a  <yrs>
<name 2>          <pct>  $<n>      $<n>    $<n>     $<n>/yr or n/a  <yrs>
[one row per card]

Combined utilization:   $<sum balances> / $<sum limits> = <pct>%
Average account age:    <n> years, weighted by <count | balance>

Stated goal:             <pay down fastest | protect score | simplify | more than one — named
                         as competing, not merged>

Payoff order (avalanche): <ranked by APR, highest first> — interest-cost-optimal
[If snowball or another order is requested]: <ranked as requested> — named as a preference
                         trade, not the interest-optimal order

Proposed action:          <e.g. "close card X">
  Utilization if taken:   <new combined %> — <improves | worsens, and by how much>
  Avg age if taken:       <new average> — <improves | worsens>
  Net effect on goal:     <helps | hurts | mixed — say which>

Red flags:                <verdict given with a card's fields unknown | utilization computed
                          per-card only | close proposed with no before/after utilization or
                          age computed | no goal stated | none found>
```

---

## Red flags — the recommendation isn't done

- A close/consolidate/keep verdict given before every card's APR, balance, limit, fee, and
  rewards value is on the table.
- Utilization quoted per-card without the combined figure across all cards.
- A card closure recommended ("you don't use it, cut it") with no computed before/after
  combined utilization and average account age.
- Snowball or another non-APR payoff order presented as the interest-optimal choice instead
  of a named behavioral trade-off.
- No goal stated — "clean up my cards" acted on as if pay-down-fastest, protect-score, and
  simplify were the same request.
- A rewards card's value asserted ("I keep it for the points") with no annual spend or point
  value behind the number.
- Installment debt (a mortgage, a student loan) run through the utilization/closure framing
  built for revolving credit.

---

## Example invocations

> "I have 11 credit cards. Which ones should I close?"

Gate. Build the full table first — every card's APR, balance, limit, fee, age. Ask the goal.
Compute combined utilization and average age *before* naming any candidate to close, then
show the before/after for each candidate against the stated goal.

> "Should I pay off my Chase card or my Amex first?"

Payoff order from the same per-card table — avalanche (highest APR) unless the user states a
different goal. Two cards is still the full precondition; don't skip the table because the
comparison feels small.

> "I have a $3k emergency fund goal but also a card at 24% APR — which comes first?"

Names the tension explicitly (a 24% guaranteed "return" from paying it down usually beats
building cash past a thin safety buffer) but does not set the capital-routing policy — that's
`asset-allocation-policy`'s capital map, which this skill points to rather than overrides.

> "What's a good credit utilization ratio to aim for?"

No real cards on the table — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the table and verdict in chat. Copy the
`debt-credit-management/` directory into another repo's `.claude/skills/`. Names but does not
resolve the capital-routing tension with `asset-allocation-policy`; otherwise standalone.
