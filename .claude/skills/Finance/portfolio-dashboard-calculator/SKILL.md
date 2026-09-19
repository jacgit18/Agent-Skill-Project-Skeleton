---
name: portfolio-dashboard-calculator
description: Chat-only calculator behind Joshua's portfolio dashboard: runs its exact math, no page. Split a total across asset classes to the cent, drift and rebalance or new-money-only buys, account fill check, stress test, monthly deposit split, shares for a chosen risk (stop, target, reward:risk), and ranking tickers under one shared risk budget. Use for "run the numbers", "split $X across my classes", "am I off target", "what would a bad year do", "split my monthly deposit", "rank these tickers", or the full picture. Arithmetic only, never a verdict. A share count is not "should I buy" (`equity-trade-decision`); a rebalance plan is not tax-aware (`rebalancing-execution`); band widths come from `asset-allocation-policy`.
---

# Portfolio dashboard calculator

The dashboard's brain without the screen. **Run `scripts/calc.py`** and answer from its output. Do not build a page or do the arithmetic by hand. Rules, defaults and expected numbers: `references/rules.md`.

```
python3 scripts/calc.py <split|drift|held|stress|monthly|trade|rank|full> '<json>'
python3 scripts/test_calc.py        # after any edit to calc.py; must say "all passed"
```
Defaults match the dashboard (capital $23,000; Real estate 50, Company stocks 15, Stock ETFs 15, Speculative 18, Gold 2; trade account $10,000, 2% risk, min reward:risk 2). Say which defaults you used.

## Which question runs which command

| He asks | Command | Get first |
|---|---|---|
| "Run the numbers on X" / share count | `trade` | Cash in that trading account, risk %, entry, stop or stop %, target or target % |
| "Rank these tickers" | `rank` | Same account and risk, plus entry, stop, target per ticker |
| "Split $X across my classes" | `split` | Capital, any changed percentages |
| "Am I off target?" | `drift` | Dollars per class, new money, rebalance or new-money-only |
| "Are my accounts filled?" | `held` | Dollars per class per account |
| "What would a bad year do?" | `stress` | Base, scenario, optional loss limit |
| "Split my monthly deposit" | `monthly` | Amount, months, mode, holdings |
| "Full picture" | `full`, in the order below | Whatever he can give |

Ask for at most one missing input at a time, only what changes the answer. A live entry price can come from the Webull connector (`get_stock_snapshot`) when connected; say the quote time. If no connector or code runner is available, ask him to paste the entry price, and say the script could not be run rather than doing the math by hand.

"Full picture" order (stop where he stops giving data): split, drift, where it is held, stress test, monthly deposits, trade sizing and ranking. Lead with what he asked for, then supporting numbers. State assumptions in one line.

## How this sits beside the gates

This skill is the **arithmetic layer**. Each gate keeps the decision; this skill is where its numbers can come from.
- **`trade` / `rank`**: same math as `equity-trade-decision` (risk budget ÷ per-share risk, round down, 2:1 floor). A share count here is not that skill's verdict: it withholds "good size" until the checklist and cycle stage are done. If he asks "should I buy", run the gate; use this only for the numbers.
- **`drift` / `monthly`**: plain target-minus-current. **No tax-aware ordering** (new money, then tax-advantaged, then taxable, then lot choice): that is `rebalancing-execution`. Say so whenever `drift` shows a sell.
- **Bands and targets**: the defaults and band widths are placeholders. If an `asset-allocation-policy` exists, use its targets and bands as inputs; do not judge them here.
- **Lump sums** are `lump-sum-vs-dca`, not `monthly`.

## Account rules (his own, apply before any verdict)

Accounts: Wealthfront robo Roth IRA, self-directed Roth IRA, rollover IRA, individual taxable brokerage, HSA, high-yield savings, checking, and a Webull individual cash brokerage (one share each of several companies, a deliberate collecting habit).
1. **Account control first.** A holding inside the Wealthfront account is the robo's decision, not his ticker call. Do not critique individual tickers there; redundancy across the whole picture is still fair to flag.
2. **Tax treatment gates execution, not the decision.** Lot choice, short vs long term and wash-sale timing only matter in the taxable brokerage.
3. **Connected data is incomplete by default.** A Webull position showing one share is not proof he owns one. Before any portfolio-level claim (total size, weight, concentration, covered calls) ask: "Webull shows one share of [Ticker]. Is this a standalone collecting share, or do you own more in another account? About how many in total, and in which account types?" Use his answer as the ownership from then on. A collecting share he calls non-financial is not judged by sizing standards.

## What this skill does not do

It computes; it never decides. Do not say a split is good or bad, recommend a class mix, project returns, or call a ranked stock a good investment. Route decisions and say which skill owns them:
- Target shape, bands, contribution order: `asset-allocation-policy`, `retirement-contribution-sequencing`
- Executing a flagged drift: `rebalancing-execution`; one-time sum: `lump-sum-vs-dca`
- Whether a name deserves research: `watchlist-screener-criteria`, `stock-review-order`, `equity-research-writeup`
- Entry and size verdict: `equity-trade-decision`; stops and exits: `position-exit-rules`
- Keep, sell or fix a held position: `portfolio-thesis-audit`; which taxable lot: `tax-lot-selection`
- Covered calls: `covered-call-decision`; funds: `etf-selection`; recurring review: `weekly-portfolio-review`

Fixed cautions: a stop is not a guaranteed exit price; stress moves are scenarios he sets, not forecasts; band widths, stress presets and the 3% warning are placeholders; ranking is reward:risk arithmetic only; no cost-basis tracking, options, shorting or fractional shares.

## Rules that make the numbers right (keep when editing the script)

- Plan math is integer cents with largest-remainder splitting, so pieces add up exactly.
- **Shares round down**, so planned loss never exceeds the risk budget (matches `equity-trade-decision`).
- One risk budget, `account x risk%`, is shared by a single trade and a ranking. The same ticker in both is the same dollars, not additive.
- A ranking candidate needs a ticker, entry above stop above zero, and target above entry; others are listed as excluded.
- Tickers are sanitised (letters, digits, `.`, `-`) before they go into any list or CSV.
