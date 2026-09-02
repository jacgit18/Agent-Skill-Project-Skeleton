---
name: skill-interaction-testing
description: Use after writing or substantially revising a skill in .claude/skills/, before considering it done — tests the new or changed skill against every other skill already in this project for stacking (multiple gates firing in sequence), contradiction (skills giving opposite instructions), silent override (the right skill never fires because a broader one claims the request first), or beneficial chaining (one skill's output feeding another's input). Complements writing-skills, which only tests whether the new skill complies in isolation — it has no step for checking the new skill against siblings already in the project. Also use when an existing skill's trigger description is edited in a way that could newly overlap with another skill's. Skip when the project has fewer than two skills, and skip for edits that don't change what triggers the skill (typo fixes, wording polish, added examples that don't widen or narrow scope).
---

# Skill Interaction Testing

`writing-skills` proves a new skill works alone: baseline fails without it, the skill fixes the failure, refactoring keeps it fixed. None of that touches what happens when the new skill sits next to the other skills already in this project and a real request could plausibly trip more than one. That gap isn't hypothetical here — a new skill was drafted and screened in this project without anyone, including the model doing the drafting, proposing a check against the existing skill set until asked directly. This skill closes that gap as a checklist step after `writing-skills`, not a replacement for it.

## Step 1 — Find overlap candidates

Read every other skill's frontmatter `description` in `.claude/skills/`. For each one, ask a single question: **could one realistic user prompt plausibly trip both this skill and the new one?** Don't reason abstractly about "similar domains" — the failure mode is a shared *trigger shape* (both fire on "vague ask," both fire on "architecture decision," both fire on "cost question"), not shared subject matter. List the candidates; most skills will have zero.

## Step 2 — Write the collision scenarios

For each candidate pair, write one prompt a real user would plausibly send about their actual problem — not a prompt artificially engineered to force both triggers. Include:

- **A multi-turn pair if the new skill is gate-shaped** (it withholds an answer pending a precondition): a good-faith answer on turn 2, confirming the gate releases without a second skill re-firing on the new detail; and separately, the specific pressure named in the skill's own description ("already decided," "just tell me," authority), confirming the gate holds without going rigid or caving.
- **One control prompt** that should trip only the new skill, or only an existing one, and nothing else. This catches the opposite defect — gates firing on everything — which is just as bad as stacking and easy to miss if every test is a deliberate collision.

## Step 3 — Run and observe

Send each scenario to a fresh agent with the full project available — don't strip the skill set down to isolate the new one, since the failure only exists in combination. Isolate the run (background agent, worktree) so nothing lands in the repo uninvited. Watch for:

| Outcome | What it looks like |
|---|---|
| **Hand-off** (good) | One skill classifies and routes to another; one coherent response |
| **Absorption** (good) | The skill that fires covers what a second skill would have asked; the second correctly stays out |
| **Chaining** (good, worth noting) | One skill's output becomes another's input, producing a conclusion neither reaches alone |
| **Stacking** (bad) | Multiple rounds of questions, or the same ground covered twice |
| **Contradiction** (bad) | Two skills give opposite instructions with no resolution |
| **Starvation** (bad) | The right skill never fires because a broader one claims the request first |

## Step 4 — Fix or record

If a bad outcome appears, the fix is almost always a one-line addition to a description — an explicit hand-off note, or a scope narrowing ("does not apply when X, see [other-skill]") — not a rewrite of either skill. Re-run the failing scenario to confirm the fix actually closes it before moving on.

Either way, record the result in project memory: which pairs were tested, what happened, and — if nothing broke — a note not to re-test the same pair without a new reason. An interaction test that isn't recorded gets silently re-run, or silently skipped, the next time a skill is added, which defeats the point of running it at all.

## What this is not

Not a reason to design skills around avoiding overlap. Overlap that hands off or chains cleanly is a feature, not a risk to eliminate — a cost skill and a services skill chaining together can produce a number neither reaches alone. The test exists to catch overlap that fights instead of composes, not to minimize overlap itself.
