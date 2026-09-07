# Commands

There is no build, lint, or test runner. The two operational commands:

```bash
# Chunked commit + push — never puts more than N files in one push.
# Args: [batch_size=90] [branch=current] [commit_prefix="Add files"]
scripts/git/batch-git-push.sh 50 main "Add skills"
DRY_RUN=1 scripts/git/batch-git-push.sh            # preview only
INCLUDE_MODIFIED=1 scripts/git/batch-git-push.sh   # also stage modified/deleted, not just untracked
```

Two hooks run automatically (wired in `.claude/settings.json`), both defensive by design —
always exit 0, never block, only touch their own output:

- `scripts/hooks/log-prompt.sh` (`UserPromptSubmit`) — appends every prompt to the dated
  log. Needs `jq`; prints nothing.
- `scripts/hooks/catalog-drift-check.sh` (`SessionStart`) — runs the two unambiguous
  `/sync-catalog` checks (skills with no `README.md` row, open `SKILL-BACKLOG.md` markers)
  and injects a short summary only when one trips. Silent on a clean catalog and on
  resume/compact restarts. Fixes nothing — hand drift to `catalog-drift-audit` / `/new-skill`.

**"Testing" a skill is done by invoking a skill, not a shell command:**

- `Prompts/skill-interaction-testing` — run a new/changed skill against its siblings for
  stacking, contradiction, silent override, and beneficial chaining.
- `Prompts/catalog-drift-audit` — periodic whole-catalog hygiene pass.
- `Skill Development/spec-drift-gate` — gate a multi-file/multi-session build behind a
  written spec, then diff work against it at checkpoints.
