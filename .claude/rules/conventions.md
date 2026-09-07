# Conventions

- **Branches / PRs:** branch per change; PRs target `main`. Automated routines open PRs,
  they do not push to `main`.
- **`.gitignore`:** `*.csv` is ignored (personal financial exports live in the working tree
  but are never committed).
- **Commit messages** end with:
  `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`
- **Staging** is always explicit pathspecs — never `git add -A` / `git add .`. Check
  `git diff --cached` before a pathspec-less `git commit`.
- **Prompt log rides along.** Every commit also stages any uncommitted files under
  `.claude/_Prompts/logs/` (the current day's log, plus any older un-committed ones). The
  log is bookkeeping produced by the `UserPromptSubmit` hook — it travels with whatever
  commit is being made rather than piling up as a separate chore. `scripts/git/commit.sh`
  does this automatically; when committing by hand, add the log path alongside your real
  pathspecs.

## Git helper scripts

`scripts/git/` wraps the rituals so a commit is one call, not four:

```bash
scripts/git/state.sh                       # one-call snapshot: branch/tracking, staged
                                           #   vs unstaged vs untracked, diffstat, recent log
scripts/git/commit.sh -m "Subject" [-m body] -- path [path...]
                                           # stage exactly those paths (+ fold in prompt
                                           #   logs), sanity-check the staged set, append
                                           #   the Co-Authored-By trailer, then commit
scripts/git/push.sh [remote] [branch]      # push with a timeout + HTTP/1.1 fallback + one
                                           #   retry, so a stalled push fails fast
scripts/git/batch-git-push.sh 90 main "Add skills"   # bulk: many new files, N per push
```

`state.sh` is read-only. `commit.sh` never pushes and never `git add -A`. `push.sh` is a
thin resilience wrapper — a rejected push (non-fast-forward, protected branch) still stops
for a human.
