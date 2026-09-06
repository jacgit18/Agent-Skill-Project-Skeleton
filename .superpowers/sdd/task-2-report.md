# Task 2 Report: System Design Communication Agent

## Status: DONE

## What I implemented

Created `system-design-communication/` with the four files specified in the brief:

1. **`AGENTS.md`** — agent definition with frontmatter (`name`, `description`), a Purpose section, and all three modes (Design Walkthrough, Mock Interview, Tradeoff Defense), each with a "What it does" and "Success" line. Matches the brief's structure exactly.

2. **`prompts/explain-design.md`** — Design Walkthrough prompt. Kept the brief's structure (ask what they're designing → listen for purpose/architecture/data flow → ask calibrated follow-ups → point out gaps without filling them → don't critique) and added a "Notes on running this well" section based on testing (see Refinements below).

3. **`prompts/interview-simulation.md`** — Mock Interview prompt. Kept the brief's script (open-ended question → listen and press → introduce a constraint change → summarize/ask what they'd change/give feedback) and added a "Notes on running this well" section, also refined after testing.

4. **`README.md`** — usage guide with the three-mode overview, a "when to use each mode" table, invocation examples per mode, success criteria, and tips. Also notes that Tradeoff Defense (Mode 3) has no dedicated prompt file yet — the brief only asked for two prompt files (`explain-design.md`, `interview-simulation.md`), so Mode 3 is documented in `AGENTS.md`/`README.md` only; I flagged this explicitly in the README rather than silently leaving it unbacked, with a note to split it into its own file if it sees real use.

No file content deviates from what the brief specified for AGENTS.md, explain-design.md's core structure, interview-simulation.md's core script, or README.md — I added to each rather than rewriting, and all additions came from testing evidence, not speculation.

## Tests run

Because this is an interactive coaching agent and there's no real human user in this session, I tested it the way Task 1 tested its adversarial gate (per that task's report): via independent subagents, so the critique wouldn't just be me grading my own prompt-writing. I ran two subagents in parallel, each given only the relevant prompt file (not my design rationale) and told to simulate a full session playing **both** the coach/interviewer role (strictly following the prompt file's instructions) and a plausible candidate role (with realistic, not artificially placed, gaps), then critique the prompt independently afterward.

**Test 1 — Design Walkthrough**, design: "real-time notification system for 1M users" (push, in-app, email digest). Full transcript produced (7 exchanges). Findings:
- Follow-ups stayed anchored to what the candidate actually said (Kafka choice, caching mention, digest scheduling) rather than jumping to unmentioned components — matches the prompt's "ask follow-ups to clarify" intent.
- The prompt succeeded at exposing gaps without solving them: on both a cache-invalidation gap and a timezone/batching gap, the coach persona named the gap and stopped rather than suggesting a fix.
- Two rough edges surfaced: (a) the prompt's example follow-ups ("You mentioned caching...") could read as a literal checklist rather than illustrative, risking a coach that waits for exact keyword matches; (b) nothing bounded session length, so a stricter coach could keep opening new gaps indefinitely instead of moving to recap.

**Test 2 — Mock Interview**, question: "Design a distributed cache" (10x traffic constraint introduced mid-round, node failure introduced near the end). Full transcript produced (11 exchanges, ~15-minute equivalent arc: clarifying questions → approach → follow-ups → constraint change → node-failure follow-up → summary → "what would you change" → feedback). Findings:
- Read as a realistic interview, not an interrogation — one follow-up at a time, one nudge when the candidate froze on the 10x-traffic question ("no wrong answers here — what would you try first?"), which unstuck them toward the hot-key/local-cache insight.
- Staying in character and saving coaching for the debrief worked: a shaky justification for choosing Redis over Memcached surfaced naturally under pressure instead of being pre-empted by a hint.
- Debrief was specific, not generic — it cited the actual moments (hot-key reasoning as a strength, unjustified Redis pick and eyeballed node count as the growth area).
- One gap: the prompt gave no guidance on whether/how to react when the candidate self-identifies their own gap mid-round ("that's something I hadn't built in") — left ambiguous whether an in-character acknowledgment breaks the "stay in character until debrief" rule.

## Refinements made

Based on the two critiques, I edited both prompt notes sections (not the brief's core script/structure, which I left untouched):

- **`explain-design.md`**: added a line clarifying the example follow-ups are illustrative, not a literal checklist to pattern-match against; added a pacing guideline ("aim for 2-4 follow-up threads before moving to the recap... more isn't better").
- **`interview-simulation.md`**: added a line permitting a brief in-character acknowledgment ("noted, keep going") when the candidate self-identifies a gap, explicitly framed as not-coaching so it doesn't conflict with the "save coaching for the debrief" rule.

## Concerns / observations

- **Mode 3 (Tradeoff Defense) has no dedicated prompt file.** The brief's file list only requested `explain-design.md` and `interview-simulation.md`, so this is intentional per-spec, but it means Mode 3 is currently guided only by the one-paragraph description in `AGENTS.md`. Flagged in the README with a note to split it out if it sees real use — recommend a follow-up task if Tradeoff Defense becomes a primary practice mode.
- **Testing method is simulated, not a live human session.** Both tests used subagents playing both roles from the prompt text alone (no visibility into my design rationale), which is a reasonable proxy for objectivity but isn't the same as the user actually practicing. The real signal on whether this agent reduces interview anxiety will come from the user's own use, per the brief's success metric.
- **`.superpowers/` and `docs/` remain untracked**, consistent with Task 1's report — left out of this commit as unrelated to this task's file scope.

## Commit

- `4941236` — "feat: add system design communication agent for interview prep"
  - 4 files changed (all new): `system-design-communication/AGENTS.md`, `system-design-communication/README.md`, `system-design-communication/prompts/explain-design.md`, `system-design-communication/prompts/interview-simulation.md`.
