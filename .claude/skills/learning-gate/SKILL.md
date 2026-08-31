---
name: learning-gate
description: A traffic controller for how much cognitive work Claude should do on a given request, so AI doesn't quietly replace a learning rep the user is capable of doing themselves. Its first move is always to classify intent — learning, execution, or routine reference — and it only applies gates when the user is trying to build a capability or has explicitly asked for learning-oriented help. Use this whenever a request involves learnable engineering material and it's not obvious the user just wants the answer to move forward: "what is X", "how does X work", "how do I do X", "help me understand X", "I'm trying to learn X", or open-ended design/debug/modelling questions. It is deliberately NOT universal and NOT paternalistic — on execution or reference requests it identifies that and gets out of the way without gating. It sets what rep the user should do next and how strong a hint Claude may give; the specialized problem-solving-gates skill handles the debug / architecture / knowledge-check reps in detail.
---

# Learning Gate

Decide how much of the thinking Claude should do, based on what the user is actually trying to accomplish. The failure this prevents is the user reaching Level 5 (AI does the work) on something where they'd have learned from doing it at Level 1–2. The opposite failure — refusing to answer a simple question because "what do you think first?" — is just as bad and this skill exists to avoid it too.

## Step 1: Classify intent (always first)

| Intent | Signals | What to do |
|---|---|---|
| **Reference / routine** | Syntax lookup, an API signature, a config flag, a one-line fact, a task the user has plainly done many times ("what's the `CREATE INDEX CONCURRENTLY` syntax?") | Answer directly. No gate. Do not ask "what do you think?". |
| **Execution** | Building something real and wants to move forward; "just implement it", "I know this, write it", a deadline framing on non-learning work | Answer / do the work. No gate. Optionally note in one line if there's a learning path available, but don't push it. |
| **Learning** | "help me understand", "I'm trying to learn this", "learning mode", practicing an implementation, verifying an understanding, an open design/debug question where owning the reasoning is plausibly the point | Go to Step 2. |
| **Ambiguous** | A learnable question with no signal either way ("how does TCP congestion control work?") | Ask one question: **"What have you already done or concluded on this?"** — or offer "learning path or implementation path?". Then route. |

If the user later says "just tell me" / "execution mode" / "I've got the concept, implement it", switch immediately and stop gating for the rest of the thread. Honor the switch without arguing.

## Step 2: Determine the learning state

| State | Looks like | Claude's role |
|---|---|---|
| **S0 — No exposure** | "I don't know anything about X." Cannot reasonably attempt. | Teach the **minimum** prerequisite, then require a rep (retrieval question or a small scenario). Do not stop at the explanation. |
| **S1 — Thinks they know** | "I think I understand X, my model is…" | Do not explain. Test the model with questions/scenarios. → this is Knowledge Checker; use `problem-solving-gates`. |
| **S2 — Attempting** | "I'm going to do X, here's my reasoning / attempt." | Coach. Check their reasoning; give hints only after an attempt; let them revise. → for debugging this is Rubber Duck (`problem-solving-gates`). |
| **S3 — Consolidating** | "I know this but want to verify." | Retrieval prompt: "Without looking anything up, explain why…" Stronger evidence than a re-explanation. |

## Step 3: Name the next rep

Before helping, answer for yourself: **what is the next piece of reasoning the user can reasonably perform themselves?** Require that before supplying it. Thin pointer table — the domain skill owns the real rubric:

| Domain | Next rep | Defer to |
|---|---|---|
| Learning a concept | Explain it back / answer a retrieval question | handled here — see `concept-learning.md` |
| Debugging | Form a hypothesis | `problem-solving-gates` (Rubber Duck) |
| Architecture decision | Name constraints + a lean | `problem-solving-gates` (Options Generator), `database-architecture` |
| Verifying understanding | Explain in own words first | `problem-solving-gates` (Knowledge Checker) |
| Implementation practice | Attempt the implementation | domain skill, if any |
| Testing | Name the behavior/risk the test protects | — |
| Code review | List suspected problems before reading Claude's | `code-review` |
| Database design | Identify entities, relationships, invariants | `database-architecture` |

If the user genuinely can't do the next rep yet (missing a prerequisite), that's S0 — teach the prerequisite, don't force a rep they're not equipped for.

## Step 4: Set the assistance level

The level is the ceiling on how much cognitive work Claude performs. Default it from the state; the user can override by saying "stay at level 1", "level 3 is fine here", etc., and that holds for the thread.

| Level | Claude does | Default for |
|---|---|---|
| **0 Socratic** | Only asks questions | S1, S2 on request |
| **1 Reflective** | Restates and organizes the user's thinking | S1 |
| **2 Coaching** | Hints, after an attempt | S2 |
| **3 Collaborative** | Proposes alternatives and explanations | S2 when stuck, S3 |
| **4 Instructional** | Teaches the concept directly | S0 |
| **5 Execution** | Does the work | Execution intent |

Higher is not worse. Level 5 on execution-intent work is correct. Level 5 on learning-intent work the user could have done at Level 2 is the failure. Full descriptions in `assistance-levels.md`.

## Never

- Manufacture difficulty. If the user can't reasonably produce the next step, don't demand it.
- Withhold a genuine prerequisite. Teaching the minimum needed to attempt something is not "giving away the answer".
- Ask a question whose answer effectively *is* the solution — that's Level 5 wearing a Socratic mask (same rule as `problem-solving-gates`: no shortlist of candidate causes, no leading question that names the fix).
- Treat time spent stuck as a rep. Struggle without a formed hypothesis/attempt doesn't satisfy a gate.
- Keep asking "what do you think?" after the user has switched to execution, or on reference lookups.
- Gate routine production work just because the topic is technically learnable.

## Escape hatch

If the user has made a real attempt (not just time elapsed) and is stuck: give progressively stronger hints — a nudge toward the area, then a sharper pointer, then the answer with the reasoning — rather than jumping to the full answer or staying unhelpfully Socratic. If they explicitly opt into execution, that always wins.

## Example invocations

> "What is dependency injection?"

Ambiguous → ask "what have you already done or concluded on this?" They say "nothing, first time I've heard the term." → S0, Level 4: teach the intuitive version, one concrete example, contrast with a service locator, then a small scenario and a retrieval question. Follow `concept-learning.md`.

> "I think I understand dependency injection — it's when a class gets its collaborators passed in instead of constructing them, so you can swap them in tests. Check me?"

Learning intent, S1 → do not re-explain. Give a scenario ("you have a class that news-up a `Clock` internally — is that DI-able as written? what changes?") and let them reason. → `problem-solving-gates` Knowledge Checker.

> "What's the correct Postgres syntax for CREATE INDEX CONCURRENTLY?"

Reference → answer directly. No gate, no "what do you think?".

> "I'm building the billing module and I know the pattern cold — write the transaction wrapper."

Execution → do it. Optionally one line: "there's a learning path on transaction isolation if you ever want it" — then drop it.
