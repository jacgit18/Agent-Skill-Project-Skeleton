# Phase 2 Design: AI-Powered Learning Portfolio — Interleaved Learning Loop

**Date:** August 30, 2026  
**Timeline:** August 2026 → May 2027 (9 months)  
**Primary Deliverable:** Production financial dashboard + 4 learning projects + DevHiveMind integration  
**Success Criteria:** Confident in production AI development; unique, coherent portfolio narrative; job-ready by May 2027

---

## Executive Summary

Phase 2 shifts from *foundational skill-building* (Phase 1: foundation skills, project plans, AI QA exploration) to *integrated production development*. You'll practice AI-assisted development through a deliberate 9-month progression:

- Build 4 focused learning projects (console chatbot → structured output → tool-calling → RAG)
- Integrate each immediately into a real fullstack application (financial dashboard)
- Use your Obsidian vault (DevHiveMind) as RAG ground truth
- End with a polished portfolio piece + demonstrated mastery of production AI patterns

**Key insight:** Small wins + real failures → deep learning + confidence.

---

## Context & Constraints

**From Phase 1:**
- Foundation skills available: problem-solving gate, system design agent, decision-making agent
- Project plans drafted: personal finance dashboard, collaborative code editor
- AI QA testing exploration completed

**For Phase 2:**
- Timeline: Hard deadline May 2027 (job search readiness)
- Priorities: Confidence, unique narrative, marketability
- Approach: Practice full-cycle AI development (planning → execution, not AI replacing core logic)
- Existing assets: Obsidian vault (technical notes, psychology reading, tech articles) ready for RAG

---

## Why Approach C: Interleaved Learning Loop

Three approaches were considered:

| Approach | Timeline | Narrative | Tradeoff |
|----------|----------|-----------|----------|
| **A: 5-Project Sequence** | Projects 1-5 (6 mo), then old project (3 mo) | "I built a learning progression then unified it" | Slower to portfolio piece; 5 projects may feel scattered |
| **B: Old Project + Parallel** | Old project (start immediately) + 2-3 learning projects | "I rebuilt my legacy app with modern AI" | Fast to portfolio; but juggling context |
| **C: Interleaved (Chosen)** | Alternate: foundation → learning → integrate → repeat | "I built a process for production AI" | Maximum small wins; old project evolves with skills |

**Why C:** Builds momentum through monthly wins. Each learning project directly improves the dashboard. Failures in experiments → iteration in production. By May, you have both breadth (four patterns) and depth (a polished fullstack app).

---

## Detailed Timeline & Projects

### Month 1: Financial Dashboard Foundation (Aug-Sep 2026)

**Focus:** Architecture, schema design, API setup  
**What you'll build:**
- Schema: `User`, `Expense`, `Category`, `Insight` models
- FastAPI app with SQLAlchemy ORM
- Auth (session-based or JWT)
- CRUD endpoints for expenses
- Planning & decision-making using AI agents

**Deliverable:** Working FastAPI backend with expense management API  
**Time:** 3-4 weeks coding + planning  
**AI Integration:** Use problem-solving gate (schema design), decision-making agent (framework choice, auth strategy)

**Integration Point (for Month 3):** Chat interface endpoint will be added here

---

### Month 2: Console Chatbot Project (Sep-Oct 2026)

**Focus:** Claude API fundamentals, streaming, conversation management  
**What you'll build:**
- Persistent CLI chatbot with Claude
- Streaming responses
- Conversation history (JSON or SQLite)
- Prompt design iteration

**Deliverable:** Standalone working chatbot repo; demonstrated mastery of Claude API patterns  
**Time:** 2-3 weeks  
**What it teaches:**
- Claude API (streaming, token management)
- Prompt engineering (clarity, context, constraints)
- Conversation state management
- Error handling (API failures, timeouts)

**Integration Point (for Month 3):** This becomes a WebSocket endpoint in the dashboard

---

### Month 3: Chat Integration into Dashboard (Oct-Nov 2026)

**Focus:** Production integration, grounding AI in user data  
**What you'll add to the dashboard:**
- WebSocket endpoint for real-time chat
- Chat tied to user's expense data
- Prompts grounded in user context ("You spent $X on groceries this month")
- Example queries: "What did I spend on groceries?", "Should I be worried about my spending?"

**Deliverable:** Dashboard can chat about user's finances  
**Time:** 2-3 weeks  
**What it teaches:**
- Grounding Claude's responses in actual data
- Prompt engineering for domain-specific context
- Real production issues (latency, error handling, user feedback)

**Key Learning:** AI doesn't work in isolation—it needs data, validation, and context.

---

### Month 4: Structured Output Project (Nov-Dec 2026)

**Focus:** Reliable structured outputs, validation, schema design  
**What you'll build:**
- Expense categorizer: user provides description → Claude categorizes reliably
- Use Pydantic models for validation
- Learn Claude's structured output mode
- Build tests for validation edge cases

**Deliverable:** Standalone categorizer repo; demonstrated mastery of structured outputs  
**Time:** 2-3 weeks  
**What it teaches:**
- Pydantic schema design
- JSON schema generation
- Claude's structured output mode
- Validation patterns
- Testing AI output

**Integration Point (for Month 6):** Dashboard expense categorization will use this pattern

---

### Month 5: Tool-Calling Project (Dec-Jan 2027)

**Focus:** Function calls, file operations, safety, error handling  
**What you'll build:**
- CLI tool where Claude can call functions:
  - `read_file(path)` → read file contents
  - `write_file(path, content)` → write file
  - `list_directory(path)` → list files
  - `run_command(cmd)` → execute shell commands (with restrictions)
- Error handling, permissions, safety guardrails
- Edge cases (permission denied, file not found, command failure)

**Deliverable:** Standalone tool-calling project repo; demonstrated mastery of safe execution  
**Time:** 2-3 weeks  
**What it teaches:**
- Tool definitions and schemas
- Function calling patterns
- Safety guardrails (what Claude can and can't do)
- Error handling in production
- Permission management

**Integration Point (for Month 6):** Dashboard file import/export uses this pattern

---

### Month 6: Tool-Calling Integration into Dashboard (Jan-Feb 2027)

**Focus:** Multi-step operations, file handling, safe automation  
**What you'll add to the dashboard:**
- CSV upload: Claude parses file → validates → imports expenses
- Export reports: Claude generates formatted reports → exports as PDF/CSV
- Multi-step workflows: validate → categorize → insert → report

**Deliverable:** Dashboard can ingest/export data via AI-powered operations  
**Time:** 2-3 weeks  
**What it teaches:**
- Composing multiple tool calls
- Handling partial failures
- User feedback on long operations
- Real-world file handling edge cases

**Key Learning:** Tool-calling is powerful but requires careful orchestration and error handling.

---

### Month 7: RAG Project (Feb-Mar 2027)

**Focus:** Embeddings, vector DB, semantic search, RAG architecture  
**What you'll build:**
- Embed your Obsidian vault (DevHiveMind):
  - Technical notes (system design, architecture patterns)
  - Psychology reading (decision-making, behavioral economics)
  - Tech articles (AI, personal finance, best practices)
- Vector DB (pgvector or similar)
- Semantic chunking strategy
- Retrieval + prompt augmentation
- Query interface (CLI or web)

**Deliverable:** Working RAG system querying DevHiveMind; production-ready retrieval pipeline  
**Time:** 3-4 weeks  
**What it teaches:**
- Embeddings (OpenAI, Anthropic, local)
- Vector DB operations
- Chunking strategy (affects retrieval quality)
- Retrieval-augmented prompting
- Handling irrelevant results
- RAG debugging (why didn't it find the right context?)

**Integration Point (for Months 8-9):** Dashboard insights powered by DevHiveMind

---

### Months 8-9: RAG Integration + Polish (Mar-May 2027)

**Focus:** Production RAG, full integration, deployment, interview prep  
**What you'll add to the dashboard:**
- Insight generation powered by DevHiveMind:
  - "Based on your psychology reading, here's why you might be overspending"
  - "Your notes on financial best practices suggest you should automate savings"
  - Contextual recommendations using your own knowledge

**Deliverable:**
- Production-ready financial dashboard (deployed)
- Full end-to-end AI integration (chat → categorization → tool-calling → RAG)
- Portfolio materials (demo, docs, case studies)

**Time:** 5-6 weeks (feature completion + polish + deployment)

**What it teaches:**
- Production RAG (quality matters; garbage in, garbage out)
- Iteration on retrieval quality
- User-facing AI (handling wrong answers gracefully)
- DevOps (deployment, monitoring)
- Communication (writing about your work)

**Additional Work (parallel):**
- Write 2-3 case studies or blog posts
- Record demo video of dashboard (5-10 min)
- Prepare interview narratives
- Clean up commit history on all repos

---

## Integration Strategy

### Pattern Across All Integrations

Each integration follows the same workflow:

1. **Prototype (learning project):** Build the pattern in isolation
2. **Design:** How does this fit into the dashboard? What data? What prompts? (use decision-making agent)
3. **Implement:** Add the feature; *you* write the glue logic
4. **Iterate:** Test edge cases, handle failures, refine prompts
5. **Reflect:** What worked? What's the mental model for production AI?

### Data Flow

```
User Input (web UI) 
  ↓
[FastAPI endpoint with Claude]
  ↓
Claude (with access to: expense data, tool calls, DevHiveMind via RAG)
  ↓
Response (chat, categorized expense, file operation, insight)
  ↓
Update database / File output
```

### Where Claude Fits

| Feature | Claude Role | Data Grounding | Tools |
|---------|-------------|-----------------|-------|
| Chat queries | Answer questions about expenses | User's expense data | None |
| Categorization | Categorize new expenses reliably | Category list + guidelines | Structured output |
| Insights | Generate personalized insights | Expense trends + DevHiveMind context | RAG retrieval |
| File operations | Parse CSVs, generate reports | User data, formatting rules | File I/O, subprocess |

---

## Skill Development Arc

### Tier 1: Foundations (Months 1-3)
**What you learn:** Claude API, prompt design, production integration patterns

- Claude API (streaming, conversation management)
- Domain-specific prompt engineering
- Grounding responses in user data
- Production integration (WebSocket, error handling)

**Mental model:** Claude isn't a black box—responses depend entirely on data, prompts, and context.

**By end of Month 3:** You can build a conversational interface powered by Claude and integrate it into a real app.

---

### Tier 2: Reliability & Control (Months 4-6)
**What you learn:** Structured outputs, tool-calling, safety, error handling

- Structured output validation (Pydantic, JSON schemas)
- Tool definitions and safe execution
- Multi-step workflows and state management
- Edge case handling

**Mental model:** Production AI requires validation, safety guardrails, and graceful failure handling.

**By end of Month 6:** You can make Claude produce reliable structured data and safely execute operations in a real application.

---

### Tier 3: Knowledge & Scale (Months 7-9)
**What you learn:** RAG, retrieval quality, end-to-end production AI

- Embeddings and vector DBs
- Semantic chunking and retrieval
- Prompt augmentation with retrieved context
- Debugging retrieval quality

**Mental model:** RAG is a workflow (retrieve → augment prompt → generate), not a feature. Quality depends on all three steps.

**By end of May:** You can architect and implement production AI systems with breadth (multiple patterns) and depth (real application).

---

## Interview Narrative

### The Story You Tell

*"I didn't just learn AI development—I built a process for it. I took four foundational AI patterns (chat, structured output, tool-calling, RAG) and deliberately integrated them into a real financial application. Each pattern taught me something about production AI: grounding, validation, safety, scale. By the end, I had both the breadth and depth to speak credibly about building AI systems."*

### Key Interview Angles

**"Tell me about a time you debugged a hard problem"**
→ Month 4-6: "I built a structured output system that kept hallucinating. I learned to validate rigorously, iterate on prompts, and test edge cases. That's when I realized production AI isn't about the latest model—it's about the details."

**"How do you approach system design with AI?"**
→ Month 1: "I designed the financial dashboard schema specifically to ground Claude's responses in actual user data. That grounding is crucial—without it, Claude can't reason effectively about your finances."

**"What's your approach to testing AI systems?"**
→ Month 6: "I built a test suite for tool-calling to ensure Claude could safely import/export files without data loss. Testing AI is different—you test both correctness and robustness."

**"How would you integrate AI into [some product]?"**
→ You have four proven patterns to draw from; you can speak to tradeoffs and real production lessons.

### Unique Positioning

- ❌ Not: "I built 4 unrelated projects" (scattered)
- ❌ Not: "I built one app with AI sprinkled in" (shallow)
- ✅ But: "I systematically integrated AI patterns into one production app, learning from each integration" (coherent + credible)

---

## Portfolio Deliverables

### By May 2027, You Ship:

#### 1. Live Financial Dashboard (Primary Piece)
- **Tech Stack:** FastAPI, SQLAlchemy, Psycopg2/SQLite, Claude API
- **Features:**
  - User authentication
  - Expense tracking + AI categorization
  - Chat interface for queries
  - Insights powered by DevHiveMind
  - File import/export via Claude
- **Deployed:** Live URL (Render, Railway, or self-hosted)
- **Supporting materials:**
  - GitHub repo with clear README
  - Demo video (5-10 min walkthrough)
  - Architecture diagram
  - API documentation

#### 2. Four Learning Project Repos (Secondary Pieces)

**Console Chatbot**
- GitHub repo: clean structure, good commit history
- README explaining Claude API patterns
- Example usage and key learnings

**Structured Output Project**
- GitHub repo with Pydantic schemas
- Examples of validation edge cases
- Testing strategy documented

**Tool-Calling Project**
- GitHub repo with tool definitions
- Safety considerations documented
- Error handling examples

**RAG Project (DevHiveMind)**
- GitHub repo with retrieval pipeline
- Embedding strategy documented
- Example queries and results

#### 3. DevHiveMind Integration (Unique Differentiator)
- Obsidian vault organized for RAG (folders: technical, psychology, articles)
- Documented chunking strategy
- Example insights generated by dashboard

#### 4. Interview Materials
- 2-3 blog posts / case studies:
  - "How I Built a Production AI Chatbot" (Month 3)
  - "Reliable AI Output: Lessons from Building a Categorizer" (Month 6)
  - "RAG in Practice: Integrating My Knowledge Vault" (Month 9)
- Demo video
- GitHub repos with good commit history (shows iterative development)

---

## Success Criteria

✅ **By May 2027:**

1. **Confidence:** "I can build production AI systems end-to-end"
2. **Portfolio:** Live financial dashboard + 4 learning projects
3. **Breadth:** Demonstrated mastery of chat, structured output, tool-calling, RAG
4. **Depth:** Real financial app, not toy project
5. **Narrative:** Coherent story about production AI development
6. **Interview-Ready:** Can speak credibly to AI patterns, tradeoffs, production lessons
7. **Marketability:** Clear positioning for AI-backend or full-stack roles

---

## Risks & Mitigation

| Risk | Mitigation |
|------|-----------|
| Projects slip; can't finish RAG by May | Prioritize: dashboard + 3 projects (chat, structured output, tool-calling) are core. RAG is nice-to-have. |
| Learning project doesn't integrate smoothly | Build with integration in mind (e.g., chatbot as module, not monolith). Test integration early. |
| RAG retrieval quality is poor | Start RAG work early (Month 7). Iterate on chunking and prompting. Document strategy. |
| Dashboard scope creeps | MVP is expense categorization + chat. File operations and insights are Phase 2. |
| Burnout from 9-month push | Build in iteration cycles (learn → integrate → reflect). Celebrate wins monthly. |

---

## How AI Fits Into This Phase

**For Planning & Architecture:**
- Problem-solving gate skill (rubber duck schema design, options for tech choices)
- System design agent (design reviews, tradeoff discussions)
- Decision-making agent (prioritization, what to build first)

**For Execution:**
- Claude for brainstorming feature ideas, debugging hard problems
- Claude for prompt design iteration
- Claude for code review of your integrations

**What Claude Doesn't Do:**
- Replace your hands-on coding
- Make project decisions for you
- Debug your code without you understanding it

**What You Do:**
- Design schemas and APIs
- Write core business logic
- Integrate Claude features
- Test edge cases
- Iterate on prompts

---

## Timeline Summary

| Phase | Months | Work | Outcome |
|-------|--------|------|---------|
| **Foundation** | 1 | Dashboard schema + FastAPI | Working backend |
| **Chat** | 2-3 | Chatbot project + integration | Dashboard can chat |
| **Structure** | 4 | Structured output project | Reliable categorization |
| **Tools** | 5-6 | Tool-calling project + integration | File import/export |
| **RAG** | 7-9 | RAG project + integration + polish | Production dashboard + portfolio |

---

## Next Steps (After Design Approval)

1. ✅ This design is approved
2. → Invoke `writing-plans` skill to create detailed implementation plan (Month 1 breakdown, dependencies, testing strategy)
3. → Begin Month 1 work: financial dashboard foundation

---

## Appendix: DevHiveMind Organization

Your Obsidian vault should be organized for RAG:

```
DevHiveMind/
├── Technical/
│   ├── System Design/
│   ├── Architecture/
│   ├── API Design/
│   ├── Database/
│   └── Tools & Frameworks/
├── Psychology/
│   ├── Behavioral Economics/
│   ├── Decision-Making/
│   ├── Cognitive Biases/
│   └── Habits & Motivation/
├── Articles/
│   ├── Personal Finance/
│   ├── AI & LLMs/
│   └── Best Practices/
└── Insights/
    ├── Monthly Reflections/
    └── Lessons Learned/
```

Each note should be:
- Substantial enough to chunk (~500-1000 words)
- Self-contained (understandable without reading others)
- Tagged for retrieval (e.g., `#decision-making`, `#finance`)
- Dated and sourced

This makes RAG retrieval high-quality (relevant context, not noise).

---

**Document Status:** Ready for review  
**Next Gate:** User approval → invoke writing-plans skill → implementation

