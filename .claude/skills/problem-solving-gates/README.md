# Problem-Solving Gates

This skill blocks Claude from doing your thinking for you. It defines three modes — Rubber Duck, Options Generator, Knowledge Checker — each gated behind proof you've done the first pass yourself. The gate exists because forming the hypothesis, scanning the options, or attempting the explanation is what builds skill; skipping to Claude's answer skips the rep.

## Which mode do I need?

```
Debugging something broken? → Rubber Duck. Bring a hypothesis.
Deciding between approaches? → Options Generator. Bring constraints + a lean.
Checking you understood something? → Knowledge Checker. Bring a first-pass explanation.
Writing new code or reviewing a finished draft? → This skill doesn't apply.
```

## Invoking each mode

State your situation plus the precondition input directly — Claude infers the mode from context. Missing the precondition? Say so instead of guessing:

- No hypothesis yet? Say so; form one, even a bad one, before asking.
- No constraints/lean yet? List what's unknown first.
- Haven't tried explaining it? Take a rough first pass before asking for a check.

## Common mistakes

| Mistake | What happens |
|---|---|
| "What's wrong with my code?", no hypothesis | Claude asks for your hypothesis and stops. |
| "What should I do?", no constraints/lean | Claude asks you to name unknowns and a lean first. |
| "Explain X?" without attempting it | Claude asks for your first-pass explanation first. |
| "Just tell me" mid-mode | Claude declines, redirects to the next narrowing question (unless the escape hatch applies). |
| Expecting Claude to rank options or diagnose | Out of scope by design — that's the point. |
