---
name: retirement-contribution-sequencing
description: |-
  Decide the funding order for new retirement dollars across more than one account — 401(k), HSA, Roth IRA, rollover IRA, taxable: "where should my next contribution go", "am I maxing my match", "should I do a backdoor Roth". A gate: no answer until the user supplies, per account, this year's contributions so far and the limit remaining, the employer match formula + capture status, HSA eligibility (on an HDHP), and — if income is near the Roth phase-out — the existing pre-tax IRA balance (the backdoor-Roth pro-rata trap). Applies the standard hierarchy — full match, HSA, Roth (direct or backdoor), rest of the 401k, taxable — against the real limits and dollars supplied, never assumed. Names, doesn't resolve, competing high-interest debt (`debt-credit-management`) or the asset-class choice once money lands (`asset-allocation-policy`). Not backdoor-Roth conversion tax-form mechanics — names a CPA. Not a bare concept question with no real accounts — `learning-gate`.
---

# Retirement Contribution Sequencing

"Max your 401(k) match, then your HSA, then your Roth" sounds obvious once someone says it —
and yet unclaimed employer match is walked-away-from money, a Roth contribution made over the
income limit has to be unwound, and a backdoor Roth done while an old rollover IRA still holds
pre-tax dollars quietly makes part of the conversion taxable. None of that is visible from "I
have $500 extra a month, where should it go" — it only shows up once every account's real
numbers are on the table. This skill is a **gate**: no funding-order answer until they are.

## What this does not do

- **Set the target asset allocation, or pick which fund fills it, once the dollar lands in an
  account.** `asset-allocation-policy`'s contribution routing decides which asset class the
  next dollar buys inside whichever account this skill names; `etf-selection` /
  `equity-trade-decision` / `watchlist-screener-criteria` pick the specific security. This
  skill only sequences *which account* — the tax wrapper — gets the dollar first.
- **Decide whether to pay down debt instead of contributing.** `debt-credit-management` owns
  that decision. This skill names the tension — an unclaimed match still comes first
  regardless, but beyond that, a high-APR balance often outguns any contribution past the
  match — without resolving it, the same posture `asset-allocation-policy` already takes on
  this exact tension.
- **Walk the actual backdoor-Roth conversion or file the paperwork.** Flags the pro-rata trap
  and the mechanical shape (contribute nondeductible to a traditional IRA, convert to Roth)
  at a high level; the actual Form 8606 filing and edge cases are a CPA's job, named.
- **Place accounts in the capital map or set investable-pool targets.** That's
  `asset-allocation-policy` input 1. This skill assumes the accounts already exist there and
  only sequences new contributions among them.
- **Answer a bare conceptual question.** "Why max the match first", "what is a backdoor Roth"
  with no real accounts and numbers on the table is `learning-gate`.

---

## The precondition — every account, real numbers, the facts that change the order

1. **New dollars available** this period (per paycheck or a lump sum), and whether it's a
   one-time allocation or a recurring split to set going forward.
2. **Per account** — type (401(k)/other employer plan, HSA, Roth IRA, traditional/rollover
   IRA, taxable), this year's contributions so far, and the annual limit remaining. An account
   already maxed is not a candidate this period regardless of where it'd otherwise rank.
3. **Employer match formula** (e.g. "100% up to 3% of pay, 50% up to 5%") and whether it is
   currently being fully captured. An unclaimed match is the single highest-priority gap —
   walking away from it is a guaranteed-return loss no market return beats, and it outranks
   every other line below.
4. **HSA eligibility** — is the user actually enrolled in a qualifying High-Deductible Health
   Plan? An HSA offered by name means nothing if the underlying plan doesn't qualify; don't
   assume eligibility from "my employer offers an HSA."
5. **Income relative to the Roth MAGI phase-out**, and — if at or near it — the user's
   existing pre-tax IRA balance (traditional, rollover, or SEP, anywhere, including an old
   401(k) rollover). This is the pro-rata-rule input: converting to Roth while pre-tax IRA
   money exists anywhere makes part of every future conversion taxable, not just the new
   contribution — a trap that costs real money when skipped.
6. **Any high-interest debt** the user is weighing against these same dollars — named here,
   sized and decided in `debt-credit-management`.

A missing account or figure is `not yet known — ask`, never assumed favorable to the order.

---

## The sequencing block

Goes **before** any "put it here" answer.

```
Retirement contribution sequencing — <date>

New dollars this period:   $<n>   (<one-time | recurring per <period>>)

ACCOUNTS
  401(k) / employer plan:    contributed $<n> of $<n> limit  ·  match: <formula> — captured?
                             <yes — fully captured | NO — $<n>/period still unclaimed>
  HSA:                       contributed $<n> of $<n> limit  ·  HDHP eligible? <yes | no —
                             not a candidate this period>
  Roth IRA:                  contributed $<n> of $<n> limit  ·  MAGI vs. phase-out: <under |
                             near | over — backdoor required>
  Traditional/rollover IRA:  balance $<n>  ·  <pro-rata trigger if a backdoor Roth is in play>
  Taxable brokerage:         <default once tax-advantaged space is full>

COMPETING CLAIM (named, not resolved here)
  High-interest debt:        <none | $<n> at <pct>% APR — see debt-credit-management before
                             funding anything past the unclaimed match>

SEQUENCE APPLIED TO THIS PERIOD'S $<n>
  1. Employer match (if unclaimed):   $<n>  →  <account>
  2. HSA (if eligible, room left):    $<n>
  3. Roth IRA — direct or backdoor:   $<n>  ·  <pro-rata check: CLEAR | FLAG — pre-tax IRA
                                       balance of $<n> makes part of any conversion taxable>
  4. Rest of 401(k) up to its limit:  $<n>
  5. Taxable brokerage:               $<n>   (routed by asset-allocation-policy from here)

Red flags:                  <match not fully captured | HSA/HDHP eligibility assumed, not
                             confirmed | Roth/backdoor recommended with no pro-rata check |
                             debt tension resolved inline instead of named | none found>
```

---

## Red flags — the sequence isn't done

- Match not fully captured — nothing else in the sequence matters until this line is
  resolved; recommending anything else first is the single most common mistake this gate
  exists to catch.
- A Roth or backdoor-Roth answer given with no check of the MAGI phase-out, or with a
  pre-tax IRA balance sitting unexamined anywhere.
- HSA prioritized — or skipped — without actually confirming HDHP enrollment.
- A sequencing order given as generic textbook advice ("max your 401k") with no real
  limits-remaining numbers behind any line.
- The debt-vs-contribution tension resolved inline (a specific dollar amount diverted to debt
  paydown decided here) instead of named and handed to `debt-credit-management`.
- A specific fund, ticker, or asset-class split recommended for the dollars once they land —
  that's `asset-allocation-policy` / `etf-selection` / `equity-trade-decision`, not this skill.

---

## Example invocations

> "I get a 100% match up to 3% on my 401(k), I'm on an HDHP with an HSA option, and I have
> $500/month extra. Where should it go?"

Gate. Build the account table — contributions so far and limits remaining for each — confirm
the match is actually being captured, confirm real HDHP/HSA eligibility. If the match isn't
full, that's first regardless of anything else; then HSA; then the rest of the hierarchy.

> "My income just went over the Roth limit — should I do a backdoor Roth?"

Gate on the pro-rata check specifically: any pre-tax IRA balance anywhere — including an old
401(k) rollover sitting untouched — makes part of every future conversion taxable. Name the
mechanical shape at a high level; a CPA handles the actual Form 8606 filing.

> "I have a 24% APR credit card and also want to max my Roth this year."

Names the tension — an unclaimed match still comes first either way; past that, a 24% APR
usually outguns a Roth contribution — but the card-level decision is `debt-credit-management`'s
gate, not resolved here.

> "Why do people say to always get the full 401(k) match?"

No real accounts on the table — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the sequencing block in chat. Copy the
`retirement-contribution-sequencing/` directory into another repo's `.claude/skills/`. Sits
upstream of `asset-allocation-policy`'s contribution routing — this picks the account, that
picks the asset class once the dollar is inside it — and names, without resolving, the
tension with `debt-credit-management`.
