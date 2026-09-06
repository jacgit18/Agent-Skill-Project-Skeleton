# Decision-Making/Prioritization Agent

## What This Does

Helps you decide what to work on next when you're stuck between options. Uses your stated prioritization criteria to evaluate options clearly.

## Criteria (in order of importance)

1. **Confidence/anxiety reduction** (highest weight) — Does this help you solve problems calmly?
2. **Interview relevance** (medium weight) — Does this prepare you for tech interviews?
3. **Job marketability** (medium weight) — Does this make you more hireable?
4. **Interest/sustainability** (lower weight) — Will you enjoy this and keep going?

## Modes

| Mode | When | Why |
|---|---|---|
| Quick Decision | 2-3 options, need to decide fast | Gut-check scores, no deep deliberation |
| Deep Analysis | Multiple options, want to understand tradeoffs thoroughly | Full per-criterion breakdown, isolates the load-bearing criterion if you're still torn |
| Criteria Check | Not sure the four standard criteria are the right ones for this decision | Validate/adjust criteria before scoring options against them |

## When to Use

- "I'm between building project X or learning system design. Which should I prioritize?"
- "Should I focus on backend or frontend first?"
- "Should I explore AI QA testing or stick with full-stack?"
- "I'm stuck on a bug. Should I keep debugging or move on?"

## How to Invoke

> "I'm stuck between [option 1] and [option 2]. Help me decide using my criteria."

Use `prompts/prioritize-options.md` as the guiding prompt. The agent will ask clarifying questions, break down how each option scores against your criteria, and help you decide.

For a fast, low-stakes call, say so up front: "Quick decision — I don't need the deep breakdown." For a decision where you're not sure the standard criteria even apply (e.g., a personal or non-career choice), say: "Can we do a criteria check first?"

## Success Looks Like

- You make decisions without paralysis
- Your learning path feels coherent (each thing builds on the last)
- You're not second-guessing your choices
- Momentum keeps you moving forward

## Tips

- Don't skip naming the criteria that matter for *this* decision, even though the four are the default — sometimes only two of them are actually relevant.
- If the breakdown produces a near-tie, that's a valid outcome. Pick based on which option you'd rather start today rather than forcing a tiebreaker that isn't really there.
- Use this agent for stop/continue decisions too ("should I keep debugging or move on?"), not just either/or choices between two forward paths.
- If you're torn, try the isolation question: which option wins on confidence alone? Which wins on interview relevance alone? That usually reveals which criterion is actually driving your hesitation.
