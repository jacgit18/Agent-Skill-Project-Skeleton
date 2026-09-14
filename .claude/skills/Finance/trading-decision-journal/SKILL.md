---
name: trading-decision-journal
description: |-
  Two modes. Capture — the moment a real buy/sell/add/trim decision is made, log it verbatim to `Finance/Investment/Trading Decision Log.md`: ticker, action, the user's own stated reason, sourced (a screen/skill) or unsourced (tip/video/gut), and, for an exit, whether the stop was honored or moved first. "log this decision", "I just bought/sold X", "track why I did this". Review — periodic, pulls entries since last review and flags patterns the data supports: rising stop-overrides, thesis rewrites w/ no new evidence, more unsourced entries, frequency spikes, asymmetric win/loss detail. "run my trading journal review", "am I overriding my stops more", "check my decision patterns". Neither mode is a live gate — Capture never judges, Review never diagnoses from too few entries. Checks the user's behavior, not the thesis (`portfolio-thesis-audit`) or a coding error (`problem-journal`). Not a substitute for `position-exit-rules` (sets the stop) or a live block on the current trade.
---

# Trading Decision Journal

`portfolio-thesis-audit` checks whether a thesis is still valid. Nothing checks whether the
process *around* deciding is drifting — are stops getting moved instead of honored more often
than they used to, are theses getting quietly rewritten after the fact to justify holding a
loser, is the ratio of sourced-screen buys to gut/tip buys creeping the wrong direction. This
skill is that check. It grades the user, not the position.

Two modes, deliberately separate, mirroring `problem-journal`'s Capture/Journal split:

| Ask | Mode |
|---|---|
| "log this decision", "I just bought/sold X", a real buy/sell/add/trim just happened | **Capture** — one entry appended to the log, no judgment attached |
| "run my trading journal review", "am I overriding my stops more", "check my decision patterns" | **Review** — a periodic pass over the log, flagging only patterns the data actually supports |

Neither mode is a live gate on the trade itself. Capture does not block or slow down the
decision being made — the point is an honest record of the real reasoning, including when
that reasoning is bad. Gating it would just produce a cleaner-sounding lie in the log.

## Out of scope — hand these off

- **Whether the thesis is still valid.** `portfolio-thesis-audit`. This skill never asks "is
  the bull case still true" — only "did the user follow their own stated process."
- **Setting the stop, invalidation events, or size ceiling.** `position-exit-rules` produces
  those; this skill only records afterward whether they were honored.
- **A coding error or debugging problem.** `problem-journal` — different domain entirely, no
  ticker, no trade.
- **Blocking or slowing the current decision.** Not a gate. Capture is mechanical recording
  after the fact of deciding, same as `problem-journal`'s Capture mode.
- **A bare conceptual question** — "what's a stop-loss" — `learning-gate`.

---

## Mode: Capture a decision

Use the moment a real buy, sell, add, or trim happens (or was just decided) — whether it was a
good decision or not. No judgment, no pattern-matching against history — that's Review's job,
and only later, with enough entries to say something real.

### 1. Get the decision's facts

- **Date, ticker, action** (buy / sell / add / trim / write-call / etc.).
- **The user's own stated reason** — their words, not Claude's paraphrase. If it's short
  ("felt right," "saw it on a video"), log it exactly that short. Don't pad it into something
  more considered-sounding than it was.
- **Sourced or unsourced** — did this trace back to a screen or skill result (`watchlist-screener-criteria`
  pass, `equity-trade-decision` sizing, `portfolio-thesis-audit` sell verdict), or a tip/video/gut
  call with nothing behind it? Same distinction `watchlist-screen-sync` already flags as
  "unverified" for a filed candidate — this is the same discipline applied to the decision
  itself, not just the ticker's sourcing.
- **For an exit only: was the stop honored or moved?** If `position-exit-rules` set a hard
  price stop, state whether this exit happened at/through that level as originally set, or
  whether the stop was moved (once, or repeatedly) before the exit happened. This single field
  is what Review's stop-override check depends on — don't skip it on an exit entry.
- **Optional: context.** Market conditions, how the user was feeling, anything that might
  matter later. Leave blank if not offered — never invented.

### 2. Append to the log

One entry per decision, appended (never overwritten) to `Finance/Investment/Trading Decision
Log.md` in the vault (not this repo). Create the file with a simple dated-entry format if it
doesn't exist yet:

```markdown
## <YYYY-MM-DD> — <TICKER> — <ACTION>

- Reason (user's words): <verbatim>
- Sourced: <screen/skill name> | Unsourced: <tip/video/gut — named>
- Stop honored: <yes | moved from $X to $Y before exit | N/A (not an exit)>
- Context: <optional, or omitted>
```

### 3. Confirm

State what was logged and where — no silent writes.

---

## Mode: Review

A periodic pass — monthly or quarterly is the natural cadence, matching `performance-benchmarking`'s
suggested rhythm, though the user can ask any time. Pulls every entry since the last review (or
a stated window) and looks for patterns, but only reports what the entries actually show.

**Minimum bar: don't diagnose a trend from a handful of entries.** Fewer than ~5 entries in the
window is "not enough to say anything meaningful yet" — a valid, honest answer, not a reason to
stretch a pattern out of two data points.

With enough entries, check:

1. **Stop-override rate.** Of this window's exits, what fraction moved the stop before exiting
   vs. honored it as originally set? Compare to the prior window if one exists. A rising rate
   is flagged as a hypothesis worth the user's own confirmation — not asserted as a diagnosed
   problem — matching `portfolio-thesis-audit`'s existing convention of surfacing disposition
   effect as a hypothesis, not a verdict.
2. **Thesis rewrites.** Cross-reference against `portfolio-thesis-audit` findings if the user
   has them: a logged reason for continuing to hold that changed since entry, with no new
   *evidence* cited for the change, counts as a rewrite. Flag the count, not each instance as
   a character judgment.
3. **Sourced vs. unsourced drift.** The ratio of screen/skill-sourced entries to tip/video/gut
   entries this window, vs. the prior window. A creeping shift toward unsourced is named
   directly.
4. **Frequency.** Entry count this window vs. prior windows. A spike is flagged as worth asking
   about — not automatically bad, just worth the user's own read on whether it means
   overactivity.
5. **Asymmetric detail.** Are loss-exit entries systematically shorter or vaguer than win-exit
   entries? A common self-protective bias — flagged if the pattern is actually there in the
   text, not assumed.

### Output

A short report: entries reviewed (count + window), each of the five checks above with its
actual number/finding (or "not enough data" per-check if that check's own minimum isn't met),
and nothing else — no unsolicited trade advice, no thesis re-litigation.

## What this does not do

- Does not judge whether any single decision was right — outcome isn't the question, process
  is.
- Does not set or move a stop — `position-exit-rules` owns that; this only records what
  happened to one already set.
- Does not audit whether a held thesis is still valid — `portfolio-thesis-audit`.
- Does not block, slow, or add friction to the decision being logged.
- Does not diagnose a pattern from too few entries — see the Review minimum bar above.
- Does not log a coding error or an unrelated behavioral pattern with no ticker behind it —
  `problem-journal`, `learning-gate`.

## Example invocations

> "I just sold half my GOOGL position — log it. Reason: needed cash for a car repair, not
> thesis-related."

> "Run my journal review for this quarter — am I moving my stops more than I used to?"
