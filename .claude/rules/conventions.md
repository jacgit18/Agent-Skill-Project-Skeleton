# Conventions

- **Branches / PRs:** branch per change; PRs target `main`. Automated routines open PRs,
  they do not push to `main`. Merging a PR is fine from the terminal — `scripts/git/land.sh`
  does it through `gh` (branch protection and checks still apply); that is merging a PR, not
  a direct push to `main`.
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
scripts/git/land.sh [PR|branch] [--merge|--squash|--rebase]
                                           # merge the PR via gh (default: merge commit),
                                           #   delete its remote branch, then check out the
                                           #   base, fast-forward it, prune, drop the local
                                           #   head branch. No arg = current branch's PR.
scripts/git/batch-git-push.sh 90 main "Add skills"   # bulk: many new files, N per push
```

`state.sh` is read-only. `commit.sh` never pushes and never `git add -A`. `push.sh` is a
thin resilience wrapper — a rejected push (non-fast-forward, protected branch) still stops
for a human. `land.sh` goes through GitHub, so a merge the web UI would block is blocked
here too; its local-resync steps are best-effort and skip (with a note) rather than force.

The scripts carry no hard dependency on this repo. Portability knobs: `commit.sh` takes the
commit trailer from `COMMIT_TRAILER` (empty = none), else `git config commit-helper.trailer`
— and if neither is set, its first run writes that git-config key once (to the
`Co-Authored-By` line the repo's recent history already uses, or the built-in default) and
says so, so a fresh clone needs no manual setup. Prompt-log dir is `PROMPT_LOG_DIR` (default
`.claude/_Prompts/logs`, a no-op if that dir is absent). `push.sh` runs without the stall
guard if neither `timeout` nor `gtimeout` is on `PATH`.
