# Task 3 Report: Decision-Making/Prioritization Agent

## Status: DONE

## What I implemented

Created `decision-making-prioritization/` with the three files specified in the brief:

1. **`AGENTS.md`** — agent definition with frontmatter (`name`, `description`), a Purpose section, the four criteria stated in weight order (confidence/anxiety reduction highest, then interview relevance, then job marketability, then interest/sustainability lowest-but-non-zero), an explicit note that the hierarchy should be surfaced as a tradeoff rather than silently applied as a weighted formula, and all three modes (Quick Decision, Deep Analysis, Criteria Check) each with a "What it does" / "Success" line — matching the pattern used in the sibling `system-design-communication` agent from Task 2.

2. **`prompts/prioritize-options.md`** — the Deep Analysis prompt. Kept the brief's five-step core (state options → name criteria → score each option per criterion with a "because" clause → ask which feels right → isolation question if still torn) and the four-criteria list verbatim, then refined steps 2-5 and added a new step 6 based on testing (see Refinements below).

3. **`README.md`** — usage guide with the criteria list, a modes table (Quick Decision / Deep Analysis / Criteria Check — when/why), invocation examples, success criteria, and a Tips section (name only the criteria relevant to *this* decision, near-ties are a valid outcome, use it for stop/continue decisions too, try the isolation question when torn).

No file deviates from what the brief specified for the core structure, criteria list, or hierarchy — refinements were additive (expanding ambiguous steps, adding step 6) and grounded in testing evidence, not speculation.

## Tests run

Following the same methodology as Task 2 (there's no live human user in this session, so testing an interactive coaching prompt requires simulation rather than direct use): I ran one subagent that played **both** roles — the coach, following `prompts/prioritize-options.md` strictly and only, and a candidate with a realistic, messy decision — then critiqued the prompt independently afterward, without visibility into my design rationale.

**Test scenario:** "Should I build a portfolio project (small full-stack app) or spend the next two weeks focused entirely on system design interview prep?" with interviews lined up in ~3 weeks. The candidate persona pushed back naturally: raised two off-menu concerns (already has two portfolio projects, so marketability upside is muted; worried about burnout from two straight weeks of drilling), self-scored each criterion with real reasoning rather than parroting the coach's suggestions, expressed genuine uncertainty ("my gut says system design but I don't fully trust it"), and at the end tried to propose a hybrid schedule outside the original two options.

Full 8-exchange transcript was produced. Findings:

- **The isolation question was the strongest mechanic.** The candidate was stuck on a 4-way split (confidence + interview relevance favored system design; marketability + interest favored the portfolio project) until asked "if you had to pick based on confidence alone, which wins? Interview readiness alone?" Both isolated cleanly on system design, and the candidate immediately recognized they'd been over-weighting a criterion (marketability) they'd already said mattered less. This validates the framework's central premise from the brief.
- **The brief's step-3 example, read literally, invites a robotic failure mode.** The brief shows all four scored criteria for an option delivered as one block. Read literally, a coach would dump eight numbers on the candidate in a single turn immediately after they name their options — nothing spoken, no real back-and-forth. In the simulation I paced it one criterion at a time and assembled the table only at the end; that felt natural. The brief didn't instruct this pacing.
- **Who assigns the scores was genuinely ambiguous.** The brief's phrasing ("score it against each criterion," followed by an example that reads like the assistant produced the numbers) doesn't say whether the coach elicits scores from the candidate or invents them unilaterally. A literal reading could easily produce a paternalistic coach that hands the candidate numbers instead of asking for them — which would undercut "don't tell them what to do."
- **No instruction for off-menu criteria once revealed.** Step 2 asks "any others?" but never says what to do with what's surfaced. In the test, the candidate volunteered two things outside the four criteria (redundant-project discount, burnout risk); the coach had to improvise folding them into existing rows rather than adding new scored dimensions or ignoring them.
- **No operational definition of "still torn"** (the trigger for the isolation question in step 5) — it worked fine here because the candidate used clearly hedging language, but a less cooperative "I guess system design, sure" could be misread either way.
- **No guardrail against editorializing right before the "which feels right?" question** — the moment of highest risk for a coach to lean on the scale ("looks like Option A edges it out") right after laying out numbers that visually favor one side.
- **No coverage for hybrid/blended proposals.** The candidate's closing question ("what if I do 3 days portfolio + 11 days system design?") had zero guidance in the brief; the coach had to invent a response (offer to score it as a third option, or let it stand as the candidate's own call).

## Refinements made

Edited `prompts/prioritize-options.md` steps 2 through 5 and added step 6, all traceable to the findings above:

- **Step 2**: added instructions for off-menu criteria — fold into the closest existing criterion's reasoning and name which one, so the candidate can correct a bad fold.
- **Step 3**: clarified scores are elicited from the candidate, not invented by the coach; added pacing guidance (one criterion at a time across options, not a one-turn data dump); kept the "because" clause requirement and the brief's original example, now framed as the *assembled* table rather than the delivery format.
- **Step 4**: added an explicit no-editorializing guardrail at the exact point of highest risk (before the candidate has weighed in on the breakdown).
- **Step 5**: replaced the unconditional "if they're still torn" with concrete triggers (hedging, stated uncertainty, or asking the coach what to do) and an explicit skip condition (already stated a clear preference); added guidance for the previously uncovered case where the two isolation answers disagree with each other — name the conflict, don't force a resolution.
- **New step 6**: added guidance for hybrid/blended/third-option requests mid-session — offer to score the new option(s) if they want that, otherwise don't force the original binary.

`AGENTS.md` and `README.md` were not changed after testing — the criteria, hierarchy, and modes framework itself held up; only the execution details in the prompt file needed sharpening.

## Concerns / observations

- **Testing method is simulated, not a live human session**, same caveat as Task 2. The subagent played both coach and candidate from the prompt text alone, which is a reasonable proxy for catching literal-reading failure modes but isn't the same as the user's own experience of decision paralysis. The real signal on whether this reduces paralysis and sustains momentum comes from the user's actual use, per the brief's success metric.
- **The isolation question's "still torn" trigger remains a judgment call**, not a hard rule, even after refinement — I gave concrete signals (hedging, stated uncertainty, asking the coach directly) rather than a strict heuristic, since an overly mechanical trigger risks asking the isolation question when the candidate has already decided, which would feel patronizing. Worth watching in real use.
- **`.superpowers/` and `docs/` remain untracked**, consistent with Tasks 1 and 2's reports — left out of this commit as unrelated to this task's file scope.

## Commit

- `448490c3960a371a7515e5318537723e8673ddfa` (short `448490c`) — "feat: add decision-making agent for prioritization and momentum"
  - 3 files changed (all new): `decision-making-prioritization/AGENTS.md`, `decision-making-prioritization/README.md`, `decision-making-prioritization/prompts/prioritize-options.md`.
