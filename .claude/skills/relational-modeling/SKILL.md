---
name: relational-modeling
description: Turns a settled "we're using a relational database" into an actual table design — normal form and the denormalization exceptions, key strategy (surrogate vs natural, int vs UUID), constraint placement, an index plan, lifecycle/audit columns, and relationship patterns (junction tables, self-joins, nullable FKs). Use this skill after the source-of-truth / persistence decision is made (by `database-architecture` or because a relational store already exists) and the user needs the schema itself: "model the schema for X", "how should I normalize this", "what should I index", "surrogate or natural key", "how do I handle soft deletes", "one table or two for this". It produces an ERD sketch, a table-by-table spec, and an index list — not migration code, and not the where-should-the-schema-live decision (that is `database-architecture`).
---

# Relational Modeling

Given a relational database that is already the chosen store, design the tables: how normalized, keyed how, what the database enforces, what gets indexed, how lifecycle is tracked. The skill makes the user state the entities, relationships, and access patterns first, then produces a concrete design with the tradeoffs named.

## When to use

- The source-of-truth / persistence decision is **already made** — an ADR exists in `docs/architecture/decisions/`, or the user says plainly "we're on Postgres/MySQL/SQL Server and staying there" — and now the tables need designing.
- The user asks a modeling question: normalization level, key choice, index strategy, constraint placement, soft-delete/lifecycle, junction vs nullable FK, self-referencing hierarchy.
- An existing schema needs a modeling review — over/under-normalized, missing or redundant indexes, keys that will not scale.

## Out of scope — hand these off

- **Where the schema should live** (database-first / code-first / contract-first), what the consumers and boundaries are, whether a formal API contract is warranted → `database-architecture`. If that decision has **not** been made, stop and send the user there first; do not model on top of an unstated assumption.
- **Sharding, replication, connection pooling, transaction isolation levels, distributed-transaction patterns (2PC / Saga)** → `data-tier-operations`. Note when the design will need them; don't design them here.
- **Analytical / OLAP modeling** — star and snowflake schemas, fact and dimension tables, data grain, warehouses and marts, materialized views for reporting → `dimensional-modeling`. A different discipline with the opposite default (denormalize, not normalize); this skill is for the transactional (OLTP) store.
- **ORM / query-builder selection**, migration tooling, and writing the migrations themselves. This skill stops at the design.

---

## The gate

Lighter than `database-architecture`'s, but it is still a gate. Do not produce tables until these are answered.

**Prerequisite (check first):**

- **The store is relational and settled.** Point to the ADR or get the user to state it. If the persistence decision is open, stop — this is `database-architecture`'s job, not this skill's.

**From the user, in their own words** (do not invent these, do not model without them):

1. **Entities** — the things being stored, named as business concepts. Not tables yet.
2. **Relationships** — how the entities relate, with cardinality in plain words: "one customer has many orders", "a product can be in many orders and an order has many products", "an employee reports to one other employee".
3. **Access patterns** — the handful of queries that matter: what is looked up by what, what is filtered or sorted, what is joined. Plus the read/write ratio, roughly.
4. **Volume** — rough row counts per entity and growth rate. "Hundreds of customers, millions of orders, tens of millions of order-lines" changes the index and key calculus; "everything under 10k rows" means most of this skill is overkill and you should say so.
5. **Lifecycle needs** — does anything need soft delete, history/audit, effective-dated versions, or a hard "is this row still active" flag — and is any of it driven by a retention or compliance rule.

"Model the schema for X" with 1–5 absent is not valid input. Ask for what's missing and stop.

---

## Challenge the framing

If the user opens with the design half-made ("just give me the tables, fully normalized" / "I'll use a UUID primary key on everything" / "one big table is fine"), don't just execute it. Test it against what they gave for the gate:

- **"fully normalized"** — at what volume and read pattern? 3NF is the default, but a read-heavy path that joins five tables on every request is where a controlled denormalization or a materialized view earns its place. Which queries drove the "fully"?
- **"UUID everywhere"** — do you actually need client-generated or cross-system-unique ids, or is this cargo-culted? UUID primary keys cost index size and, for random UUIDs, write locality on the clustered index. A surrogate `bigint` plus a `UNIQUE` external id is often the better split.
- **"one big table"** — how many of the columns are null for any given row? Wide sparse tables are a normalization smell. What made you avoid the join?
- **"no foreign keys, the app handles it"** — every writer goes through that app? Forever? FK constraints are the cheapest integrity you will ever get; dropping them is a decision, not a default.

Flag the assumption as a question, not a correction.

---

## The process

Work `modeling-framework.md` in order once the gate is satisfied. In short: entities → relationships and their table shapes → normal form and named exceptions → keys → constraints the database enforces → indexes → lifecycle columns → the ERD and table specs.

Two reference files support it:

- `normalization-and-keys.md` — the normal forms in brief, when denormalization is the right call, and how to choose keys.
- `indexing-and-constraints.md` — building the index plan, where constraints live (column vs table vs app), referential actions, and lifecycle/audit columns.

---

## Output

**1. In chat, a design summary:**

```
Store:              <database technology, from the ADR>
Normal form:        <target, e.g. 3NF> with exceptions: <denormalizations and why, or "none">
Tables:             <count and names>
Key strategy:       <surrogate bigint | natural | UUID — and why>
DB-enforced:        <the constraints the database owns: NOT NULL, UNIQUE, FK + actions, CHECK>
App-enforced:       <invariants the schema can't express, and where they live>
Indexes:            <one line per index: table(columns) — the query it serves>
Lifecycle:          <soft-delete / audit / versioning approach, or "hard delete, no history">
Deferred:           <what this design will eventually need — sharding, partitioning, an OLAP copy — with the trigger>
```

**2. A table-by-table spec and an ERD sketch** (ASCII or a `mermaid erDiagram`), written to `docs/data-model/<slug>.md`. Include every table: columns with types, nullability, keys, FKs with their referential actions, and the indexes. Create the directory if absent.

Then stop. Migrations and ORM wiring are a separate step the user starts explicitly.

---

## Escape hatch

If the user has already modeled it — entities settled, normal form chosen with reasons, keys and indexes decided — and wants a review or a tie-break rather than a walk through the framework, they can say so and you give a direct assessment. That is an opt-in, not a default.

---

## Example invocations

> "We've got the ADR — Postgres, code-first, internal API. Now I need the schema for a course-enrollment feature. Entities: students, courses, enrollments, instructors. A student enrolls in many courses; a course has many students; a course has one instructor; instructors teach many courses. Main queries: a student's current courses, a course's roster, an instructor's course list. ~50k students, ~2k courses, ~500k enrollments/term. Enrollments need history — we report on drops."

Gate satisfied (prerequisite ADR, entities, relationships with cardinality, access patterns, volume, lifecycle). Work `modeling-framework.md`: `enrollments` is the junction table (student_id, course_id, status, enrolled_at, dropped_at); 3NF throughout; surrogate `bigint` keys with a `UNIQUE(student_id, course_id, term_id)`; indexes on `enrollments(student_id, status)` and `enrollments(course_id)`; drops kept as status transitions with timestamps rather than row deletion. Write `docs/data-model/course-enrollment.md`.

> "Design the database for our app."

Gate not satisfied on multiple axes, and possibly the wrong skill — there's no evidence the source-of-truth decision was made. Response: ask whether `database-architecture` has been run, and name the gate items 1–5 that are missing. Do not produce tables.

---

## Portability

Repo-agnostic. Reads `docs/architecture/decisions/` for the prerequisite ADR, writes `docs/data-model/`. Copy the `relational-modeling/` directory into another repo's `.claude/skills/` to use it there.
