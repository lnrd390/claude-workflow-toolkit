# Standalone execution-grade planning prompt

Use this when you cannot install the CWT hook/skill integration.

You are creating an implementation plan for another coding agent. Optimize for reliable execution with minimal codebase rediscovery, not for explanatory prose.

Before broad exploration, consume any already available project context (CLAUDE.md, scoped rules, relevant skills/memory, architecture docs, context-system metadata). Verify task-critical facts against current source. Escalate discovery progressively: exact path/symbol reads -> targeted Grep/Glob -> bounded module exploration -> broad exploration only as a last resort.

Produce a verified change map. Never invent likely paths: verify existing files, mark deliberate new paths CREATE and deletions DELETE, and prefer stable symbols/functions/classes over line numbers.

Turn the request into an execution contract containing explicit requirements, derived requirements, non-goals, constraints, compatibility expectations, and architecture decisions. Split the work only when useful: each increment must be independently executable by a fresh agent and leave the project coherent.

For every increment include status, dependencies, exact repositories/files/symbols, required behavior, constraints/decisions, validation, and objective done criteria. Reference existing patterns by path+symbol rather than copying large code blocks. Include only context that prevents meaningful searching, ambiguity, or architectural drift.

Use this structure:

<!-- cwt-plan:v1 -->
# <title>
## Request contract
## Existing context reused
## Change map
## Execution increments
### Increment 1 — <name>
Status: pending
Depends on: ...
#### Goal
#### Files
#### Existing behavior / facts
#### Required behavior
#### Constraints / decisions
#### Validation
#### Done when
## Final verification

The implementation agent should mostly be able to read the listed files/symbols, execute, and validate rather than restudy the repository.
