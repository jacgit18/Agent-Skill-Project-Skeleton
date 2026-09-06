# AI QA Testing Learning Plan

## Why This Path
- You have QA background (valuable signal for AI QA roles)
- AI testing is an emerging area with fewer competitors
- Creates a backup career path if full-stack roles don't work out
- Complements your agent/prompt work (testing is built-in to reliability)
- Growing need for specialized AI safety and quality testing expertise

## What to Learn

### High Priority (Start here)
- [ ] **Prompt validation**: How do you test if a prompt works consistently?
  - Consistency across inputs
  - Edge case handling
  - Failure modes
  - Example: Running same prompt 5 times, measuring output variance

- [ ] **Output validation**: How do you check if an AI output is correct?
  - Rule-based checks (exact match, format validation)
  - Semantic checks (does it mean the right thing?)
  - Human-in-the-loop validation
  - Example: JSON format checking, semantic similarity scoring

- [ ] **Safety & bias testing**: How do you test for harmful outputs?
  - Adversarial inputs
  - Bias detection
  - Refusal behavior
  - Example: Testing if a model refuses harmful requests

- [ ] **Automated eval frameworks**: Tools for testing
  - promptfoo (easiest to start with)
  - Braintrust (more powerful)
  - LangSmith, other providers
  - Example: Using promptfoo to run 100 test cases against a prompt

### Medium Priority (After high-priority)
- [ ] Testing agent behavior: How do you verify an agent does what it's supposed to?
- [ ] Performance testing for LLMs: Latency, cost, token usage
- [ ] Regression testing for prompts: How to catch when a prompt breaks
- [ ] Evaluation design: Writing good test cases
- [ ] Tracing and observability: Understanding what an LLM does step-by-step

### Resources
- promptfoo documentation (github.com/promptfoo/promptfoo) — start here, tutorials
- Braintrust documentation (braintrust.dev)
- Papers: "Towards a Unified Framework for AI Testing" (search for LLM eval papers)
- DeepLearning.AI course on evals (if available)
- OpenAI Cookbook (github.com/openai/cookbook) — evaluation examples
- Articles: "Prompt Engineering vs. Prompt Validation" concept blogs

## Learning Approach
- Learn one high-priority topic at a time
- Build something small to practice (test harness, eval framework demo)
- Document patterns as you go
- Don't try to learn everything — focus on high-priority first
- Leverage your existing agent/prompt work as test subjects

## Success Criteria
- [ ] Can explain 3 ways to validate an AI output
- [ ] Have built or used at least one eval framework (promptfoo minimum)
- [ ] Can write a simple test case for a prompt
- [ ] Understand the gap between traditional QA and AI QA
- [ ] Have one small project or test harness as proof of concept
- [ ] Can identify when to use automated vs. human evaluation

## Key Insights (To Discover)
- How LLM non-determinism affects testing (temperature, randomness)
- Why traditional QA practices don't translate 1:1 to AI
- Cost implications of running large eval suites
- The importance of test case design in AI QA
