# Agent-Skill-Project-Skeleton

A reusable starting point for **system-design work driven by Claude skills**. It bundles
three things that normally live apart:

1. A curated library of authored [Claude Skills](.claude/skills/) — mostly *decision gates*
   that force a reasoning step before Claude does the work.
2. The [`Architecture/`](Architecture/) knowledge base those skills are built from — the
   system-design notes that supply each skill's frameworks and vocabulary.
3. The plumbing to keep it honest — a prompt-logging hook, a batch-push script, and a
   skill that tests every new skill against its siblings for conflicts.

Drop this skeleton in front of a design problem and the relevant skill fires, asks for the
decision or the rep it needs, and produces an ADR / model / handoff doc from there.

## Layout

| Path | What's in it |
|---|---|
| [`.claude/skills/`](.claude/skills/) | The skill library (see below). |
| [`.claude/settings.json`](.claude/settings.json) | Wires the `UserPromptSubmit` prompt-logging hook. |
| [`.claude/_Prompts/logs/`](.claude/_Prompts/logs/) | Dated logs of every prompt submitted in the repo. |
| [`Architecture/`](Architecture/) | System-design notes: system design, backing services, web-server architecture, design patterns, devops, networking, security, testing, 12-factor. Source material for the skills. |
| [`Goals/`](Goals/) | Personal learning roadmap and AI-engineering framework notes. |
| [`Books/`](Books/) | Business and tech book notes. |
| [`scripts/`](scripts/) | `hooks/log-prompt.sh`, `git/batch-git-push.sh`. |
| `READ DELETE/` | Pre-reorg flat copies of skills, kept for diffing. Slated for deletion. |

## The skill library

Skills follow one shape: a `SKILL.md` entry point, companion `*.md` reference files for the
deep material, and a `README.md` explaining where the skill sits relative to its siblings.
Many are **gates** — they withhold the answer until a precondition (a hypothesis, a listed
unknown, a settled prior decision) is met, so AI doesn't quietly replace a learning rep.

### Data — a gated pipeline for data-architecture decisions

| Skill | Role |
|---|---|
| [`Data/database-architecture`](.claude/skills/Data/database-architecture/) | Decides **where** the source of truth lives (database-first / code-first / contract-first) and **which** store. Produces an ADR. |
| [`Data/relational-modeling`](.claude/skills/Data/relational-modeling/) | Turns a settled "we're relational" into table design — normal form and exceptions, keys, constraints, index plan, lifecycle columns. |
| [`Data/data-tier-operations`](.claude/skills/Data/data-tier-operations/) | Scales an existing database — replication topology, partitioning vs sharding, isolation level, distributed-transaction pattern, failover, pooling. |
| [`Data/dimensional-modeling`](.claude/skills/Data/dimensional-modeling/) | Designs an analytical OLAP model — fact-table grain, conformed / role-playing / degenerate dimensions, SCD strategy, star vs snowflake vs galaxy. |

```
database-architecture   →  WHERE the schema lives + WHICH store  (ADR)
relational-modeling      →  tables for a relational store
data-tier-operations     →  sharding / replication / pooling / txn isolation
dimensional-modeling     →  star / snowflake / fact / dimension / warehouse
```

### Prompts — authoring, testing, and session hygiene

| Skill | Role |
|---|---|
| [`Prompts/ambiguity-gate`](.claude/skills/Prompts/ambiguity-gate/) | Asks before acting when a request could reasonably be read more than one way. |
| [`Prompts/prompt-archive`](.claude/skills/Prompts/prompt-archive/) | Archives a keeper prompt into `.claude/_Prompts/`, or logs the current session's prompts. |
| [`Prompts/prompt-tester`](.claude/skills/Prompts/prompt-tester/) | Runs a prompt against a few examples and reports whether it does what it claims. |
| [`Prompts/session-handoff`](.claude/skills/Prompts/session-handoff/) | Writes a structured handoff file before a session compacts or work resumes elsewhere. |
| [`Prompts/skill-interaction-testing`](.claude/skills/Prompts/skill-interaction-testing/) | Tests a new or changed skill against every sibling for stacking, contradiction, silent override, and beneficial chaining. |

### Decision skills (top level)

| Skill | Role |
|---|---|
| [`learning-gate`](.claude/skills/learning-gate/) | Classifies intent (learning / execution / reference) and sets how much of the thinking Claude may do. |
| [`problem-solving-gates`](.claude/skills/problem-solving-gates/) | Rubber Duck (debugging), Options Generator (architecture), Knowledge Checker — each requires prior independent effort. |
| [`microservices-decision`](.claude/skills/microservices-decision/) | Whether and how to split services, bounded by the number of people who can own them. |
| [`api-interface-style`](.claude/skills/api-interface-style/) | Picks the interaction style for one API surface — REST / GraphQL / gRPC / WebSocket / SSE / webhooks / async messaging — from its consumers, interaction shape, and latency / real-time needs. Produces an ADR. |
| [`technical-cost-decision`](.claude/skills/technical-cost-decision/) | Forces the cost arithmetic on any decision that carries a recurring price. |
| [`ticket-evaluation`](.claude/skills/ticket-evaluation/) | Separates what a ticket says from what it's missing from what can be judged; verdict last. |
| [`explaining-my-work`](.claude/skills/explaining-my-work/) | One evidence base rendered at three altitudes — plain summary, spoken script, public post. |
| [`commit-and-push`](.claude/skills/commit-and-push/) | Stages, commits, and pushes with a message derived from the actual diff. |

`Git/` is an empty placeholder for future git-workflow skills.

## Prompt logging

[`.claude/settings.json`](.claude/settings.json) registers a `UserPromptSubmit` hook that
runs [`scripts/hooks/log-prompt.sh`](scripts/hooks/log-prompt.sh). Every submitted prompt is
appended to `.claude/_Prompts/logs/YYYY-MM-DD.md` with a timestamp and short session id. The
hook is defensive by design — it always exits 0 and prints nothing, so it can neither block a
prompt nor inject text into context.

## Adding a skill

1. Draft it (`SKILL.md` + reference files + `README.md`) under the right group in `.claude/skills/`.
2. Screen it in isolation — baseline fails without it, the skill fixes the failure.
3. Run [`Prompts/skill-interaction-testing`](.claude/skills/Prompts/skill-interaction-testing/)
   against the existing skill set. Record what you found (hand-off, absorption, chaining, or a
   fix for stacking / contradiction / silent override).
