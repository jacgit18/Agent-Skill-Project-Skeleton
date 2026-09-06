# Task 2 Review: System Design Communication Agent

## Summary of Implementation

The implementer created `system-design-communication/` with all four files the brief specified:

- `AGENTS.md` — agent definition with frontmatter, Purpose section, and all three modes (Design Walkthrough, Mock Interview, Tradeoff Defense).
- `prompts/explain-design.md` — Design Walkthrough prompt, brief's structure preserved verbatim, plus an added "Notes on running this well" section.
- `prompts/interview-simulation.md` — Mock Interview prompt, brief's script preserved verbatim, plus an added "Notes on running this well" section.
- `README.md` — usage guide with mode table, invocation examples per mode, success criteria, and tips.

The prompts were tested via two parallel subagents, each given only the relevant prompt file (not the implementer's rationale) and instructed to play both the coach/interviewer role and a plausible candidate role, then critique independently. Findings from those tests drove small, targeted additions to the "Notes" sections of both prompt files — the brief's core structure/script was left untouched in both files. Work was committed as `4941236`.

## Spec Compliance: ✅

- All four required files present at the specified paths, verified directly against the working tree and the commit's file list (4 files changed, matches exactly).
- `AGENTS.md` defines all three modes, each with a "What it does" and "Success" line, matching the brief's structure exactly (byte-for-byte, in fact — the implementer copied the brief's example content rather than deviating from it).
- `explain-design.md` follows the required structure: ask → listen for (purpose/architecture/data flow) → ask follow-ups → point out gaps without filling them → don't critique. Core structure matches the brief verbatim; additions are appended notes, not replacements.
- `interview-simulation.md` follows the required script: question → listen/press/introduce constraints → summarize + ask what they'd change + give feedback → don't reveal "the right answer." Core script matches the brief verbatim.
- `README.md` has all four required elements: mode selection table ("When to Use Each Mode"), invocation examples per mode ("How to Invoke"), success criteria ("Success Looks Like"), and tips ("Tips").
- Prompts were tested (via subagent simulation, see Quality section) and refinements were made based on that testing.
- Commit made: `4941236`, "feat: add system design communication agent for interview prep" — matches the brief's suggested commit message, correct file scope (only `system-design-communication/`), no unrelated changes bundled in.

No deviations from spec found.

## Quality: ✅

**Design Walkthrough prompt (`explain-design.md`):** Effective for its stated purpose. The added notes address real failure modes rather than padding: explicitly flagging the example follow-ups as illustrative (not a literal checklist to pattern-match) prevents a plausible failure where the agent waits for the candidate to say the word "caching" before asking about invalidation. The pacing guideline (2-4 follow-up threads before moving to recap) closes a real gap the brief's script leaves open — nothing in the original script bounds session length, so an over-eager coach could spiral into an unending audit. The "if they genuinely don't know something, that's a successful outcome" note is a good instinct-check against the natural pull to over-help.

**Mock Interview prompt (`interview-simulation.md`):** Effective for simulating a realistic interview. The added notes are well-targeted: staying in character until debrief (with a defined exception for in-character acknowledgment of self-identified gaps, explicitly framed as "not coaching") resolves a genuine ambiguity the brief's script didn't address — without this note, an interviewer persona would have no guidance on a plausible scenario (candidate says "oh, I hadn't thought about that") and might either break immersion or feel unnaturally silent. The "one nudge if they freeze" and "calibrate pressure, don't stack curveballs" notes match how real system design interviews are actually run, which supports the interview-focused global constraint.

**README.md:** Clear and complete. The mode table, invocation examples, and success criteria map directly to the brief's required content. One good addition beyond spec: a tip about redirecting an off-target mock interview question, which anticipates a real usage friction point.

**Refinements based on testing:** All three cited refinements (illustrative-not-checklist framing, pacing guidance, in-character acknowledgment) trace directly to specific findings in the two test transcripts described in the report, not speculative additions. This is exactly the kind of narrowly-scoped, evidence-driven refinement the task's "learn by using" constraint calls for.

**Testing methodology:** Using independent subagents to play both interviewer/coach and candidate roles (without visibility into the implementer's design rationale) is a reasonable proxy for objectivity in a non-interactive review context, consistent with how Task 1 handled a similar constraint. It surfaces real prompt ambiguities (as evidenced by the two genuine gaps found) rather than being a rubber-stamp exercise. It is not a substitute for the user's own live practice session, and the report is appropriately honest about that limitation, correctly deferring the actual anxiety-reduction success metric to real use.

**Mode 3 (Tradeoff Defense) — noted, not a failure.** The brief's file list only requested `explain-design.md` and `interview-simulation.md`; no prompt file for Tradeoff Defense was required. The implementer flagged this explicitly in both the report and the README (with a concrete recommendation to split it into its own file if it sees real use), which is the right way to handle a spec gap — visible and actionable rather than silently absent.

No gaps or weaknesses found beyond what the implementer already self-identified.

## Findings

None. Approved as-is.

## Commit Verified

Yes — `4941236`, "feat: add system design communication agent for interview prep", 4 files changed (139 insertions), scope limited to `system-design-communication/` as intended.
