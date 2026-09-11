---
name: portfolio-thesis-audit
description: Use when positions are already held and someone wants to know which to keep, which to sell, and which need work — a review of existing holdings against their thesis, not a new trade. Triggers include "which of these should I sell", "review my portfolio", "do I still have a reason to own X", "help me clean up my positions", "audit my holdings", pasting a list of tickers with P&L and asking what to cut, or naming a losing position and asking whether to hold, sell, or buy more. "Research my X position" / "deep dive on a stock I own" when X is already held starts here, not `equity-research-writeup` (which is pre-purchase); this audit may then route to it to build the writeup. For each position it withholds the keep/sell verdict until the user supplies three things themselves: the written thesis (why they own it, stated so it could be proven wrong), whether that thesis is still valid and on what evidence, and the specific exit condition (a price, an event, a size cap — "I'll know when" does not count); a held position with a live thesis but no exit condition routes to `position-exit-rules` to build one. A position missing any of the three cannot be graded "hold". Claude's job is to stress-test what the user brings — is this a thesis or a slogan, is the exit condition actually observable — assign one of three verdicts (hold / exit / research required), and flag behavioral patterns as hypotheses to check: holding a loser to "get back to even" (disposition effect), a large unrealized gain with no entry or exit criteria recorded (luck read as skill), a thesis that traces to a video or a tip with no financials behind it, "averaging down" offered as risk management, or a stated return target / income pressure inflating risk tolerance. It never authors the thesis for the user and never asserts a fundamentals read it has not actually seen. Not for entering or sizing a new position, or re-entering one after an exit — real entry price, stop, and capital producing a share count is `equity-trade-decision`. Not for options positions — covered calls, cash-secured puts, spreads carry assignment and theta risk this review does not model; name the gap and stop. Deciding whether to write covered calls on a position that survives the audit is `covered-call-decision` — run this audit first, then hand off. Not portfolio-level allocation, diversification-vs-concentration policy, sector weights, or rebalancing bands — this grades each position on its own thesis and does not set the target shape; that's `asset-allocation-policy`, and a combined "which do I keep, and is my mix right" request audits the positions here first, then sets/checks allocation there on what survives. Not a held broad index / target-date fund (no per-position thesis to audit); a held sector / factor / thematic fund's tilt thesis is checked in `etf-selection`, not with a stock-style audit here. When it is not yet clear what "clean up my account" or "sort out my positions" means — thesis review vs. rebalancing to a target mix vs. consolidating or closing accounts vs. tax-loss harvesting — that disambiguation is `ambiguity-gate` first; this skill takes the thesis-review reading once it is settled. Not the recurring, scheduled operational pass over the whole account — "do my weekly review", "what do I need to look at this week" is `weekly-portfolio-review`, a procedure that flags individual positions *for* this audit; this skill runs the per-position keep/sell gate once a position is flagged. Not a substitute for a financial advisor, and not a bare conceptual question — "what makes a good thesis", "what is the disposition effect" with no real holdings behind it is `learning-gate`.
---

# Portfolio Thesis Audit

Handed a list of tickers, Claude will happily write a confident-sounding thesis and a
plausible exit condition for every one of them — manufacturing the look of a disciplined
portfolio while the user has done none of the thinking. Paired with a habit of treating
confident delivery as evidence, that is worse than no answer. This skill is a **gate**: for
each position, the *user* states the thesis, its current validity, and the exit condition, or
the position is graded as unjustified. Claude stress-tests what comes back and assigns a
verdict — it does not fill in the thesis.

This is the mirror of `equity-trade-decision`: that skill sizes a position going in, this one
re-examines positions already held.

## What this does not do

- **Enter or size a new position, or re-enter one after an exit.** A real entry price, a
  stop, capital to size against, a share count — that's `equity-trade-decision`. This skill
  produces no share counts and no cycle-stage sizing; when the audit ends in "exit and
  redeploy", the redeploy is a separate `equity-trade-decision` pass.
- **Options positions.** Covered calls, cash-secured puts, spreads — assignment risk, theta
  decay, strike and expiry selection are a different model this review doesn't carry. Name
  the gap and stop rather than run an equity thesis audit on an options overlay. Whether to
  write calls on a position that passes this audit is `covered-call-decision`, downstream of
  here.
- **Portfolio-level allocation policy.** How many names to hold, sector weights, concentration
  vs. diversification, rebalancing bands — this skill grades each position on its own thesis
  and stops there. It does not set or judge the target shape of the whole book — that's
  `asset-allocation-policy`.
- **Tax-advantaged autopilot accounts.** An IRA / 401(k) in broad index or target-date funds
  has no per-position thesis to audit — leave it out of the review. This extends to any
  robo-managed account (e.g. a Wealthfront Roth) regardless of tax treatment: check the
  control type in `asset-allocation-policy`'s capital map before auditing a specific holding
  inside it — a robo's pick is the provider's decision, not a thesis the user owns.
- **A held sector / factor / thematic fund.** It *does* carry a tilt thesis (why this
  exposure, why now) — but that check is `etf-selection`, not a stock-style thesis audit run
  here. A held broad-core index fund has no thesis by design.
- **Replace a financial advisor.** Names when a position's validity call needs research the
  user hasn't done; never asserts a fundamentals read it hasn't actually seen.
- **Answer a bare conceptual question.** "What makes a good investment thesis", "what's the
  disposition effect" with no real holdings on the table is `learning-gate` territory — this
  skill activates once actual positions are named.
- **Coach the user out of a recurring pattern.** The behavioral flags here are hypotheses to
  check on *this* review; turning "I keep doing this" into a deliberate study pass is
  `learning-gate` — not this skill, and not `problem-journal` (which is for coding errors). A
  standing "I keep buying names off YouTube" process gap is `watchlist-screener-criteria`.
- **Build a missing exit rule.** When a holding's thesis is intact but it has no exit
  condition, that is a RESEARCH REQUIRED verdict routed to `position-exit-rules` — this skill
  flags the gap, it does not write the rule.
- **Author the thesis from scratch.** A position whose thesis was never written down, or
  whose validity needs financials the user hasn't opened, is a RESEARCH REQUIRED routed to
  `equity-research-writeup` (the 8-section writeup) — this audit grades what exists, it does
  not write the thesis.
- **Run the periodic whole-account review.** The scheduled weekly walk — positions vs.
  thesis, stops, expiring options, earnings calendar, allocation drift — is
  `weekly-portfolio-review`. It surfaces and routes; when it flags a position's thesis as
  shaky or missing, that position comes here for the full keep/sell gate.

---

## The precondition — three things per position, from the user

Before any position gets a keep-or-sell verdict, the user supplies, **for each position under
review**:

1. **The written thesis.** Why they own it, stated so it could be proven wrong — a testable
   claim ("margins expand as the new segment scales past break-even in the next few
   quarters"), not a direction or a slogan ("it's a good company", "AI is the future",
   "long-term hold"). If there is no written thesis, say so — that is itself the finding.
2. **Current validity.** Is the thesis still true? Yes / no / can't tell — and the evidence
   for that call. "Can't tell without reading the last two quarterlies" is a valid answer and
   routes to *research required*, not *hold*.
3. **The exit condition.** The specific, observable trigger that ends the position: a price
   level, a thesis-invalidating event, a position-size cap. "I'll know when to sell" and "if
   it drops a lot" are not exit conditions.

Once per portfolio, also state: **any return target, income need, or time pressure** on this
money (e.g. "I need this to generate $X/year", "I'm between jobs"). This turns on the
urgency-distortion watch and does not otherwise change the per-position math.

If the user pastes a ticker list with none of this, ask for the three items per position and
**stop**. Do not pre-fill theses or exit conditions to keep things moving — the empty fields
are the point.

"Just give me your call" / "I don't want to write a thesis for each one" does **not** release
the gate — that is a reason to want it skipped, not a thesis. The rubric already has the
answer for it: a position with no stated thesis is **EXIT — no surviving thesis**, never a
keep/sell read pulled from ticker knowledge.

Claude's contribution once the precondition is met is deliberately narrow:

- Judge whether each stated thesis is **falsifiable** or just a direction.
- Judge whether each exit condition is **observable** — could a third party tell from the
  outside that it had triggered?
- Apply the verdict rubric.
- Raise behavioral flags **as hypotheses to check**, never as settled diagnoses.

---

## The audit block

Goes **before** any "keep it" / "sell it" answer. Every line appears for every position; an
unknown is written `not supplied — ask: <the question>`, never omitted or assumed favorable.

```
Portfolio thesis audit — <n> positions reviewed

Return target / income pressure:  <stated: "<what>" | none stated>
  Urgency-distortion watch:        <ON — any "hold for the recovery" or upsized risk gets
                                   checked against this | off>

── <TICKER> ────────────────────────────────────────────────
  Thesis (user-stated):     <the thesis verbatim | NONE SUPPLIED>
  Falsifiable?              <yes — names what would have to be true | no — it's a direction
                            or a slogan, nothing to disprove>
  Still valid?              <user's call + evidence cited | can't be judged without: <the
                            specific unread document / unresolved question>>
  Exit condition:           <the specific trigger | NONE — "I'll know" / "if it tanks" don't
                            count>
  Observable?               <yes — an outsider could tell it fired | no — restate it as a
                            number or an event>
  Unrealized P&L:           <+/- $<n> or +/- <pct> | unknown>
  Behavioral flags:         <disposition effect — losing position, stated plan is "get back
                            to even" or "average down" | luck-as-skill — large gain, no entry
                            criteria recorded, no exit condition | informal input — thesis
                            traces to <video / tip / "I use the product">, no financials seen
                            | averaging-down-as-risk-management — named as such; it isn't |
                            none>
  Verdict:                  HOLD — thesis intact | EXIT — no surviving thesis |
                            RESEARCH REQUIRED — <the specific task>, by <date>

  [repeat the block per position]

Portfolio summary:
  HOLD: <n>    EXIT: <n>    RESEARCH REQUIRED: <n>
  Positions with no written thesis at all:  <n>   ← the number to watch
  Behavioral patterns raised (hypotheses, not diagnoses): <list, or "none">
  Not audited here: <cash-equivalent / options / autopilot-account positions set aside, and
                    why>
```

---

## The verdict rubric

| Verdict | When |
|---|---|
| **HOLD — thesis intact** | All three present: a falsifiable thesis, a still-valid call backed by named evidence, **and** an observable exit condition. Anything less is not a hold. |
| **EXIT — no surviving thesis** | No written thesis; **or** the thesis is acknowledged dead / invalidated; **or** the only stated reason to keep it is to "get back to even" or recover the loss. The loss is not a reason to hold — "is this the best use of this capital now?" is the question, never "how do I get back to even". |
| **RESEARCH REQUIRED** | A thesis exists and is plausibly live, but its current validity can't be judged without work the user hasn't done (unopened financials, an unresolved thesis-invalidating question), **or** the exit condition is missing while the thesis is otherwise intact. Name the **specific** task and a **date** — an open-ended "look into it" collapses back to a silent hold. When the gap is a missing exit condition, the specific task is: run `position-exit-rules` for that position (measured from the current price) to build the rule set. When the gap is an unwritten thesis or unread financials, the task is: run `equity-research-writeup` for that name, by <date>. |

"EXIT" is a verdict on the thesis, not an order. Timing, tax lots, and what replaces the
position are out of scope — any re-entry is a fresh `equity-trade-decision`.

A position whose thesis is intact but sits on a large loss is still a HOLD — *if* the three
boxes are genuinely ticked. The audit doesn't punish red P&L; it punishes the absence of a
reason.

---

## Behavioral flags — raise as hypotheses, never diagnoses

These are patterns to name and check, phrased as "this looks like it might be X — is it?",
not verdicts on the user:

- **Disposition effect.** A losing position held while winners get trimmed; a default
  response of "hold longer and buy more" to being down. The tell: the stated plan for a
  loser is "wait for it to recover" or "average down", with no fresh thesis behind the
  add.
- **Luck misattributed as skill.** A large unrealized gain with no entry criteria ever
  written down and no exit condition now. The gain is not evidence the thesis was right — it
  may be evidence of a rising market. A winner with no exit plan is not a validated position.
- **Urgency distortion.** A stated return target or income pressure (unemployment, a
  withdrawal need) inflating risk tolerance in ways easy to underestimate. Any "hold for the
  recovery" or willingness to size up gets checked against it explicitly.
- **Informal input treated as research.** The thesis traces to a video, a forum, a tip, or
  "I use the product and like it" — with no financials opened. Product familiarity is not a
  thesis; it's a reason to go do the research.
- **Averaging down framed as risk management.** It isn't. Buying more of a losing position is
  a fresh entry decision — route it to `equity-trade-decision` with its own checklist and
  sizing — not a reflex to being wrong.

---

## Red flags — the audit isn't done

- A keep/sell verdict handed down before the user supplied the thesis / validity / exit for
  that position.
- A thesis Claude wrote or completed on the user's behalf, then graded.
- "HOLD" assigned with a missing or unobservable exit condition.
- "RESEARCH REQUIRED" with no specific task and no date — that's a hold in disguise.
- A losing position graded HOLD on the strength of the loss itself ("it's due for a bounce").
- Options, margin, or a new entry pulled into a review built for plain long-equity positions
  already held.
- The portfolio's return target named by the user and then never referenced again in the
  verdicts.

---

## Example invocations

> "Here are eight positions with P&L. Which do I cut?"

Ask for the thesis, the current-validity call, and the exit condition for each of the eight,
plus any return/income pressure on the account. Stop there — no verdicts until those come
back. Don't offer a provisional read from ticker knowledge.

> "I'm down $900 on this one, a guy on YouTube called it. Should I hold or average down?"

The audit block for that position: thesis `NONE SUPPLIED` (a call from a video is not a
thesis), exit condition `NONE`, flags: informal-input + disposition-effect (the "average
down" framing). Verdict: **EXIT — no surviving thesis**. If the user wants to open a *new*
position in the name on a real thesis, that's `equity-trade-decision`, sized from scratch.

> "Should I buy more NVDA at $120 with a $110 stop?"

Not this skill — that's a new entry with a real price and stop. `equity-trade-decision`.

> "What's the disposition effect and how do I avoid it?"

No holdings on the table — answered directly, no gate. `learning-gate`.

---

## Portability

Repo-agnostic. Writes nothing; produces the audit block in chat. The behavioral flags are
generic — copy the `portfolio-thesis-audit/` directory into another repo's `.claude/skills/`
to use it there. Pairs with `equity-trade-decision` (new entries and sizing) as the two ends
of a position's life, and with `position-exit-rules` (building a missing exit rule for a held
position).
