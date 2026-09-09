# Catalog drift audit — log

Durable trail for `catalog-drift-audit` runs (manual and the weekly cloud routine). Each run
reads this first so it never re-flags something already resolved. Newest entry on top.

---

## 2026-09-09 — manual run (post the 8-skill Finance batch, PRs #22–#29)

Run against `main` after PRs #22–#29 merged (the whole `Finance/` equity system:
`portfolio-thesis-audit`, `position-exit-rules`, `covered-call-decision`,
`watchlist-screener-criteria`, `weekly-portfolio-review`, `equity-research-writeup`,
`asset-allocation-policy`, `etf-selection`). PR #30 (a Finance README pipeline diagram) open,
not yet merged. Triggered by the user after `/sync-catalog` flagged two unlisted skills.

**Step 1 — stale markers:** CLEAN. No `[x] Built … Memory: pending` / TODO markers in
`SKILL-BACKLOG.md`. The three `- [ ]` items in "## Loose threads" (requirements-elicitation
cluster, event-driven-architecture pattern choice, application-internal-structure gate) are
deliberately-open future candidates, not stale bookkeeping. The `Memory: pending` / `TODO`
strings that grep surfaced were all prose inside `catalog-drift-audit`'s and
`codebase-file-orientation`'s own descriptions.

**Step 2 — catalog-doc sync:** 2 skills on disk with no `README.md` row, **both fixed**:
- `Skill Development/incremental-build-pacing` — a gate; row added to the
  "Architecture, Business, Skill Development, Git" table after `spec-drift-gate`.
- `Architecture/tech-decision-walkthrough` — a procedure; row added after `design-scoping`.
Both were added in the user's commits `7e0b0bd` / `4a41f06` before this session, outside the
add-a-skill workflow. Also added `SKILL-BACKLOG.md` items 30 + 31 (reconciliation entries).
All 8 new Finance skills (items 22–29) have rows, backlog entries, and memory files —
clean.

**Step 3 — dead references:** CLEAN. Every backticked hyphenated skill-name token in a
`SKILL.md` resolves to a real directory (the `Architecture/Data/` subgroup —
`caching-strategy`, `database-architecture`, `data-tier-operations`, `dimensional-modeling`,
`index-tuning`, `relational-modeling` — is real, just one level deeper than a naive
`maxdepth 3` scan). Cross-cutting gates all resolve. Matches the `/sync-catalog` run's result.

**Step 4 — untested-pair backfill:** recent work is covered — all 8 Finance skills carry a
`skill-interaction-testing` result in memory (`skill-added-*.md`), and the
`tech-decision-walkthrough` × `watchlist-screener-criteria` pair was tested during item 25.
FLAGGED, not fixed: `incremental-build-pacing` and `tech-decision-walkthrough` have **no
recorded isolation screen or interaction test** — they shipped wired into many siblings'
descriptions but with no memory record of a test. Hand to `skill-interaction-testing` Step 2
onward if revisited (candidate pools noted in backlog items 30/31). The 2026-09-06 run's
`session-handoff` flag was already resolved that same day.

**Step 5 — starvation-by-neglect:** CLEAN. All 8 new Finance skills are pointed at by 6–11
sibling `SKILL.md` files. `incremental-build-pacing` / `tech-decision-walkthrough` are
heavily referenced (not starved — their gap was doc bookkeeping only). `reddit-researcher`
remains referenced by nothing but is a standalone tool with no gate collision surface — same
non-finding as the 2026-09-06 run.

**Applied:** the 2 `README.md` rows + the 2 `SKILL-BACKLOG.md` reconciliation entries,
directly. **Flagged (judgment call, not resolved):** the missing retroactive interaction
test for `incremental-build-pacing` and `tech-decision-walkthrough`.

**Separate, noted not fixed:** `README.md`'s top "## Layout" table still lists vault
directories that aren't tracked in this repo (`Architecture/`, `Communication/`,
`Business Venture/`, `Goals/`, `Books/`, `READ DELETE/`) — the same drift `.claude/rules/repo-map.md`
already documents. Out of scope for this skill (it's a hand-written prose section, not a
catalog cross-reference); left for a human.

Memory: `catalog-drift-audit-2026-09-09.md`.

---

## 2026-09-06 — manual run (post `_Other/` triage + `prompt-authoring`)

Run against `main` after PRs #11/#12 merged and the prior session's uncommitted catalog docs
were reconciled (`0874bb9`, `17228c6`).

**Step 1 — stale markers:** CLEAN. No live `Memory: pending` / TODO markers in `SKILL-BACKLOG.md`
(the 5 the prior audit flagged were resolved in the reconciliation commit). One stale *note*
fixed: the item-16 "Bonus finding" about `Architecture/reddit-researcher/` still described it as
untriaged with no memory record — updated to point at `skill-folds-other-directory.md` and the
`Research/` relocation.

**Step 2 — catalog-doc sync:** 3 missing `README.md` rows, all added:
- `Research/reddit-researcher` (+ new `### Research` group section)
- `Prompts/prompt-authoring`
- `Business/delete-ai-words`
Plus 3 stale descriptions refreshed for fold changes: `software-carpentier-brand` (feed-post
mode), `spec-drift-gate` (Step 2a), `learning-gate` (`guided-walkthrough.md`).
`SKILL-BACKLOG.md`: added item 18 (`prompt-authoring`) and a `_Other/`-triage entry to the
"Fold into existing skills" section.

**Step 3 — dead references:** CLEAN. Cross-cutting gates all resolve (`ambiguity-gate` ×10,
`learning-gate` ×26, `problem-solving-gates` ×34, `problem-journal` ×6). Deleted skills
(`grill-me`, `my-viral-post`, `how-to`, `linkedin-hook`, `Prompt optimizer`) referenced
nowhere. `reddit-researcher`'s one hit is its own frontmatter.

**Step 4 — untested-pair backfill:** recent work is covered (`skill-folds-other-directory.md`,
`skill-added-prompt-authoring.md`). FLAGGED, not fixed: `Prompts/session-handoff` has no
recorded interaction test and shares a "session state / handoff artifact" concept with
`spec-drift-gate` and `prompt-archive` — low priority, hand to `skill-interaction-testing`
Step 2 if revisited.

**Step 5 — starvation-by-neglect:** 1 gap fixed — `prompt-tester` and `prompt-archive` both said
"not for writing a new prompt from scratch" without naming `prompt-authoring`; added the pointer
to both. `reddit-researcher` is pointed at by nothing but shares no collision surface with any
gate (it's a standalone tool) — not a real starvation finding.

**Applied:** all Step 1/2/3/5 mechanical fixes directly.

**Step 4 backfill (done same day):** ran `skill-interaction-testing` on `session-handoff` (1
worktree agent, 6 scenarios vs `spec-drift-gate` / `prompt-archive` / `problem-journal` /
`ambiguity-gate` + 2 controls). 5 clean; 1 fix — `session-handoff` triggers on
"recap" / "before I forget" and could pre-empt `problem-journal` Journal mode on a post-fix
bug write-up. One-line scope-narrowing clause added to `session-handoff`'s description pointing
resolved-bug post-mortems to `problem-journal`. Memory: `skill-interaction-session-handoff.md`.
