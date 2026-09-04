# Execution Model Decision

The compute-primitive and invocation-model comparisons behind gate items 3–5 in `SKILL.md`.
Written in AWS terms (Lambda / Fargate / ECS / API Gateway); the shapes transfer to Azure
Functions/Container Apps or GCP Cloud Functions/Cloud Run.

## Compute primitive: FaaS vs container task vs long-running service

| | FaaS (Lambda) | Container task (Fargate/ECS) | Long-running service |
|---|---|---|---|
| **Max duration** | Hard platform ceiling (15 min on Lambda) | No inherent ceiling | No ceiling |
| **State between invocations** | None — assume a fresh environment every time (though the runtime *may* be reused, never design around it) | Can hold in-memory state for the task's lifetime | Can hold state indefinitely |
| **Cold start** | Real, on the order of tens of ms to a few seconds depending on runtime/package size and whether it's the first invocation in a while | Slower to start a new task, but typically kept running so it's not a per-request cost | None — already running |
| **Scaling model** | Automatic, per-invocation, scales to zero when idle | Scales by task count, typically via a target-tracking policy — minutes, not milliseconds | Manual or autoscaled by the same mechanism as any service |
| **Local disk / custom runtime / GPU** | Limited ephemeral storage, restricted runtimes, no GPU | Full container control — any runtime, attached storage, GPU-enabled instance types available | Full control |
| **Cost model** | Pay per invocation + duration; free at zero traffic | Pay for the task's running time regardless of whether it's handling a request | Pay for the instance regardless of load, unless autoscaled to zero (rare) |
| **Ops burden** | Lowest — no servers, no runtime patching | Moderate — you own the container image and its base-image patching, not the underlying host | Highest — you own the host, the runtime, and the process supervision |

**Decision rule:** rule out by the hard limits first, then choose on preference within what's
left.

- Duration above the FaaS ceiling, or a need for a custom runtime, GPU, large local disk, or
  a persistent network connection (a long-lived WebSocket, a database connection pool kept
  warm across many logical requests) → **not FaaS**. Choose a container task if the workload
  is still bursty/on-demand, or a long-running service if it's genuinely always-on.
- Short (well under the ceiling), stateless, event-driven, and either bursty or low-volume
  enough that cold starts and per-invocation billing are net wins → **FaaS**.
- Steady, predictable, high-volume traffic where a warm process avoids repeated cold starts
  and the per-request cost of an always-on container beats per-invocation FaaS pricing at that
  volume → **container task or long-running service**, sized by `capacity-estimation` and
  priced by `technical-cost-decision`.
- If cold starts are the only objection to FaaS and duration/resource profile otherwise fit,
  consider provisioned concurrency (keeps a set number of instances warm) before abandoning
  FaaS for a container — it's a narrower fix than moving the whole workload.

## Invocation models and their built-in failure handling

Three distinct models, each with different consequences for who retries what:

### 1. Synchronous

The caller blocks until the function returns a response.

- **Examples**: API Gateway → Lambda for an HTTP response; any direct SDK invoke-and-wait
  call; a Step Functions Task invoked in synchronous mode.
- **Error handling**: errors return directly to the caller. There is no automatic retry —
  the *caller* decides whether and how to retry, which is exactly the retry-budget policy
  `resilience-strategy` owns for a live request path.
- **Cost of chaining synchronously**: if this function's job is itself to call another
  function and wait for it, the caller's timeout must exceed the callee's, cold starts stack
  across hops, and a change to the callee's duration or contract silently affects the caller.
  Prefer an async or event-based handoff between steps that don't need an immediate answer
  passed back up the chain.

### 2. Asynchronous (fire-and-forget)

The caller does not wait; the platform queues the invocation and runs it later.

- **Examples**: S3 upload event → Lambda; EventBridge scheduled/rule-matched event → Lambda;
  SNS message → Lambda subscriber.
- **Error handling**: the platform retries automatically a small, fixed number of times (on
  Lambda, twice — three attempts total) with no caller involvement. What's left after retries
  are exhausted goes to a configured **failure destination** (a DLQ, another queue, or an
  EventBridge bus) if one exists — if none is configured, the failure is silently dropped.
  This makes configuring the failure destination a design decision (gate item 7), not an
  afterthought.

### 3. Poll-based (event source mapping)

The platform continuously polls a queue or stream and invokes the function with batches of
records.

- **Examples**: Lambda triggered by SQS, Kinesis, DynamoDB Streams, or a Kafka-compatible
  source.
- **Error handling differs by source type**:
  - **SQS**: a failed message becomes visible again after its visibility timeout and is
    redelivered; a **redrive policy** with a `maxReceiveCount` sends it to a DLQ once that
    count is exceeded. Partial-batch-failure reporting lets the function tell SQS exactly
    which messages in a batch succeeded, so only the failed ones are redelivered — implement
    this rather than failing (and thus retrying) the whole batch for one bad message.
  - **Kinesis / DynamoDB Streams**: records are retried for up to 24 hours (configurable) or
    until a configured retry-attempt limit, then either skipped or sent to a failure
    destination — but note these sources preserve *order per shard/partition key*, so a
    stuck record can block everything behind it on the same shard until it's resolved or
    skipped. This is a materially different failure mode than SQS's per-message redelivery.

### Comparison

| Model | Caller waits? | Who retries | Typical use |
|---|---|---|---|
| Synchronous | Yes | The caller, per its own retry-budget policy | API responses, interactive requests |
| Asynchronous | No | The platform, a small fixed number of attempts, then a failure destination | Event-driven side effects with no immediate answer needed |
| Poll-based (event source mapping) | No (auto-triggered) | Depends on source — redelivery (SQS) or ordered per-shard retry (Kinesis/DynamoDB Streams) | Continuous queue/stream consumption |

**Choosing between them** follows directly from gate item 4: if whatever triggers this needs
an answer before it can proceed, it's synchronous, full stop — there's no version of "make it
faster by going async" that also hands back an immediate real answer. If nothing is waiting,
default to asynchronous for a single event, or poll-based when the source is inherently a
queue or stream to be continuously drained rather than a one-off event.
