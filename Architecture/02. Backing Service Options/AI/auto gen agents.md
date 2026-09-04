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
# Skills vs. generated agents

  

"Agent" does two different jobs in this project, and knowing which one you mean

decides whether you want a skill or a generated module.

  

## Two different things share the word "agent"

  

1. **A generated module in `agents/`** (like `commit_message_agent.py`) — this is

*runtime code*. It's a function your product calls, at 2am, from a cron job,

from a web request — no human, no Claude Code session involved. It exists to

be part of your software.

2. **The tier in the Claude API decision table** (open-ended, tool-using,

multi-step loop) — most of what `build_agent.py` generates isn't actually

this. `commit_message_agent.py` is one API call wrapped in a function. It

only earns the "agent" label in the looser "a piece of code that calls

Claude" sense.

  

A **skill** is neither of those — it's *dev-time* behavior. It changes what

Claude Code does for *you*, in *this* session, while you're building things. It

has no existence outside a Claude Code conversation.

  

So "skills vs. agents" isn't really a spectrum you pick a point on — they

operate at different times:


| Component                  | Runs when                               | Exists for         |
| -------------------------- | --------------------------------------- | ------------------ |
| **Skill**                  | While you're coding, inside Claude Code | You, the developer |
| **Generated agent module** | In production, unattended               | Your product/users |


## When you actually want to generate an agent module

  

Reach for it when the task needs to run *without* you driving Claude Code:

  

- It's triggered by something other than a person typing — a webhook, a

schedule, another service's request

- It needs to be called from other code (`from agents.foo import bar`), not

just from a chat

- It's cheap-enough and narrow-enough that a fixed function beats a

tool-using loop (see the "Should I Build an Agent?" bar in the claude-api

skill — complexity/value/viability/cost-of-error)

  

If none of that's true — if what you actually want is "when I ask for X in a

coding session, do these steps consistently" — that's a skill, not a

generated module. The `generate-agent` skill is a good example of getting this

right: it's dev-time process, not a runtime artifact.

  

## The real-world version, once you have an actual codebase

  

Right now `build_agent.py` has one input: the spec file. That's fine for a

greenfield toy project, but it doesn't know anything about the rest of the

codebase — so every generated agent reinvents error handling, client setup,

naming, wherever the model's prior happens to land, and drifts further from

whatever else is out there. That's the gap between what exists today and

"generating agents based on the architecture."

  

The pattern that scales is splitting the input into two layers instead of one:

  

1. **Task-specific** — the spec (`specs/foo.md`): what *this* agent does.

Stays exactly as-is.

2. **Codebase-wide** — how things are built *here*: shared client setup,

error-handling convention, where new agents get registered, how they're

tested, directory layout. This is what a real `ARCHITECTURE.md`/per-directory

`README.md` set captures — `CLAUDE.md` and `agents/README.md` are the seed

of this already, just thin.

  

Once layer 2 exists, there are two ways to use it, and which one wins depends

on scale:

  

- **Small/templated** (what exists today): `build_agent.py` reads the spec

*and* the architecture doc, stuffs both into one prompt, gets back a file.

Works fine while the codebase is small enough to summarize in one doc.

- **Large/real**: a skill replaces the standalone script. Instead of a static

architecture doc going stale, the skill's instructions tell Claude Code to

*read the actual code* — grep for the existing agents, open two or three

similar ones, check how they're wired into whatever registers them, then

write the new file directly with Edit/Write. This is strictly better once

the codebase is real, because it's reading ground truth, not a description

someone forgot to update.

  

So the natural trajectory is: `generate-agent` (skill, dev-time) absorbs

`build_agent.py`'s job as the codebase grows, not the other way around. The

standalone script stays useful only as the mechanical "call the API and write

the file" step the skill invokes — the judgment about *how* to fit the

architecture moves into the skill's instructions, backed by Claude actually

reading the surrounding code.




Right — "production" was too narrow a word on my part. The defining trait isn't _which_ environment, it's _what triggers execution_: a human typing into a Claude Code session vs. anything else. That "anything else" shows up at every stage of the lifecycle, not just prod:

|Environment|Example trigger|What it might do|
|---|---|---|
|Local dev|a git hook (`prepare-commit-msg`)|run `commit_message_agent.py` on your own commits before they're even pushed|
|CI / build (GitHub Actions)|PR opened, push to branch|a workflow step calls an agent module to summarize a diff, draft a PR description, flag risky changes|
|QA / staging|test suite finishes, nightly job|an agent module triages failing tests, summarizes a flaky-test report, generates test data|
|Production|webhook, scheduled job, user request|the agent module is part of the running product — drafts a support reply, classifies an incoming ticket|

Same code, same "generated module" pattern in every row — `agents/commit_message_agent.py` doesn't need to change to move from your laptop's git hook to a GitHub Actions step. What changes is:

- **The trigger** — a hook, a workflow YAML step, a cron entry, a request handler
- **The environment/secrets** — which `ANTHROPIC_API_KEY` it runs with, what other env vars are available (CI secrets vs. `.env` vs. prod secret manager)
- **What it's allowed to do with the output** — locally it might just print to your terminal; in CI it might post a PR comment; in prod it might write to a database

A concrete version of your actual example: `commit_message_agent.py` running as a GitHub Action step on `pull_request` that posts a suggested PR title as a comment is a completely realistic use — that's "build process," not production, and it's exactly the same generated module.

So: yes to QA, yes to GitHub/CI, yes to build steps — anywhere execution is unattended counts. Production is just the row people default to picturing because it's the one that stays running longest.