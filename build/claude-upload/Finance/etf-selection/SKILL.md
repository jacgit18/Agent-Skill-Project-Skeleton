---
name: etf-selection
description: |-
  Choose, compare, or re-check a specific ETF or index fund by ticker. Triggers: "SPY or VOO", "is this thematic ETF worth adding", "which bond ETF for my sleeve", "check the ETFs I own". A gate: no hold/buy/swap verdict until the user has (a) named which `asset-allocation-policy` sleeve the fund fills and (b) pulled its facts from the fact sheet or prospectus, not memory — expense ratio, index and true holdings, AUM and volume, multi-year tracking difference, structure, distribution yield and any return-of-capital, fund age; plus duration/credit/YTM for a bond fund, physical-vs-futures for a commodity fund. Also forces a holdings-overlap check against every fund held, and for any non-core tilt a why-now plus a decay check. Claude structures the comparison and checks every fact is sourced; it does not fetch data or pick a theme. Not `asset-allocation-policy` (sets whether the sleeve exists), not `equity-research-writeup` (single-stock thesis), not individual-bond selection.
---

# ETF Selection

ETFs get bought on the ticker everyone knows, a fund name that matches a theme the buyer
likes, or a headline yield — without checking what is inside, what it costs to hold, whether
it tracks its index, or whether it is 85% the same names as something already owned. A
thematic ETF is often a narrative in a wrapper. This skill is a **gate**: the user assigns
the fund a role and pulls its real facts from the issuer; Claude structures the comparison,
checks the sourcing, flags the traps, and gives a verdict. It does not fetch the data or
pick the theme.

Where it sits: `asset-allocation-policy` decides a sleeve exists and how big it is → **this**
picks the fund that fills it → once the verdict is `BUY` / `HOLD`, sizing and entry timing
for the purchase is `equity-trade-decision` (this fact-checked review satisfies its pre-trade
checklist item 1; its cycle-stage sector-tilt table does not apply to a broad-market basket).

## What this does not do

- **Set the allocation.** Whether a bond / commodity / sector sleeve exists and its target %
  is `asset-allocation-policy`. This skill chooses the fund inside an already-decided sleeve;
  a fund with no assigned sleeve is a finding, not an input.
- **Research an individual stock.** `equity-research-writeup` is the single-company thesis
  writeup. This is the funds counterpart — a rules-based basket, judged on cost, holdings,
  tracking, and overlap, not business and moat.
- **Audit a held stock's thesis.** `portfolio-thesis-audit` does that. A held broad-core
  index fund has no per-position thesis by design; a held sector / factor / thematic fund's
  tilt thesis is checked *here*.
- **Pick individual bonds, a robo-advisor, or a whole managed portfolio.** Out of scope.
- **Do in-depth fund-tax mechanics.** It flags return-of-capital distributions, the
  futures-fund tax treatment, and the physical-metal collectibles rate; it names a CPA for
  the specifics.
- **Write options on an ETF.** Covered calls on a fund you hold is `covered-call-decision`.
- **Answer a bare conceptual question.** "What's an expense ratio", "how do ETFs work",
  "physical vs synthetic replication" with no fund on the table is `learning-gate`.
- **Provide the fund's facts.** Claude's recollection of an expense ratio or a holdings list
  is a prompt to open the fact sheet, never the figure of record.

---

## The precondition — role + sourced facts, per fund

For each fund (or each candidate in a comparison), the user supplies:

### 1. The role

Which `asset-allocation-policy` sleeve does this fill — broad equity core / a deliberate
factor or sector tilt / fixed income / commodities / income? A fund with **no assigned
role** is being bought because it is interesting, not because the policy has a slot for it —
say so and stop.

### 2. The facts, from the issuer fact sheet or prospectus (named and dated)

| Fact | Why it matters |
|---|---|
| Expense ratio | The one cost that compounds against you every year, guaranteed |
| Index tracked · # holdings · top-10 weight · sector/geo mix | What you actually own — "S&P 500" and "total market" are different products |
| AUM · average daily volume | Thin AUM/volume → wide spreads and real closure risk |
| Tracking difference vs. the index, 1y / 3y / 5y | "It tracks the index" is a claim; the number is the fact |
| Structure: physical vs. synthetic · in-kind creation/redemption · domicile | Drives counterparty risk and tax efficiency |
| Distribution yield · is any of it return-of-capital | ROC dressed as yield is your own money handed back |
| Fund age / track record | A fund with 18 months of history through one market regime hasn't been tested |
| **Bond fund**: effective duration · credit quality · yield-to-maturity | Distribution yield is not the return; duration is the rate risk |
| **Commodity fund**: physically-backed vs. futures-based · tax treatment | Futures-based funds bleed on contango; physical metals can be taxed as collectibles |

A fact "from memory" or "roughly" is `not sourced — get it from <the fact sheet>`, never
filled in by Claude. "Just tell me if VOO beats SPY", "I don't want to pull fact sheets",
"you already know the expense ratios" are reasons to want the gate skipped, not a release of
it — Claude still sources no fact and gives no verdict from memory.

### 3. Holdings overlap

For every fund already held that this would sit beside, the **holdings overlap %**. A new
fund that is largely the same names as one already owned is not diversification — it is a
fee-heavy duplicate, or a concentrated tilt that should be recognised and sized as one.

### 4. Tilt thesis — non-core funds only

For any sector / factor / thematic fund (not the broad core), the user states **why this
tilt and why now**, and it gets a **decay check**: is this a durable structural exposure, or
a narrow product — few holdings, short history, launched near a hype peak — that tends to
bleed out after the story cools? The broad core index needs no thesis; that is the whole
point of holding it. A thematic fund with no thesis is a `PASS`.

---

## The evaluation block

```
ETF evaluation — <TICKER(s)>   ·   role: <the asset-allocation-policy sleeve | UNASSIGNED>

Facts (each sourced — issuer fact sheet, dated):
  Expense ratio:        <n>%              source: <...>
  Tracks:               <index>  ·  <n> holdings  ·  top-10 = <n>%  ·  <sector/geo note>
  AUM / ADV:            $<n> / $<n>/day   → closure risk <low | elevated>
  Tracking difference:  <n>% 1y  /  <n>% 3y  /  <n>% 5y   vs the index
  Structure:            <physical | synthetic>  ·  in-kind <yes/no>  ·  domicile <...>
  Yield:                <n>%   (<qualified dividends | includes ROC | YTM for a bond fund>)
  Age:                  <n> years
  [bond]       duration <n>y  ·  credit <avg>  ·  YTM <n>%
  [commodity]  <physically backed | futures-based → roll drag>  ·  tax <treatment>

Overlap with current holdings:
  vs <TICKER>:  <n>%  → <fine | near-duplicate | it's a tilt — size it as one>
  [repeat per adjacent fund]

Tilt thesis (non-core only):  <the user's why-this / why-now  |  NONE — and it's not the core>
  Decay check:  <durable structural exposure  |  narrow + new + launched near the hype>

Red flags:  <no assigned role | expense ratio above the category norm | thin AUM/volume |
            persistent tracking drag | overlap sold as diversification | ROC dressed as yield |
            futures commodity fund, roll cost unacknowledged | thematic fund with no thesis |
            none>

Verdict:  <HOLD / BUY — fills its role, cost + tracking fine, not a duplicate |
          SWAP — name the cheaper / better-tracking fund for the same role |
          PASS — <no role | duplicate | thematic, no thesis | cost or structure bad> |
          RESEARCH — facts not sourced: <which> — get them first>
```

---

## Red flags — the evaluation isn't done

- A verdict given with facts taken from Claude's memory instead of the issuer fact sheet.
- No sleeve / role assigned — the fund is being chosen before the allocation has a slot for
  it.
- Overlap never computed against the funds already held, so a near-duplicate passes as
  diversification.
- A thematic / sector fund waved through with no why-this-why-now and no decay check.
- Distribution yield quoted as return with no check for return-of-capital, or a bond fund
  judged on distribution yield rather than duration + YTM.
- A futures-based commodity fund compared to a physical one as if the structures were
  equivalent.
- Expense ratio compared to nothing — it needs the category norm beside it to mean anything.
- "SPY is the standard" as a reason to hold it over a cheaper share-class of the same
  exposure.

---

## Example invocations

> "Should I hold SPY, or switch to VOO or VTI?"

Ask which sleeve this is (the broad equity core, presumably) and have the user pull the
expense ratio and tracking difference for each from the issuer sheets. Note VTI is
total-market, not S&P 500 — a different product, not just a cheaper SPY. Produce the block
with a per-fund verdict.

> "I want to add an AI ETF and a cybersecurity ETF — those are long-term winners."

Non-core tilt. Ask which sleeve and what % cap `asset-allocation-policy` gives it, require a
why-this-why-now for each, run the decay check, and compute the overlap between the two funds
*and* with any broad index already held (AI + cyber + S&P 500 is a lot of the same mega-cap
tech, counted three times). Likely `PASS` on both without a real tilt thesis and a sleeve
cap.

> "How much of my portfolio should be in bonds?"

That's the sleeve size — `asset-allocation-policy`, not this. This picks the bond fund once
the sleeve exists.

> "What does 'synthetic replication' actually mean?"

No fund on the table — answered directly. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the evaluation block in chat. Copy the
`etf-selection/` directory into another repo's `.claude/skills/`. Fills the fund slot that
`asset-allocation-policy` defines; the funds counterpart to `equity-research-writeup`.
