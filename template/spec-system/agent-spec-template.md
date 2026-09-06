<!--
AGENT SPEC TEMPLATE

Before filling this in, run the candidate task through the agent-worthiness test:
  - Does it require coordinating multiple tools?
  - Do decisions depend on intermediate results (not a fixed, known-in-advance sequence)?
  - Is occasional error tolerable, given a human will review the output?

If any of those is "no" -- if the task is fixed-sequence, high-stakes/irreversible, or has
poorly-defined success criteria -- it should stay a plain prompt or script. Do not spec it.

To use: copy this file, fill in the bracketed parts, delete this comment block, save as
.claude/agents/<name>.md. Claude Code auto-discovers files there; no registration step.
-->
---
name: kebab-case-id
description: >
  Third person. This field alone decides whether the agent ever fires -- pack it with literal
  phrases a user would type, or the scenarios where Claude should self-invoke this. Vague
  description = agent never triggers, or triggers on everything. Prefer 2-4 concrete scenarios
  over one abstract sentence.
tools: []
model: inherit
---

You are [role], specializing in [narrow domain -- the narrower the better; this is scope too].

## When to invoke
- **[Scenario A].** [What the situation looks like, concretely, and what triggers dispatch.]
- **[Scenario B].** [2-4 total. Cover different phrasings of the same underlying trigger.]

## Out of scope
- [What this agent must NOT decide or touch. Paired with `tools:` above -- together they define
  the scope boundary. Explicit exclusions here prevent silent scope creep.]

## Process
1. [Step]
2. [Step]

## Output format
[Exactly what must come back, and in what shape. This is the spec's success criteria: something
a human reviewer -- or you -- can check the output against without redoing the work.]
