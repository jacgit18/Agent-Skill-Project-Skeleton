---
name: watchlist-screen-sync
description: |-
  Run a candidate ticker through the user's written watchlist screen (per `watchlist-screener-criteria`) AND automatically file the result into the matching Webull watchlist — "Screen Passed" if it clears, "Screen Rejected" if it doesn't. Use whenever the user brings a specific ticker to screen and wants the outcome actually reflected in Webull, not just reported in chat — e.g. "does TICKER pass my screen, add it if so", "run X through the screen", "screen this and track it". A bare "does TICKER pass my screen" with no Webull/tracking intent stays with `watchlist-screener-criteria` — chat-only, writes nothing. Not for defining the screen itself (`watchlist-screener-criteria` Define mode), sizing or entering a trade (`equity-trade-decision`), the full thesis writeup on a name that passed (`equity-research-writeup`), or "what order do I look at a stock in" with no ticker in view (`stock-review-order`) — this skill only decides pass/fail and where the ticker gets parked for tracking.
---

# Watchlist Screen Sync

Bridges two things that otherwise stay disconnected: `watchlist-screener-criteria`
(chat-only, writes nothing) and Joshua's actual Webull watchlists. A ticker that clears
the screen should show up somewhere real, not just get typed out in a chat response he
has to remember to act on. A ticker that fails should still be logged — not silently
dropped — so a name that resurfaces later (another YouTube video, another tip) can be
checked against "we already rejected this" before spending time re-litigating it.

**This skill does not replace any gate.** A name landing in "Screen Passed" is not a buy
signal. It still needs `equity-research-writeup`'s full thesis before `equity-trade-decision`
sizes anything. This skill only automates the filing step that `watchlist-screener-criteria`
already recommends doing by hand.

## Precondition — a written screen must already exist

If Joshua has not defined a screen yet (style, criteria with metric/threshold/direction/why,
disqualifiers, review cadence), gate back to `watchlist-screener-criteria` Define mode first.
Do not run this skill against a screen that only exists in conversation memory from a prior
session unless Joshua confirms it's still current — screens have a stated review cadence for
a reason.

## Steps

1. **Get the candidate inputs**, same as `watchlist-screener-criteria` Screen mode:
   - The ticker.
   - Each screen metric's value, from a named real source (broker, data provider, filing).
     Never fetch, estimate, or reason out a value yourself. A missing value is
     `not supplied — get it from <source>`. A value merely repeated from a video, tip, or
     headline — with no broker/data-provider/filing behind it — is not a named real source
     either; flag it `unverified — confirm against a real source before filing` rather than
     running it as if sourced. This matters more here than in chat-only Screen mode, because
     a pass here writes to a real, persistent watchlist.
   - How the candidate surfaced (screen run, video, tip, product familiarity, headline).

2. **Run Screen mode** exactly as `watchlist-screener-criteria` specifies — produce the full
   screen-result block (criteria table, disqualifier check, pass count, verdict, informal-input
   flag). Don't skip or compress this — the table is what makes the Webull action defensible
   later.

3. **Check for an existing entry first** — call `Webull:get_watchlist_instruments` on both
   "Screen Passed" and "Screen Rejected" and confirm the ticker isn't already sitting in
   either before filing. If it's already in the watchlist the new verdict would file it into,
   say so and skip the redundant add; if it's in the *other* list (a prior verdict flipped),
   flag that explicitly and confirm with the user before moving it — don't silently relocate a
   ticker between lists on a re-run.

4. **Route based on verdict:**

   | Verdict | Action |
   |---|---|
   | `ADD TO WATCHLIST` (clears the screen, no disqualifier triggered) | `Webull:add_watchlist_instruments` with `watchlist_id: d478a39a042c4612aa3d57493121b3c1` ("Screen Passed"), `category: US_STOCK`, `symbols: [<TICKER>]` |
   | `REJECT` (fails one or more criteria, or a disqualifier triggered) | `Webull:add_watchlist_instruments` with `watchlist_id: ffe8dc1df7344497b040f76ecf461d2f` ("Screen Rejected"), `category: US_STOCK`, `symbols: [<TICKER>]` |
   | `INCOMPLETE` (metric values missing) | No Webull action. Report which values are still needed. Don't file it anywhere until the screen can actually be run. |

5. **Confirm the action taken** — name the watchlist the ticker landed in and why (pass/fail
   summary), so the Webull change isn't a silent side effect of a chat response.

6. **If a rejected ticker resurfaces later** and gets brought again for screening, check
   "Screen Rejected" first (via `Webull:get_watchlist_instruments`) before re-running the full
   screen — per `watchlist-screener-criteria`'s rule, a rejected name isn't re-litigated unless
   something material actually changed. If it's already on the rejected list and nothing
   material changed, say so directly instead of re-running the table.

## What this does not do

- Does not define or modify the screen itself.
- Does not pull metric values from any data source — Joshua supplies them.
- Does not size, price, or execute a trade on a passed name.
- Does not write the thesis for a passed name — that's the next stage
  (`equity-research-writeup`), not automated here.
- Does not remove a name from "Screen Rejected" automatically if circumstances change —
  that's a manual `Webull:remove_watchlist_instruments` call once Joshua confirms the
  re-run and a new verdict.
- Does not screen an ETF or fund ticker. `watchlist-screener-criteria`'s own Screen mode
  excludes them (`etf-selection` territory) — this skill inherits that exclusion and refuses
  to file an ETF ticker into either watchlist.

## Portability

**Not repo-agnostic — the one exception in `Finance/`.** Every other skill in this group
writes nothing and copies cleanly between repos or users. This one hardcodes two watchlist
IDs (`d478a39a042c4612aa3d57493121b3c1` "Screen Passed", `ffe8dc1df7344497b040f76ecf461d2f`
"Screen Rejected") specific to Joshua's Webull account (Individual Cash, 5MU64629) and
requires the connected Webull MCP tool. Copied to another account or repo, these IDs won't
resolve — call `Webull:get_watchlists` to find or recreate the equivalent lists and update
this file before use.