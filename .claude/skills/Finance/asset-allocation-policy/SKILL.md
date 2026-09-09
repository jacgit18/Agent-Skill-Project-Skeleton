---
name: asset-allocation-policy
description: Use when someone wants to set — or revise — the target shape of a whole portfolio, the policy that every single-position decision then operates inside: "help me set a target allocation", "what should my stock/bond/cash split be", "I've never set an allocation, it's just what I bought over time", "how much should any one position be", "when should I rebalance", "where should new contributions go", "am I too concentrated". It is a gate: it withholds an allocation recommendation, and refuses to hand over target percentages off a risk-tolerance quiz, until the user supplies the inputs that actually determine allocation — (1) the capital map: what is runway / near-term-need money and therefore not investable, versus the investable pool broken out by account type (taxable, Roth/IRA, 401k), since tax treatment changes what belongs where; (2) the withdrawal plan and time horizon: when money comes out and how much a year, reconciled as income vs. drawdown; (3) risk capacity (can the withdrawal plan survive a 40% equity drawdown) versus risk tolerance (how it feels) — capacity binds; (4) the concentration stance: the user's own explicit call on running a concentrated book (few high-conviction names, benchmark to the best) versus a diversified one (broad, volatility-managed) — a real tension the skill will not decide for them; (5) what each bucket is for, if they run buckets (a long-term core, an income sleeve, a small active/learning sleeve). Then the user commits the policy — asset-class targets with tolerance bands, the split within equities (broad index/ETF vs. individual names vs. active sleeve), position-sizing bands (starter size, single-name cap, trim trigger, position count), diversification limits (per sector, per theme/factor, geography, a correlation check), the rebalancing trigger and its tax-aware ordering, and default routing for new contributions and dividends — and Claude checks it is complete, internally consistent (the equity sub-splits sum to the equity target; the cash sleeve actually covers the stated withdrawal; the single-name cap matches the stated concentration stance), and stress-tests it against the constraints, then produces the policy block. The single-name cap and trim trigger it sets are the house defaults `position-exit-rules` rule 3 references; the bands are what `weekly-portfolio-review` step 5 checks drift against. Not `equity-trade-decision` — that sizes one position against one risk tier *inside* this policy's bands; this sets the bands. Not `position-exit-rules` (per-position exits) or `portfolio-thesis-audit` (per-position keep/sell) — both defer the target shape to here. Not `watchlist-screener-criteria` (which names to research). Not retirement-account contribution-strategy mechanics (Backdoor Roth, employer match, contribution sequencing) — the policy places the accounts in the capital map, it does not optimise the tax-advantaged funding order. Not tax or legal advice — it flags the tax-aware rebalancing order and names a CPA. Not a bare conceptual question — "what is a 60/40 portfolio", "how does rebalancing work" with no real portfolio is `learning-gate`. Not a substitute for a financial advisor, and not a formal legal investment policy statement for a third party.
---

# Asset Allocation Policy

Without a written policy, a portfolio's shape is an accident — the sum of individual buys,
whatever they happened to add up to. Then a winner quietly becomes 30% of the book with no
rule to catch it (there was no target), cash piles up or runs dry with no plan, "diversified"
means "I own a lot of things" rather than a decided mix, and rebalancing happens on emotion
or never. Every position-level skill in this group explicitly hands the whole-book shape
here. This skill is a **gate**: the user states the inputs and commits the policy; Claude
checks it holds together and stress-tests it. It does not hand over an allocation from a
risk quiz.

## What this does not do

- **Size a single position.** `equity-trade-decision` does that, against one risk tier,
  *inside* the bands this policy sets. This skill sets the bands and the concentration stance;
  it does not size a trade.
- **Set per-position exits or audit a held thesis.** `position-exit-rules` and
  `portfolio-thesis-audit` own those. This policy's single-name cap and trim trigger are the
  house defaults `position-exit-rules` rule 3 points at.
- **Pick which names to research.** `watchlist-screener-criteria` → `equity-research-writeup`.
  This policy decides *how much* goes to individual names versus index funds versus the active
  sleeve, not which ones — and not which specific fund or ticker fills a sleeve (expense
  ratio, tracking error, SPY-vs-VOO is a separate fund-selection question).
- **Execute a rebalance.** Which lots to sell, in what order, today — that follows the
  trigger and the tax-aware ordering this policy *sets*. `weekly-portfolio-review` step 5
  flags the drift that fires one.
- **Allocate a purchase price across the assets of a business being acquired.** That's
  `seller-financing-evaluation` — a different meaning of "allocation".
- **Optimise tax-advantaged contributions.** Backdoor Roth mechanics, capturing an employer
  match, the order to fund accounts — separate territory. This policy places the accounts in
  the capital map and routes new taxable contributions; it doesn't sequence the funding.
- **Give tax or legal advice.** It flags the tax-aware rebalancing order (new money and
  dividends first, then tax-advantaged accounts, then taxable only on a bad band breach) and
  names a CPA for specifics.
- **Answer a bare conceptual question.** "What's a 60/40 portfolio", "how does rebalancing
  work" with no real portfolio is `learning-gate`.
- **Disambiguate a vague ask.** "Get my portfolio in order", "sort out my investments" —
  that's `ambiguity-gate` first; this takes the set-the-target-shape reading once it's
  settled.
- **Draft a formal Investment Policy Statement for a third party.** This produces the user's
  own working policy, not a legal document.

---

## The precondition — five inputs the user supplies

1. **The capital map.** Split every dollar into: **runway / emergency fund** (untouchable —
   never the source of a buy or a rebalance), **near-term need** (a house down payment, a tax
   bill, tuition inside ~3 years — out of the investable pool), and the **investable pool**,
   itself broken out by account: taxable brokerage, Roth / IRA, 401(k). Tax treatment changes
   what belongs where (income-heavy and high-turnover assets lean tax-advantaged; long-hold
   equity and municipals lean taxable), so the accounts are named, not merged.
2. **Withdrawal plan and horizon.** When money comes out and how much per year, stated as a
   figure and a % of the investable pool. Reconcile it out loud: a withdrawal rate the
   portfolio's expected return can't sustain is a **drawdown plan**, not an income plan — say
   which it is. (This is where a stated income target gets checked against the actual pool.)
3. **Risk capacity vs. risk tolerance.** Capacity: could the withdrawal plan survive the
   equity sleeve falling 40% for two years — would the user still be solvent and not forced
   to sell at the bottom? Tolerance: how that would feel. **Capacity binds.** Unemployed and
   withdrawing = low capacity regardless of how aggressive the user feels.
4. **The concentration stance.** The user's own explicit decision: a **concentrated** book
   (a handful of high-conviction names, willing to benchmark to the best idea, higher
   single-name cap) or a **diversified** one (broad exposure, single-name risk deliberately
   small, volatility managed). This is a real, unresolved tension — the skill will **not**
   pick for them; it makes them choose, and then holds the rest of the policy consistent with
   that choice.
5. **Bucket purposes**, if they run buckets — e.g. a long-term **core** (index funds +
   thesis-backed holds), an **income** sleeve (the underlyings covered calls are written on),
   a small **active / learning** sleeve with a hard dollar cap. The % to each and the rules
   for moving capital between them.

If inputs 1–4 are missing, ask for them and **stop** — an allocation off a risk-tolerance
label alone is the thing this skill exists to prevent. "Just tell me a good split", "a rule
of thumb for someone my age", "60/40 is fine, right?" are reasons to want the gate skipped,
not a release of it.

If the user only wants **one band** — a single-name cap requested mid-`position-exit-rules`,
say — don't run the full five-input gate: give that one number from the concentration stance
if it's stated, or ask only for the stance, and note the rest of the policy is unset.

Claude's contribution once the inputs are in: check the policy the user builds is **complete**
(all six areas below), **internally consistent** (equity sub-splits sum to the equity target;
the cash/short-bond sleeve actually covers the stated annual withdrawal plus a buffer; the
single-name cap matches the stated concentration stance; the active sleeve's dollar cap is
inside the pool), and **stress-test it** against inputs 2–3 (a 70/30 target with an
unemployed user drawing 20%+ of the pool a year → name the mismatch: the cash sleeve is
too thin and capacity doesn't support the equity weight). Claude does not supply the target
numbers.

---

## The policy — six areas the user commits

```
Asset Allocation Policy — <date>   ·   review: <annually | on a life change>

CAPITAL MAP
  Runway / emergency (not investable):   $<n>   — never a buy/rebalance source
  Near-term need (< ~3y, not investable): $<n>   — <what for>
  Investable pool:                        $<n>
    Taxable brokerage:  $<n>     Roth/IRA:  $<n>     401(k):  $<n>
  Withdrawal plan:      $<n>/yr  = <pct>% of the pool  →  <income plan | drawdown plan>
  Risk capacity:        <can/can't take a 40% equity drawdown for 2y and stay solvent>
  Concentration stance: <CONCENTRATED — cap <pct>%/name, <n>–<n> names | DIVERSIFIED —
                        cap <pct>%/name, <n>+ names / mostly funds>

1. ASSET-CLASS TARGETS (with bands)
   Equities:       <pct>%  (band <pct>–<pct>%)
   Fixed income:   <pct>%  (band ...)
   Cash / T-bills: <pct>%  — must cover ≥ <n> months of expenses + the annual withdrawal
   <other: metals, alternatives>: <pct>%

2. WITHIN EQUITIES
   Broad index / ETF core:  <pct> of equities
   Individual names:        <pct> of equities   (→ position bands below)
   Active / learning sleeve:<pct> of equities, hard cap $<n>

3. POSITION-SIZING BANDS  (the house defaults position-exit-rules rule 3 uses)
   Starter position:  <pct>%      Max single name:  <pct>%  (= trim trigger)
   Target count of individual names:  <n>–<n>

4. DIVERSIFICATION LIMITS
   Max per sector:  <pct>%     Max per theme/factor:  <pct>%
   Geography:       <US / ex-US split, or "US-only, acknowledged">
   Correlation check: <named — "no more than <n> names driven by the same factor (rates,
                     oil, AI-capex)">

5. REBALANCING
   Trigger:  <a band is breached | calendar <freq> | both>
   Order (tax-aware): new contributions + dividends first → tax-advantaged accounts →
                     taxable only if a band is badly breached (name the threshold)
   Never: sell from runway / near-term-need money to rebalance.

6. NEW CONTRIBUTIONS
   Default routing of the next $<n>:  <to whichever asset class is furthest below its band>
   Cadence:  <lump sum on arrival | spread over <n> weeks>

Consistency check:  <equity sub-splits sum to the equity target? cash sleeve ≥ withdrawal +
                    buffer? single-name cap matches the concentration stance? active sleeve
                    inside the pool? — each: OK | FLAG <what>>
Stress test:        <the target vs. capacity/withdrawal: OK | MISMATCH <what to change>>
```

---

## Red flags — the policy isn't real

- Claude supplied the target percentages, or produced them from a risk-tolerance label with
  no capital map, withdrawal plan, or capacity check behind them.
- The concentration stance left unstated, so the single-name cap and position count are
  arbitrary.
- A cash / short-bond sleeve that doesn't cover the stated annual withdrawal plus a buffer,
  on a portfolio that is being drawn down.
- Equity sub-splits (index / individual / active) that don't sum to the equity target, or an
  active sleeve whose dollar cap exceeds its stated %.
- Runway or near-term-need money folded into the investable pool, or named as a rebalance
  source.
- A rebalancing rule with a trigger but no tax-aware ordering, or no ordering at all.
- The policy treated as a one-time answer — no review date, no contribution-routing rule.
- A target that fails the stress test (capacity can't support the equity weight) left
  standing because "that's the return I need".

---

## Example invocations

> "I've got ~$45k across 12 stocks, some ETFs and T-bills, a separate autopilot Roth, and
> $30k in savings I'm treating as my emergency fund while I'm between jobs. I never set a
> target allocation. Help me set one."

Gate. Ask for the capital map (confirm the $30k stays out; break the $45k by account), the
withdrawal plan and horizon (any income target stated as a % of the pool), the capacity
check, and the concentration stance as an explicit choice. Then have the user commit the six
areas; check consistency and stress-test against the withdrawal plan. Don't open with "go
70/30".

> "What should any one stock be as a share of my portfolio?"

That's the position-sizing band — part of this policy (area 3). It's also the house default
`position-exit-rules` rule 3 points at. Set it here, from the concentration stance.

> "My tech names have grown to 45% of the account — should I trim?"

If a policy exists, that's `weekly-portfolio-review` step 5 (drift vs. the band) → a trim
flag. If no policy exists, this skill first — the 45% has nothing to be "too much" against
yet.

> "What's the classic argument for a 60/40 portfolio?"

No real portfolio on the table — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the policy block in chat as the user's working
document — `weekly-portfolio-review` step 5 and `position-exit-rules` rule 3 both read from
it. Copy the `asset-allocation-policy/` directory into another repo's `.claude/skills/`. It
is the frame the rest of the `Finance/` equity pipeline operates inside.
