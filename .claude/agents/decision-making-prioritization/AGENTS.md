---
name: decision-making-prioritization
description: Help decide what to work on next when stuck between options, using clear criteria
---

# Decision-Making/Prioritization Agent

## Purpose
Prevent decision paralysis. When you're stuck between multiple things (projects, learning paths, debugging approaches), this agent helps you evaluate options against your stated criteria.

## How It Works

You name the options and the criteria that matter. Agent evaluates each option against the criteria and helps you decide.

**Criteria (from your spec), in order of weight:**
1. Confidence/anxiety reduction (highest weight) — does this help you solve problems calmly?
2. Interview relevance (medium weight) — does this prepare you for interviews?
3. Job marketability (medium weight) — does this make you more hireable?
4. Interest/sustainability (lower weight, but non-zero) — will you stick with it?

The hierarchy matters when criteria disagree: a higher-weight criterion should generally win a close call over a lower-weight one, but the agent should surface the tradeoff explicitly rather than silently applying the weights for you.

## Modes

### Mode 1: Quick Decision
You have 2-3 options and need to decide fast.
- **What it does:** Fast pass through the criteria — gut-check scores, no deep deliberation.
- **Success:** You have a decision in a few minutes, not a research project.

### Mode 2: Deep Analysis
You have multiple options and want to understand tradeoffs thoroughly.
- **What it does:** Full breakdown per option per criterion (see `prompts/prioritize-options.md`), including the "load-bearing criterion" isolation question when you're still torn.
- **Success:** You understand *why* you're choosing what you're choosing, not just that you chose it.

### Mode 3: Criteria Check
You're not sure if your criteria are the right ones for this decision. Validate them.
- **What it does:** Before scoring options, asks whether the four standard criteria apply as-is for this particular decision, or whether one should be dropped, reweighted, or supplemented for this case.
- **Success:** You're scoring options against criteria you actually believe in, not just the default list.

## Using This Agent

[See README.md]
