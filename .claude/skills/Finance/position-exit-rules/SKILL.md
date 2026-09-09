---
name: position-exit-rules
description: Use when a position is about to be entered (or is held with no exit plan) and the exit rules need to be written down before the market makes the decision under pressure. Triggers include "what should my exit be on this", "where do I set the stop", "define my sell rules before I buy", "I own this and never set exit conditions", "help me set stop-losses / trim rules", or a stated entry price plus a thesis with no exit attached. It is a gate: it withholds "the entry plan is complete" until the user commits, in writing and as numbers, to (1) a hard price stop — a single level or % below entry that forces an exit with no discretion, never "a mental stop" or a range; (2) the thesis-invalidating events — for each clause of the user's own thesis, the specific observable metric or event that would prove that clause wrong, tied to the thesis, not generic "bad earnings"; (3) a position-size ceiling — the % of the portfolio at which the position gets trimmed regardless of conviction, which also caps how far a loser can be averaged down. A recommended fourth, the upside review trigger (a price or valuation that forces a deliberate re-check that the thesis still holds — not an automatic sale), keeps the rule set symmetric so winners are neither round-tripped nor panic-sold. Claude's job is to check each rule is a committed number or an observable event, that the invalidating events actually map to thesis clauses rather than just restating the price stop, and to produce the exit-rule block — it does not invent the thesis or the events for the user. This is where the disposition effect is removed at the process level: the exit is defined while the user is calm and unbiased, before entry. Not sizing the position or running the pre-trade checklist — that's `equity-trade-decision`, which consumes this skill's price stop as its stop-loss input. Not reviewing a position already held for whether its thesis still stands — that's `portfolio-thesis-audit`, whose "exit condition" precondition and research-required verdict point here to build one. Not options exit logic — covered calls, assignment, rolling change what "exit" means and are out of scope — that's `covered-call-decision`, which consumes this skill's price target as its strike floor. Not tax-lot selection or the mechanics of when to actually place the sell, and not portfolio-level target allocation (the size ceiling here is a per-position guardrail, not a rebalancing model). Not a bare conceptual question about how stop-losses or trailing stops work with no real position behind it — that's `learning-gate`. Not a "why do I keep getting whipsawed / what's wrong with my strategy" post-mortem treated as a debugging session — `problem-solving-gates` is software-only; here the job is the exit-rule set itself. Not a substitute for a financial advisor.
---

# Position Exit Rules

Almost everyone sets an entry price and a rough "I'll sell if it drops a lot." Then it drops,
loss aversion takes over, the rule was never a rule, and the position gets held or averaged
down. The disposition effect works precisely because the exit was never committed while the
user was calm. This skill is a **gate**: the entry plan is not complete until the exit rules
exist as numbers and observable events, written before entry. Claude checks the rules are
real — it does not author the thesis or the invalidating events.

The exit rules defined here feed forward: `equity-trade-decision` takes the **price stop** as
its stop-loss input when it sizes the position.

## What this does not do

- **Size the position / run the pre-trade checklist.** Fundamentals, technical trend,
  relative performance, entry timing, cycle stage, share count from a risk budget — that's
  `equity-trade-decision`. It consumes the price stop this skill produces; it does not
  re-derive the exit rules.
- **Audit a held position's thesis.** Whether an existing holding still has a live reason to
  be owned is `portfolio-thesis-audit`. That skill's "exit condition" precondition and its
  RESEARCH REQUIRED verdict route *here* when the exit rule is missing and needs building.
  This skill takes the thesis as given and asks only "what would end the position".
- **Options exit logic.** Covered calls, cash-secured puts, assignment, rolling — "exit"
  means something different when a short option is involved. Name the gap and stop; that's
  `covered-call-decision` territory (separate skill).
- **Tax lots and sell mechanics.** Which lot to sell, wash-sale timing, limit vs. market —
  this skill defines *when the rule triggers*, not how the order is placed.
- **Portfolio target allocation.** The size ceiling here is a per-position guardrail that
  forces a trim; it is not a model of what the whole book should look like.
- **Answer a bare conceptual question.** "How does a trailing stop work", "what's a good
  stop-loss percentage in general" with no real position is `learning-gate`.

---

## The precondition — four rules, committed by the user

Before the entry plan is called complete, the user supplies, for **this specific position**:

1. **Hard price stop.** One number — a price level, or a % below the entry that converts to a
   price. It forces an exit with no discretion when hit. Not a range ("15–20%"), not "a
   mental stop", not "I'll see how it looks". If the user won't commit a single number, that
   is the finding — say so and stop. Decide now, too, whether and at what gain the stop
   moves up (e.g. to breakeven at +X%) — a static stop is a valid choice, but it is a choice
   made pre-entry, not a thing to improvise later.
2. **Thesis-invalidating events.** The user first states the clauses of their own thesis (the
   two or three things that have to be true for the position to work). For **each clause**,
   they name the specific observable event or metric that would prove that clause wrong — and
   it must be tied to the clause, not a generic "a bad quarter". Example: thesis clause
   "gross margin expands past 40% as the new segment scales" → invalidating event "two
   consecutive quarters with gross margin below 35%". At least one real invalidating event;
   if every one the user gives is just the price falling, the thesis check collapses into the
   price stop and needs redoing.
3. **Position-size ceiling.** One number — the % of the portfolio at which the position is
   trimmed back regardless of conviction. It caps a winner that quietly compounds into an
   outsized share of the book, and it is the hard limit on how far a losing position can be
   averaged down before the add is disallowed.
4. **Upside review trigger** (recommended, not strictly required). A price or valuation level
   that forces a deliberate re-check — "at this price, is the thesis still doing the work, or
   is this now just a rising market?" — **not** an automatic sale. Its absence is allowed but
   noted; without it, "luck read as skill" on a winner runs unchecked.

If the user has **standing house rules** (e.g. "I always stop at 25% and cap any position at
8%"), rules 1 and 3 can be satisfied by stating that they apply here — but they still get
written into the block, and the user can override them for this position with a reason. Rule
2 is always specific to this position and is never a standing default.

Claude's contribution once the four are supplied is narrow:

- Check rule 1 is a single number, not a range or a "mental" stop.
- Check each rule-2 event is **observable** (a third party could tell it had happened) and
  **mapped to a named thesis clause**, not floating.
- Check rule 3 is a number and is below any level the user has already exceeded elsewhere.
- Produce the exit-rule block. Do not fill in a thesis clause or an invalidating event the
  user did not give.

---

## The exit-rule block

Goes **before** "you're good to enter" / any confirmation the plan is done. Every line
appears; an unknown is written `not supplied — ask: <the question>`, never omitted.

```
Position exit rules — <TICKER>

Entry reference:          $<n>/share  (the level the rules are measured from)
Standing house rules:     <"25% stop, 8% cap" applied | none — set per position>

1. HARD PRICE STOP
   Level:                 $<n>/share   (<pct>% below entry) — single number, no discretion
   Check:                 <OK — one committed number | FLAG: a range / "mental stop" / not
                          supplied — not a rule yet>

2. THESIS-INVALIDATING EVENTS
   Thesis clause A:       <the user's words>
     Invalidating event:  <the observable event/metric that disproves clause A>
     Observable?          <yes | no — restate it so an outsider could confirm it fired>
     Mapped to clause?    <yes | FLAG: generic, not tied to A>
   Thesis clause B:       <...>
     Invalidating event:  <...>
     [repeat per clause]
   Check:                 <OK — at least one real, clause-mapped event | FLAG: every event
                          is just price falling → collapses into the stop, redo>

3. POSITION-SIZE CEILING
   Trim above:            <pct>% of portfolio — regardless of conviction
   Check:                 <OK — a committed number | FLAG: not supplied / above a level
                          already exceeded>
   Averaging-down limit:  adding to this position is disallowed once it is at or above the
                          ceiling; any add below it is a fresh `equity-trade-decision`, not a
                          reflex

4. UPSIDE REVIEW TRIGGER
   Re-check at:           <$<n>/share or <valuation level> — forces a thesis re-check, NOT an
                          automatic sale | not set — noted: "luck read as skill" runs
                          unchecked on the upside>

Feeds forward:            price stop $<n> → `equity-trade-decision` stop-loss input for sizing
Red flags:                <price stop is a range or mental | invalidating events all
                          price-based | no size ceiling | none>
```

---

## Red flags — the rules aren't done

- A price stop given as a range, a "mental stop", or "I'll watch it" — that is not a
  pre-committed rule and the whole point is pre-commitment.
- Thesis-invalidating events that are all just "the price drops" in different words — the
  position then has a stop and no thesis check, and a thesis that dropped 30% on news the
  user would have ignored still gets held.
- An invalidating event that isn't observable from outside ("if it stops feeling right") or
  isn't tied to a stated thesis clause.
- No position-size ceiling — the mechanism that both caps a compounding winner and stops
  open-ended averaging down is simply absent.
- Claude writing the thesis clauses or the invalidating events, then checking its own work.
- Exit rules loosened right after a drawdown (stop moved down, ceiling raised) — that is the
  disposition effect editing the rule instead of following it. Rules change on new thesis
  information, not on price pain.

---

## Example invocations

> "I'm about to buy XYZ at $40, thesis is share gains plus margin expansion. Where do I set
> my exits?"

Ask for: the single price-stop number, the clauses of the thesis and one observable
invalidating event per clause, the size-cap %, and optionally an upside review level. Produce
the block. Don't propose the invalidating events — make them derive each from their own
thesis clause.

> "I've held ABC for a year and realized I never set any sell rules."

In scope — same four rules, measured from the current price rather than an entry. If the
question is really "should I still own this at all", that's `portfolio-thesis-audit` first,
then back here to build the rules for whatever survives.

> "How many shares of XYZ should I buy with a $10k risk budget?"

Not this skill — `equity-trade-decision`. It will use the price stop defined here as its
stop-loss input.

> "What's the difference between a stop-loss and a trailing stop?"

No real position — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the exit-rule block in chat. Copy the
`position-exit-rules/` directory into another repo's `.claude/skills/`. Chains with
`equity-trade-decision` (sizing consumes the price stop) and `portfolio-thesis-audit` (which
routes here when a held position has no exit rule).
