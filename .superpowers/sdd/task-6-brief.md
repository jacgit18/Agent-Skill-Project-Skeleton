# Task 6: Plan Full-Stack Project #2 (or Deepen Project #1)

**Phase:** Tier 2 Application (Weeks 5-12)

**Goal:** Build or deepen a second project. By now you've got one interview story solid. This adds depth and shows iteration.

## What This Task Consumes
- Lessons from Project 1 (task-4-report.md documents problems and solutions)
- Feedback from system design practice (task-5 log will have insights)
- Decision-making agent (Task 3) to choose between new project vs. deepening Project 1

## What This Task Produces
- `projects/PROJECT-2-plan.md` (or enhanced PROJECT-1-plan.md if deepening)
- Clear architecture, success criteria, and timeline
- A second interview story (draft)
- Optionally: `projects/PROJECT-2-log.md` if starting a new project

## Detailed Steps

### Step 1: Decide: New Project or Deepen Existing?

You have two options:

**Option A (Recommended): Build a second, smaller project (4-6 weeks)**
- Different technical focus from Project 1 (if P1 was collaborative, maybe P2 is distributed systems; if P1 was backend, maybe P2 is frontend-focused)
- Teaches a complementary full-stack skill
- Shows breadth in your portfolio

**Option B: Deepen Project 1**
- Add a significant feature (from MVP to production-ready)
- Shows iteration and polish
- Might be faster if you're already deep in the codebase

**Decision criteria (use decision-making agent if stuck):**
1. Confidence/anxiety: Which would make you feel more confident in interviews? (new breadth or deep expertise in one area?)
2. Interview relevance: Which tells a better story? (two different projects or one deeply refined?)
3. Job marketability: What does your target role value? (breadth or depth?)
4. Interest/sustainability: Which will you enjoy more?

### Step 2: Plan the Project

Create `projects/PROJECT-2-plan.md` with this structure (same as Task 4):

```markdown
# Project 2: [Name]

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
[Estimate weeks based on scope — probably 4-6 weeks if new, or 2-4 if deepening]

## Interview Story (Draft)
"I built [project name]. The challenge was [main technical challenge]. I solved it by [your approach]. Here's what I learned: [one insight about system design, debugging, or problem-solving]."
```

### Step 3: Create working log (if new project)

If you chose Option A (new project), also create `projects/PROJECT-2-log.md`:

```markdown
# Project 2 Working Log

[Initially empty — you'll fill this as you work, same format as PROJECT-1-log.md]
```

If you chose Option B (deepening), just update PROJECT-1-plan.md with a new "Phase 2" section.

### Step 4: Commit

```bash
git add projects/PROJECT-2-plan.md
git commit -m "doc: project 2 plan and architecture"
```

Or if deepening Project 1:
```bash
git add projects/PROJECT-1-plan.md
git commit -m "doc: project 1 phase 2 plan and extended timeline"
```

## Success Criteria
- ✓ Decision made (new project or deepen?)
- ✓ `PROJECT-2-plan.md` (or updated PROJECT-1-plan.md) exists
- ✓ Architecture documented with technical decisions
- ✓ Non-trivial challenges identified
- ✓ Success criteria and timeline clear
- ✓ Interview story drafted
- ✓ Commit created

## Important Notes
- Don't start building yet — this task is planning only
- The actual project work (building, testing, logging) comes after this task is reviewed
- Use the decision-making agent if you're stuck on the choice (new vs. deepen)
- Project 2 doesn't have to be bigger than Project 1 — it just needs to teach something new
