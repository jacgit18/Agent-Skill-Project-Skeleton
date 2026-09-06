# Task 4: Plan Full-Stack Project #1

**Files:**
- Create: `projects/PROJECT-1-plan.md` (project brief, architecture, success criteria)
- Create: `projects/PROJECT-1-log.md` (working log: problems hit, how you solved them, what you learned)

**Interfaces:**
- Consumes: Problem-solving gate system (Task 1), System design communication agent (Task 2)
- Produces: A shipped full-stack project + documented problem-solving process + a 5-minute interview story

**What this does:** Plan one solid full-stack project. This is where problem-solving and communication skills apply to real work. The project becomes interview talking point and proof you can ship.

## Steps

### Step 1: Help the user choose a project

Guide them toward a project that:
- Requires full-stack work (backend + frontend, or multiple interacting systems)
- Has at least one non-trivial technical challenge (caching, concurrency, real-time updates, distributed coordination, etc.)
- Is doable in 6-8 weeks of part-time work
- Genuinely interests them (they'll stick with it)

Examples: real-time collaborative app, system with non-trivial backend logic, full-stack feature they've wanted to build

Avoid: tutorial projects, toy projects, 24-hour clones

Get from user: project name, high-level goal, why this one (what will it teach?)

### Step 2: Write the project brief (architecture)

Help them create `projects/PROJECT-1-plan.md` with:

**Structure:**
```
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

### Step 3: Create the working log template

Help them create `projects/PROJECT-1-log.md` (initially empty) with template:

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

### Step 4: Clarify the execution phase

Explain that the actual building (Step 4 in the original plan) will happen over weeks 5-12, when they:
- Use the problem-solving gate system when stuck
- Document problems and solutions in PROJECT-1-log.md
- Build incrementally (test each piece)

### Step 5: Extract interview story (for later)

Note that once the project ships, they'll add a "Final Interview Story" section to the plan.

### Step 6: Commit

```bash
git add projects/PROJECT-1-plan.md projects/PROJECT-1-log.md
git commit -m "doc: project 1 plan and working log"
```

---

## Global Constraints

- Timeline: Flexible, but this planning happens weeks 1-4
- Success metric: User can explain architecture and tradeoffs
- Project must be real (not tutorial)
- Must be doable in 6-8 weeks part-time
