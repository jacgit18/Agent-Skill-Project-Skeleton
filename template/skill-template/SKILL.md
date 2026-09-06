<!--
SKILL TEMPLATE — entry point

To use: copy the whole `skill-template/` directory to
`.claude/skills/<Group>/<kebab-case-name>/`, rename nothing (the dir name IS the skill
name), fill in the bracketed parts, delete every comment block, and work the file down.
Claude Code auto-discovers `.claude/skills/**/SKILL.md`; there is no registration step.

Before drafting, decide which shape this is:
  - GATE — withholds the answer until the user supplies a rep (a hypothesis, a listed set
    of unknowns, a settled prior decision, a charter). Most skills here are gates.
  - PROCEDURE — a mechanical walk that needs concrete inputs but doesn't withhold judgment
    (e.g. change-surface-audit, failure-mode-analysis, reliability-math, document-page-check).
Keep only the sections that fit the shape you picked; the comments below say which is which.

The `description` field is the single most important line in the file — it is what makes
the skill fire or stay silent, and it is where this skill is disambiguated from every
sibling it could be confused with. Budget real time on it. See the checklist in that block.
-->
---
name: [kebab-case-name — must equal the directory name]
description: >
  [WHAT IT DOES, in one dense sentence — the decision it forces or the procedure it runs,
  and what it produces (an ADR / a plan / a register / a gated coding action / no artifact).]
  [WHEN IT FIRES — pack in the literal phrases a user would actually type: "design a system
  for X", "what could this break", "help me test this", etc. 4+ concrete triggers beat one
  abstract sentence.]
  [WHAT IT IS NOT — one clause per sibling skill it could be mistaken for, each naming that
  sibling in backticks and the tell that routes there instead. This is not optional; a new
  skill with no carve-outs will collide with something. Check the group's other skills and
  the four cross-cutting gates: `ambiguity-gate`, `learning-gate`, `problem-solving-gates`,
  `spec-drift-gate`.]
  [A bare conceptual question ("what even is X") is answered directly, no gate/procedure.]
---

# [Skill Title]

[One or two paragraphs: the failure this skill exists to prevent, and the single question
it puts at the center. State plainly whether it's a gate (withholds the answer pending a
user rep) or a procedure (needs concrete inputs, doesn't withhold judgment).]

## When to use

- [Concrete scenario, phrased close to how a user would say it.]
- [Another. Cover different phrasings of the same underlying trigger.]
- [3–5 total.]

## Out of scope — hand these off

- **[The adjacent concern]** — that's `[sibling-skill]`. [The one-line tell that separates
  them, written so it also makes sense read from the other skill's side.]
- [One bullet per sibling. Every bullet here should have a mirror-image bullet in that
  sibling's own description or Out-of-scope list — reciprocity is the point.]
- **A bare conceptual question** — "[example]" — answered directly, no [gate/procedure].

---

<!-- GATE shape: use this section. Delete the "Inputs" section below. -->
## The precondition

[The rep the user must supply before Claude does the work. Be specific about what "stated"
means — a written hypothesis, a numbered list of unknowns, a named prior decision. If it's
missing, Claude asks for it and stops. State explicitly what Claude may contribute once the
precondition is met — deliberately narrow.]

<!-- PROCEDURE shape: use this section instead. Delete "The precondition" above. -->
## Inputs the procedure needs

[The concrete facts the walk can't run without. Don't invent them. If any is missing, ask
and stop.]

1. [Input — concrete, not "the context".]
2. [Input.]

---

## The procedure

<!-- Work any companion reference files alongside these steps; name them here. -->

### 1. [First step]

[What happens, what it produces, what it's checked against.]

### 2. [Next step]

[…]

---

## Output

[Exactly what comes back and in what shape — a chat summary block, a written ADR/register
at a specific path, or "no artifact, the gated action is the output". Then: "Then stop."
Anything downstream is a separately started step.]

```
[If there's a summary block, show its literal skeleton here.]
```

---

## Example invocations

> "[A request that should trigger this skill.]"

[How the skill responds — which precondition it asks for, or which inputs it restates.]

> "[A request that looks similar but should route to a sibling.]"

[Name the sibling and the tell.]

---

## Portability

Repo-agnostic [or: assumes `<path>` exists — drop `<line>` if not]. Copy the directory into
another repo's `.claude/skills/`. See `README.md` for where it sits among the siblings.
