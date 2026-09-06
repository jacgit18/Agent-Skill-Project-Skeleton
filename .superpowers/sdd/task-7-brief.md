# Task 7: Explore AI QA Testing Fundamentals

**Phase:** Tier 3 Alternative Path (optional, after Tier 1 & 2 solid)

**Goal:** Build familiarity with AI testing patterns as a potential alternative career path. This is explicitly secondary — only explore if Tier 1 & 2 are solid and you've started job applications.

## What This Task Consumes
- Understanding of evals & observability concepts (from high-priority engineering layer)
- Your QA background (you have prior QA experience)

## What This Task Produces
- `ai-qa-testing/LEARNING-PLAN.md` — structured learning path with priorities
- `ai-qa-testing/notes.md` — patterns and insights as you learn
- Optional: A small AI QA testing project or test harness
- One commit documenting the exploration

## Detailed Steps

### Step 1: Map the learning path

Create `ai-qa-testing/LEARNING-PLAN.md`:

```markdown
# AI QA Testing Learning Plan

## Why This Path
- You have QA background (valuable signal for AI QA roles)
- AI testing is an emerging area with fewer competitors
- Creates a backup career path if full-stack roles don't work out
- Complements your agent/prompt work (testing is built-in to reliability)

## What to Learn

### High Priority (Start here)
- [ ] Prompt validation: How do you test if a prompt works consistently?
  - Consistency across inputs
  - Edge case handling
  - Failure modes
- [ ] Output validation: How do you check if an AI output is correct?
  - Rule-based checks (exact match, format validation)
  - Semantic checks (does it mean the right thing?)
  - Human-in-the-loop validation
- [ ] Safety & bias testing: How do you test for harmful outputs?
  - Adversarial inputs
  - Bias detection
  - Refusal behavior
- [ ] Automated eval frameworks: Tools for testing
  - promptfoo (easiest to start with)
  - Braintrust (more powerful)
  - LangSmith, other providers

### Medium Priority (After high-priority)
- [ ] Testing agent behavior: How do you verify an agent does what it's supposed to?
- [ ] Performance testing for LLMs: Latency, cost, token usage
- [ ] Regression testing for prompts: How to catch when a prompt breaks
- [ ] Evaluation design: Writing good test cases

### Resources
- promptfoo documentation (github.com/promptfoo/promptfoo) — start here, tutorials
- Braintrust documentation (braintrust.dev)
- Papers: "Towards a Unified Framework for AI Testing" (search for LLM eval papers)
- DeepLearning.AI course on evals (if available)

## Learning Approach
- Learn one high-priority topic at a time
- Build something small to practice (test harness, eval framework demo)
- Document patterns as you go
- Don't try to learn everything — focus on high-priority first

## Success Criteria
- [ ] Can explain 3 ways to validate an AI output
- [ ] Have built or used at least one eval framework (promptfoo minimum)
- [ ] Can write a simple test case for a prompt
- [ ] Understand the gap between traditional QA and AI QA
- [ ] Have one small project or test harness as proof of concept
```

### Step 2: Start learning

Pick one high-priority topic and start. Recommended order:
1. Prompt validation (foundation)
2. Output validation (most common use case)
3. Safety & bias testing (increasingly important)
4. Automated eval frameworks (the tooling)

### Step 3: Build something small

Create a simple AI QA project:
- Option A: Write a test harness for one of your existing agents/prompts using promptfoo
- Option B: Create a simple eval script that tests a prompt's consistency
- Option C: Build a prompt validator that checks multiple output properties

This doesn't need to be large — even a 10-line eval script counts. The goal is hands-on experience.

### Step 4: Document patterns

Create `ai-qa-testing/notes.md`:

```markdown
# AI QA Testing Notes

## Pattern 1: Consistency Testing
**What it does:** Tests if a prompt produces similar outputs for the same input (run 3-5 times, check consistency)
**When to use:** When you need stable, predictable behavior
**Example:** Testing a prompt that generates product descriptions
**Tools:** promptfoo, custom harness
**Tradeoffs:** Takes multiple API calls (cost); catches real LLM variance

## Pattern 2: Format Validation
**What it does:** Tests if output matches expected structure (JSON, markdown, etc.)
**When to use:** When you need structured outputs
**Example:** Testing an agent that returns JSON with specific fields
**Tools:** JSON Schema validation, regex, custom checkers
**Tradeoffs:** Easy to check; doesn't validate semantic correctness

## Pattern 3: Semantic Validation (Human-in-the-loop)
**What it does:** Human reviewer checks if output is correct (not just well-formed)
**When to use:** When correctness matters, rules can't capture it
**Example:** Testing if an explanation is actually accurate
**Tools:** Braintrust, custom UI, score cards
**Tradeoffs:** Slow, expensive; captures real meaning

## Pattern 4: Adversarial Testing
**What it does:** Test behavior on edge cases, adversarial inputs, boundary conditions
**When to use:** Safety-critical or public-facing applications
**Example:** Testing if a chat agent refuses harmful requests
**Tools:** Prompt injection test suites, custom adversarial cases
**Tradeoffs:** Takes creativity to find good test cases; catches real risks

[Add more patterns as you discover them]
```

### Step 5: Commit

```bash
git add ai-qa-testing/
git commit -m "docs: ai qa testing learning plan and initial exploration"
```

Then, after you build your first small project:
```bash
git add ai-qa-testing/
git commit -m "feat: basic prompt validation test harness"
```

## Success Criteria
- ✓ `ai-qa-testing/LEARNING-PLAN.md` exists with structured priorities
- ✓ At least one high-priority topic researched (and documented in notes)
- ✓ Small project or test harness built (optional but recommended)
- ✓ `ai-qa-testing/notes.md` has at least 2-3 patterns documented
- ✓ Commit created with the exploration work

## Important Notes
- This is explicitly secondary — only pursue after Tier 1 & 2 are solid
- The goal is familiarity, not mastery
- Combine with your full-stack projects: as you build agents, test them
- This is a backup path, not a requirement
- Start with promptfoo (easiest onramp), don't get bogged down in advanced frameworks
