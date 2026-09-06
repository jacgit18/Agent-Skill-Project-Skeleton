# Task 5: Practice System Design Communication

**Phase:** Tier 2 Application (Weeks 5-12)

**Goal:** While building Project 1, practice system design communication in parallel. Create a practice log and do at least one mock interview or design walkthrough.

## What This Task Consumes
- System Design Communication Agent (Task 2) — already built and tested in the repo at `system-design-communication/AGENTS.md`
- Problem-solving log structure from Task 4

## What This Task Produces
- `practice-logs/system-design-practice.md` — practice log file with entries
- At least one completed practice session (mock interview or design walkthrough) documented in the log
- A commit documenting the practice work

## Detailed Steps

### Step 1: Create practice log file
Create `practice-logs/system-design-practice.md` with this structure:

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

### Step 2: Do one practice session
Pick ONE of these:
1. **Mock Interview (Higher Pressure):** Use the system-design-communication agent in Mock Interview mode. Pick a realistic system design question (URL shortener, notification system, distributed cache, etc). Let the agent ask you a question and simulate the interview for 15 minutes.
2. **Design Walkthrough (Lower Pressure):** Pick a design from Project 1 that you've built. Walk through explaining it to the agent. Let it ask clarifying questions.

Either option is fine — the goal is one practice session to get baseline.

### Step 3: Document the session
Add one entry to `practice-logs/system-design-practice.md` with:
- What you practiced (mock interview or walkthrough)
- The question/design
- Your approach or explanation
- Feedback from the agent
- One specific thing to focus on next time

### Step 4: Commit
```bash
git add practice-logs/
git commit -m "docs: system design communication practice log and first session"
```

## Success Criteria
- ✓ `practice-logs/system-design-practice.md` exists with the structure above
- ✓ At least one practice session documented (mock interview or walkthrough)
- ✓ Feedback from agent captured
- ✓ Commit created with the practice work

## Notes
- This is ongoing work (will have more entries over weeks), but we need at least one entry to establish the practice
- The agent is already built — just invoke it in the appropriate mode
- Focus on getting the practice in, not perfection in the first session
