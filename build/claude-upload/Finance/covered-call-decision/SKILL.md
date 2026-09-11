---
name: covered-call-decision
description: |-
  Decide whether to write covered calls against 100+ shares already held, and at what strike and expiration. Triggers: "should I write calls on X", "what strike and expiration", "how much premium can I get", "my calls keep getting assigned before a pullback". A gate: before any strike, a qualification screen — 100+ shares, a liquid options chain, the user genuinely willing to be assigned at a realistic strike, the strike at or above the user's own price target, not the top-conviction "let it run" name, assignment tax character understood. Only then: strike, expiration (earnings and ex-dividend aware), contract count, premium math (not guaranteed, not downside protection), assignment outcome. Not `equity-trade-decision` (long-equity entry; this is its options hand-off). Not `portfolio-thesis-audit` (whether to keep the shares at all) — run first. Consumes `position-exit-rules`' price target as the strike floor. Covered calls only — not puts, spreads, the wheel, or multi-leg.
---

# Covered Call Decision

Covered calls read like free money: keep the shares, collect a premium, repeat. The failure is
everything that framing hides — writing calls on the one position you least want assigned,
picking a strike below your own price target so you've bet against your thesis, treating the
annualized premium as guaranteed income, or forgetting that assignment is a taxable sale that
closes the position. This skill is a **gate**: it runs a qualification screen before it will
name a strike, and for a position that doesn't qualify it says so instead of optimizing the
premium anyway.

It sits downstream of `portfolio-thesis-audit` (which decides whether the shares are worth
holding) and alongside `position-exit-rules` (whose price target is the floor for strike
selection).

## What this does not do

- **Enter or size the underlying stock position.** That's `equity-trade-decision`, which
  explicitly excludes options. This skill assumes the shares are already held; it does not
  decide whether to buy them.
- **Judge whether to keep the shares at all.** `portfolio-thesis-audit` does that — run it
  first. Writing calls on a position that fails the audit is polishing something you should
  be selling outright.
- **Define the equity exit rules.** `position-exit-rules` owns the price stop, the
  thesis-invalidating events, and the size ceiling. This skill consumes that skill's price
  target as the lowest acceptable strike, and treats an assignment as one specific exit path.
- **Any options structure other than a covered call.** Cash-secured puts, spreads, the wheel,
  naked calls/puts, multi-leg, long options, LEAPS — different risk and margin profiles this
  skill doesn't model. Name the gap and stop.
- **Teach options mechanics from scratch.** "What is theta / delta / assignment / an option
  chain" with no real position is `learning-gate`.
- **Give tax or legal advice.** It flags the long-term vs short-term gain question, the
  taxable vs tax-advantaged account difference, and wash-sale timing — then names a CPA for
  the specifics. It does not compute the user's actual tax.
- **Replace a financial advisor.**

---

## The precondition — inputs before any strike is named

The user supplies:

1. **The position.** Ticker; shares held (must be ≥ 100); cost basis per share; current
   price; unrealized gain/loss; how long held (long-term vs short-term for an assignment
   sale); account type (taxable vs IRA/401(k) — assignment in a taxable account triggers a
   realized gain).
2. **The price target / thesis on the underlying.** What the user thinks the stock is worth
   or where it's going — ideally the number already set in `position-exit-rules` (the upside
   review trigger) or stated in `portfolio-thesis-audit`. If there is no view, that's a gap
   to close first: a covered call is a bet the stock stays below the strike, which requires
   having a view.
3. **Willingness to be assigned, and conviction level.** A direct answer to: "would you be
   genuinely fine selling these shares at strike $K?" plus whether this is a stable /
   fully-valued / lower-conviction holding or the highest-upside name in the book. If the
   honest answer is "no, I want to keep it" at any strike the market pays a worthwhile
   premium for — or this is the top-conviction position — it does not qualify. Chasing a
   near-the-money premium to hit an income target *is* a decision to sell the stock; name
   that when it's what's happening.
4. **Options-market quality.** Is there a liquid chain — a tight bid/ask (cents, not dollars,
   on liquid names), real open interest and volume at the strikes being considered? If the
   user doesn't know, that check comes before a recommendation, not after.
5. **Why covered calls / any income target.** If there's a stated income need ("I need this
   to make $X/year"), name it — it drives strike-too-close-to-the-money premium chasing, and
   the premium is not guaranteed income.

If any of 1–4 is missing, ask for it and **stop**. Do not name a strike off assumed inputs.
"Just tell me the strike and the premium, skip the screening" is a reason to want the screen
skipped, not a pass through it — report pass/fail per screen line and produce a strike only
for a position that clears it.

When the position is an **already-open call being managed into expiration** — roll vs. let
assign, e.g. routed from `weekly-portfolio-review` step 3 — the share-lot, liquidity, and
conviction lines are a confirmation, not a re-derivation; the live decision is the new
strike/expiration versus accepting assignment.

Claude's contribution once the inputs are in:

- Run the **qualification screen** (below) and report pass/fail per line. A single fail on
  "willing to be assigned", "strike ≥ price target", or "not the highest-conviction name" is
  a stop — recommend a different position, not a different strike.
- Only for a qualifying position: strike, expiration, contract count, premium math,
  assignment outcome — as the block below.

---

## The qualification screen

| Check | Pass condition | Fail → |
|---|---|---|
| **Share lot** | ≥ 100 shares (each contract covers 100) | Can't write a standard covered call; stop. |
| **Liquidity** | Tight bid/ask + real open interest at the candidate strikes | Wide spreads eat the premium and make assignment/roll messy; don't write here. |
| **Assignable willingly** | User would genuinely accept a sale at a realistic strike | This is a "let it run" holding — writing calls means selling your best idea for a small premium. Pick another position. |
| **Strike ≥ price target** | A strike at or above the user's own target still pays a worthwhile premium | A strike below the target bets against the thesis. Either the target is wrong (revisit `portfolio-thesis-audit`) or this isn't a covered-call candidate. |
| **Not top-conviction** | This is a stable, fully-valued, or lower-conviction holding — not the highest-upside name in the book | Assignment caps the position you most wanted uncapped. |
| **Tax understood** | User knows whether an assignment sale is LT or ST, and the account is taxable or not | Resolve before writing — a taxable ST assignment on a big embedded gain can swamp the premium. |

---

## The decision block

Produced **only** for a position that clears the screen. Every line appears.

```
Covered call — <TICKER>

Position:              <n> shares @ cost basis $<n>  ·  current $<n>  ·  unrealized <+/- $n>
                       held <LT | ST>  ·  account <taxable | tax-advantaged>
Price target (floor):  $<n>   (from position-exit-rules / portfolio-thesis-audit) — no strike
                       below this
Qualification:         <PASS — all six | FAIL: <which check> → <the different position or the
                       prerequisite skill>>

Strike:                $<n>   (<pct>% above current; at/above the price-target floor;
                       ~<delta> ≈ rough assignment probability)
Expiration:            <n> days out  ·  <before / after> the next earnings date
                       (<intentional | avoid — earnings move can blow through the strike>)
                       ex-dividend <date> falls <inside | outside> this window → <early-
                       assignment risk around it | none>
Qualified-CC check:    OTM, >30 days out, not deep in-the-money → holding period keeps
                       running, dividends stay qualified. A deep-ITM or very short-dated
                       call can suspend the holding period and unqualify dividends for the
                       option's life. <OK | FLAG>
Contracts:             <n>  (covers <n×100> of <total> shares — <all | a portion, leaving
                       <n> uncovered to keep some upside>)

Premium math:
  Premium received:    $<n>   ( bid $<n> × 100 × <contracts> )
  As % of underlying:  <pct>%  on $<covered notional>
  Annualized (if re-written):  ~<pct>%  — NOT guaranteed, NOT downside protection beyond the
                       premium; the stock can fall well past $<breakeven> and the premium
                       only offsets the first $<premium/share>
  Breakeven:           $<cost basis − premium/share>/share
  If unassigned (static return):   premium ÷ underlying = <pct>% for the period
  If assigned (called return):     (strike − cost basis + premium/share) = $<n>/share =
                       <pct>% on cost — <acceptable outcome? the user said yes at this strike>

Assignment outcome:
  You end with:        $<strike × 100 × contracts> cash, shares gone
  Realized gain:       $<(strike − cost basis) × shares covered>  ·  tax character <LT | ST>
                       — this is a real tax event in a taxable account
  Thesis position:     closed. Re-entry is a fresh equity-trade-decision; if buying back
                       within 30 days of a loss leg elsewhere, watch the wash-sale rule.

Red flags:             <strike below price target | written against the top-conviction name |
                       illiquid chain | earnings inside the window unintentionally | premium
                       treated as downside protection | annualized yield quoted as if
                       guaranteed | whole position covered when the user still wants upside |
                       none>
```

---

## Red flags — the decision isn't done

- A strike named before the qualification screen was run and reported.
- A strike **below the user's own price target** — the call is then a bet against the thesis
  the user is still holding the shares on.
- Calls written against the **highest-conviction, largest-unrealized-gain** position because
  its premium is fattest — that's where assignment costs the most, in upside and in tax.
- The annualized premium yield quoted as income the user can count on. It requires re-writing
  every cycle, it stops if the shares are assigned, and it does nothing for a real decline.
- "It's covered, so there's no risk." The risk is the stock falling (premium offsets only its
  first slice) and the upside being capped at the strike.
- Earnings inside the expiration window when the user didn't intend to write through them.
- The full position covered when the user, asked directly, still wants upside on some of it.
- Ex-dividend date inside the window with no mention of early-assignment risk.
- Assignment tax character (LT/ST) and account type never established.

---

## Example invocations

> "I've got 200 shares of AXP, basis ~$150, it's ~$240 now. I want income against it — what
> call do I write?"

Ask for: the price target on AXP, whether they'd truly accept selling at a plausible strike
(~$260?), the account type and holding period, and confirm the AXP chain is liquid. If AXP is
a high-conviction hold with a $90/share embedded LT gain, the screen likely fails on "willing
to be assigned" / "not top-conviction" — recommend writing against a stabler, lower-embedded-
gain position instead, and say why. Only if it passes: the strike/expiration/premium block.

> "How much would I make selling the $260 call on AXP expiring next month?"

Same gate — the premium number is easy, but it's not produced until the qualification screen
has run. A premium figure with no assessment of whether the position should be written at all
is the failure this skill exists to prevent.

> "Should I sell a cash-secured put on AXP instead to get in cheaper?"

Not this skill — that's a different structure (short put, cash collateral, no shares yet).
Name the gap and stop.

> "What does 'delta' mean on an option?"

No position on the table — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the decision block in chat. Copy the
`covered-call-decision/` directory into another repo's `.claude/skills/`. Chains from
`portfolio-thesis-audit` (keep-the-shares decision) and `position-exit-rules` (price-target
floor); `equity-trade-decision` hands options questions here.
