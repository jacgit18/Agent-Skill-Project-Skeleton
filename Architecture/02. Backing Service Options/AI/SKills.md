---
tags: 
author:
  - gitUserNamePlaceHolder
banner: "![[Banner.gif]]"
banner_x: 
banner_y: 
cssclasses:
  - dashboard
Comments: Placeholder comment any thing else you want to mention about the document.
Purpose: This documentation discusses
Status: 
Started: 
EditDate: 
Relates:
---
Yes — and seeing the `problem-solving-gates` skill changes my recommendation quite a bit.

What you're building isn't really a collection of **"AI agents that know how to do X."** It's closer to an **AI-assisted engineering methodology** where different skills govern _how Claude participates in different parts of your development process_.

Your `problem-solving-gates` skill is actually a particularly good example of this philosophy.

## The key distinction I'd make

I'd separate your system into **three layers**:

```text
┌──────────────────────────────────────────────┐
│             DEVELOPMENT WORKFLOW             │
│                                              │
│  Discover → Design → Implement → Test →     │
│             Review → Ship → Learn            │
└──────────────────────┬───────────────────────┘
                       │
              ┌────────▼────────┐
              │      SKILLS      │
              │                  │
              │ How AI behaves   │
              │ in each activity │
              └────────┬─────────┘
                       │
              ┌────────▼────────┐
              │     AGENTS       │
              │                  │
              │ Who can execute  │
              │ multi-step work  │
              └──────────────────┘
```

**Skills should establish behavior and methodology.**

**Agents should execute larger workflows using those skills.**

That's an important distinction.

---

# Your `problem-solving-gates` skill is a different kind of skill

I'd actually classify it as a **meta-skill**.

It isn't teaching Claude:

> "Here's how to debug a race condition."

It's teaching Claude:

> **"Here's how you should behave when helping me learn to debug."**

That's much more interesting.

And I would preserve that distinction.

You could eventually have something like:

```text
.claude/
└── skills/
    │
    ├── problem-solving-gates/
    │
    ├── architecture/
    │
    ├── database-design/
    │
    ├── api-design/
    │
    ├── testing/
    │
    ├── debugging/
    │
    ├── code-review/
    │
    ├── security/
    │
    ├── performance/
    │
    └── documentation/
```

But **don't create all of those just because you can**.

The interesting question is what _behavior_ you want each skill to enforce.

---

# I'd organize your skills around development activities

Rather than technologies.

For example, I wouldn't start with:

```text
prisma/
postgres/
react/
typescript/
jest/
```

Those are mostly **knowledge domains**.

Instead:

```text
architecture/
database-design/
api-design/
implementation/
testing/
debugging/
review/
security/
performance/
documentation/
```

Those correspond to **engineering decisions and activities**.

The technologies become context that the skills operate within.

---

# 1. Problem-Solving Gates

You've already built this one.

I'd keep it relatively independent from the others.

Its purpose is essentially:

> **Don't let AI substitute for the learner's reasoning.**

Your three modes are excellent examples:

```text
Debugging
    ↓
"I have a hypothesis."

Architecture
    ↓
"I know my constraints + have a position."

Learning
    ↓
"I can explain it in my own words."
```

That's a **learning gate**, not merely an engineering skill.

And I'd probably make this one have higher priority than many of the others.

---

# 2. Architecture Skill

This would complement your Options Generator.

But I'd make it substantially more systematic.

Its job would be to help you reason about:

```text
Requirements
     ↓
Constraints
     ↓
System boundaries
     ↓
Responsibilities
     ↓
Data ownership
     ↓
Interfaces/contracts
     ↓
Architecture
     ↓
Decisions
```

The important rule:

> **Architecture skill does not immediately generate architecture.**

It first makes sure you've identified the relevant decisions.

For example:

```text
Decision:
Where should the source of truth for User live?

Known:
- PostgreSQL
- REST API
- One backend
- Web frontend
- No external consumers

Unknown:
- Expected future consumers
- Whether API will become public
- Domain stability

Initial position:
Contract-first
```

Then AI helps you explore the decision space.

That fits beautifully with your existing gate philosophy.

---

# 3. Database Design Skill

I'd make this separate from architecture.

Architecture asks:

> "What should the system look like?"

Database design asks:

> **"Given that architecture, how should persistence work?"**

It could enforce a workflow like:

```text
Requirements
     ↓
Entities
     ↓
Relationships
     ↓
Invariants
     ↓
Access patterns
     ↓
Normalization
     ↓
Constraints
     ↓
Indexes
     ↓
Migration strategy
```

And importantly, I'd make AI ask:

> **"What invariant belongs in the database rather than merely in application code?"**

That's an incredibly valuable habit to develop.

---

# 4. API / Contract Skill

This deserves its own skill because it's a different mental model.

It should teach you to distinguish:

```text
Domain model
       ≠
Database model
       ≠
API contract
       ≠
Frontend type
```

The skill could help you reason about:

- REST/OpenAPI
    
- GraphQL
    
- Protobuf
    
- versioning
    
- compatibility
    
- DTOs
    
- validation
    
- error contracts
    
- pagination
    
- idempotency
    
- backwards compatibility
    

And it should aggressively ask:

> "Is this an internal implementation detail or part of the public contract?"

That's the kind of question you want AI repeatedly training you to ask.

---

# 5. Testing Skill

This is where your idea becomes particularly interesting.

I **wouldn't** make a testing skill whose job is simply:

> "Write tests."

That's too shallow.

I'd make it teach you to answer:

```text
What behavior are we protecting?
          ↓
What could go wrong?
          ↓
What is the appropriate test boundary?
          ↓
What should be tested?
          ↓
What should NOT be tested?
          ↓
What kind of test?
          ↓
How do we know the test is meaningful?
```

So before Claude generates a test, it might require:

> "What behavior do you believe this test should protect?"

Then you answer.

Only afterward does it help.

That would make testing another **reasoning exercise**, rather than outsourcing test-writing.

---

# 6. Debugging Skill

Interestingly, I'd keep debugging separate from your `problem-solving-gates`.

Think of:

### `problem-solving-gates`

> **How should AI interact with me while I'm debugging?**

versus:

### `debugging`

> **What debugging methodology should we use?**

The debugging skill could encode things like:

```text
Reproduce
   ↓
Observe
   ↓
Form hypothesis
   ↓
Predict evidence
   ↓
Experiment
   ↓
Update hypothesis
   ↓
Isolate
   ↓
Fix
   ↓
Regression test
```

Your existing gate then controls whether Claude is allowed to participate at each point.

That's a powerful combination.

---

# 7. Code Review Skill

I'd have a very different philosophy here.

Code review shouldn't just be:

> "Find bugs."

I'd structure it around categories:

```text
Correctness
Security
Maintainability
Architecture
Performance
Error handling
Concurrency
Testing
Observability
```

But there's another important distinction:

### Review mode

Claude can tell you what's wrong.

### Learning mode

Claude makes you discover what's wrong.

Your `problem-solving-gates` can determine which mode you're in.

That prevents your learning workflow from accidentally turning every review into answer consumption.

---

# 8. Security Skill

I'd absolutely have one eventually.

But again, make it methodological rather than a giant security checklist.

Something like:

```text
Assets
 ↓
Trust boundaries
 ↓
Threats
 ↓
Attack surface
 ↓
Controls
 ↓
Failure modes
 ↓
Verification
```

Then AI can ask questions like:

> "What does the attacker control here?"

That's much more useful for learning security than having Claude spit out OWASP terminology.

---

# 9. Performance Skill

Similar philosophy:

Don't start with:

> "Optimize this."

Start with:

```text
Observed problem?
     ↓
Measurement?
     ↓
Baseline?
     ↓
Hypothesis?
     ↓
Bottleneck identified?
     ↓
Intervention?
     ↓
Measurement again?
```

This is another place where your problem-solving gates become extremely valuable.

AI shouldn't let you call something a performance problem simply because it _feels_ slow.

---

# 10. Documentation / Decision Skill

This one might be underrated.

I'd create a skill whose job is to turn important decisions into **durable engineering knowledge**.

For example:

```text
Decision
Context
Constraints
Options considered
Decision
Consequences
Rejected alternatives
```

That's essentially ADRs, but I'd make AI responsible for detecting when something is worth recording.

For example:

> "You just made a decision that changes the source of truth for API data. This appears architecturally significant. Do you want to record it?"

You don't want 400 ADRs.

You want the **important decisions** preserved.

---

# Where agents enter the picture

This is where I would _not_ create an agent for every skill.

Instead, I'd have a smaller number of agents that orchestrate skills.

For example:

## Architecture Agent

Could invoke:

```text
problem-solving-gates
        +
architecture
        +
database-design
        +
api-contract
        +
ADR
```

Its workflow might be:

```text
Feature request
      ↓
Discover requirements
      ↓
Architecture gate
      ↓
Explore options
      ↓
User decides
      ↓
Generate architecture decision
      ↓
Create ADR
```

---

## Implementation Agent

```text
Approved architecture
        ↓
Inspect repository
        ↓
Identify affected components
        ↓
Implementation plan
        ↓
User approval
        ↓
Implement
        ↓
Tests
        ↓
Review
```

Notice:

**It shouldn't be deciding architecture.**

It's implementing an architectural decision that already exists.

---

## Testing Agent

This one could operate after implementation:

```text
Changed code
     ↓
Understand behavior
     ↓
Identify risk
     ↓
Determine test boundaries
     ↓
Run existing tests
     ↓
Add missing tests
     ↓
Evaluate failures
```

But your learning mode could prevent it from doing the reasoning for you.

---

# I'd probably end up with this architecture

```text
                         YOU
                          │
                          ▼
                 ┌─────────────────┐
                 │ Problem-Solving  │
                 │     Gates       │
                 └────────┬────────┘
                          │
            ┌─────────────┼─────────────┐
            │             │             │
            ▼             ▼             ▼
       Architecture    Testing       Debugging
          Skill          Skill          Skill
            │             │             │
            ▼             ▼             ▼
       Database        Security      Performance
        Design           Skill          Skill
            │
            ▼
       API / Contract
           Skill
            │
            ▼
       Documentation
           Skill
            │
            └──────────────┐
                           ▼
                    ┌──────────────┐
                    │    Agents    │
                    ├──────────────┤
                    │ Architecture│
                    │ Implementer  │
                    │ Testing      │
                    │ Review       │
                    └──────────────┘
```

---

# But there's one thing I'd change about your philosophy

Your current skill says:

> "Claude's contribution is deliberately limited..."

I **wouldn't make that universally true across your entire AI setup.**

I'd explicitly create different **interaction modes**.

### Learning mode

AI protects your thinking.

```text
You think → AI questions → You reason → AI verifies
```

### Collaboration mode

AI thinks alongside you.

```text
You think ↔ AI thinks
```

### Execution mode

AI does substantial work.

```text
You specify → AI executes → AI reports
```

### Review mode

AI aggressively critiques.

```text
You produce → AI challenges
```

That is more flexible than trying to make every skill behave like `problem-solving-gates`.

---

# The biggest opportunity I see

Your goal isn't really:

> **"How do I build a bunch of Claude skills?"**

It's:

> **"How do I design an AI development environment that makes me a better engineer instead of making me dependent on AI?"**

That's a much more interesting problem.

And your `problem-solving-gates` skill demonstrates that you've already identified the central danger:

**AI can make you dramatically more productive while simultaneously reducing how much engineering reasoning you personally perform.**

So I'd make that principle a **top-level design constraint for the entire system**, not just a feature of one skill.

A useful rule might ultimately be:

```text
                    ┌───────────────┐
                    │  Is this a    │
                    │ learning      │
                    │ opportunity?  │
                    └───────┬───────┘
                            │
                   ┌────────┴────────┐
                   │                 │
                  YES                NO
                   │                 │
                   ▼                 ▼
             Gate reasoning      Optimize for
             before AI help      execution
```

That gives you something much more sophisticated than a folder full of prompts: **an AI engineering system with an explicit philosophy about when AI should think, when it should challenge you, and when it should simply execute.**