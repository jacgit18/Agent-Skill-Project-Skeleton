# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A **catalog**, not an application. It holds authored Claude skills (mostly decision *gates*),
a small amount of unattended-agent infrastructure, and the plumbing that keeps the catalog
honest. There is nothing to compile, serve, or unit-test. "Work" here means authoring a
skill, testing it against its siblings, and keeping the bookkeeping files in sync.

## Rules

Topic guidance lives in `.claude/rules/` and is imported below. Edit the rule files, not this list.

| Rule | Covers |
|---|---|
| [`repo-map.md`](.claude/rules/repo-map.md) | What's actually tracked; the `README.md` layout-drift warning |
| [`commands.md`](.claude/rules/commands.md) | The two operational scripts; "testing" a skill means invoking one |
| [`skill-architecture.md`](.claude/rules/skill-architecture.md) | Skill-directory shape, gate vs procedure, the four cross-cutting meta-skills |
| [`adding-a-skill.md`](.claude/rules/adding-a-skill.md) | Isolation → interaction → reciprocal edits → bookkeeping |
| [`agents.md`](.claude/rules/agents.md) | `spec-executor`, the weekly cloud routine, authoring a new agent |
| [`conventions.md`](.claude/rules/conventions.md) | Branches/PRs, `.gitignore`, commit-message footer |

@.claude/rules/repo-map.md
@.claude/rules/commands.md
@.claude/rules/skill-architecture.md
@.claude/rules/adding-a-skill.md
@.claude/rules/agents.md
@.claude/rules/conventions.md
