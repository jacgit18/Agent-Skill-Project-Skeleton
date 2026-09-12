---
name: strategy-backtest-design
description: |-
  Backtest a rule-based trading strategy on real historical price data before capital is risked — not a live-trade recommendation. Triggers: "backtest this on X", "how would this rule have performed on X", "test my entry/exit rule". A gate: withholds the run until ticker(s), a testable entry rule, a paired exit rule (stop-loss + trend/target), timeframe/lookback, and a sizing assumption are stated — offers a sourced menu (Van Tharp/Turtle/fractional-Kelly sizing; Minervini/golden-cross/Connors RSI(2) entries; ATR-chandelier/death-cross/RSI exits) rather than inventing the logic. Pulls real daily bars via Webull, walks the rule bar-by-bar, reports trade count vs. the ~100-trade floor, win rate, drawdown, buy-and-hold — never simulates a price. Not sizing/entering a live trade (`equity-trade-decision`), not exit rules for a held position (`position-exit-rules`), not options, walk-forward validation, multi-asset, or macro-regime backtests (`macro-cycle-read` names that gap) — none built, name the gap.
---

# Strategy Backtest Design

"I think this RSI rule would have crushed it" is a claim nobody has actually run against real
prices. This skill withholds any backtest until the rule is specific enough to code and the
data is real, then walks the rule forward bar-by-bar over actual historical bars — never a
simulated or estimated price series. The output is a trade log and summary stats next to a
buy-and-hold benchmark, not a verdict on whether to trade the rule live.

## What this does not do

- **Size or enter a live trade.** A backtest result, however good, is not a share count or an
  entry signal for real capital. That's `equity-trade-decision` — hand off once the user wants
  to act on a rule that tested well.
- **Set exit rules for a position already held.** The stop/thesis/size-ceiling rules for a real
  open position are `position-exit-rules`. This skill's exit rule is a backtest parameter (a
  Chandelier stop, a death cross, an RSI level) applied uniformly across history, not a
  commitment about one specific holding.
- **Options strategies.** Theta decay, assignment, and margin math aren't modeled here. Name
  the gap; `covered-call-decision` is the options skill in this catalog, but it doesn't backtest
  either — flag that as a further gap if asked.
- **Formal walk-forward / out-of-sample validation, or multi-asset portfolio backtests.** Not
  yet built. Say so rather than improvising a partial version — a single in-sample run on one
  ticker is what this skill delivers, and it says so in every output (see caveats below).
- **Invent the entry/exit logic.** Claude offers the sourced menu below; the user picks from it
  or supplies their own specific, testable rule. "Buy when it looks strong" never becomes a
  backtest input — ask for the actual condition instead.
- **Fabricate or estimate price data.** If the Webull tool can't return real bars for a ticker
  or window, say so and stop — never fill the gap with a plausible-looking series.

---

## The gate — five inputs, all required before any run

1. **Ticker(s)** — a real symbol, named directly or pulled from a Webull watchlist (e.g.
   "Screen Passed").
2. **Entry rule** — a specific, testable condition. Not "buy when it looks good."
3. **Exit rule** — paired to the entry style; must include both a stop-loss and a trend/target
   exit, not just one.
4. **Timeframe & lookback** — how much historical data and what bar size. Daily is the default
   if unstated.
5. **Position sizing assumption** — % of capital risked per trade, and the hypothetical
   starting capital.

Any of the five left unspecified stops the backtest — offer the relevant menu item below rather
than guessing a default silently.

---

## Parameter menu — sourced, not invented

**Position sizing**
- Fixed-fractional: 0.5–2% of capital per trade (1% is the default — Van Tharp's R-multiple
  framework)
- ATR/volatility-based (Turtle Traders' "N" method): size so a 2×ATR move ≈ target risk %
- Fractional Kelly (25–50% of full Kelly) — only with a well-estimated win rate/payoff ratio

**Timeframe & lookback**
- Swing trading: 2–3 years, 200+ trades minimum
- Position trading: 3–5+ years, 100+ trades minimum
- Must span multiple market regimes (bull/bear/sideways) — a single bull run overstates the
  rule
- Overfitting guardrail (Bailey/López de Prado): don't try more than ~45 parameter combinations
  on 5 years of data for one asset

**Entry rule**
- A — Trend-following: price above 50/150/200-day MAs, all aligned, 200-day rising (Minervini
  trend template)
- B — Simple golden cross: 50-day SMA crosses above 200-day SMA
- C — Mean-reversion: RSI(2) < 10 while price is above the 200-day SMA (Connors)

**Exit rule** (paired to entry style)
- A/B — 3×ATR(22) Chandelier trailing stop, or death cross (50 crosses back below 200), plus a
  7–8% hard stop as a backstop
- C — RSI(2) > 65, or close above the 5-day SMA

A user-supplied rule outside this menu is fine — it still has to clear the same bar: a
condition specific enough to code, not a vibe.

---

## Data source

Pull real historical daily bars via the Webull tool (`get_stock_bars_single`, category
`US_STOCK`, timespan `D`, up to 1200 bars ≈ 4.8 years). Never simulate, estimate, or recall
price data from memory — if the tool can't return it, say so and stop.

---

## Execution

1. Fetch bars for the ticker(s); sort ascending by date.
2. Compute the required indicators (SMA50/SMA200, RSI(2), ATR, etc.) per bar.
3. Walk forward bar-by-bar:
   - Flat + entry condition fires → enter at that bar's close, set the stop, size the position
     as `(capital × risk%) / (entry price − stop price)`.
   - In a position + exit condition fires (stop hit OR trend/target exit) → close at that bar's
     close, log the trade with its exit reason.
4. Track a mark-to-market equity curve throughout. Close any position still open at the last
   available bar and flag it "open at data end" — not a completed signal, don't count it as a
   win or loss.
5. Compute: total return, number of trades, win rate, average win/loss, max drawdown.
6. Compute buy-and-hold return over the identical window for direct comparison.
7. Output the full trade log (entry/exit date, price, shares, P&L, % return, exit reason) plus
   the summary table.

---

## Required caveats — every output, no exceptions

- **Trade count vs. the reliability floor.** State the count and whether it clears ~100 trades;
  below that, say the result is directional only, not statistically meaningful.
- **Buy-and-hold, explicitly.** A rule that underperforms it after all this machinery is a real
  finding, not a bug to explain away.
- **Single-stock/single-path fragility.** A result on one ticker's specific history doesn't
  generalize to other tickers or other periods of the same ticker.
- **No live-trading inference.** A backtest result never implies "so trade this live" — that
  step, if the user wants it, is a separate `equity-trade-decision` with its own checklist.

---

## Red flags — the backtest isn't done

- A run started with any of the five gate inputs missing, defaulted silently instead of asked
  for.
- An entry/exit rule invented by Claude rather than picked from the menu or supplied by the
  user.
- Simulated, estimated, or memory-recalled price data standing in for a real Webull pull.
- A trade count under the reliability floor reported without the directional-only caveat.
- Buy-and-hold omitted from the summary.
- An open-at-data-end position counted as a completed win or loss in the win-rate math.
- A backtest result framed as clearing the way for a live trade.

---

## Portability

Repo-agnostic logic; the data pull is Webull-tool-specific (`get_stock_bars_single`) — a port
to another repo needs an equivalent real-bars source substituted in Step 1 of Execution. Writes
nothing on its own; produces the trade log and summary in chat. Chains to `equity-trade-decision`
if a well-tested rule is to be sized and traded live, and to `position-exit-rules` if the user
then wants to commit real exit rules for an actual position.
