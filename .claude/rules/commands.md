# Commands

There is no build, lint, or test runner. The two operational commands:

```bash
# Chunked commit + push — never puts more than N files in one push.
# Args: [batch_size=90] [branch=current] [commit_prefix="Add files"]
scripts/git/batch-git-push.sh 50 main "Add skills"
DRY_RUN=1 scripts/git/batch-git-push.sh            # preview only
INCLUDE_MODIFIED=1 scripts/git/batch-git-push.sh   # also stage modified/deleted, not just untracked
```

The prompt-logging hook (`scripts/hooks/log-prompt.sh`) runs automatically on every prompt.
It needs `jq` on PATH; it is defensive by design — always exits 0, prints nothing, cannot
block a prompt or inject context.

**"Testing" a skill is done by invoking a skill, not a shell command:**

- `Prompts/skill-interaction-testing` — run a new/changed skill against its siblings for
  stacking, contradiction, silent override, and beneficial chaining.
- `Prompts/catalog-drift-audit` — periodic whole-catalog hygiene pass.
- `Skill Development/spec-drift-gate` — gate a multi-file/multi-session build behind a
  written spec, then diff work against it at checkpoints.
