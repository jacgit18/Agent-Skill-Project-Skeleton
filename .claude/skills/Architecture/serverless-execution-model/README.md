# serverless-execution-model skill

A gated decision for **how one unit of work actually runs** — the compute primitive (FaaS /
container task / long-running service), the invocation model (sync / async / poll-based),
whether a multi-step process needs a central orchestrator or tolerates event-driven
choreography, and the failure contract (retry/backoff, catch routing, DLQ/failure
destination, idempotency). Not service boundaries or team ownership (that's
`microservices-decision`), not the execution role or network placement (that's
`cloud-iam-boundary`), not overload/cascade defense on a live path (that's
`resilience-strategy`), not dollar cost (that's `technical-cost-decision`).

Built from the `Architecture/02. Backing Service Options/Cloud/` notes — `Lambda vs
Fargate.md`, `Microservices vs FaaS.md`, `Lambda Invocation Models.md`, `AWS/AWS Async Vs
Sync.md`, `AWS/Step function.md`, `AWS/Step Function Extension.md`, `Step Function Catch
Blocks.md`, `Failure States.md`, `AWS Parallel State.md`, `AWS/DLQ.md`, and `AWS/DLQ
Drainer.md`.

Note: `Lambda Invocation.md` in the same folder is about generic programming-language lambda
expressions (Python/JavaScript closures), not AWS Lambda invocation — it was not used as a
source here despite the name; don't confuse the two when re-reading the vault notes.

## Where it sits

```
microservices-decision     →  how many services, team ownership (assumed given, upstream of this skill)
capacity-estimation        →  concurrency / volume numbers this skill consumes
serverless-execution-model →  compute primitive + invocation model + orchestration + failure contract   (this skill)  → ADR
cloud-iam-boundary          →  the execution role and network placement this workload needs
resilience-strategy        →  overload/cascade retry-budget on a live request path (composes with this skill's per-invocation retry contract)
technical-cost-decision    →  the dollar cost of the chosen primitive/concurrency
observability-strategy     →  alerting on execution failures and a filling DLQ
```

## The shape

A gate skill. It refuses to recommend a primitive or orchestration approach until the user
supplies:

- **the unit of work** — one request, one event-triggered side effect, a multi-step process,
  a stream to consume — not "a backend thing"
- **duration and resource profile** — checked against hard platform ceilings before anything
  is compared on preference
- **trigger and response need** — does the caller need to wait
- **concurrency and burst pattern**, including cold-start tolerance
- **whether steps need central coordination** or can tolerate independent event reaction
- **failure semantics** — retry vs park vs drop, and whether the operation is idempotent

Then it rules primitives in/out by hard limits, picks the invocation model from the
trigger/response need, decides orchestration vs choreography by the coordination need (not by
default in either direction), assigns per-step Retry/Catch only where something fallible is
actually called (Task/Parallel/Map, never Choice/Pass/Wait), and designs the DLQ/failure
destination plus the idempotency requirement it imposes.

## Files

| File | Role |
|---|---|
| `SKILL.md` | Entry point. The gate (items 2–8 from the user), challenge-the-proposal, output contract. |
| `execution-model-decision.md` | FaaS vs container-task vs long-running-service decision table; the three invocation models (sync, async, poll-based event-source mapping) and each one's built-in retry/error behavior; the cost of synchronous function-to-function chaining. |
| `orchestration-and-failure-handling.md` | Orchestration vs choreography tradeoff; Step Functions state types and which can carry Retry/Catch and why; hard vs soft failure classification; Parallel/Map fan-out failure semantics and Distributed Map's tolerated-failure option; DLQ/failure-destination mechanics and the idempotency requirement retries impose. |

## Output

1. A recommendation block in chat (unit of work, compute primitive, invocation model,
   orchestration decision, retry & catch per step, DLQ/failure destination, concurrency &
   scaling, tradeoffs, follow-ups).
2. On approval: an ADR in `docs/architecture/decisions/` reusing `database-architecture`'s
   `adr-template.md`. "Revisit when" must be a concrete trigger (duration grows past the FaaS
   ceiling, a linear chain gains real branching and needs reconsidering as orchestrated, the
   DLQ fills faster than it's triaged, concurrency needs exceed account limits).

Stops before implementation (the state machine definition, IaC, handler code).

## Interaction with sibling skills

- **Assumes `microservices-decision`'s output** — takes one already-scoped unit of work as
  given; does not decide whether it should be its own service.
- **Hands off to `cloud-iam-boundary`** — this skill names what a Task/function needs to call;
  that skill designs the role and network placement. The two are typically worked together
  when standing up a new workload.
- **Composes with `resilience-strategy`** — that skill's retry-budget-under-load concern and
  this skill's per-invocation retry/DLQ contract are different questions that share
  vocabulary ("retry with backoff"); an async worker built here can still need a concurrency
  limit from that skill if its retries are hammering an overwhelmed downstream.
  Reciprocal boundary note pending — add to `resilience-strategy` and `microservices-decision`
  when `skill-interaction-testing` runs.
- **Feeds `technical-cost-decision`** — the chosen primitive and concurrency ceiling are the
  usage-driver inputs; this skill doesn't price them.
- **Consumes `capacity-estimation`** — concurrency and volume numbers, rather than re-deriving
  them.
- **Feeds `observability-strategy`** — the DLQ-triage cadence and execution-failure alert
  requirement are named here, designed there.

Run `skill-interaction-testing` after any trigger-description change here — the overlap risk
is with `microservices-decision` (unit-of-work vs service-boundary altitude),
`resilience-strategy` (retry/backoff vocabulary shared across two different problems), and
`cloud-iam-boundary` (which skill runs first when standing up a new workload).

## Using it in another repo

Repo-agnostic. Reads and writes `docs/architecture/decisions/` alongside
`database-architecture` and reuses its `adr-template.md`. Written in AWS vocabulary (Lambda,
Fargate, Step Functions, SQS/Kinesis); swap the platform-specific limits and mechanics in the
reference files for Azure Functions/Container Apps/Durable Functions or GCP Cloud
Functions/Cloud Run/Workflows if this repo targets a different cloud — the gate items and
decision structure carry over unchanged.

```
cp -r ".claude/skills/Architecture/serverless-execution-model" /path/to/other-repo/.claude/skills/
```
