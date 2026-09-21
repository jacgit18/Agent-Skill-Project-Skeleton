---
name: spec-drift-gate
description: Use before substantial AI-assisted implementation (feature, refactor, new system, script) spanning multiple files, turns, or sessions with no written spec. Triggers on vague one-liners too ("make me a dashboard") — Step 2a runs a short interview to draft the spec; a whole-system one-liner still goes to design-scoping first (Step 1). Also use mid-build at a checkpoint (new phase, resumed session, action the ask never mentioned) to diff work against the spec. Not a single fully-specified one-shot request. Not design-scoping (whole-system scope; its settled statement counts as input here). Not ambiguity-gate (one request, several readings). Not change-surface-audit (blast radius of one change). Not session-handoff (end-of-session dump). Not learning-gate's guided-walkthrough (user performs it). Not incremental-build-pacing (delivery cadence after this gate names a slice). Substantial slices can go to the spec-executor subagent (Step 3a); its report is a Step 4 checkpoint, never self-approval.
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
| Mid-build: the user wants the remaining slices delivered slowly / file by file to learn the codebase | Hand the *delivery* to `incremental-build-pacing` once a slice is named; the spec and the Step 4 drift checks stay here. |

## Step 2 — The gate: refuse to start writing code until a spec exists

Before touching a file, get these stated — draft them from context and confirm with the user rather than silently skipping, the same "state it back, don't invent it unchallenged" discipline other gates in this catalog use:

1. **Problem framing** — what problem, for whom, in a sentence or two. Not the request restated; the actual need behind it.
2. **Tradeoffs actually considered** — at least one real alternative named and why it lost. A tradeoff that shows up for the first time in the finished answer, never having been weighed against anything, is a rationalization, not a decision.
3. **Scope boundary** — explicit in-scope *and* explicit out-of-scope. The out-of-scope line is the one that gets skipped, and it is the one that actually stops drift later — "in scope" alone doesn't bound anything.
4. **A controlled-experiment slice**, when the approach is genuinely uncertain or the infrastructure commitment is heavy — scope a narrow, cheap-to-discard first slice (just the read path, just one component, just the frontend piece) to learn real system behavior before committing to the full build. Skip this for routine, well-understood work — not every change needs a spike.

Write it down — a markdown file, or at minimum a stated block in the conversation the user can point back to. This is the artifact Step 4 checks against; without it, Step 4 has nothing to compare.

## Step 2a — When context doesn't supply the spec: run a scoped extraction interview

If the request is a one-liner, or the four items above can't be drafted honestly from what's on the table, interview for them — don't guess, and don't start building to find out.

- **Batch, don't barrage.** 2–3 rounds of 4–6 numbered questions, not fifteen at once. Round 1 is fundamentals (the problem, who it's for, must-haves vs. explicitly out); later rounds drill into what those answers exposed. You can't ask a sharp edge-case question before you know what the thing is.
- **Every question must be able to change the build.** If you'd do the same thing regardless of the answer, cut it. Never ask what the conversation, the files, or memory already answered.
- **Probe across:** what triggered the request and what success looks like in the user's own words; audience and context of use; scope in *and* explicitly out; constraints (deadline, stack, brand, platform, integrations); where data comes from and real examples; edge cases and failure states; taste references; whether it's one-off or maintained; and what would make them reject the result on delivery — that last one is often the most revealing.
- **Adapt depth to stakes.** A throwaway script needs a few questions; a client-facing build needs the full pass.
- **If the user says "just build it":** don't gatekeep. Compress to the 3 questions whose answers would most change the outcome, say you'll proceed on stated assumptions, and if they decline even those, build immediately with every assumption listed at the top of the deliverable so a wrong guess is visible and cheap to fix.

Feed the answers straight into the Step 2 spec block, confirm it, then continue. Once that spec exists, don't re-interview the same build — later revisions get at most one or two clarifying questions, and a contradiction with the spec is a Step 4 decision, not a fresh interview.

## Step 3 — Precision instruction

Once the spec is settled, the next instruction should be scoped to one slice of it — the next concrete step on the map, not "now build all of it." A spec describes the destination; a precision instruction is the next move toward it.

## Step 3a — Execution handoff, when the slice warrants running unattended

Most slices just get built inline, in the same conversation — that's still the default. Consider handing a slice to the `spec-executor` subagent (background, worktree-isolated) instead when the slice is substantial enough to run unattended and doesn't need turn-by-turn judgment calls: a well-bounded chunk of a multi-phase build, a controlled-experiment slice from Step 2 item 4, or a slice starting after the user has stepped away and won't be available to answer questions mid-build.

Brief the subagent with exactly three things: the written spec, the precision instruction for this one slice, and the worktree to run in. Nothing else — a spec-executor that has to guess at scope is the exact failure this skill exists to prevent, just relocated into an agent instead of a foreground conversation. The subagent commits its own work in the worktree but does not merge or push; it reports back what it did, what it flagged as out-of-spec, and what it thinks the next slice is — treat that report as input to Step 4, not as a merge-ready result.

Don't reach for this by default. A slice small enough to finish in the current conversation, or one where the next move genuinely depends on a judgment call only the user can make, stays inline.

## Step 4 — Drift check at each checkpoint

At a checkpoint, diff the proposed or actual work against the written spec:

- **Inside the stated scope?** Proceed.
- **Not in the spec?** This is a decision, not a default. Say so out loud, and do one of two things — never neither:
  - **Amend the spec** — write down what's expanding and why the boundary is moving.
  - **Pull back** to what was actually scoped.

Never silently expand ("while I'm in here, I'll also...") without naming that it's happening. A silent expansion is exactly the failure this step exists to catch.

**A `spec-executor` report is a checkpoint, not an approval.** Run the same diff against it: check its "still in scope" claim against the actual spec rather than trusting the subagent's own assessment, and treat every "flagged — not in spec" item as a real Step 4 decision (amend or pull back) — the subagent surfaces drift, it doesn't resolve it.

## Red flags — this gate is not doing its job

- Multi-file or multi-session work started with no spec anyone could point back to.
- A tradeoff appears in the final answer that was never actually weighed against an alternative.
- Only "in scope" was ever stated — "out of scope" never got a line.
- A later action touches something the spec never mentioned, and nobody flagged it.
- The spec was written once at the start and never looked at again across multiple sessions or phases.
- A controlled experiment was skipped on a genuinely uncertain approach in favor of building the whole thing at once and finding out later.
- "It's basically the same thing" is used to fold a new piece of work into an already-approved scope instead of naming it as an amendment.
- A `spec-executor` report on a nontrivial slice has nothing in its "flagged — not in spec" section and that absence is trusted at face value instead of being checked.
- A `spec-executor` result got merged or pushed on the strength of the subagent's own report, with no Step 4 diff performed by whoever's reviewing it.
