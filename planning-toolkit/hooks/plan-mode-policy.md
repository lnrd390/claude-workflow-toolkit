# Execution-grade planning policy

You are in Plan mode. Optimize the plan for reliable execution by a fresh implementation agent with minimal rediscovery, not for explanatory prose.

1. **Reuse context before exploring.** Start from already loaded `CLAUDE.md`, path rules, relevant skills/memory, and any existing `.claude/context-system/` routing metadata. Treat them as hints that must still be verified where correctness matters. Do not broadly rescan the repository just to restate known architecture.
2. **Use a discovery budget.** Escalate only as needed: existing context -> exact path/symbol reads -> targeted Grep/Glob -> module exploration -> broad exploration as a last resort. Delegate noisy independent research to isolated Explore/Plan agents when useful, and ask them for terse path/symbol findings.
3. **Verify the change map.** Every file path in the final plan must be verified existing or explicitly marked `CREATE`/`DELETE`. Prefer stable symbols/classes/functions over line numbers. Never invent likely paths. If a required path genuinely cannot be determined, state the unresolved discovery explicitly instead of guessing.
4. **Preserve the request as a contract.** Record explicit requirements, important derived requirements, non-goals, constraints, compatibility expectations, and architecture decisions. Distinguish existing facts from decisions the implementer should not casually reopen.
5. **Split only when useful.** Use one increment for a small coherent task. For larger work, create the minimum number of independently valid increments. Each increment should leave the project in a consistent state and be executable by a fresh agent without reading unrelated increments.
6. **Make each increment an execution packet.** Include status, dependencies, exact repositories/files/symbols, required behavior, constraints/decisions, validation commands/tests, and objective done criteria. Mention existing patterns by path+symbol instead of copying large code blocks.
7. **Minimize execution discovery.** The implementation agent should mostly read the listed files/symbols, make the change, and validate it. Add context only when it materially prevents searching, ambiguity, or architectural drift.
8. **Do not over-document.** Optimize total planning + execution cost. Path+symbol > copied code; decision > long rationale; acceptance criterion > essay.

Use the schema below unless the task is genuinely non-code/research-only. For such tasks, include `<!-- cwt:relaxed -->` and still provide Goal, Steps, and Validation.

Required execution-plan structure:

- `# <Plan title>`
- `## Request contract`
- `## Existing context reused`
- `## Change map`
- `## Execution increments`
  - `### Increment N — <name>`
  - `Status: pending`
  - `Depends on:`
  - `Files:` with `MODIFY`, `CREATE`, or `DELETE` paths and relevant symbols
  - `Required behavior`
  - `Constraints / decisions`
  - `Validation`
  - `Done when`
- `## Final verification`

Add `<!-- cwt-plan:v1 -->` near the top so downstream execution skills can identify the plan format.
