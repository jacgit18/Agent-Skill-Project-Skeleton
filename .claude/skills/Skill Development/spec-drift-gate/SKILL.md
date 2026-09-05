---
name: spec-drift-gate
description: Use before starting substantial AI-assisted implementation work — a feature, a refactor, a new system, a script — that will span multiple files, multiple turns, or multiple sessions, and no written spec exists yet for it. Also use mid-build, at a natural checkpoint (a new phase starting, a session resuming after a gap, a proposed action that touches something the original ask never mentioned), to check work so far against the spec that was written at the start. Not for a single, fully-specified, one-shot request (fix this bug, add this function, answer this question) — nothing to gate when the request already is the spec. Not system-design specifically — purpose/audience/functional/non-functional numeric targets for a whole system is `design-scoping`'s front door; this skill treats a settled design-scoping scope statement as an equivalent input and doesn't re-gate it, but still wants the build-level spec (tradeoffs actually weighed, an explicit out-of-scope line, a controlled-experiment slice) once implementation starts. Not a one-shot "which of several readings did you mean" check on a single request — `ambiguity-gate` (resolve the reading first; once intent is settled as "build this multi-step thing," this skill's spec requirement applies next, not a second clarifying question). Not auditing the blast radius of one already-decided change against the existing codebase's dependents — `change-surface-audit` (this skill audits the build against its OWN stated plan over time, not the codebase against a proposed change). Not the end-of-session context dump — `session-handoff` (this skill's spec is what a handoff should point back to, not a replacement for writing one).
---

# Spec Drift Gate

Long AI-assisted builds fail less often from a wrong first answer than from a slow, unnoticed drift away from what was actually asked — a scope that grows one "while I'm in here" at a time, a tradeoff that gets asserted in the final answer but was never actually weighed, a plan that existed in someone's head at the start of session one and nowhere in writing by session four. This skill forces the plan into writing before code starts, and checks the build against it as it goes — instead of only ever checking the most recent message.

## Step 1 — Does the gate apply?

| Situation | What to do |
|---|---|
| A single, fully-specified request — the request itself is the spec | Skip this skill. Do not manufacture a spec document for "add a null check here." |
| A request to design, architect, or redesign a whole system | `design-scoping` owns that front door. Once its scope statement is settled, treat it as this skill's Step 2 items 1 and 3 (problem framing, scope boundary) satisfied — but items 2 and 4 (tradeoffs actually weighed, a controlled-experiment slice) are not design-scoping's job and are still required before moving to Step 3. |
| Substantial implementation about to start — multiple files, multiple turns, or multiple sessions expected — and no written spec exists | Continue to Step 2. |
| Mid-build: a new phase is starting, a session is resuming after a gap, or a proposed action touches something the original spec never mentioned | Skip to Step 4. |

## Step 2 — The gate: refuse to start writing code until a spec exists

Before touching a file, get these stated — draft them from context and confirm with the user rather than silently skipping, the same "state it back, don't invent it unchallenged" discipline other gates in this catalog use:

1. **Problem framing** — what problem, for whom, in a sentence or two. Not the request restated; the actual need behind it.
2. **Tradeoffs actually considered** — at least one real alternative named and why it lost. A tradeoff that shows up for the first time in the finished answer, never having been weighed against anything, is a rationalization, not a decision.
3. **Scope boundary** — explicit in-scope *and* explicit out-of-scope. The out-of-scope line is the one that gets skipped, and it is the one that actually stops drift later — "in scope" alone doesn't bound anything.
4. **A controlled-experiment slice**, when the approach is genuinely uncertain or the infrastructure commitment is heavy — scope a narrow, cheap-to-discard first slice (just the read path, just one component, just the frontend piece) to learn real system behavior before committing to the full build. Skip this for routine, well-understood work — not every change needs a spike.

Write it down — a markdown file, or at minimum a stated block in the conversation the user can point back to. This is the artifact Step 4 checks against; without it, Step 4 has nothing to compare.

## Step 3 — Precision instruction

Once the spec is settled, the next instruction should be scoped to one slice of it — the next concrete step on the map, not "now build all of it." A spec describes the destination; a precision instruction is the next move toward it.

## Step 4 — Drift check at each checkpoint

At a checkpoint, diff the proposed or actual work against the written spec:

- **Inside the stated scope?** Proceed.
- **Not in the spec?** This is a decision, not a default. Say so out loud, and do one of two things — never neither:
  - **Amend the spec** — write down what's expanding and why the boundary is moving.
  - **Pull back** to what was actually scoped.

Never silently expand ("while I'm in here, I'll also...") without naming that it's happening. A silent expansion is exactly the failure this step exists to catch.

## Red flags — this gate is not doing its job

- Multi-file or multi-session work started with no spec anyone could point back to.
- A tradeoff appears in the final answer that was never actually weighed against an alternative.
- Only "in scope" was ever stated — "out of scope" never got a line.
- A later action touches something the spec never mentioned, and nobody flagged it.
- The spec was written once at the start and never looked at again across multiple sessions or phases.
- A controlled experiment was skipped on a genuinely uncertain approach in favor of building the whole thing at once and finding out later.
- "It's basically the same thing" is used to fold a new piece of work into an already-approved scope instead of naming it as an amendment.
