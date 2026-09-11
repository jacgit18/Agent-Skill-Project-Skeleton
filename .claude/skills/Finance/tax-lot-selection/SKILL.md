---
name: tax-lot-selection
description: |-
  Use once a sell is already decided — by position-exit-rules, portfolio-thesis-audit, a rebalance, or an assignment — and the question is which lot: "which shares of X do I sell", "specific ID vs FIFO", "will this trigger a wash sale". A gate: no answer until the user supplies each lot held (date, quantity, cost basis) and the goal — minimize this year's tax, avoid short-term treatment, or harvest a loss. Computes each lot's holding period and gain/loss, then picks lots matching the goal — a broker's FIFO default may differ from specific ID. Before any loss sale, checks the wash-sale window — 30 days either side, including a dividend-reinvestment buy — and flags a disallowed loss. Taxable accounts only; a Roth/IRA/HSA sale has no lot or gain/loss to track — name it and stop. Not `position-exit-rules` — decides whether/when to exit; this decides which shares once it has. Not a full tax return — names a CPA. Not a bare concept question with no real position — `learning-gate`.
---

# Tax Lot Selection

"Sell 20 shares of X" isn't a complete order in a taxable account — it's incomplete until
someone says *which* 20 shares. Left unsaid, the broker's default method picks for you, and
that default (often FIFO) tends to sell the oldest lot first, which is frequently the
lowest-cost-basis lot — the single choice most likely to maximize the gain realized, and the
tax owed on it. This skill is a **gate**: no lot answer until every lot is on the table, real
numbers behind it, and one goal named.

This skill does not decide **whether** to sell. It starts once `position-exit-rules`,
`portfolio-thesis-audit`, `weekly-portfolio-review`, or `covered-call-decision` has already
produced a sell (or assignment) and hands off the mechanical question of which shares.

## What this does not do

- **Decide whether or when to exit.** `position-exit-rules` sets the trigger (a price stop or
  thesis-invalidating event), `portfolio-thesis-audit` grades a held position keep/exit,
  `weekly-portfolio-review` flags a rebalance trim, `covered-call-decision` names an
  assignment. This skill starts only once one of those has already produced a sell and a share
  count — it does not re-derive or second-guess *that* decision.
- **A Roth, traditional IRA, or HSA sale.** No cost basis or capital-gain tracking exists
  inside a tax-advantaged account — there is no lot decision to make. Name the gap and stop;
  the upstream skill's exit/keep decision still applies, this skill's mechanics don't.
- **Compute the actual tax owed, or file anything.** It flags short-vs-long-term treatment and
  a wash-sale trap as facts about the sale; the dollar liability (marginal bracket, NIIT,
  state tax, AMT interactions) is a CPA's job, named and deferred.
- **Run a proactive, whole-portfolio tax-loss-harvesting scan.** This skill answers "which lot,
  for a sale already decided." Surfacing every unrealized loss across the whole book on a
  schedule is a different, broader pass — not built here.
- **Options assignment or exercise tax mechanics beyond which lot gets called.**
  `covered-call-decision` owns the premium and assignment math; this skill only picks which
  specific lot is delivered when more than one is eligible.
- **Answer a bare conceptual question.** "What's a wash sale", "how does FIFO differ from
  specific identification" with no real position on the table is `learning-gate`.

---

## The precondition — every lot, real numbers, one goal named

For the position being sold, in the taxable account:

1. **Every lot held** — acquisition date, share count, and cost basis (per-share and total).
   A position bought in one trade is still "one lot," stated as such.
2. **Current price**, to compute unrealized gain or loss per lot.
3. **The share count to sell.** This comes from the sell decision already made upstream — a
   price stop, a thesis exit, a rebalance trim, an assignment, or any other already-fixed
   reason with a real share count behind it (a debt payoff that needs the cash is a real
   source too, even though no Finance skill currently decides *that* tension for the user —
   `debt-credit-management` and `asset-allocation-policy` both name it without resolving it).
   This skill does not decide *how many* shares, only *which* ones make up that count.
4. **The goal**, because it changes which lots are the right answer:
   - **Minimize this year's tax bill** — usually the highest-cost-basis lot(s) first (smallest
     gain), or a losing lot deliberately harvested.
   - **Avoid triggering short-term treatment** — exclude any lot held under a year from the
     sale, even if it's a cheaper per-share choice, unless no other combination reaches the
     required share count.
   - **Simplicity / already using the broker's default** — confirm which lot(s) that default
     (state it — FIFO, average cost, or an existing specific-ID election) actually selects; no
     optimization attempted.

A lot missing date, quantity, or cost basis is `not yet known — ask`, never assumed. A
selection given with no goal stated is a guess at what the user actually wants.

---

## The lot-selection block

Goes **before** any "sell these shares" confirmation.

```
Tax lot selection — <TICKER>, <account, e.g. "taxable brokerage">

Lot   Acquired     Qty    Cost basis/sh   Current price   Unrealized G/L   Holding period
1     <date>       <n>    $<n>            $<n>             $<n>            <ST | LT>
2     <date>       <n>    $<n>            $<n>             $<n>            <ST | LT>
[one row per lot]

Shares to sell:        <n>   (from <position-exit-rules stop | portfolio-thesis-audit exit |
                        rebalance trim | assignment> — not decided here)
Stated goal:            <minimize tax | avoid short-term | broker default>

Lots selected:           <lot IDs and share counts>
Realized gain/loss:      $<n> total   —  ST: $<n>   LT: $<n>
Broker default check:    <matches selection | DIFFERS — broker's FIFO/avg-cost would instead
                         sell <which lots>; specific ID must be elected at trade time>

Wash-sale check (only if any selected lot is a loss):
  Same/substantially-identical security bought <n> days before this sale?  <yes — loss of
                         $<n> disallowed, added to new lot's basis | no>
  Planned to buy back within 30 days after?      <yes — flag before selling | no>
  Automatic dividend reinvestment active on this position?  <yes — check DRIP dates fall
                         inside the window | no>

Red flags:               <no per-lot table | broker default assumed without confirming |
                         loss sale confirmed with no wash-sale check | none found>
```

---

## Red flags — the answer isn't done

- A lot-selection answer given without an actual per-lot table (date, quantity, cost basis for
  every lot, not just the one being proposed).
- The broker's default method (often FIFO) assumed without the user confirming it — many
  brokers let the user elect average-cost or specific identification, and using the wrong
  assumption silently changes the tax outcome.
- A loss sale confirmed with no wash-sale check, or a check that ignores automatic dividend
  reinvestment (a DRIP buy inside the 61-day window is a common invisible trigger).
- A short-term gain triggered by picking a recently-acquired, cheaper-per-share lot without
  naming the tax-rate difference against a long-term lot that was also available.
- This skill asked to also decide *whether* to sell — the sell decision's source (a price
  stop, a thesis exit, a rebalance trim, an assignment, or any other already-fixed decision
  with a real share count) must be named before lot selection proceeds.
- A Roth/IRA/HSA position run through this skill's gain/loss or wash-sale mechanics as if it
  were taxable.

---

## Example invocations

> "`position-exit-rules` just triggered my stop on 50 shares of NOBL in my taxable account.
> Which shares do I actually sell?"

Gate. Get every NOBL lot in that account (date, quantity, cost basis), the current price, and
the goal. Produce the table; run the wash-sale check if any selected lot shows a loss.

> "I want to sell my worst-performing lot of XYZ to harvest a loss before year-end."

Same gate, plus an explicit wash-sale check: has XYZ, or a fund tracking a substantially
identical index, been bought (including any DRIP) within 30 days either side of the sale date?

> "Should I sell this position at all?"

Not this skill. `position-exit-rules` if there's no exit plan yet, `portfolio-thesis-audit` if
it's a held-position keep/exit call. This skill starts once that answer is yes.

> "What's the difference between FIFO and specific identification?"

No real position — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the lot table and wash-sale check in chat. Copy the
`tax-lot-selection/` directory into another repo's `.claude/skills/`. Downstream of
`position-exit-rules`, `portfolio-thesis-audit`, `weekly-portfolio-review`, and
`covered-call-decision` — consumes their sell decision, never makes one.
