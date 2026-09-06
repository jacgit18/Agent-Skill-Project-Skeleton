# Task 6 Report: Plan Full-Stack Project #2

**Status:** DONE

## Summary

Task 6 has been completed. A comprehensive plan for Project 2 has been created, a decision to build a new project (Option A) has been made using the decision framework, and the working log template is ready. The decision centers on **building a complementary, AI-specific project** rather than deepening Project 1.

## Decision: Build New Project #2 (Option A)

### Decision Framework Analysis

Using the criteria from the brief:

**1. Confidence/Anxiety:**
- New project shows adaptability and demonstrates learning across different technical domains
- After completing a system design practice (distributed systems, Kafka), taking on a new problem space builds confidence in problem-solving broadly
- Score: New project provides better confidence signal for interviews

**2. Interview Relevance:**
- **Two projects** tell richer stories than one deepened project
- Project 1 (full-stack + Claude API optimization + multi-user isolation) + Project 2 (agent orchestration + tool use + structured outputs) cover complementary AI engineering patterns
- Hiring managers see breadth: "They understand both simple classification patterns and complex multi-step reasoning"
- Score: New project shows more versatility and depth in Claude ecosystem knowledge

**3. Job Marketability:**
- For AI engineering roles (apparent portfolio goal), showing multiple Claude integration patterns is valuable
- Project 1: simple classification, cost/latency optimization, batch processing
- Project 2: agents, tool use, structured outputs, real-time coordination
- Most AI engineering roles want to see both "I can optimize a simple task at scale" AND "I can orchestrate complex reasoning"
- Score: New project significantly improves marketability for target roles

**4. Interest/Sustainability:**
- A focused 4-6 week build on a new system (agents, orchestration, RAG) provides psychological momentum and novelty
- Deepening Project 1 risks becoming maintenance work rather than learning
- Multi-agent research is more exciting as a learning domain than adding features to existing finance app
- Score: New project is more sustainable and intellectually engaging

**Conclusion:** Option A (new project) is strongly recommended.

## Project Chosen: Multi-Agent Research Assistant

### Why This Project

**Complementary to Project 1:**
- Project 1 teaches: monolithic full-stack architecture, simple Claude classification at scale, cost/latency optimization, multi-user isolation
- Project 2 teaches: **multi-agent orchestration**, **tool use**, **structured outputs**, **information coordination**, **graceful degradation**
- P1 is about "classify many things efficiently"; P2 is about "coordinate multiple reasoning steps reliably"
- Different enough to demonstrate versatility; similar enough to build on Claude expertise

**Claude-Specific Patterns:**
- Project 2 showcases agents, function calling, structured outputs, model-tier selection for different reasoning tasks
- Directly relevant for Anthropic ecosystem and AI engineering roles
- Builds on P1's foundation without just repeating the same patterns

**Clear Technical Challenges:**
1. Agent coordination without duplication (structured JSON handoff, central result store)
2. Tool reliability and graceful degradation (error handling, partial failures)
3. Prompt engineering for distinct agent roles (avoiding chaos vs. over-specification)

**Strong Interview Story:**
"I built a multi-agent research system that orchestrates specialized Claude instances. The main challenge was preventing duplicate work and coordinating context across multiple agents. I solved it using structured JSON schemas and a central result store; each agent queries what's already been found before making tool calls. I also had to handle tool failures gracefully — web search can fail, but the pipeline keeps going. What I learned: scaling AI reasoning requires thinking about agent roles, information flow, and failure modes, not just calling Claude more."

## Deliverables

### 1. PROJECT-2-plan.md
- **Path:** `/home/jac/AI/Agents/PromptingAgent/projects/PROJECT-2-plan.md`
- **Status:** Created and committed
- **Contents:**
  - Goal: AI research orchestration system with multiple agents (researcher, analyst, synthesizer)
  - High-level architecture: 3-agent pipeline with web search + vector retrieval tools, central result store (Postgres), real-time frontend updates
  - Technical decisions table covering: agent coordination strategy (sequential with branching), tools (web search + pgvector), Claude model tiers (Haiku/Sonnet/Opus), structured outputs (JSON schemas), real-time updates (WebSocket + polling fallback), error handling (graceful degradation), caching (prompt cache on system prompts), deployment (Render + Vercel)
  - Three non-trivial challenges with approaches:
    1. Agent orchestration and context management (prevent duplication via structured handoff)
    2. Tool reliability and graceful degradation (error handling, partial failures)
    3. Prompt engineering for distinct roles (clear role definitions, few-shot examples, iterative tuning)
  - Success criteria: deployment, core features, agent handoff, error handling, clean code, architecture explanation
  - 5-6 week timeline (slightly longer than typical due to multi-agent complexity)
  - Draft interview story emphasizing orchestration patterns and model-tier selection

### 2. PROJECT-2-log.md
- **Path:** `/home/jac/AI/Agents/PromptingAgent/projects/PROJECT-2-log.md`
- **Status:** Template ready (empty, to be filled during build phase)
- **Structure:** Consistent with PROJECT-1-log.md format

### 3. Git Commit
- **Commit Hash:** c9ec356
- **Message:** "doc: project 2 plan and architecture — multi-agent research assistant"
- **Files Changed:** 1 file modified (PROJECT-2-plan.md)

## Success Criteria Assessment

- ✅ Decision made (new project chosen; reasoning documented using decision framework)
- ✅ PROJECT-2-plan.md exists with required sections: goal, architecture, technical decisions, challenges, success criteria, timeline, interview story
- ✅ Architecture emphasizes different patterns from Project 1 (agent orchestration vs. monolithic, tool use vs. simple classification, complex coordination vs. simple batch processing)
- ✅ Non-trivial challenges identified with clear approaches (structured handoff prevents duplication, error handling enables graceful degradation, prompt engineering tunes agent roles)
- ✅ Success criteria and timeline clear (5-6 weeks with optional compression, deployment + core features + agent handoff + error handling + tests)
- ✅ Interview story drafted, grounded in concrete technical trade-offs (agent coordination, tool reliability, model selection)
- ✅ Commit created to main branch

## Design Highlights

### Architecture Intentionality
- **Sequential agent pipeline with central coordination:** Avoids complexity of fully parallel agents while preventing duplication. Researcher finds facts, analyst vets them, synthesizer writes narrative. Each agent reads prior results before acting.
- **Structured JSON schemas for agent outputs:** Ensures predictable handoff between agents; downstream agents can validate and parse cleanly; frontend knows what to expect.
- **Model tier selection (Haiku/Sonnet/Opus):** Researcher does high-volume tool coordination (Haiku), analyst does mid-tier reasoning (Sonnet), synthesizer does deep reasoning (Opus). Matches cost to task.
- **Tool failures don't crash pipeline:** Web search can fail, vector retrieval can return empty — agents adapt and report limitations. Production-ready resilience.

### Project Scope Justification
- **5-6 weeks (not 8 like Project 1):** Smaller, more focused. Single feature area (research orchestration) vs. full-stack app (finance dashboard).
- **Compression possible:** If weeks 1-5 are tight, can scope to 2 agents (researcher + synthesizer, skip analyst) or single tool (web search only, skip vector DB).
- **Teaches different patterns:** Not just "another full-stack app," but specifically "how do you coordinate multiple AI reasoning steps?"

## Why Not Other Options

**Collaborative Code Editor (CRDT-based real-time editor):**
- Strong distributed systems project, but doesn't use Claude at all
- Less relevant for AI engineering portfolio; more for systems engineers
- Doesn't build on Project 1's Claude expertise
- Would waste opportunity to deepen AI-specific knowledge

**Deepen Project 1:**
- Valid option, but less compelling for portfolio breadth
- "Version 2 of the same app" is weaker interview story than "two different projects"
- After planning Project 1, best to move on and show versatility

**Simple RAG/Document Q&A (DevDocs-style):**
- Tempting (focused RAG scope), but less ambitious than multi-agent coordination
- Would show retrieval patterns but not orchestration/tool-use patterns
- Multi-agent research teaches RAG + coordination, strictly superset

## Next Steps (for user post-review)

1. **If this plan is approved:** Start build phase during weeks 5-12, using the same cadence as Project 1 — scaffold first, test each component (researcher agent, then analyst, then synthesizer), integrate incrementally.
2. **Build strategy:**
   - Week 1: FastAPI setup, Postgres schema (queries, results, logs), mocked Claude calls
   - Week 2: Researcher agent with real web search tool integration
   - Week 3: Analyst and synthesizer agents
   - Week 4: Frontend and real-time coordination
   - Week 5: Integration, edge cases, error handling
3. **During build:** Log problems/solutions in PROJECT-2-log.md per brief; use problem-solving gates when stuck.
4. **Upon shipping:** Add "Final Interview Story" section to PROJECT-2-plan.md documenting what actually happened (unexpected challenges, shortcuts, learnings).

## Notes

- This plan is planning-only; actual building comes after review and approval.
- The decision framework clearly favored a new project, and the multi-agent research assistant is the most complementary and relevant choice for the user's portfolio goals (AI engineering, Anthropic ecosystem).
- No external dependencies or blockers; plan is self-contained and ready to build.
- If during build the scope feels too large, the timeline includes optional shortcuts (fewer agents, fewer tools).
