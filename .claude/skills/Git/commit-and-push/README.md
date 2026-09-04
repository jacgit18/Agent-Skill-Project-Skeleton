# commit-and-push skill

Stage → commit → push, with the commit message built from the actual diff instead of the
filenames or a vague "update". Reads `git status` / `git diff` / recent `git log` first,
matches the repo's message convention, splits unrelated changes into separate commits, runs a
pre-commit sanity pass (secrets, `.env`, large blobs, debug code, merge markers), branches off
the default branch when the user hasn't said to commit straight to it, and confirms before
anything outward-facing.

## Files

| File | Role |
|---|---|
| `SKILL.md` | The whole process — read state, branch guard, group, sanity pass, message rules, commit, push, report. |

## Boundaries

Stops after `git push`. Does **not** open PRs, resolve merge conflicts, rewrite published
history (`rebase` / `amend` / `--force`), or design a branching strategy.

## Related

- `scripts/git/batch-git-push.sh` — for bulk file additions (90+ unrelated new files), the
  skill defers to this batched stage/commit/push script.
- Commit trailer (`Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`) is fixed by the
  session's attribution guidance; the skill just enforces it on every message it writes.

## Portability

Repo-agnostic. Copy the directory into another repo's `.claude/skills/`. The batch-push
reference assumes `scripts/git/batch-git-push.sh` exists in that repo; drop that line if not.
