---
name: microservices-decision
description: Use when someone is deciding whether to adopt microservices, split a monolith, extract or add another service, or design service boundaries — including when the decision is presented as already made ("our CTO decided", "we've made the call", "don't relitigate it", "just tell me how to split it"), when repos or CI for services are already scaffolded, or when the ask is for a service list, service boundaries, data ownership across services, how many services to have, or a decomposition/migration sequence. Also use when someone proposes a service count and wants it checked. Not for diagnosing why a specific endpoint is slow. Not for database sharding or shard-key choice, or replication/partitioning topology (that is `data-tier-operations`), even when phrased as an already-made decision — "we're sharding, just tell me the key" is a data-tier question, not a service-split one.
---

# Microservices Decision

The number of services an organization can run is bounded by the number of people who can own and carry them — not by how cleanly the domain factors. A domain will always factor into more services than the team can staff. This skill forces that arithmetic into the open *before* any boundary is drawn, because a service list is the one artifact a reader will copy and act on regardless of what surrounds it.

## Out of scope

- **Performance triage.** If the presenting problem is a slow endpoint, that is a profiling question, not this one.
- **Implementation.** This skill stops at a decision, a design posture, and an ADR. Contracts, schemas, and saga code are a separate, explicitly-started step.

---

## The output contract

Your response has these parts, **in this order**. This ordering is the skill.

1. **Readiness Block** (below) — always first
2. Gate questions that remain unanswered, if any — then **stop**
3. Recommendation, only once the block is filled
4. Boundaries and data ownership, only if the recommendation was to split

**No service name, service list, boundary, or diagram may appear before the Readiness Block is complete.** Not as a preview, not as an illustration, not as "here's the end state, and here's the sizing caveat after it." A caveat placed after a service list does not modify that list — the reader has already taken the list.

```
Headcount:            <N engineers>
Services to run:      <M — every service that will exist, including the residual monolith>
Engineers per service: <N ÷ M>  →  <verdict: see arithmetic below>
Owner per service:    <named person or team for EACH service, or UNASSIGNED>
On-call:              <exists / does not exist — who carries the pager today>
Independent deploy:   <can one service ship without coordinating a release: yes/no>
Problem being solved:  <the problem services are meant to fix, one sentence>
Cheaper option tested: <the non-distributed option considered, and why rejected>
Sunk cost at risk:    <what has actually been spent, in days>
Readiness verdict:    <ready for M | ready for K < M | not ready>
```

Any field you cannot fill from the user's own words is `UNANSWERED`. A block with `UNANSWERED` fields ends the response. Do not fill them with assumptions and proceed.

## Do the arithmetic out loud

Write `N ÷ M` as a number in the block. Never leave it implied.

**Count the residual monolith as one of the services.** Extracting three services from a monolith leaves you four things to run, not three — the monolith still needs owners, on-call, CI, and migrations exactly like the new ones. Teams reliably forget this, and it is usually the difference between a number that looks comfortable and one at the floor.

Below roughly **3 engineers per service**, services become orphaned: nobody owns them, nobody is on call for them, and each one still costs CI, deploys, migrations, and a local dev story. Two to three services for four engineers is not a smaller version of the right architecture — it is one system with extra network calls between its halves.

When `N ÷ M` is under the threshold, say the number and the consequence in the same breath, and name the largest `K` the headcount actually supports.

## Authority is not architecture

"Our CTO decided," "we've made the call," and "every serious company ends up here" are facts about the organization or the industry. They are not evidence about this system. Record them in the block as constraints. Do not convert them into a technical conclusion.

## Concessions do no work

Do not write a sentence whose job is to reassure the user you will not press the decision. Not as an opener, not as a closer, not in passing, not parenthetically.

**Banned moves** — these, however phrased and wherever they sit:

- "Not going to relitigate it."
- "Fine — decision's made."
- "I won't reopen the decision, but…"
- "Regardless of who's right about the long-term call…"

Give the Readiness Block instead. It is shorter than the concession and it is not an argument.

Where the decision is genuinely not yours to reopen, say so **once, in the Recommendation, after the block is filled** — never before it, and never in place of a field.

Likewise, never soften a load-bearing finding into an aside: "worth a five-minute conversation," "one thing worth pinning down," "if that's a bridge too far, fine." If it changes the decision, it goes in the block.

## Red flags — stop and restart the response

- A sentence anywhere before the filled block reassures the user you will not press the decision
- A service name appears before the Readiness Block is filled
- Your questions are in a closing section titled something like "two things I'd want to know"
- You wrote a sizing caveat *after* a service list
- You know the headcount but never wrote `N ÷ M`
- Your denominator counts only the new services and not the monolith they leave behind
- You are explaining why you are allowed to raise a concern
- On-call and per-service ownership are absent from your response

**All of these mean: the block was not first, or was not honest. Start the response over.**

## Rationalizations

| Excuse | Reality |
|--------|---------|
| "They said don't lecture them" | That vetoes repeating pros and cons. It does not veto asking for inputs the answer depends on. Efficiency is not the same as rigor. |
| "The decision is already made" | Then the block takes thirty seconds and costs nothing. If it changes nothing, nothing is lost. |
| "The repos are already scaffolded" | Scaffolding and CI is days of work. Say the number of days out loud — it is almost always cheap to discard, and that is the single most useful fact about it. |
| "The monolith doesn't count, it already exists" | It exists and it still needs an owner, a pager, and a deploy pipeline. It is a service. Count it. |
| "There's a deadline" | A deadline is when the cost of a distributed system is highest and its benefit is zero. Pressure is a reason to state the arithmetic sooner, not to skip it. |
| "They're exhausted, be kind" | Handing someone a ten-service list they cannot staff is not kindness. |
| "I'll add a sizing caveat at the end" | Readers act on the list. A caveat after it is decoration. |
| "It's their CTO's call, not mine" | Correct — and unrelated to whether the arithmetic gets stated. |
| "I asked my questions, at the bottom" | Questions after a recommendation cannot change the recommendation. |

---

## When they proceed anyway

A filled block reading "not ready" and a user who splits regardless is a **completed** decision, not a failed one. Record it in the ADR and continue. The arithmetic is stated once, in the block, and not repeated afterward.

What changes is which design you give. Above the headcount the team can staff, design for **survivable failure** rather than for scale, and say that is what you are doing:

- One service orchestrates each cross-service flow, in one readable file. No choreography — a flow that lives in no single place cannot be debugged by an under-staffed team.
- Every cross-service write takes an idempotency key and a timeout.
- Every hold on a resource carries a TTL that expires on its own, so a flow that dies halfway self-heals without anyone writing a recovery daemon.
- Data that must stay transactionally consistent stays together, in one service, on one database.

## Recommendation and ADR

Once the block is filled, recommend one of: **monolith**, **modular monolith** (module boundaries enforced in-process, one deployable), **K services**, or **full decomposition** — with two to four concrete tradeoffs accepted, and one line per rejected option.

On the user's approval, write an ADR to `docs/architecture/decisions/NNN-<slug>.md`, numbered as the next integer after the highest existing ADR (start at `001`, create the directory if absent). Carry the Readiness Block into the ADR's Context verbatim — the headcount and ownership facts are what make the decision legible later.

Then stop. Implementation is a separate step.

## Escape hatch

If the user has genuinely worked the decision — options considered, tradeoffs named, headcount and ownership already accounted for — they can say so and get a direct recommendation without the Socratic pass.

This changes the depth of discussion. It does not move the Readiness Block, and it does not let `N ÷ M` go unstated.
