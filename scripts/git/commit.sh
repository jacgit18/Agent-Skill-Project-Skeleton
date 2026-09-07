#!/usr/bin/env bash
#
# commit.sh — commit with this repo's conventions baked in.
#
#   scripts/git/commit.sh -m "Subject line" [-m "body paragraph" ...] \
#       [--] <pathspec> [<pathspec> ...]
#
# What it does, in order:
#   1. Stages exactly the pathspecs you name — never a blanket `git add -A`
#      (see .claude/rules/conventions.md).
#   2. Also stages any uncommitted prompt-log files under
#      .claude/_Prompts/logs/ so the log rides along with whatever commit is
#      being made and never has to be staged by hand.
#   3. Runs a sanity pass over the staged set: refuses on .env files, obvious
#      key/cert files, files larger than 1 MiB (override with ALLOW_BIG=1),
#      and staged merge-conflict markers.
#   4. Appends the required Co-Authored-By trailer unless a -m already carries it.
#   5. Prints `git diff --cached --stat` and the assembled message, then commits.
#
# It does NOT push and does NOT open PRs. Use scripts/git/push.sh to push.

set -uo pipefail

top="$(git rev-parse --show-toplevel 2>/dev/null)" || { echo "commit.sh: not a git repo" >&2; exit 1; }
cd "$top" || exit 1

TRAILER="Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>"

msgs=()
paths=()
while [ $# -gt 0 ]; do
  case "$1" in
    -m)
      shift
      [ $# -gt 0 ] || { echo "commit.sh: -m needs an argument" >&2; exit 2; }
      msgs+=("$1"); shift ;;
    --)
      shift
      while [ $# -gt 0 ]; do paths+=("$1"); shift; done ;;
    -*)
      echo "commit.sh: unknown flag: $1" >&2; exit 2 ;;
    *)
      paths+=("$1"); shift ;;
  esac
done

[ "${#msgs[@]}" -gt 0 ]  || { echo "commit.sh: need at least one -m \"message\"" >&2; exit 2; }
[ "${#paths[@]}" -gt 0 ] || { echo "commit.sh: name at least one pathspec (never blanket-add)" >&2; exit 2; }

# 1. Stage the named pathspecs.
git add -- "${paths[@]}"

# 2. Fold in any uncommitted prompt logs.
logdir=".claude/_Prompts/logs"
if [ -d "$logdir" ]; then
  logs="$(git status --porcelain -- "$logdir" | sed 's/^...//')"
  if [ -n "$logs" ]; then
    while IFS= read -r f; do
      [ -n "$f" ] && git add -- "$f"
    done <<EOF
$logs
EOF
  fi
fi

# Nothing staged? Stop.
if git diff --cached --quiet; then
  echo "commit.sh: nothing staged after add — aborting." >&2
  exit 1
fi

# 3. Sanity pass over the staged set.
problems=""
staged_files="$(git diff --cached --name-only)"
while IFS= read -r f; do
  [ -z "$f" ] && continue
  case "$f" in
    .env|*/.env|.env.*|*/.env.*)              problems="${problems}  env file staged: ${f}"$'\n' ;;
    *id_rsa|*id_ed25519|*.pem|*.p12|*.pfx)    problems="${problems}  key/cert staged: ${f}"$'\n' ;;
  esac
  if [ -f "$f" ]; then
    sz="$(wc -c < "$f" 2>/dev/null || echo 0)"
    if [ "${ALLOW_BIG:-0}" != "1" ] && [ "$sz" -gt 1048576 ]; then
      problems="${problems}  large file >1MiB staged: ${f} (${sz} bytes) — set ALLOW_BIG=1 to allow"$'\n'
    fi
    if git show ":$f" 2>/dev/null | grep -qE '^(<<<<<<<|>>>>>>>|=======)([[:space:]]|$)'; then
      problems="${problems}  merge-conflict markers in: ${f}"$'\n'
    fi
  fi
done <<EOF
$staged_files
EOF

if [ -n "$problems" ]; then
  echo "commit.sh: pre-commit checks flagged the staged set:" >&2
  printf '%s' "$problems" >&2
  echo "commit.sh: fix or unstage, then retry." >&2
  exit 1
fi

# 4. Assemble -m args, appending the trailer if absent.
commit_args=()
for m in "${msgs[@]}"; do commit_args+=(-m "$m"); done
if ! printf '%s\n' "${msgs[@]}" | grep -qF "$TRAILER"; then
  commit_args+=(-m "$TRAILER")
fi

# 5. Show, then commit.
echo "── staged ─────────────────────────────"
git diff --cached --stat
echo "── message ────────────────────────────"
for m in "${msgs[@]}"; do printf '%s\n\n' "$m"; done
printf '%s\n' "$TRAILER"
echo "───────────────────────────────────────"
git commit "${commit_args[@]}"
