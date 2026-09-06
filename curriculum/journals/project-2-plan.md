# Project 2: Multi-Agent Research Assistant

## Goal
Build an AI research orchestration system where users submit complex research queries and multiple specialized Claude agents work together (researcher, analyst, synthesizer) with access to tools (web search, document retrieval) to produce comprehensive, sourced insights with structured reasoning chains.

## Architecture

### High-Level

The system accepts user research queries (e.g., "What are emerging risks in AI chip manufacturing?") and orchestrates three specialized Claude agents to systematically explore the topic. The **researcher agent** uses web search and document retrieval tools to gather facts and sources; the **analyst agent** synthesizes and critiques the research, identifying gaps and confidence levels; the **synthesizer agent** composes a final narrative report with structured findings, sources, and reasoning.

Agents communicate through a central **result store** (Postgres) where each writes findings as structured JSON. A coordination layer routes queries through the pipeline, surfaces intermediate results to the user, and handles failures gracefully. The frontend displays the research workflow in real-time (which agent is active, what tools they're calling, partial results as they emerge) and the final structured report.

Key constraints: agents should not duplicate work (researcher doesn't re-fetch what analyst already found); calls should be idempotent (re-running a query produces the same result); tool calls should be reliable (graceful fallbacks if web search or retrieval fails); cost should be manageable (caching, model tier selection, rate limiting).

### Technical Decisions

| Decision | Choice | Why | Alternative |
|---|---|---|---|
| Agent coordination | Sequential with branching (researcher → analyst → synthesizer, with optional parallel researcher branches) | Simple, deterministic control flow; easy to debug; clear handoff points. Parallel agents would be faster but harder to coordinate information flow without duplication. | Fully parallel agents with voting/consensus (more complex, less clear who owns which facts) |
| Tools/integrations | Web search API (e.g., Google Custom Search or SerpAPI) + vector search over ingested documents (Supabase pgvector or Pinecone) | Web search for current/published info; vector search for company/domain-specific docs (filings, reports, internal docs if available). | Just web search (shallow, public-only info) or just retrieval (limited to pre-indexed docs) |
| Claude models | Haiku 4.5 for researcher (cheap, good retrieval feedback), Sonnet 5 for analyst (mid-tier reasoning), Opus 5 for synthesizer (deep reasoning for final narrative). Model selection justifies cost and matches task complexity. | Researcher does high-volume tool-calling and summarization (Haiku sufficient). Analyst does reasoning/critique (Sonnet). Synthesizer produces high-quality output (Opus). | Using one model tier (e.g., Sonnet for all) — simpler code, higher cost, no benefit to e.g. researcher using Opus when Haiku is cheaper and just as good at tool feedback. |
| Structured outputs | JSON schema for each agent's output: researcher = `{facts: [], sources: [], gaps: []}`, analyst = `{critiques: [], confidence_by_fact: {}, next_searches: []}`, synthesizer = `{narrative: string, key_findings: [], limitations: [], sources_cited: []}`. Model uses `json_mode` or structured outputs. | Predictable, machine-readable output; makes it easy for downstream processing, frontend rendering, and agent handoff. | Free-text output (harder to parse, inconsistent structure, frontend doesn't know what to expect) |
| Real-time updates | WebSocket connection to frontend; backend sends agent progress events (agent_started, tool_called, tool_result, agent_done) as they happen. Also polling fallback for reliability. | User sees research happening (transparency, trust); can cancel if query is going wrong. Matches modern UX expectations. | Batch output only (user sees nothing until done — frustrating for long-running queries). |
| Error handling & fallbacks | Tool failures (web search 404, retrieval returns no results) logged but don't block pipeline. Researcher re-frames as "no public sources found" for analyst. If analyst fails, synthesizer works with researcher findings only. | Research is incomplete by nature; graceful degradation is better than hard failures. If one agent can't complete, the pipeline continues with available info. | Hard fail on any tool error (causes entire query to fail; frustrating). |
| Caching | Prompt cache on stable researcher/analyst/synthesizer system prompts (role definitions, reasoning instructions). Re-use cached prompts across queries. Do NOT cache on tool outputs (they're query-specific). | System prompts are stable and expensive (long role descriptions, few-shot examples); caching them 5-10 queries = ~50% savings on prompt tokens. | No caching (higher cost per query). Caching tool outputs (wrong — each query is different, defeats the purpose). |
| Deployment | Backend: FastAPI on Render (managed Postgres + pgvector, Redis for job tracking). Frontend: React on Vercel. External APIs: web search (SerpAPI with free tier or Bing/Google API), vector DB via Supabase pgvector. | Render + Vercel = simple GitHub-based CI/CD, no ops burden. Supabase pgvector = managed vector DB without separate vendor lock-in. | Self-hosted everything (more control, higher ops burden than justified for a portfolio project). |

### Non-Trivial Challenges

1. **Agent orchestration and context management** — Multiple agents need to share findings without duplicating work (e.g., researcher shouldn't re-fetch a source analyst already critiqued; synthesizer shouldn't re-reason facts that analyst already vetted). If context is too short, agents miss information; if too long, cost explodes and they get confused by irrelevant details. Approach: structured JSON handoff between agents with explicit "available facts" section each downstream agent reads first; a result store (Postgres JSON columns) that each agent queries before making tool calls; optional caching of intermediate results so re-running queries doesn't re-process facts. Test by running the same query twice and ensuring the second run is faster/cheaper.

2. **Tool reliability and graceful degradation** — Web search API might be down (503), return irrelevant results, or rate-limit the query. Vector search might have no matching documents in the DB (cold start). Neither should crash the pipeline. Instead, agent should adapt ("no public sources found" or "internal docs don't cover this angle, relying on web research"). Approach: wrap all tool calls in try/catch; return structured "tool_failed" result rather than raising; analyst agent explicitly checks tool result quality and reports confidence; synthesizer notes limitations in final output. Test by mocking tool failures (e.g., simulating web search returning 0 results) and verifying pipeline completes.

3. **Prompt engineering for distinct agent roles** — Each agent needs a clear, narrow role so they specialize and don't duplicate work. But roles must be defined enough that agents know what to do with tool results and what questions to ask. Too vague ("research this topic") = chaos; too rigid ("call exactly these tools in this order") = no flexibility. Approach: start with clear role definitions in system prompts (researcher = "find facts and sources", analyst = "critique and identify gaps", synthesizer = "weave into narrative"); use few-shot examples showing successful handoffs between agents; iterate based on query results (log queries where agents duplicated work or missed obvious next steps); consider a "query planner" micro-agent that reads the user's query and routes to the right combination of agents (e.g., a financial question might skip synthesizer and go straight to analyst output). Test by comparing agent outputs across multiple queries and manually checking for duplication and gaps.

## Success Criteria
- [ ] Shipped and deployed (backend + frontend at a public URL)
- [ ] Core features working: multi-agent orchestration, tool integration (web search + vector search), real-time progress updates, structured JSON output
- [ ] Agent handoff works: researcher → analyst → synthesizer with no lost context or duplication
- [ ] Tool failures handled gracefully: web search or retrieval failures don't crash pipeline
- [ ] Code is clean and testable: agent orchestration logic is decoupled from Claude calls; tools are mocked for unit tests
- [ ] Can explain architecture and tradeoffs: why multi-agent (vs. monolithic reasoning), why this tool set, how agent roles prevent duplication, model-tier selection rationale

## Timeline
- **Week 1**: Setup, schema, scaffold agents — FastAPI project, Postgres schema (queries, results, tool_logs), basic JWT auth, Anthropic SDK integration, define JSON schemas for agent outputs, mock Claude calls
- **Week 2**: Researcher agent + tools — Build researcher agent with web search (SerpAPI free tier) and document retrieval (pgvector ingestion + semantic search), test tool integration, handle failures gracefully
- **Week 3**: Analyst + synthesizer agents — Build analyst (critique, confidence scoring) and synthesizer (narrative composition); test agent handoff and structured output format
- **Week 4**: Frontend + orchestration — React dashboard showing agent progress (real-time updates via WebSocket or polling), query submission, result display; implement central result store and agent routing logic
- **Week 5**: Integration, hardening, polish — End-to-end testing, caching implementation, edge case handling (empty results, slow searches, tool failures), cost tracking (log token counts per agent)
- **Weeks 5-6** (optional): Deploy, document, interview prep — Deploy to Render + Vercel, write README with architecture overview and agent design patterns, draft/polish interview story

*Note: Slightly longer than typical 4-6 week project due to multi-agent complexity; can be compressed by scoping to 2 agents (researcher + synthesizer, skip analyst) or using only web search (skip vector DB).*

## Interview Story (Draft)

"I built a multi-agent research assistant where specialized Claude instances collaborate to answer complex research questions. The main challenge was orchestrating agents without duplicating work or losing context — if the researcher found a source, the analyst shouldn't re-fetch it, but the synthesizer still needs access to it for the final narrative.

I solved it by designing structured JSON schemas for each agent's output (researcher returns facts + sources + identified gaps, analyst returns critiques + confidence scores, synthesizer returns a final narrative). Agents communicate through a central Postgres result store, and each agent queries what's been found so far before making tool calls, preventing duplication.

A second challenge was tool reliability. Web search can fail or return irrelevant results, and I needed the pipeline to degrade gracefully — no hard crashes. I wrapped all tool calls in error handlers and had agents report what they couldn't find, so the synthesizer could note limitations in the final output.

What I learned: scaling AI reasoning from single-shot (Project 1: categorize one transaction) to multi-step orchestration (Project 2: research a topic) requires thinking carefully about agent roles, information flow, and failure modes. It's not just about calling Claude more — it's about designing hand-offs so agents can specialize, share context efficiently, and recover from partial failures. I also learned that model tier selection matters: Haiku for high-volume tool feedback, Sonnet for mid-tier reasoning, Opus for final synthesis — matching the tool to the task keeps costs reasonable while maintaining quality where it matters."

---

*Once shipped, add a "Final Interview Story" section here reflecting what actually happened during the build.*
