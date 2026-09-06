<!--
SKILL README TEMPLATE — sibling positioning

This file is for a human (and for the next author) deciding whether this skill overlaps
another. It is NOT loaded as skill context. Keep it about boundaries, not usage.

Fill in, delete the comments, and keep it roughly this shape — it matches the other
skills' READMEs.
-->

# [skill-name] skill

[One paragraph in prose: what it does, what it produces, and the single rep or input it
turns on. Same substance as the `description` frontmatter, but readable.]

<!-- Optional, if the skill was distilled from specific notes. -->
Built from [source notes / framework], covering [the pieces it pulls in].

## Where it sits

```
[sibling-a]        →  [its job]                                    (its artifact)
[this-skill]       →  [its job]                                    (this skill)
[sibling-b]        →  [its job]                                    (its artifact)
learning-gate      →  classifies intent; its Step 3 "[row]" defers here
```

[One or two sentences on the boundary that most needs stating — the sibling this is most
often confused with, and the tell.]

## Files

| File | Role |
|---|---|
| `SKILL.md` | Entry point — when it applies / doesn't, the [gate precondition / inputs], the steps, the output. |
| `[reference-file].md` | [What deep material it holds and how a step uses it.] |

## What it produces

[The artifact and its path, or "No artifact — it gates a [coding/design] action; the output
is [X], or a request for the missing rep."]

## When it does NOT apply

- [Case] → `[sibling-skill]`.
- [Case] → `[sibling-skill]`.
- [The rep was already in the request] → gate satisfied on arrival, just do the work.

## Using it in another repo

Repo-agnostic [or note the assumption]. Produces [no files / a doc at `<path>`].

```
cp -r ".claude/skills/[Group]/[skill-name]" /path/to/other-repo/.claude/skills/
```

## Interaction with sibling skills

Run `skill-interaction-testing` whenever this skill or a sibling's description changes.
Known boundaries to hold:

- **vs `[sibling]`** — [the boundary, stated so it reads correctly from both sides].
- **vs `learning-gate`** — [which one sets the ceiling, which owns the domain rep; don't
  stack both sets of questions].
