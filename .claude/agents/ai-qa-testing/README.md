# AI QA Testing Learning Path

An exploration of AI testing fundamentals as an alternative career path, with focus on practical patterns and tools.

**Status:** Learning/exploration phase. This directory documents foundational patterns and includes proof-of-concept implementations.

## Contents

### 1. Learning Plan
**File:** `LEARNING-PLAN.md`
- Structured learning priorities (high/medium priority topics)
- Resources and learning approach
- Success criteria for competency

**Key Topics:**
- Prompt validation (consistency testing)
- Output validation (format, semantic, human-in-the-loop)
- Safety & bias testing (adversarial inputs)
- Automated eval frameworks (promptfoo, Braintrust)

### 2. Pattern Documentation
**File:** `notes.md`
- Detailed exploration of 6 core patterns
- What each pattern does, when to use it, examples
- Tools for implementation
- Tradeoffs and practical considerations

**Patterns Covered:**
1. Consistency Testing - Multiple runs, variance measurement
2. Format Validation - JSON schema, regex, structure checking
3. Semantic Validation - Human-in-the-loop, LLM-as-judge
4. Adversarial Testing - Edge cases, safety, robustness
5. Regression Testing - Change detection, baseline comparison
6. Similarity-Based Validation - Embedding-based scoring

### 3. Proof-of-Concept Tools

#### `prompt_consistency_tester.py`
A working implementation of Pattern 1: Consistency Testing.

**What it does:**
- Runs a prompt multiple times with same input
- Measures string similarity and semantic similarity
- Reports consistency metrics (avg, min, max)
- Uses Claude Haiku for efficiency

**Key Features:**
- String similarity via Python's difflib
- Semantic similarity via LLM evaluation (Claude)
- Temperature control for testing determinism
- Sample output preview in results

**Usage:**
```python
python prompt_consistency_tester.py

# Or programmatically:
from prompt_consistency_tester import run_prompt_consistency_test

results = run_prompt_consistency_test(
    prompt="Summarize this in one sentence: {input}",
    test_input="Some text to summarize",
    num_runs=5,
    temperature=0.5
)
```

**Example Output:**
```
String Similarity: 85.2% (avg)
Semantic Similarity: 92.1% (avg)
```

#### `format_validator.py`
A working implementation of Pattern 2: Format Validation.

**What it does:**
- Validates JSON structure and required fields
- Regex pattern matching
- Length constraints
- Keyword presence
- Custom validation functions
- Multi-validator suites

**Key Features:**
- Built-in validators for common cases
- Composable validation suite
- Detailed error messages with context
- Type checking for JSON schema

**Usage:**
```python
from format_validator import FormatValidator, ValidationSuite

# Simple JSON validation
result = FormatValidator.validate_json(
    output='{"name": "Alice", "age": 30}',
    required_fields=["name", "age"]
)

# Multi-validator suite
suite = (
    ValidationSuite()
    .add_json_validation(required_fields=["role", "experience"])
    .add_keywords_validation(["Python", "engineer"])
    .add_length_validation(min_length=20)
)
passed, results = suite.run(llm_output)
```

### 4. Quick Start

#### Option A: Understand the Patterns
1. Read `LEARNING-PLAN.md` for overview
2. Read `notes.md` for deep dives into each pattern
3. Study the pattern tradeoffs and use cases

#### Option B: Run the Tools
```bash
# Install dependencies
pip install anthropic

# Test prompt consistency
python prompt_consistency_tester.py

# Validate formats
python -c "from format_validator import FormatValidator; \
result = FormatValidator.validate_json('{\"name\": \"test\"}'); \
print(result.message)"
```

#### Option C: Extend for Your Agents
Use these patterns to test your existing agents/prompts:
1. Add consistency checks to catch regression
2. Validate structured outputs with format validator
3. Build a simple eval suite for your agents

### 5. Key Learnings

#### AI QA vs Traditional QA
| Aspect | Traditional QA | AI QA |
|--------|---|---|
| **Determinism** | Expected (bugs are failures) | Probabilistic (variance is normal) |
| **Correctness** | Pass/Fail | Spectrum (graded) |
| **Cost** | Per test is cheap | Per API call costs money |
| **Automation** | High (most things can be automated) | Medium (human judgment needed) |
| **Testing focus** | Code behavior | Prompt/model behavior + output quality |

#### Critical Success Factors
1. **Baseline establishment** - Know what "good" looks like before testing
2. **Cost awareness** - Each eval costs money; balance coverage vs. expense
3. **Multi-layered testing** - Combine fast (format) with thorough (human) checks
4. **Versioning** - Track prompt changes like code changes
5. **Regression detection** - Catch unintended changes to prompt behavior

### 6. Next Steps (Medium Priority)

After solidifying high-priority patterns, explore:
- [ ] Agent behavior testing (orchestration, routing, state)
- [ ] Performance testing (tokens, latency, cost at scale)
- [ ] Regression testing automation (CI/CD for prompts)
- [ ] Eval framework deep-dive (promptfoo, Braintrust setup)
- [ ] Building a test harness for your agents

### 7. Resources

**Tools:**
- [promptfoo](https://github.com/promptfoo/promptfoo) - Eval framework (start here)
- [Braintrust](https://braintrust.dev) - Advanced evaluation platform
- [LangSmith](https://smith.langchain.com) - LLM observability

**Concepts:**
- LLM evaluation frameworks and patterns
- Prompt engineering + testing integration
- Quality metrics for non-deterministic systems

**Learning:**
- Papers: "Towards a Unified Framework for AI Testing"
- OpenAI Cookbook: evaluation examples
- DeepLearning.AI: evals courses

## Summary

This learning path explores AI QA testing as a foundational alternative career track. By understanding prompt validation, output validation, safety testing, and eval frameworks, you build skills that apply across AI development.

The tools here demonstrate practical implementation of core patterns. As you build agents and prompts, these patterns directly apply to verifying reliability and quality.

**Main takeaway:** AI QA isn't about finding bugs; it's about measuring and improving the quality of probabilistic systems.
