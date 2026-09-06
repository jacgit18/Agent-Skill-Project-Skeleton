# AI QA Testing Patterns & Notes

## Pattern 1: Consistency Testing (Prompt Validation)
**What it does:** Runs a prompt multiple times with the same input, measures output variance

**When to use:** When you need stable, predictable behavior (e.g., categorization, classification)

**Example:** Test "categorize this expense" prompt 5 times with same transaction → check if it always picks same category

**Tools:** Custom Python script, promptfoo consistency tests

**Tradeoffs:** 
- ✓ Cheap to run (just API calls)
- ✗ Temperature/randomness matters (need to control model settings)
- ✗ Doesn't validate correctness, only consistency

## Pattern 2: Format Validation (Output Validation)
**What it does:** Checks if output matches expected structure (JSON schema, regex, etc.)

**When to use:** When you need structured outputs (JSON, markdown, CSV)

**Example:** Prompt returns JSON with required fields → validate schema matches, all fields present, types correct

**Tools:** JSON Schema, Pydantic, regex validators

**Tradeoffs:**
- ✓ Fast and cheap
- ✓ Catches obvious breakage immediately
- ✗ Doesn't check semantic correctness (output could be valid JSON but wrong content)

## Pattern 3: Semantic Validation (Human-in-the-Loop)
**What it does:** Human reviewer checks if output is actually correct (meaning, accuracy, helpfulness)

**When to use:** When correctness matters and rules can't capture it (e.g., explaining a concept, generating code)

**Example:** Ask for explanation of a complex topic → expert reads it and scores accuracy 1-5

**Tools:** Braintrust, custom scoring rubrics, crowd-sourced evaluation

**Tradeoffs:**
- ✓ Catches real correctness problems
- ✗ Expensive and slow
- ✗ Subjective (need rubric calibration)

## Pattern 4: Adversarial/Boundary Testing
**What it does:** Test behavior on edge cases, adversarial inputs, boundary conditions

**When to use:** Safety-critical or public-facing systems, or when trying to break something

**Example:** Try to make a content moderation prompt reject legitimate inputs or allow harmful ones

**Tools:** Custom test cases, fuzzing, prompt injection libraries

**Tradeoffs:**
- ✓ Finds real problems
- ✗ Requires creativity to design good adversarial cases
- ✗ Can be expensive (many API calls to find failures)

## Pattern 5: Cost/Latency Profiling
**What it does:** Measure token usage, API latency, and total cost of running a prompt at scale

**When to use:** When deploying to production with volume or latency constraints

**Example:** Evaluate 1000 transactions with categorization prompt → total tokens, avg latency, cost at 100k/month scale

**Tools:** Anthropic token counter, custom instrumentation, promptfoo metrics

**Tradeoffs:**
- ✓ Essential for production planning
- ✗ Requires actually running at scale (not just single tests)
- ✗ Costs money to profile comprehensively

## Pattern 6: Regression Testing (Change Detection)
**What it does:** Compare prompt outputs before/after a change, flag significant differences

**When to use:** After tweaking a prompt, want to ensure you didn't break existing behavior

**Example:** Refactor categorization prompt for clarity → run on 100 historical transactions, compare before/after categorizations

**Tools:** Braintrust, custom diff scripts, promptfoo comparison mode

**Tradeoffs:**
- ✓ Catches subtle regressions
- ✗ Requires baseline for comparison
- ✗ Need to define "significant difference" (fuzzy)

## Key Insight: Determinism Matters
LLMs are non-deterministic by default (temperature > 0). This means:
- Same prompt + input → different outputs each time
- Testing must account for variance (multiple runs, statistical aggregation)
- Determinism is possible (temperature=0) but sometimes reduces quality
