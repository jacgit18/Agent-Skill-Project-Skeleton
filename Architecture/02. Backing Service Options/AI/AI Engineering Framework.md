---
tags: 
author:
  - gitUserNamePlaceHolder
banner: "![[Banner.gif]]"
banner_x: 
banner_y: 
cssclasses:
  - dashboard
Comments: Placeholder comment any thing else you want to mention about the document.
Purpose: This documentation discusses
Status: 
Started: 
EditDate: 
Relates:
---
# AI Engineering Framework

### When to own it. When to offload it.

A decision system for maintaining critical thinking while leveraging AI effectively.

**Success metrics (6 months):** debug under pressure · read unfamiliar code cold

---

## 01 — Core Decision Rule

> **"Would doing this myself close a specific skill gap I've identified?"**

|Answer|Action|
|---|---|
|YES|Own it. No exceptions.|
|NO|Eligible to offload — only if it's execution of something you already understand.|
|UNSURE|Apply the tiebreaker.|

**Tiebreaker:** "Could I be asked to explain or defend this in a technical interview?"

- Yes → own it
- No → eligible to offload

**Secondary check:** "Can I confidently evaluate whatever AI produces here?"

- No → own it first
- Yes → eligible to offload

**Unfamiliar concept rule (no override):** If you have never implemented this concept before, the value filter does not apply. No workload justification. No "is it worth it" calculation. Encountered for the first time = own it.

---

## 02 — SDLC Phase Rules

### Requirements & Problem Definition

_Default: Own_

|Task|Call|
|---|---|
|Translating ambiguous requirements into specs|OWN|
|Identifying edge cases and failure modes|OWN|
|Listing unknowns before starting design|OWN — always first|
|Formatting docs, templates, boilerplate text|OFFLOAD|

---

### Architecture & Early Design

_Strict — own the decision_

**Rule:** List your unknowns first. Form a position first. AI presents options you haven't considered — it does not make the decision.

|Task|Call|
|---|---|
|Choosing components, patterns, tradeoffs|OWN|
|Generating list of patterns to evaluate|AI as input — not as answer|
|Unfamiliar domain — facts about a service|Offload facts, own decisions|
|Diagramming after decisions are finalized|OFFLOAD|

---

### Implementation

_Draft-first protocol — no exceptions_

**Rule:** Write your attempt before looking at AI output. It can be wrong — that's the point. Use AI to review your draft, not generate the first one.

|Task|Call|
|---|---|
|Logic touching your identified skill gaps|OWN — draft first|
|Unfamiliar concepts (first encounter)|OWN — draft first|
|Refactoring — the why|OWN|
|Refactoring — mechanical execution|Offload if logic is clear|
|Boilerplate you've implemented before and own|OFFLOAD|

---

### Debugging

_Non-negotiable — no AI diagnosis_

**Rule:** AI is a rubber duck only. You describe the problem and your hypothesis. AI asks clarifying questions. It does not diagnose. No exceptions — this is one of your two 6-month success metrics.

**Hypothesis format required before touching anything:**

> "I think X is happening **because** Y, which means I should see Z if I'm right."

|Task|Call|
|---|---|
|Forming the hypothesis|OWN — always|
|Pressure-testing the hypothesis|Agent 1 only|
|Diagnosing the bug|OWN — never offload|

---

### Testing

_Mixed — predict first_

**Rule:** Before writing or running tests, write down what you expect to break and why. Prediction is where the thinking lives. Then use AI for scaffolding and structure.

|Task|Call|
|---|---|
|Predicting which branches/paths will fail|OWN — always first|
|Identifying edge cases before testing|OWN|
|Test scaffolding and boilerplate|OFFLOAD|
|Assertions and edge case definitions|OWN|

---

### Ops & Tooling (CI/CD, Infra)

_Apply gap rule directly_

Actively learning a service or config pattern → own the design decisions, offload syntax lookups. No active gap → offload freely.

---

## 03 — Agent Routing

### Agent 1 — Rubber Duck

**Job:** Reflect your thinking back. Ask clarifying questions. Never diagnoses.

**Trigger:** Debugging session — only after written hypothesis exists. Do not open this agent before that.

```
I'm debugging and want you to act as a rubber duck.
Do not diagnose or suggest fixes. Only ask clarifying
questions about my hypothesis.

Hypothesis: [I think X because Y, which means I should see Z]
Next test: [what I'm about to try]

Ask me one question that stress-tests my hypothesis.
```

---

### Agent 2 — Options Generator

**Job:** Ensure you haven't missed viable approaches. Never makes the decision.

**Trigger:** Architecture decisions — only after unknowns are listed and you have an initial position. "What should I do?" is not valid input.

```
I'm making an architecture decision and want to
pressure-test my thinking. Do not tell me what to do.

Context: [what you're building]
My unknowns: [list them]
My position: [your decision and why]
My reasoning: [tradeoffs you evaluated]

Identify what I haven't considered and present
alternatives I should evaluate.
```

---

### Agent 3 — Code Reviewer

**Job:** Reviews your draft. Identifies issues. Does not generate the first version.

**Trigger:** After you've written a draft — unfamiliar concepts, security-critical code, anything touching your skill gaps. No draft = agent doesn't activate.

```
Review my implementation. Do not rewrite it.

Identify issues in order of severity: correctness
first, then security, then efficiency.

For each issue explain what's wrong and why, but
let me fix it myself unless I ask otherwise.

Context: [what this code does]
My implementation: [your draft]
My concern: [what you're least confident about]
```

---

### Agent 4 — Knowledge Checker

**Job:** Tests your understanding after you've formed it. Never explains first.

**Trigger:** After reading docs or unfamiliar code — when you think you understand and want to verify. Attempt to explain first, always.

```
Test my understanding of [concept/code].
Do not explain it to me first.

My understanding: [explain in plain language,
including what breaks if you get it wrong]

Identify specifically what I have wrong, what
I'm missing, and what I've oversimplified.
```

---

### Agent 5 — Execution Agent

**Job:** Generates code, boilerplate, scaffolding for things you already own.

**Gate question:** "Can I confidently evaluate whatever this produces?" — No → use Agent 3 instead.

```
Generate [specific thing] for [specific context].
Stack: [your stack]
Constraints: [requirements]
Flag anything with non-obvious tradeoffs I should evaluate.
```

---

## 04 — Routing Map

```
NEW TASK
│
├── Familiar + own the mental model?
│   ├── Prompt exists (finalized)? → Agent 5
│   └── No prompt? → Agent 5 + evaluate the output
│
├── Unfamiliar / gap identified?
│   ├── List unknowns first. Form a position.
│   ├── Architecture decision → Agent 2
│   ├── Implementation → Draft first → Agent 3
│   ├── Debugging → Hypothesis first → Agent 1
│   └── Reading code/docs → Own first pass → Agent 4
│
└── PROBLEM SOLVED
    ├── Can answer all 4 prompt questions? → Write draft prompt
    ├── Cannot answer them? → You don't own it yet. Go back.
    └── Second use encountered? → Finalize prompt → Agent 5 permanently
```

---

## 05 — Prompt Generation Lifecycle

**The mechanic:** Every problem you solve becomes the source material for the prompt you'll use next time. The prompt is both the artifact of learning and the tool for future use.

```
UNFAMILIAR  →  own it, use Agents 1–4
SOLVED      →  generate draft prompt immediately
GENERALIZED →  finalize after second use, route to Agent 5
```

### Step 1 — Draft (immediately after solving, same session)

Answer all four questions. If you can't answer them, you don't own it yet and the prompt doesn't get written.

```
PROMPT DRAFT — [concept/problem name]
Date solved:
Context: [what problem this solved and where]

1. What does this do?
   [explain the concept in plain language]

2. What breaks if it's wrong?
   [the failure mode you now understand]

3. What are the non-obvious tradeoffs?
   [what you didn't know before solving it]

4. What should AI always flag when generating this?
   [your quality check criteria]

DRAFT PROMPT:
Generate [specific thing] for [specific context].
Requirements: [what you now know matters]
Flag if: [failure modes and tradeoffs from above]
```

### Step 2 — Finalize (after second use)

Update what the draft missed. Confirm the model generalizes. Move permanently to Agent 5.

```
PROMPT FINALIZED — [concept/problem name]
Updated: [date]

What the draft missed: [what second context revealed]
Generalization check: [broad or context-specific?]

FINAL PROMPT: [revised version]
Route: Agent 5 — Execution Agent
```

---

## 06 — Non-Negotiables

**No AI diagnosis in debugging.** Ever. Form the hypothesis yourself. AI is a rubber duck or it's nothing.

**No value filter on unfamiliar concepts.** "Is this worth learning?" does not apply the first time you encounter something. That question is avoidance with good vocabulary.

**No opening an agent before you have something to bring.** No hypothesis, no position, no draft, no explanation = you're offloading thinking, not validating it.

**No skipping the draft prompt after solving.** Same session. Every time. Skip it and you reset to zero next time you see the same problem.

**No reading without a hypothesis.** Before reading a function body, predict what it does. Passive reading builds familiarity, not models.

**No reaching outward before reasoning inward.** Teammate, AI, Stack Overflow — all legitimate. All come after you've extracted everything your own thinking has to offer.