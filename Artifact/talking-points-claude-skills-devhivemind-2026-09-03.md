# Talking points — Claude skills built from DevHiveMind — 2026-09-03

Drafted with the `explaining-my-work` skill. Every claim below traces to the repo, the parent
`PersonalBrain` vault's git history, or the session it was written in.

**Could not verify:** that DevHiveMind predates *public* generative AI. Earliest commit in the
`PersonalBrain` git history is **2024-01-13** — after ChatGPT's Nov-2022 release. The drafts
use a narrower, checkable framing ("before I had a way to point an AI at it"). If your real
timeline goes back further than the git history (notes kept before the vault was put under
git), you can strengthen that line yourself — I left it conservative on purpose.

---

## Part 1 — Evidence Block

| What was built | Mechanism (technical) | What it's worth (business) | Outcome: number or named risk | Source |
|---|---|---|---|---|
| **Data-architecture skill pipeline** | 4 chained gate-skills: `database-architecture` (source-of-truth + store → ADR), `relational-modeling` (OLTP tables), `data-tier-operations` (sharding/replication/pooling → ADR), `dimensional-modeling` (star/SCD). Each refuses output until preconditions are answered; each stops before implementation and hands off. | Stops a schema or scaling decision being locked in across many files before anyone has said where the source of truth lives or what the measured pressure is. | Design property, **not yet measured**: `database-architecture` requires 6 questions answered in the user's own words before any schema appears; each of the 4 skills emits an ADR or data-model doc with a concrete "revisit when" threshold. | `.claude/skills/Data/*/` + READMEs; source notes in `Architecture/02. Backing Service Options/Databases/` |
| **Prompts skill set** | 5 skills: `ambiguity-gate`, `prompt-archive` (curated save / session log), `prompt-tester` (run on examples, report), `session-handoff`, `skill-interaction-testing`. | Keeps prompt work and session context from being lost or redone; keeps clarification cheap. | Design property, **not yet measured**: 5 skills, each with an explicit trigger list and out-of-scope list. | `.claude/skills/Prompts/*/` |
| **Decision skills (top level)** | 7 skills: `learning-gate` (intent classify → 0–5 assistance ceiling), `problem-solving-gates` (Rubber Duck / Options Generator / Knowledge Checker), `microservices-decision`, `technical-cost-decision`, `ticket-evaluation`, `explaining-my-work`, `commit-and-push`. | Each targets one recurring way a solo engineer skips a reasoning step. | Named risks reduced: a cost decision made fluently in words and never converted to a number; a service list acted on before checking who'd own each service; a learning rep replaced by AI output. **Not yet measured.** | `.claude/skills/` top level; source note `learning Gate.md` |
| **Skill-interaction testing loop** | A skill that runs each new skill against every existing one for stacking, contradiction, silent override, and chaining, in an isolated agent. | Prevents two skills quietly fighting or double-gating the same request — a failure that only exists in combination. | **Measured:** run 4 times; every round produced a change — description disclaimers, a structural double-gating fix in `learning-gate`, a scope clause, 4 description edits. | `.claude/skills/Prompts/skill-interaction-testing/`, `memory/MEMORY.md` (4 entries) |
| **Prompt-logging hook** | `UserPromptSubmit` hook → `scripts/hooks/log-prompt.sh` appends every submitted prompt to a dated log. Exits 0, prints nothing, so it can't block a prompt or inject context. | A durable record of how the tooling is actually prompted. | Design property: 1 hook, always-exit-0, dated append-only logs. | `.claude/settings.json`, `scripts/hooks/log-prompt.sh` |
| **DevHiveMind / PersonalBrain vault (substrate)** | An Obsidian vault of software-design reference notes. `Architecture/` alone holds 1,614 markdown notes. Each skill names the note it was written from. | The skills are a compression of reference material already written — not new content generated on the spot. | **Measured:** git history from 2024-01-13; 1,614 notes in `Architecture/`; all 16 skills cite a named source note. | `PersonalBrain` git log; skill READMEs |
| **THE SET as a whole** | 16 skills, one shape: `SKILL.md` (gate + output contract) + companion reference files + `README.md`. Mostly gates. Written from vault notes, tested against each other before shipping. | One person's design knowledge turned into guardrails that make him use it — value is in *not* skipping steps. | **Measured:** 16 skills (7 + 4 + 5); 4 interaction-test rounds logged. **Not yet measured:** effect on any real project. | This session; `.claude/skills/CATALOG.md` |

---

## Part 2 — Plain-Language Summary

For about two years I've kept a private reference library on how software systems are designed —
databases, service boundaries, scaling, cost tradeoffs. I call it DevHiveMind. I've now turned
16 of those write-ups into "skills" for an AI coding assistant: small rule sets that make the
assistant stop and ask the right questions before it acts, instead of guessing. Most of them
are built to *withhold* an answer until I've personally made the decision that's mine to make —
where data should live, whether a cost is worth paying, whether I actually understand something
or just read it. The notes did the hard part; the skills are a mechanism to make myself use
them. It's early: the skills run, but haven't been through a full real project yet.

---

## Part 3 — Conversation Script

**Opener (≤2 sentences)**
"I keep a personal reference library on how software systems get designed, and I've started
turning it into guardrails for an AI coding assistant. The point isn't to make it write more —
it's to make it stop and ask me the decisions I shouldn't be skipping."

**Their question, your read**
Ask: "Do you work in software, or more on the product/business side?"

**If they go technical**
"They're Claude skills — a `SKILL.md` with a gate plus reference files. Most are precondition
gates. The data-architecture one won't emit a schema until I've answered consumers, ownership,
exposure, and source-of-truth leaning in my own words; then it writes an ADR, not code. There's
a pipeline behind it — relational modeling, then sharding and replication, then dimensional
modeling — each hands off to the next. And I run a skill that tests every new skill against the
existing set for stacking and silent override, because that failure only shows up when two
gates fire on the same prompt. That's already caught a double-gating bug between the learning
gate and the data skills."

**If they stay non-technical**
"Think of it like a checklist that refuses to let me move on. If I ask it to design a database,
it won't — it makes me answer where that data really belongs and who depends on it first. If I
say something looks expensive, it makes me actually do the math instead of guessing. The
knowledge is stuff I wrote down over the last couple of years; this is just a way to force
myself to use it instead of cutting corners when I'm in a hurry."

**Follow-up line**
"Happy to share the catalog of the 16 skills if you want to see the shape — it's all plain
markdown, and the interesting part is which decisions each one refuses to make for you."

---

## Part 4 — LinkedIn Draft

For about two years I've kept a private reference library on how software systems get designed —
databases, service boundaries, scaling, cost tradeoffs. I call it DevHiveMind. It started as a
learning habit, well before I had a way to point an AI at it.

Last month I turned 16 of those notes into Claude "skills" — small rule sets for an AI coding
assistant. Most are gates: they refuse to answer until I've done the part that's mine.

The data-architecture skill won't produce a schema until I've said, in my own words, where the
source of truth lives and who reads it. The cost skill won't let "this seems expensive" stay a
feeling — it forces the arithmetic. The learning gate checks whether I want to understand
something or just want the answer.

Each skill was written from a specific note I'd already made. The library did the hard part;
the skills make me use it. I also run every new skill against the others to catch two of them
quietly fighting — that check has changed something all four times it's run.

Caveats: early days. The skills work but haven't been through a full real project, and "it
stopped me cutting a corner" is hard to measure. One person's setup, not a team's.

*(~190 words. Hashtags optional — none, or at most `#softwarearchitecture` and `#claude`.)*
