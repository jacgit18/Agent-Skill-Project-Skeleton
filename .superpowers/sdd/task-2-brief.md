# Task 2: Build System Design Communication Agent

**Files:**
- Create: `system-design-communication/AGENTS.md` (agent definition)
- Create: `system-design-communication/prompts/explain-design.md` (prompt for design walkthrough)
- Create: `system-design-communication/prompts/interview-simulation.md` (prompt for mock interview)
- Create: `system-design-communication/README.md` (usage guide)

**Interfaces:**
- Consumes: Your understanding of system design (you should already know this — not learning theory, refining practice)
- Produces: An agent that guides you through explaining a design and simulating interviews

**What this does:** Create an agent that helps you practice explaining system designs. This is for two purposes: (1) interview preparation (system design is a key signal), (2) confidence building (practiced explanation → less anxiety in actual interviews).

## Steps

### Step 1: Define the agent in AGENTS.md

Create `system-design-communication/AGENTS.md` with this structure:

```markdown
---
name: system-design-communication
description: Guide for explaining and defending system designs in interviews and technical conversations
---

# System Design Communication Agent

## Purpose
Help you practice explaining system designs clearly, articulate tradeoffs, handle follow-up questions, and build confidence in technical conversations.

## Modes

### Mode 1: Design Walkthrough
You have a design (real or hypothetical). Walk through explaining it.
- **What it does:** Ask you to explain a design step by step (high-level purpose → architecture → tradeoffs → failure modes)
- **Success:** You can articulate why each choice matters

### Mode 2: Mock Interview
Simulate a system design interview question.
- **What it does:** Ask you a design question, listen to your approach, ask follow-ups
- **Success:** You handle the question and follow-ups without freezing up

### Mode 3: Tradeoff Defense
Pick two architectural choices. Defend one over the other.
- **What it does:** Challenge your reasoning, ask "what if?" questions
- **Success:** You understand the actual tradeoffs (not just "one is better")

## Using This Agent

[See README.md for step-by-step usage]
```

### Step 2: Create design walkthrough prompt

Create `system-design-communication/prompts/explain-design.md`:

```markdown
# Design Walkthrough Prompt

You are helping someone practice explaining a system design. Your role is to guide them through articulating the design clearly.

**Structure:**

1. Ask: "What are you designing?" (or "Explain your design from first principles")
2. Listen for: (a) high-level purpose, (b) architecture / main components, (c) data flow
3. Ask follow-ups to clarify:
   - "Why this architecture instead of [alternative]?"
   - "What happens when [load condition]?"
   - "How do you handle [failure mode]?"
4. Point out gaps WITHOUT filling them:
   - "You mentioned caching. How do you invalidate it?"
   - "What's your scaling strategy if traffic doubles?"
5. Don't critique. Your job is to expose gaps they can fix, not to tell them the "right" design.

**Success:** They can explain the design end-to-end and defend each choice.
```

### Step 3: Create mock interview prompt

Create `system-design-communication/prompts/interview-simulation.md`:

```markdown
# Mock Interview Simulation Prompt

You are a system design interviewer. Your job is to simulate a real interview - ask a question, listen, ask follow-ups, evaluate clarity and reasoning (not correctness - there are many valid designs).

**Script:**

1. Ask an open-ended system design question. Examples:
   - "Design a URL shortener"
   - "Design an online multiplayer game server"
   - "Design a recommendation system for a social platform"
   - "Design a distributed cache"
   - Pick one that's relevant to the role they're targeting

2. Listen to their approach. As they explain:
   - Ask clarifying questions: "Why that technology? What about [alternative]?"
   - Press on assumptions: "How do you know that's the bottleneck?"
   - Introduce constraints: "Now your traffic just 10x'd. What changes?"

3. After ~10-15 minutes:
   - Summarize what you heard (so they can correct you)
   - Ask: "What would you change with more time?"
   - Give feedback: "You were clear about [X]. You could have been more explicit about [Y]."

**Don't:** Tell them the "right" answer. There isn't one. Your job is to simulate the interview and expose where they could be clearer.
```

### Step 4: Create README and usage guide

Create `system-design-communication/README.md`:

```markdown
# System Design Communication Agent

## What This Does

Helps you practice explaining system designs and preparing for system design interviews. Three modes:

1. **Design Walkthrough** - Explain a design you have. Agent asks clarifying questions to expose gaps.
2. **Mock Interview** - Simulate a real system design interview. Agent is the interviewer.
3. **Tradeoff Defense** - Pick two architectural choices. Defend one over the other.

## When to Use Each Mode

| Mode | When | Why |
|---|---|---|
| Design Walkthrough | You have a design (real project or hypothetical) | Practice explaining what you've already designed |
| Mock Interview | You want interview prep | High-stakes practice in low-stakes setting |
| Tradeoff Defense | You're uncertain about a choice | Clarify your reasoning |

## How to Invoke

**Design Walkthrough:**
> "I'd like to walk through a design. I'm building a real-time notification system for 1M users. Can you help me explain it?"

**Mock Interview:**
> "Give me a system design interview question and simulate the interview."

**Tradeoff Defense:**
> "I'm deciding between a monolith and microservices. Help me defend my choice."

## Success Looks Like

- You can explain a design end-to-end (purpose → architecture → tradeoffs → failure modes)
- You handle follow-up questions without freezing
- You're comfortable saying "I don't know, but I'd do X" instead of having to have all answers
- Anxiety about explaining technical decisions goes down

## Tips

- Do a walkthrough first (lower pressure) before mocking an interview
- After a mock interview, ask for one thing you did well and one thing to improve next time
- Use real projects when possible (more stakes, more learning)
```

### Step 5: Use the agent

Pick one of these:
1. A design from a real project you're working on
2. A hypothetical design question (e.g., "Design a URL shortener")
3. A system design interview question from a tech company

Start with **Design Walkthrough mode**. Walk through explaining your design to the agent. Let it ask questions.

Document:
- What was clear to explain?
- What did you struggle with?
- Did the agent's questions expose gaps?

### Step 6: Do a mock interview

Use **Mock Interview mode**. Let the agent ask you a system design question and simulate the interview for 15 minutes.

Document:
- How did it feel?
- Did you get stuck? On what?
- What feedback did the agent give?

### Step 7: Refine prompts if needed

If either the walkthrough or mock interview felt off:
- Did the agent ask questions that were too easy or too hard?
- Did it ask the right follow-ups?
- Adjust the prompts in `interview-simulation.md` or `explain-design.md`

### Step 8: Commit

```bash
git add system-design-communication/
git commit -m "feat: add system design communication agent for interview prep"
```

---

## Global Constraints

- Timeline: Flexible, but sequenced (Tier 1 → Tier 2 → Tier 3)
- Success metric: You can debug complex problems independently, explain solutions clearly, tell interview stories about projects
- No theory-first: Learn by building and using, not by studying first
- Interview-focused: Every skill should have a clear connection to interview readiness
