# AI-Powered Learning Portfolio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a portfolio of agents and skills that help you debug independently, communicate technical decisions clearly, execute full-stack projects, and make good prioritization decisions — landing you a tech job while reducing anxiety and building sustainable confidence.

**Architecture:** Four interconnected agents/skills build progressively: (1) Problem-solving foundation (debugging + architecture communication) trains independent problem-solving; (2) Project execution + decision-making skills apply that foundation to real work; (3) AI QA testing becomes available as an alternative path. Each skill is a SKILL.md or agents.md definition with prompts, gates, and success criteria. You use them immediately, refining based on real feedback.

**Tech Stack:** Claude Code, Claude (API), problem-solving gate pattern, agent orchestration (MCP, Claude Agent SDK as applicable)

**Spec:** [2026-08-30-ai-powered-learning-portfolio-design.md](../specs/2026-08-30-ai-powered-learning-portfolio-design.md)

## Global Constraints

- **Timeline:** Flexible, but sequenced (Tier 1 → Tier 2 → Tier 3)
- **Success metric:** You can debug complex problems independently, explain solutions clearly, tell interview stories about projects
- **No theory-first:** Learn by building and using, not by studying first
- **Interview-focused:** Every skill should have a clear connection to interview readiness

---

## PHASE 1: Tier 1 Foundation (Weeks 1-4)

### Task 1: Refine Problem-Solving Gate Skill

**Files:**
- Modify: `problem-solving-gates/SKILL.md` (enhance and clarify)
- Create: `problem-solving-gates/README.md` (usage guide)
- Create: `problem-solving-gates/examples/` directory with 3-4 real debugging scenarios

**Interfaces:**
- Consumes: Your existing problem-solving-gates/SKILL.md
- Produces: Refined skill definition, runnable examples, clear preconditions for each mode

**What this does:** Your problem-solving gate skill is the foundation. This task refines it based on what you've learned, adds concrete examples, and makes it clear how to invoke each mode (Rubber Duck, Options Generator, Knowledge Checker).

- [ ] **Step 1: Review your current SKILL.md against the design**

Open `problem-solving-gates/SKILL.md` and check:
- Does the Rubber Duck mode clearly define when to use it? (debugging with a hypothesis)
- Does Options Generator clearly define its precondition? (named constraints + initial position)
- Does Knowledge Checker clearly define what "understanding" means? (can explain in own words first)
- Are the escape hatches clear?

Note any gaps or confusing sections.

- [ ] **Step 2: Enhance SKILL.md with clarifications**

For each of the three modes, add:
1. A one-sentence trigger ("Use this when you're...")
2. A clear precondition (what must be true before Claude engages)
3. What happens next (Claude's role in the mode)
4. A concrete example of invoking it

Example structure for Rubber Duck:
```
## Mode 1: Rubber Duck (Debugging)

**Trigger:** You're in a debugging session, you have a hypothesis about what's wrong.

**Precondition:** You must have formulated a hypothesis first (even a bad one). If you don't have one yet, stop here and form one before invoking this mode.

**Once precondition is met:** [existing text]

**Example:**
> "I'm debugging a race condition in my caching layer. My hypothesis: the problem is that we're not invalidating cache on concurrent writes. Can you rubber-duck this with me?"
```

Add similar examples for Options Generator and Knowledge Checker.

- [ ] **Step 3: Create README for the skill**

Create `problem-solving-gates/README.md` with:
1. What this skill is for (three-sentence overview)
2. Which mode to use when (decision tree: "Are you debugging? → Rubber Duck. Are you deciding? → Options Generator. Are you learning? → Knowledge Checker.")
3. How to invoke each mode (the precondition check is critical — if you don't have the precondition, state what's missing)
4. A table of common mistakes (e.g., "Trying Rubber Duck without a hypothesis" → "What's your hypothesis?")

Keep this under 300 words.

- [ ] **Step 4: Create examples directory**

Create `problem-solving-gates/examples/` with three files:
- `example-rubber-duck.md` — a real debugging scenario, walking through the mode
- `example-options-generator.md` — a real architecture decision, walking through the mode
- `example-knowledge-checker.md` — a real learning scenario, walking through the mode

Each example should:
- Start with context ("I just read about X and want to verify I understand it")
- Show the precondition check ("Do I have this before I start?")
- Show 2-3 back-and-forth exchanges
- End with the outcome ("I found a gap in my understanding" or "I made a decision")

Keep each example to 200-300 words.

- [ ] **Step 5: Test the skill against a real problem**

Pick a real problem you're currently stuck on (code debugging, architecture decision, or learning something). Invoke the problem-solving gate skill.
- Did the mode help?
- Was the precondition check clear?
- Did Claude's role feel right (not doing the thinking for you)?

Note any friction or confusion.

- [ ] **Step 6: Refine based on testing**

If you found confusion or friction in Step 5:
- Update `problem-solving-gates/SKILL.md` to clarify the mode or precondition
- Update `README.md` to address the confusion point
- Update or add an example if needed

- [ ] **Step 7: Commit**

```bash
git add problem-solving-gates/SKILL.md problem-solving-gates/README.md problem-solving-gates/examples/
git commit -m "refactor: clarify problem-solving gate skill with examples and usage guide"
```

---

### Task 2: Build System Design Communication Agent

**Files:**
- Create: `system-design-communication/AGENTS.md` (agent definition)
- Create: `system-design-communication/prompts/explain-design.md` (prompt for design walkthrough)
- Create: `system-design-communication/prompts/interview-simulation.md` (prompt for mock interview)
- Create: `system-design-communication/README.md` (usage guide)

**Interfaces:**
- Consumes: Your understanding of system design (you should already know this — not learning theory, refining practice)
- Produces: An agent that guides you through explaining a design and simulating interviews

**What this does:** Create an agent that helps you practice explaining system designs. This is for two purposes: (1) interview preparation (system design is a key signal), (2) confidence building (practiced explanation → less anxiety in actual interviews).

- [ ] **Step 1: Define the agent in AGENTS.md**

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

- [ ] **Step 2: Create design walkthrough prompt**

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

- [ ] **Step 3: Create mock interview prompt**

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

- [ ] **Step 4: Create README and usage guide**

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

- [ ] **Step 5: Use the agent**

Pick one of these:
1. A design from a real project you're working on
2. A hypothetical design question (e.g., "Design a URL shortener")
3. A system design interview question from a tech company

Start with **Design Walkthrough mode**. Walk through explaining your design to the agent. Let it ask questions.

Document:
- What was clear to explain?
- What did you struggle with?
- Did the agent's questions expose gaps?

- [ ] **Step 6: Do a mock interview**

Use **Mock Interview mode**. Let the agent ask you a system design question and simulate the interview for 15 minutes.

Document:
- How did it feel?
- Did you get stuck? On what?
- What feedback did the agent give?

- [ ] **Step 7: Refine prompts if needed**

If either the walkthrough or mock interview felt off:
- Did the agent ask questions that were too easy or too hard?
- Did it ask the right follow-ups?
- Adjust the prompts in `interview-simulation.md` or `explain-design.md`

- [ ] **Step 8: Commit**

```bash
git add system-design-communication/
git commit -m "feat: add system design communication agent for interview prep"
```

---

### Task 3: Create Decision-Making Agent (Prioritization Focus)

**Files:**
- Create: `decision-making-prioritization/AGENTS.md` (agent definition)
- Create: `decision-making-prioritization/prompts/prioritize-options.md` (prompt for evaluating options)
- Create: `decision-making-prioritization/README.md` (usage guide)

**Interfaces:**
- Consumes: Your learning goals (from the spec), your prioritization criteria (confidence, interview relevance, marketability, interest)
- Produces: An agent that helps you decide what to work on next

**What this does:** A meta-agent that helps you make good prioritization decisions when you're stuck between options. This prevents decision paralysis and keeps momentum.

- [ ] **Step 1: Define the agent**

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

- [ ] **Step 2: Create prioritization prompt**

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

- [ ] **Step 3: Create README**

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

- [ ] **Step 4: Test it**

Think of a decision you're currently facing (or make one up for testing): "Should I build project X or focus on system design interviews first?"

Invoke the agent. Let it walk through the criteria with you.

Document:
- Did it help clarify the decision?
- Did the criteria framework make sense?
- Are there criteria you'd add or remove?

- [ ] **Step 5: Refine if needed**

If the prioritization framework felt off:
- Add or remove criteria if needed (but keep the hierarchy)
- Update the prompts if the questions didn't feel natural

- [ ] **Step 6: Commit**

```bash
git add decision-making-prioritization/
git commit -m "feat: add decision-making agent for prioritization and momentum"
```

---

## PHASE 2: Tier 2 Application (Weeks 5-12)

### Task 4: Plan Full-Stack Project #1

**Files:**
- Create: `projects/PROJECT-1-plan.md` (project brief, architecture, success criteria)
- Create: `projects/PROJECT-1-log.md` (working log: problems hit, how you solved them, what you learned)

**Interfaces:**
- Consumes: Problem-solving gate system (Task 1), System design communication agent (Task 2)
- Produces: A shipped full-stack project + documented problem-solving process + a 5-minute interview story

**What this does:** Execute one solid full-stack project. This is where problem-solving and communication skills apply to real work. The project becomes interview talking point and proof you can ship.

- [ ] **Step 1: Choose a project**

Pick a project that:
- Requires full-stack work (backend + frontend, or multiple interacting systems)
- Has at least one non-trivial technical challenge (caching, concurrency, real-time updates, distributed coordination, etc.)
- Is doable in 6-8 weeks of part-time work (not a massive ambitious thing)
- Genuinely interests you (you'll stick with it)

Examples that fit the criteria:
- A real-time collaborative app (Figma-like sketch tool, collaborative document editor)
- A system with non-trivial backend logic (recommendation engine, job scheduler, rate limiter)
- A full-stack feature you've wanted to build (chat with file uploads, notification system, etc.)

**Avoid:** Tutorial projects, toy projects, "build X clone in 24 hours" — these don't teach real problem-solving.

Write down: **Project name**, **high-level goal**, **why this one** (what will it teach you?).

- [ ] **Step 2: Write the project brief (architecture)**

Create `projects/PROJECT-1-plan.md`:

```markdown
# Project 1: [Name]

## Goal
One sentence: what are you building and why?

## Architecture

### High-Level
[2-3 paragraphs describing the system]
- What's the main workflow?
- What are the core components?
- How do they talk to each other?

### Technical Decisions
| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Backend framework | [choice] | [reasoning] | [what you rejected] |
| Database | [choice] | [reasoning] | [what you rejected] |
| Frontend framework | [choice] | [reasoning] | [what you rejected] |
| Deployment | [choice] | [reasoning] | [what you rejected] |

### Non-Trivial Challenges
List the hard parts:
1. [Challenge 1] — Why it's hard and how you'll approach it
2. [Challenge 2] — Why it's hard and how you'll approach it

## Success Criteria
- [ ] Shipped and deployed
- [ ] Core features working
- [ ] Clean code (reviewable)
- [ ] Tests for critical paths
- [ ] Can explain the architecture and tradeoffs

## Timeline
- Week 1-2: Setup, scaffold, core backend
- Week 3-4: Backend features + testing
- Week 5-6: Frontend
- Week 7: Integration, debugging, polish
- Week 8: Deploy, document, interview story

## Interview Story (Draft)
"I built [project name]. The challenge was [main technical challenge]. I solved it by [your approach]. Here's what I learned: [one insight about system design, debugging, or problem-solving]."
```

- [ ] **Step 3: Create working log**

Create `projects/PROJECT-1-log.md` (initially empty, you'll fill this as you work):

```markdown
# Project 1 Working Log

## Entry 1: [date]
**What I worked on:** [feature/component]
**Problem I hit:** [what went wrong]
**How I solved it:** [your approach]
**What I learned:** [insight]

## Entry 2: [date]
[repeat above]
```

- [ ] **Step 4: Start building**

Begin the project. Use the problem-solving gate system when you get stuck (Rubber Duck mode for debugging, Options Generator for architecture questions).

**Each day/session:**
1. Work on the project
2. When you hit a real problem (bug, architectural decision, learning gap):
   - Use the problem-solving gate system
   - Document the problem, your approach, and what you learned in PROJECT-1-log.md
3. Build incrementally: get one thing working, test it, move to the next

**When you're done:** You have a working project, a log of how you problem-solved, and a 5-minute story about what you built.

- [ ] **Step 5: Extract the interview story**

Once the project is shipped, add to `projects/PROJECT-1-plan.md`:

```markdown
## Final Interview Story
[Write 1-2 paragraphs]

Tell this story in three parts:
1. "Here's what I built: [project + goal]"
2. "The hard part was [technical challenge]. I solved it by [your approach]."
3. "Here's what I learned: [one insight about debugging, architecture, or scaling]"

Practice telling this story in 2-3 minutes. Be ready to explain each choice.
```

- [ ] **Step 6: Commit**

```bash
git add projects/PROJECT-1-plan.md projects/PROJECT-1-log.md
git commit -m "doc: project 1 plan and working log"
```

[The code changes for the project itself will be many commits — commit frequently as you build.]

---

### Task 5: Practice System Design Communication (Ongoing During Task 4)

**Files:**
- Create: `practice-logs/system-design-practice.md` (tracking mock interviews and design walkthroughs)

**Interfaces:**
- Consumes: System Design Communication Agent (Task 2)
- Produces: Practice log + muscle memory for explaining designs

**What this does:** While building Project 1, practice system design communication in parallel. Do one mock interview or design walkthrough per week.

- [ ] **Step 1: Create practice log**

Create `practice-logs/system-design-practice.md`:

```markdown
# System Design Communication Practice Log

## Mock Interview 1: [Date]
**Question:** [What did the agent ask?]
**Your approach:** [High-level design you presented]
**Feedback:** [What the agent said you did well / could improve]
**Takeaway:** [One thing to focus on next time]

## Mock Interview 2: [Date]
[repeat above]

---

## Design Walkthrough 1: [Date]
**Design:** [What you were designing]
**Gaps exposed:** [What questions revealed you hadn't thought through]
**Resolved:** [How you filled in the gaps]

## Design Walkthrough 2: [Date]
[repeat above]
```

- [ ] **Step 2: Weekly practice schedule**

Every week during Project 1:
- **Option A:** One mock interview (simulates high-pressure interview scenario)
- **Option B:** One design walkthrough (lower pressure, still gets the practice)

Alternate if possible (don't do the same mode twice in a row).

- [ ] **Step 3: Fill in the log**

After each session, record what you did, what feedback you got, what to focus on next.

- [ ] **Step 4: Commit**

```bash
git add practice-logs/system-design-practice.md
git commit -m "doc: system design communication practice log"
```

[After each practice session, add an entry to the log and commit.]

---

### Task 6: Plan Full-Stack Project #2 (or deepen Project #1)

**Files:**
- Modify: `projects/PROJECT-1-plan.md` (or create PROJECT-2-plan.md)

**Interfaces:**
- Consumes: Lessons from Project 1, feedback from system design practice
- Produces: A second shipped project (or deepened version of first) with new problem-solving stories

**What this does:** Build or deepen a second project. By now you've got one interview story solid. This adds depth and shows iteration.

**Option A (Recommended):** Build a second, smaller project (4-6 weeks instead of 8) that teaches a different full-stack skill (e.g., if Project 1 was a collaborative app, Project 2 could be a distributed system with eventual consistency).

**Option B:** Take Project 1 and add a significant feature (push it from MVP to production-ready).

- [ ] **Step 1: Decide: new project or deepen existing?**

- [ ] **Step 2: Plan the second project (similar to Task 4)**

Create the architecture brief, success criteria, timeline.

- [ ] **Step 3: Execute and log**

Same as Task 4 — build incrementally, use problem-solving gates, log your process.

- [ ] **Step 4: Extract second interview story**

By the end, you have two interview stories: "Here's what I built" × 2.

---

## PHASE 3: Tier 3 Alternative Path (optional, after Tier 1 & 2 solid)

### Task 7: Explore AI QA Testing Fundamentals

**Files:**
- Create: `ai-qa-testing/LEARNING-PLAN.md` (what to learn, why, priority)
- Create: `ai-qa-testing/notes.md` (as you learn, document patterns)

**Interfaces:**
- Consumes: Understanding of evals & observability (from high-priority engineering layer concepts)
- Produces: Familiarity with AI testing patterns, backup career path option

**What this does:** If full-stack roles don't work out, you have an alternative. But this is explicitly secondary — only explore if Tier 1 & 2 are solid and you've started job applications.

- [ ] **Step 1: Map the learning path**

Create `ai-qa-testing/LEARNING-PLAN.md`:

```markdown
# AI QA Testing Learning Plan

## Why This Path
[From the spec: you have QA background, AI testing is an emerging area with fewer competitors]

## What to Learn

### High Priority
- [ ] Prompt validation: how do you test if a prompt works? (consistency, edge cases)
- [ ] Output validation: how do you check if an AI output is correct?
- [ ] Safety & bias testing: how do you test for harmful outputs?
- [ ] Automated eval frameworks: promptfoo, Braintrust (tools for testing)

### Medium Priority
- [ ] Testing agent behavior: how do you verify an agent does what it's supposed to?
- [ ] Performance testing for LLMs: latency, cost, token usage
- [ ] Regression testing for prompts: how to catch when a prompt breaks

### Resources
- DeepLearning.AI course on evals (if available)
- promptfoo docs + tutorial
- Papers on LLM evaluation (start with one, not all)

## Success Criteria
- [ ] Can explain 3 ways to test an AI output
- [ ] Have built/used one eval framework (promptfoo or similar)
- [ ] Can write a test case for a prompt
- [ ] Understand the gap between traditional QA and AI QA
```

- [ ] **Step 2: Start learning one topic at a time**

Pick the first high-priority topic. Learn it. Build something small to practice (e.g., write a prompt tester for one of your agents).

- [ ] **Step 3: Document patterns**

Create `ai-qa-testing/notes.md` as you learn. Write down:
- Pattern: How to test X
- Example: A concrete test you wrote
- Tradeoff: When this approach works / doesn't work

- [ ] **Step 4: Build one small AI QA project**

Create a test harness for one of your agents or prompts. This gives you concrete experience to talk about.

- [ ] **Step 5: Commit**

```bash
git add ai-qa-testing/
git commit -m "docs: ai qa testing learning plan and notes"
```

---

## Success Metrics (End of Implementation)

**Tier 1 Complete:**
- ✓ Problem-solving gate skill refined, with examples, tested on real problems
- ✓ System design communication agent built and tested (done at least 2 mock interviews)
- ✓ Decision-making agent built and used when stuck
- ✓ Can debug independently, communicate clearly, feel calmer

**Tier 2 Complete:**
- ✓ Project 1 shipped with problem-solving log
- ✓ Project 2 shipped (or Project 1 deepened)
- ✓ Two solid interview stories, practiced multiple times
- ✓ Mock interview confidence: you handle system design questions without freezing

**Tier 3 (if pursued):**
- ✓ Understand AI QA testing patterns
- ✓ Have built one small AI QA project
- ✓ Can talk about it as an alternative path

**Overall:**
- ✓ You can debug complex problems independently
- ✓ You can explain technical decisions clearly
- ✓ You have 2-3 projects to talk about
- ✓ Anxiety about tech interviews has gone down significantly
- ✓ You're ready to apply and interview
