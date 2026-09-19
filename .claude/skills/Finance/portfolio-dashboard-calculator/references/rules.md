# Rules, inputs and expected numbers

`scripts/calc.py` implements everything here. `scripts/test_calc.py` checks it against these numbers.

## Defaults
Capital $23,000. Real estate 50, Company stocks 15, Stock ETFs 15, Speculative 18, Gold 2 (class ids `re`, `cs`, `etf`, `spec`, `gold`). Sub-splits: Real estate REITs, Direct property, Crowdfunding platforms, Development projects (25 each); Company stocks Blue-chip companies, Dividend payers, Growth stocks (thirds); Stock ETFs Index, Sector, International, Dividend ETFs (25 each); Speculative Cryptocurrency and Startup investments 50/50 (or `spec_mode: "three"` adds High-risk stocks, thirds); Gold Physical gold, Gold ETFs, Gold mining stocks (thirds).
Bands (points, placeholders): 5, 3, 3, 3, 1. Stress presets (illustrative, not forecasts): moderate -10/-20/-15/-35/+5, severe -25/-40/-35/-60/+10.
Trade: account $10,000, risk 2% (tiers: 1% volatile, 2% medium, 3% low-risk), entry $25, stop 15% below, target 40% above, minimum reward:risk 2.

## Commands and inputs (all optional; JSON; class-keyed objects use ids)
- `split`: `capital`, `targets` {id: pct}, `subs` {id: [pcts]}, `spec_mode`. Output: dollars per class and sub-line.
- `drift`: `holdings` {id: $}, `new_money`, `mode` ("rebalance" or "new_money"), `targets`, `bands`. Rebalance: trade = target dollars on (holdings + new money) minus holdings. New money only: split the new money in proportion to each class's shortfall, never sell; with no shortfall it follows the targets. Status is In band, Over or Under against the band.
- `held`: `capital`, `assigned` {id: {account: $}}. Tag per class: Matches, $X unassigned, or $X over.
- `stress`: `capital`, `base` ("target" or "current"), `holdings`, `scenario` ("moderate", "severe", "custom"), `shocks` {id: pct}, `loss_limit` (percent). Change = value x move, rounded to the cent. Share of losses counts losing classes only.
- `monthly`: `monthly`, `months` (1 to 120), `mode` ("targets" or "catchup"), `holdings`. Catch-up simulates month by month, buying only shortfalls. No returns assumed.
- `trade`: `account`, `risk_pct`, `entry`, `stop` or `stop_pct`, `target` or `target_pct`, `min_rr`.
  `budget = account x risk% ; per = entry - stop ; rr = (target - entry) / per ; shares = floor(budget / per) ; position = shares x entry ; max loss = shares x per ; profit = shares x (target - entry)`. Flags: missing inputs, stop at or above entry, target at or below entry, below or clearing the minimum, zero shares, position above the account (margin), risk above 3%.
- `rank`: trade inputs plus `candidates` [{ticker, entry, stop, target}] (max 30) and `weight` ("rr" default or "equal"). Valid = ticker, entry > 0, stop > 0, entry > stop, target > entry. Sorted by reward:risk (ties keep input order); each gets `budget x weight / sum(weights)` in risk dollars, then shares = floor(risk dollars / per).
- `full`: any mix of the above keys plus `trade` and `candidates`; returns one section per part supplied.

## Expected numbers (all pass in test_calc.py)
- Split $23,000: 11,500 / 3,450 / 3,450 / 4,140 / 460. $1,000 in thirds: 333.34, 333.33, 333.33.
- Holdings 15,000 / 3,000 / 2,500 / 2,000 / 500, rebalance: Sell 3,500, Buy 450, Buy 950, Buy 2,140, Sell 40; 3 of 5 outside band. New money only $1,000: 0 / 149.25 / 273.63 / 577.12 / 0. No holdings, $1,000: 500 / 150 / 150 / 180 / 20.
- Stress moderate (target base): -1,150 / -690 / -517.50 / -1,449 / +23, whole book -$3,783.50 (-16.45%). Severe: -$7,900.50; with a 20% limit, 14.35 points over (about $3,300.50).
- Monthly $500 x 12: month 1 = 250 / 75 / 75 / 90 / 10, total $6,000. Catch-up with the holdings above: month 1 = 0 / 69.45 / 135.58 / 294.97 / 0.
- Trade defaults: 2.67x, 53 shares, $1,325, max loss $198.75, profit $530. His worked example ($10,000, 2%, entry $12, stop $10.50): 133 shares, $1,596, loss $199.50 (his notes say "$133 / 11 shares", which mixes a dollar amount with a share count). Stop $10.60: 142 shares (rounded down), loss $198.80.
- Rank AAPL 25/21.25/35, MSFT 100/90/130, TSLA 50/45/55: order MSFT, AAPL, TSLA; shares 9, 21, 6; "Total risk budget $200. 3 candidates, $1,725 deployed. 2 of 3 clear the 2x minimum." Equal split: 6, 17, 13.
