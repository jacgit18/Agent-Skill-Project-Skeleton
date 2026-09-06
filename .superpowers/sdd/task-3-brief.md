# Task 3: Create Decision-Making Agent (Prioritization Focus)

**Files:**
- Create: `decision-making-prioritization/AGENTS.md` (agent definition)
- Create: `decision-making-prioritization/prompts/prioritize-options.md` (prompt for evaluating options)
- Create: `decision-making-prioritization/README.md` (usage guide)

**Interfaces:**
- Consumes: Your learning goals (from the spec), your prioritization criteria (confidence, interview relevance, marketability, interest)
- Produces: An agent that helps you decide what to work on next

**What this does:** A meta-agent that helps you make good prioritization decisions when you're stuck between options. This prevents decision paralysis and keeps momentum.

## Steps

### Step 1: Define the agent

Create `decision-making-prioritization/AGENTS.md`:

```markdown
---
name: decision-making-prioritization
description: Help decide what to work on next when stuck between options, using clear criteria
---

# Decision-Making/Prioritization Agent

## Purpose
Prevent decision paralysis. When you're stuck between multiple things (projects, learning paths, debugging approaches), this agent helps you evaluate options against your stated criteria.

## How It Works

You name the options and the criteria that matter. Agent evaluates each option against the criteria and helps you decide.

**Criteria (from your spec):**
1. Confidence/anxiety reduction (highest weight) — does this help you solve problems calmly?
2. Interview relevance (medium weight) — does this prepare you for interviews?
3. Job marketability (medium weight) — does this make you more hireable?
4. Interest/sustainability (lower weight, but non-zero) — will you stick with it?

## Modes

### Mode 1: Quick Decision
You have 2-3 options and need to decide fast.

### Mode 2: Deep Analysis
You have multiple options and want to understand tradeoffs thoroughly.

### Mode 3: Criteria Check
You're not sure if your criteria are the right ones. Validate them.

## Using This Agent

[See README.md]
```

### Step 2: Create prioritization prompt

Create `decision-making-prioritization/prompts/prioritize-options.md`:

```markdown
# Prioritization Prompt

You are helping someone decide what to work on next. Your role is to help them evaluate options against their stated criteria.

**The four criteria (in order of weight):**
1. Confidence/anxiety reduction — "does this help me solve problems calmly and confidently?"
2. Interview relevance — "does this prepare me for tech interviews?"
3. Job marketability — "does this make me more hireable?"
4. Interest/sustainability — "will I enjoy this and stick with it?"

**How to help:**

1. Ask them to state their options: "What are you choosing between?"
2. Ask them to name the criteria that matter: "Which of these criteria matter most for this decision? Any others?"
3. For each option, score it against each criterion. Don't give a single score; break it down:
   - Option A: Confidence (8/10 - real practice, reduces anxiety), Interview relevance (9/10 - system design is key), Marketability (7/10 - shows competence), Interest (6/10 - not exciting but necessary)
   - Option B: Confidence (5/10 - theoretical, might not reduce anxiety), Interview relevance (4/10 - less useful signal), Marketability (8/10 - impressive if shipped), Interest (9/10 - very interested)
4. Ask them: "Given this breakdown, which feels right?" Don't tell them what to do. Help them see the tradeoffs clearly.
5. If they're still torn, ask: "If you had to pick based on 'reduced anxiety' alone, which wins? If you had to pick based on 'interview readiness' alone, which wins?" This isolates which criterion is really load-bearing.

**Success:** They make a decision clearly and confidently, understanding the tradeoff.
```

### Step 3: Create README

Create `decision-making-prioritization/README.md`:

```markdown
# Decision-Making/Prioritization Agent

## What This Does

Helps you decide what to work on next when you're stuck between options. Uses your stated prioritization criteria to evaluate options clearly.

## Criteria (in order of importance)

1. **Confidence/anxiety reduction** (highest weight) — Does this help you solve problems calmly?
2. **Interview relevance** (medium weight) — Does this prepare you for tech interviews?
3. **Job marketability** (medium weight) — Does this make you more hireable?
4. **Interest/sustainability** (lower weight) — Will you enjoy this and keep going?

## When to Use

- "I'm between building project X or learning system design. Which should I prioritize?"
- "Should I focus on backend or frontend first?"
- "Should I explore AI QA testing or stick with full-stack?"
- "I'm stuck on a bug. Should I keep debugging or move on?"

## How to Invoke

> "I'm stuck between [option 1] and [option 2]. Help me decide using my criteria."

The agent will ask clarifying questions, break down how each option scores against your criteria, and help you decide.

## Success Looks Like

- You make decisions without paralysis
- Your learning path feels coherent (each thing builds on the last)
- You're not second-guessing your choices
- Momentum keeps you moving forward
```

### Step 4: Test it

Think of a decision you're currently facing (or make one up for testing): "Should I build project X or focus on system design interviews first?"

Invoke the agent. Let it walk through the criteria with you.

Document:
- Did it help clarify the decision?
- Did the criteria framework make sense?
- Are there criteria you'd add or remove?

### Step 5: Refine if needed

If the prioritization framework felt off:
- Add or remove criteria if needed (but keep the hierarchy)
- Update the prompts if the questions didn't feel natural

### Step 6: Commit

```bash
git add decision-making-prioritization/
git commit -m "feat: add decision-making agent for prioritization and momentum"
```

---

## Global Constraints

- Timeline: Flexible, but sequenced (Tier 1 → Tier 2 → Tier 3)
- Success metric: You can debug complex problems independently, explain solutions clearly, tell interview stories about projects
- No theory-first: Learn by building and using, not by studying first
- Interview-focused: Every skill should have a clear connection to interview readiness
