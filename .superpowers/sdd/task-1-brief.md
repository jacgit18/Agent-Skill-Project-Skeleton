# Task 1: Refine Problem-Solving Gate Skill

**Files:**
- Modify: `problem-solving-gates/SKILL.md` (enhance and clarify)
- Create: `problem-solving-gates/README.md` (usage guide)
- Create: `problem-solving-gates/examples/` directory with 3-4 real debugging scenarios

**Interfaces:**
- Consumes: Your existing problem-solving-gates/SKILL.md
- Produces: Refined skill definition, runnable examples, clear preconditions for each mode

**What this does:** Your problem-solving gate skill is the foundation. This task refines it based on what you've learned, adds concrete examples, and makes it clear how to invoke each mode (Rubber Duck, Options Generator, Knowledge Checker).

## Steps

### Step 1: Review your current SKILL.md against the design

Open `problem-solving-gates/SKILL.md` and check:
- Does the Rubber Duck mode clearly define when to use it? (debugging with a hypothesis)
- Does Options Generator clearly define its precondition? (named constraints + initial position)
- Does Knowledge Checker clearly define what "understanding" means? (can explain in own words first)
- Are the escape hatches clear?

Note any gaps or confusing sections.

### Step 2: Enhance SKILL.md with clarifications

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

### Step 3: Create README for the skill

Create `problem-solving-gates/README.md` with:
1. What this skill is for (three-sentence overview)
2. Which mode to use when (decision tree: "Are you debugging? → Rubber Duck. Are you deciding? → Options Generator. Are you learning? → Knowledge Checker.")
3. How to invoke each mode (the precondition check is critical — if you don't have the precondition, state what's missing)
4. A table of common mistakes (e.g., "Trying Rubber Duck without a hypothesis" → "What's your hypothesis?")

Keep this under 300 words.

### Step 4: Create examples directory

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

### Step 5: Test the skill against a real problem

Pick a real problem you're currently stuck on (code debugging, architecture decision, or learning something). Invoke the problem-solving gate skill.
- Did the mode help?
- Was the precondition check clear?
- Did Claude's role feel right (not doing the thinking for you)?

Note any friction or confusion.

### Step 6: Refine based on testing

If you found confusion or friction in Step 5:
- Update `problem-solving-gates/SKILL.md` to clarify the mode or precondition
- Update `README.md` to address the confusion point
- Update or add an example if needed

### Step 7: Commit

```bash
git add problem-solving-gates/SKILL.md problem-solving-gates/README.md problem-solving-gates/examples/
git commit -m "refactor: clarify problem-solving gate skill with examples and usage guide"
```

---

## Global Constraints

- **Timeline:** Flexible, but sequenced (Tier 1 → Tier 2 → Tier 3)
- **Success metric:** You can debug complex problems independently, explain solutions clearly, tell interview stories about projects
- **No theory-first:** Learn by building and using, not by studying first
- **Interview-focused:** Every skill should have a clear connection to interview readiness
