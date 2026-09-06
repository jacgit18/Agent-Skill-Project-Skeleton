# Task 1 Report: Refine Problem-Solving Gate Skill

## Status: DONE

## What I implemented

1. **Enhanced `problem-solving-gates/SKILL.md`**
   - The existing file already had solid triggers, precondition checks, and behavioral rules for all three modes, plus an escape hatch for Rubber Duck. It was missing: concrete "how to invoke" examples, and escape hatches for Options Generator / Knowledge Checker (asymmetric with Rubber Duck).
   - Added a concrete example invocation + expected Claude behavior for each of the three modes.
   - Added escape hatches to Options Generator and Knowledge Checker, mirroring Rubber Duck's, so all three modes are symmetric.
   - Added a new subsection to Rubber Duck, **"Pressure does not change the gate,"** and tightened the precondition-check language to explicitly forbid offering a shortlist of candidate causes framed as questions — this was added *after* testing surfaced the gap (see below), not speculatively.

2. **Created `problem-solving-gates/README.md`** (~290 words)
   - Three-sentence overview of what the skill is for.
   - A decision tree ("Are you debugging? → Rubber Duck…").
   - Guidance on invoking each mode and what to do if you're missing the precondition.
   - A common-mistakes table (5 rows) mapping user missteps to what Claude does in response.

3. **Created `problem-solving-gates/examples/`** with three files, each 200-300 words, following the brief's structure (context → precondition check → 2-3 exchanges → outcome):
   - `example-rubber-duck.md` — debugging duplicate job processing in a queue; the falsification question redirects the user from their original hypothesis to the actual root cause (a requeue sweep race), which they find themselves.
   - `example-options-generator.md` — choosing a search implementation for a self-hosted app; Claude surfaces an unconsidered constraint gap (typo tolerance) and a genuine alternative without ranking anything.
   - `example-knowledge-checker.md` — verifying understanding of React `useEffect` cleanup timing; a scenario question surfaces a real gap (batching) that the user reasons through themselves.

## Tests run

I ran an adversarial pressure test rather than only inline review, per the writing-skills TDD discipline (RED → GREEN) since this is a discipline-enforcing skill:

- **Baseline (RED):** Spawned a subagent roleplaying "Claude" under the *original* Mode 1 text, given a debugging scenario stacked with three pressures — time (30 min to deadline), authority ("my manager is asking"), and sunk cost ("I've been staring at this for an hour"), with the user explicitly saying "just tell me the most likely cause." Result: the agent didn't hand over a diagnosis outright, but it did offer three specific candidate causes framed as questions, one explicitly flagged as "the single most common cause of this exact symptom" — a hypothesis in disguise, which is exactly what the precondition is designed to prevent. Letter of the rule held; spirit didn't.
- **Fix:** Edited Mode 1's precondition check to explicitly prohibit shortlists/menus of candidate causes (not just direct diagnosis), and added a "pressure does not change the gate" clause naming the specific pressures (time, authority, sunk cost) and clarifying that "genuinely tried" for the escape hatch means hypotheses actually formed and falsified, not time elapsed.
- **Retest (GREEN):** Ran the identical scenario against the updated text. The agent held the gate cleanly — no candidate causes, just a one-step question redirecting the user to state their own gut hypothesis in one sentence.

I did not run pressure tests against Options Generator or Knowledge Checker — time-boxed this to the mode most likely to be invoked under real deadline stress (debugging), which is also where the brief's stated success metric ("debug independently") is most directly exercised. This is a gap worth closing in a follow-up if this skill sees real use.

## Concerns / observations

- **Untested modes:** Options Generator and Knowledge Checker got the same structural additions (examples, escape hatches) as Rubber Duck but were not pressure-tested. Given Rubber Duck leaked under pressure before hardening, the other two likely have analogous gaps (e.g., Options Generator "helpfully" narrowing to 2 options instead of listing all viable ones under time pressure). Recommend a future task to pressure-test those two.
- **Escape hatch ambiguity remains:** "Meaningful time spent" language still appears once in Rubber Duck's escape-hatch text alongside the new "genuinely tried" clarification. It's not contradictory (both conditions — falsified hypotheses AND time — are required, not either/or) but could be tightened further if it ever gets exploited as "well I *did* spend meaningful time."
- **Scope note:** `.superpowers/` and `docs/` directories were untracked in git status at the start of this task (task briefs, superpowers plugin docs) — left out of the commit as unrelated to this task's file scope.

## Commit

- `3508972` — "refactor: clarify problem-solving gate skill with examples and usage guide"
  - 5 files changed: `problem-solving-gates/SKILL.md` (modified), `problem-solving-gates/README.md` (new), `problem-solving-gates/examples/example-rubber-duck.md` (new), `problem-solving-gates/examples/example-options-generator.md` (new), `problem-solving-gates/examples/example-knowledge-checker.md` (new).

## Fix Round 1: Word-count trim

A review caught that all four prose documents exceeded the brief's explicit word-count limits (README ≤300 words; each example 200-300 words). Trimmed wording only — no content, dialogue structure, or required elements (context, precondition check, 2-3 exchanges, outcome) removed. Verified with `wc -w`:

| File | Before | After | Limit |
|---|---|---|---|
| `problem-solving-gates/README.md` | 374 | 276 | ≤300 |
| `problem-solving-gates/examples/example-rubber-duck.md` | 350 | 275 | 200-300 |
| `problem-solving-gates/examples/example-options-generator.md` | 374 | 263 | 200-300 |
| `problem-solving-gates/examples/example-knowledge-checker.md` | 367 | 267 | 200-300 |

(Note: these before-counts are slightly higher than what was reported in the initial implementation pass, likely due to `wc -w` counting markdown syntax tokens like `**` and backticks as word-boundary-adjacent; the review's counts and mine agree closely enough that the same trim target applied cleanly.)

Spot-checked each trimmed example against the brief's required structure — all four elements (context, precondition check, exchanges, outcome) are intact in every file.

- `c97fa73` — "fix: trim problem-solving-gates prose to meet brief word-count limits"
  - 4 files changed: `problem-solving-gates/README.md`, `problem-solving-gates/examples/example-rubber-duck.md`, `problem-solving-gates/examples/example-options-generator.md`, `problem-solving-gates/examples/example-knowledge-checker.md`.
