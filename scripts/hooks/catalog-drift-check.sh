#!/usr/bin/env bash
# SessionStart hook — mechanical catalog-drift glance.
#
# Runs the two unambiguous shell checks from /sync-catalog — skills on disk with
# no README.md row, and open SKILL-BACKLOG.md bookkeeping markers — and, only
# when something trips, injects a short summary into the session so mechanical
# drift is visible at the start of work instead of waiting for the weekly cloud
# routine.
#
# The judgement-heavy /sync-catalog checks (starvation candidates, candidate
# dead pointers) are deliberately left out: they have expected false positives
# and need a model to triage, which is what running /sync-catalog itself is for.
#
# Defensive by design: always exits 0, emits nothing on a clean catalog or on
# any internal failure, and can never block session start. It only adds context.
# It does not fix anything — that is `catalog-drift-audit` / `/new-skill`.
#
# Wired from .claude/settings.json:
#   "SessionStart": [{ "hooks": [{ "type": "command",
#     "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/hooks/catalog-drift-check.sh" }] }]

payload="$(cat 2>/dev/null || true)"

# Only nudge on a genuinely fresh start. Skip resume/compact restarts so a long
# session is not re-nagged every time context is summarized.
source="$(printf '%s' "$payload" | jq -r '.source // empty' 2>/dev/null || true)"
case "$source" in
  resume | compact) exit 0 ;;
esac

cwd="$(printf '%s' "$payload" | jq -r '.cwd // empty' 2>/dev/null || true)"
root="${CLAUDE_PROJECT_DIR:-$cwd}"
[ -z "$root" ] && root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." 2>/dev/null && pwd)"
[ -z "$root" ] && exit 0
cd "$root" 2>/dev/null || exit 0
[ -d .claude/skills ] || exit 0

lines=""

# 1. Skills on disk with no README.md row.
missing="$(for s in $(find .claude/skills -name SKILL.md 2>/dev/null | sed 's#.claude/skills/##;s#/SKILL.md##'); do
  b=$(basename "$s")
  grep -qF "$b" README.md 2>/dev/null || echo "$s"
done)"
n="$(printf '%s' "$missing" | grep -c . || true)"
[ "${n:-0}" -gt 0 ] && lines="$lines
  - ${n} skill(s) with no README row: $(printf '%s' "$missing" | paste -sd, -)"

# 2. SKILL-BACKLOG.md markers that usually mean unfinished bookkeeping.
backlog="$(grep -nE 'Memory:[[:space:]]*(pending|TODO)[[:space:]]*\.?$|^[[:space:]]*-?[[:space:]]*\[ \] Built' SKILL-BACKLOG.md 2>/dev/null || true)"
n="$(printf '%s' "$backlog" | grep -c . || true)"
[ "${n:-0}" -gt 0 ] && lines="$lines
  - ${n} open SKILL-BACKLOG marker(s) ([ ] Built / Memory: pending)"

[ -z "$lines" ] && exit 0

out="Catalog drift — mechanical check:${lines}

Run /sync-catalog for the full read (also flags starvation + dead pointers);
catalog-drift-audit or /new-skill to fix."

if command -v jq >/dev/null 2>&1; then
  jq -n --arg ctx "$out" \
    '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
else
  printf '%s\n' "$out"
fi
exit 0
