#!/usr/bin/env bash
# UserPromptSubmit hook — append every submitted prompt to a dated log in
# .claude/_Prompts/logs/YYYY-MM-DD.md.
#
# Defensive by design: it always exits 0 and prints nothing to stdout, so it can
# never block a prompt (exit 2) or inject text into the model's context. Any
# failure is swallowed silently.
#
# Wired from .claude/settings.json:
#   "UserPromptSubmit": [{ "hooks": [{ "type": "command",
#     "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/hooks/log-prompt.sh" }] }]

payload="$(cat 2>/dev/null || true)"
[ -z "$payload" ] && exit 0

prompt="$(printf '%s' "$payload" | jq -r '.prompt // empty' 2>/dev/null || true)"
[ -z "$prompt" ] && exit 0

cwd="$(printf '%s' "$payload" | jq -r '.cwd // empty' 2>/dev/null || true)"
session="$(printf '%s' "$payload" | jq -r '.session_id // empty' 2>/dev/null | cut -c1-8 || true)"

root="${CLAUDE_PROJECT_DIR:-$cwd}"
[ -z "$root" ] && root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." 2>/dev/null && pwd)"
[ -z "$root" ] && exit 0

logdir="$root/.claude/_Prompts/logs"
mkdir -p "$logdir" 2>/dev/null || exit 0

logfile="$logdir/$(date +%Y-%m-%d).md"
[ -f "$logfile" ] || printf '# Prompt log — %s\n' "$(date +%Y-%m-%d)" > "$logfile" 2>/dev/null || exit 0

{
  printf '\n## %s  ·  session %s\n\n' "$(date +%H:%M:%S)" "${session:-?}"
  printf '%s\n' "$prompt"
} >> "$logfile" 2>/dev/null || exit 0

exit 0
