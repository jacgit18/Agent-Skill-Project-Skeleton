# .claude/agents/

Claude Code auto-discovers agents from **`*.md` files directly in this directory** — not
from subdirectories. So what's here is:

| Entry | Status |
|---|---|
| `spec-executor.md` | **A registered agent.** Executes one slice of an approved `spec-drift-gate` spec in an isolated worktree, unattended. Does not decide scope, merge, or push. |
| `decision-making-prioritization/` | **Not an agent** — notes, prompts, and an `AGENTS.md` sketch for a decision-prioritization helper. Nothing here is dispatched. |
| `ai-qa-testing/` | **Not an agent** — Python scratch scripts and a learning plan for prompt-QA experiments. Nothing here is dispatched. |

The weekly **Catalog Drift Audit** is also an agent, but it is a scheduled *cloud* routine
(claude.ai/code/routines), not a file in this repo. Its trail is
`.claude/_Prompts/catalog-audit-log.md`.

## Adding a real agent

1. Run the candidate through the worthiness test at the top of
   `template/spec-system/agent-spec-template.md` — fixed-sequence, high-stakes, or
   fuzzy-success tasks should stay a script or a plain prompt, not an agent.
2. Copy that template to `.claude/agents/<kebab-name>.md` and fill it in.
3. The `description` frontmatter alone decides when the agent fires — pack it with concrete
   trigger scenarios, not one abstract sentence.
