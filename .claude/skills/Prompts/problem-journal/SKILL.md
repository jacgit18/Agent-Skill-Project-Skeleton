---
name: problem-journal
description: Use after a coding problem (a bug, an unexpected error, a "why doesn't this work") gets resolved and the user wants it recorded — "log this problem", "add this bug to my log", "was that worth learning from", "have I hit this before", "document this issue" — or when reviewing whether a past problem deserves a deliberate study pass. Writes a dated entry to `.claude/_Prompts/problems-log.md`: the symptom/cause/fix, a recurrence count from grepping the prompt-archive logs (`.claude/_Prompts/logs/*.md`) for the same error signature or concept, a classification (recurring pattern vs. one-off; fundamental concept vs. environmental fluke), and a worth-learning verdict tied to that count — never asserted without it, the same discipline `technical-cost-decision` forces for dollar figures. This is a retrospective procedure, not a live gate: it runs *after* a problem is already resolved (or on-demand against history), so it does not replace `learning-gate` (which sets how much help Claude gives on the *current, live* request) or `problem-solving-gates`' Rubber Duck (which forces the hypothesis *during* the debugging itself — this skill assumes that already happened, however it happened, and journals the outcome). Once an entry's verdict is "worth learning," this skill names the next step and hands it off — it does not teach the concept itself; that's `learning-gate` (S0, teach the minimum) or `problem-solving-gates`' Knowledge Checker (verify after self-study). Not for archiving a reusable prompt or logging a session's raw prompts verbatim — that's `prompt-archive`, whose dated logs this skill reads from but writes a different, curated artifact into. Not for evaluating whether a prompt performs well — that's `prompt-tester`.
---

# Problem Journal

A bug gets fixed and the conversation moves on — nothing records whether this was the third
time this month you've hit the same class of mistake, or a one-off that's fine to forget.
This skill closes that gap: it journals a resolved problem, checks how often its shape has
actually recurred (by count, not by feel), and only then says whether it's worth a
deliberate study pass — never the reverse.

## Out of scope — hand these off

- **How much help Claude gives on the *current* request** — `learning-gate`. This skill runs
  after the problem is already resolved; it doesn't decide live assistance level.
- **Forcing the hypothesis during an active debugging session** — `problem-solving-gates`
  (Rubber Duck). This skill assumes the debugging already happened — through Rubber Duck or
  otherwise — and records the outcome. It is not an alternative path around forming a
  hypothesis; if the user is mid-debug with no hypothesis yet, that's Rubber Duck's gate,
  not this skill.
- **Teaching the flagged concept** — once a verdict is "worth learning," name the next step
  (a `learning-gate` S0 pass to teach the minimum, or `problem-solving-gates`' Knowledge
  Checker to verify after self-study) and stop. Don't teach it inline in the same turn — that
  collapses the verdict and the lesson into one step and skips the actual rep.
- **Archiving a reusable prompt, or logging a session's raw prompts verbatim** —
  `prompt-archive`. This skill reads that skill's dated logs as a recurrence-search corpus,
  but writes a different file with different content (curated problem entries, not raw
  prompt text).
- **Evaluating whether a prompt performs well** — `prompt-tester`. Unrelated.

---

## What counts as a problem

A bug, an unexpected error, a "why doesn't this work," a debugging session, a misunderstood
API/library behavior. **Not** a routine feature request, a style preference, or a design
decision — those aren't problems in this sense, even if they took a while to work through.
If it's unclear whether something qualifies, ask in one line rather than journaling a
feature build as if it were a bug.

## The gate

Two things must come from the actual record, not be invented:

1. **The problem itself** — symptom, root cause (if known), and the fix. Source this from
   **the current session's actual resolved context** whenever the problem was just worked
   through in this conversation — that's the only place the *resolution* is reliably known.
   If asked to journal a problem from an **old session** (a bare line in a past prompt log,
   or a memory), do not reconstruct the fix from guesswork — the automatic prompt log only
   captures the user's submitted text, never Claude's answer or the outcome. Ask the user to
   state what the problem and fix actually were.
2. **The recurrence count** — grep `.claude/_Prompts/logs/*.md` (and, if relevant, the
   archived prompt library) for the error signature, the concept name, or a close paraphrase.
   Report the actual count and which files it appeared in — "3 hits across
   `2026-08-12.md`, `2026-08-29.md`, `2026-09-04.md`" — never "this comes up a lot" or "I
   don't think this is common" without having actually searched.

## Classifying and judging

With the problem and the count in hand:

- **Recurring pattern (2+ hits of the same shape) vs. one-off.** A pattern is not "you asked
  about databases three times" — it's the same *kind* of mistake or gap (an off-by-one, a
  missed `await`, a misunderstood cache-invalidation rule) showing up across otherwise
  unrelated tasks.
- **Fundamental concept vs. environmental fluke.** A misunderstood language/library semantic
  recurs because the gap in understanding is still there. A broken dependency version or a
  typo doesn't recur in any meaningful sense even if superficially similar errors appear —
  don't count coincidental error-message similarity as a pattern.
- **Delegated fully vs. attempted first**, if it's known from the original exchange (e.g.
  `learning-gate` was engaged and classified the original request as execution intent, so no
  attempt was expected) — this shapes *how* the learning gap formed, not whether it exists.

**The verdict — worth a deliberate study pass, yes or no — must name which of the above
produced it.** "Worth learning: yes, this is the 3rd time (see count) this exact category of
bug has appeared, and it's a semantic gap (async/await), not an environmental fluke" is a
real verdict. "This seems like something you should probably learn" is not — go back and get
the count first.

A first-time, environmental, or trivially-explained problem gets **"not worth a dedicated
pass"** as a perfectly complete verdict — don't manufacture a lesson to seem thorough.

---

## Output block

```
Problem:              <symptom + root cause + fix, one or two sentences>
Source:               <this session | user-stated (old session, no resolution in the log)>
Recurrence check:     <N hits in <file list> | none found> — grepped for: <term(s) searched>
Classification:       <recurring pattern | one-off> · <fundamental concept | environmental
                      fluke> · <delegated fully | attempted first | unknown>
Worth learning?:       yes/no — <the one driving reason, tied to the count/classification>
Entry written:         .claude/_Prompts/problems-log.md
Next step:            <none | learning-gate (teach the minimum) | problem-solving-gates
                      Knowledge Checker (verify after self-study)>
```

## Writing the entry

Append to `.claude/_Prompts/problems-log.md` (create it with a `# Problem Journal` heading
if absent):

```markdown
## 2026-09-05 — <short problem title>

**Problem:** <symptom + root cause + fix>
**Recurrence:** <N hits — file list, or "first occurrence">
**Classification:** <recurring/one-off> · <fundamental/environmental>
**Worth learning:** <yes/no> — <reason>
**Next step:** <as in the output block, or "none">
```

Report back only the path and a one-line confirmation — don't dump the file contents back
into chat on top of the output block already shown.

---

## Red flags — the entry isn't done

- A "worth learning: yes" (or "no") verdict with no recurrence count or classification behind
  it.
- A resolution reconstructed for an old session Claude wasn't present for, instead of asking
  the user what actually happened.
- Teaching the concept in the same turn instead of naming the handoff and stopping.
- A routine feature request or style choice journaled as if it were a bug.
- "This comes up a lot" with no grep actually run against the logs.

---

## Portability

Repo-agnostic, but assumes this project's `.claude/_Prompts/logs/` convention
(`prompt-archive`'s automatic hook) exists to search against — without it, the recurrence
check has nothing to grep and should say so rather than guessing a count. Writes to
`.claude/_Prompts/problems-log.md`. Copy the `problem-journal/` directory into another repo's
`.claude/skills/` to use it there, alongside `prompt-archive`.
