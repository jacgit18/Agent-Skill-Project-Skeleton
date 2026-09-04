# Signals, SLOs, Sampling, Cardinality

Backs steps 2–8 of `observability-framework.md` and "Challenge a proposed approach" in `SKILL.md`.

---

## Monitoring vs observability

- **Monitoring** — tracking known health/performance indicators against thresholds, and alerting when they cross. Answers "is a thing I already know to watch OK right now?"
- **Observability** — enough instrumentation (metrics + logs + traces, correlated) to ask *new* questions about the system's internal state after the fact, without shipping new code. Answers "why is this specific thing behaving this way?"

You need both. Monitoring catches the known failure modes; observability lets you diagnose the unknown ones. A design that only does monitoring means every novel incident starts from zero.

---

## The signal types

### Metrics
Numeric measurements aggregated over time (counters, gauges, histograms).

- **Answers:** *that* something changed, and which SLI — rate, error %, latency percentiles, saturation. Cheap to store, fast to query, ideal for dashboards and alerts.
- **Costs:** each label combination is a separate time series — cardinality is the cost driver (see below). Aggregation loses the individual request; a metric can't tell you *which* call was slow.
- **Over-used:** high-cardinality labels (`user_id`, `request_id`) blow up series count and cost. **Under-used:** no USE metrics for the constrained resource, so saturation is invisible until it's an outage.

### Structured logs
Timestamped event records with named fields (JSON or logfmt), not free text.

- **Answers:** what happened in one specific execution — the error message, the parameters, the branch taken. With a trace/request ID field, they join to traces.
- **Costs:** highest volume-to-value ratio; ingest and hot-search storage are a real bill. Free-text logs are expensive to query and impossible to aggregate.
- **Over-used:** "log everything" — the needed line is buried and the bill balloons. **Under-used:** unstructured text with no correlation ID, so cross-service reconstruction is manual.

### Distributed traces
A tree of timed spans following one request across services and async hops.

- **Answers:** where the time went across service boundaries, which hop failed, the critical path, N+1 patterns between services.
- **Costs:** instrumentation effort (context propagation everywhere, including through queues), and span storage. Low value below ~3 hops.
- **Over-used:** tracing a monolith with two DB calls — a request ID in logs would do. 100% sampling at volume. **Under-used:** a 6-service request path with no tracing, so every cross-service incident is a war room.

### Continuous profiling
Sampled stack traces from production, aggregated into flame graphs over time.

- **Answers:** which function/line is burning CPU or allocating memory *in production*, and whether that changed across deploys.
- **Costs:** agent overhead (usually low), a specialized backend. Only relevant for compute-bound hot paths.
- **Over-used:** enabled fleet-wide when no one is CPU-bound. **Under-used:** a service with a known CPU regression and no way to see the offending frame without attaching a profiler by hand.

### Events / audit stream
Discrete, durable business or security facts ("order shipped", "role granted").

- **Answers:** the authoritative record of what state changes occurred — for audit, debugging state, or downstream processing.
- **Costs:** a schema and a store; overlaps logs but with retention and integrity guarantees.
- Use when logs' best-effort nature and short retention are inadequate for a compliance or reconciliation need.

---

## Method cheat-sheets

| Method | For | The signals |
|---|---|---|
| **RED** | request-driven services | **R**ate, **E**rrors, **D**uration — per critical route |
| **USE** | resources | **U**tilization, **S**aturation, **E**rrors — per resource (CPU, mem, disk, pool) |
| **Four Golden Signals** (Google SRE) | user-facing systems | latency, traffic, errors, saturation |

RED for the code you write, USE for the things it runs on. They overlap with the Golden Signals — pick one vocabulary and be consistent.

Related reliability metrics (from `12 Key Metrics for Measuring Service Performance.md`): **MTBF** (mean time between failures — reliability), **MTTR** (mean time to repair — how fast you recover; observability's main lever is driving this down), TTFB, throughput, error rate. The trend matters more than the absolute number.

---

## SLI / SLO / error budget

- **SLI** — a measured indicator of service health from the user's side (e.g. "proportion of requests served < 300ms").
- **SLO** — a target for an SLI over a window (e.g. "99% < 300ms over 28 days").
- **Error budget** — `1 − SLO`. The allowed amount of failure. Spent by incidents; when exhausted, the response is to stop shipping risk and fix reliability.
- **SLA** — a contractual SLO with a customer, with penalties. The SLA target should be *looser* than the internal SLO so you react before the contract breaches.

Set SLOs only where something acts on them. An SLO with no owner and no consequence is a vanity chart.

### Symptom vs cause alerting
- **Page on symptoms** — SLO burn rate (use multi-window: a fast-burn rule for acute outages, a slow-burn rule for gradual budget erosion), error-rate spikes on critical paths, availability.
- **Don't page on causes** — high CPU, memory pressure, queue depth, a single node down, elevated dependency latency. These go to dashboards and tickets. They matter, but they're only worth waking someone if a symptom is also moving.
- Cause alerts that don't map to user impact are the main source of alert fatigue, and fatigue is what makes a real page get missed.

---

## Sampling: head vs tail

| | Decides | Keeps | Trade |
|---|---|---|---|
| **Head-based** | at the start of the trace, by a fixed probability | a representative % of *all* traces | simple, low overhead; discards the rare slow/errored traces you most want |
| **Tail-based** | after the trace completes, by its properties | all errors, all slow outliers, all of chosen routes, + a small % baseline | needs a gateway collector buffering spans; keeps the high-value traces at a fraction of storage |

Above trivial RPS, tail-based is the high-value default. 100% retention is only reasonable at very low volume — and even then it's mostly noise.

---

## Cardinality — the hidden cost driver

A metric's cost is roughly `(number of label-value combinations) × (scrape frequency) × (retention)`. One unbounded label (`user_id`, `path` with IDs in it, `error_message`) turns one metric into millions of series and dominates the bill — or trips an ingest limit and drops data silently.

**Budget it:**
- Metric labels come from an **allow-list** of bounded sets: route *template* (`/orders/{id}`, not `/orders/123`), method, status class, dependency name, region.
- High-cardinality dimensions (user, tenant, device, full URL, message) belong on **traces and logs**, where they're queryable without multiplying series.
- Structured logs get a **disciplined field set**, not arbitrary per-call keys.

The rule of thumb: if a dimension has more than a few hundred possible values, it does not go in a metric label.

---

## Self-hosted stack vs managed

| | Self-hosted (open source) | Managed (SaaS) |
|---|---|---|
| Collection | OpenTelemetry Collector | vendor agent or OTel → vendor |
| Metrics | Prometheus / Mimir / Thanos | included |
| Logs | Loki / Elasticsearch / OpenSearch | included |
| Traces | Tempo / Jaeger | included |
| Dashboards | Grafana | included |
| **Asks of the team** | run, scale, and secure all of the above HA; own retention and upgrades | integration and cost management; little ops |
| **Cost shape** | infra + engineer time; flattens at scale | per host / per GB ingested / per million spans / per active series — grows with usage |
| **Best when** | large scale where SaaS ingest pricing dominates; data-residency / air-gap requirements; a platform team exists | small-to-mid team, no platform group, or an SLA that makes self-hosted monitoring's own downtime unacceptable |

OpenTelemetry for instrumentation regardless — it keeps the backend swappable, so this choice isn't a one-way door.
