---
name: plan-refine
description: Audit and refine an existing execution plan so downstream agents need less rediscovery and fewer architectural decisions.
disable-model-invocation: true
context: fork
agent: general-purpose
background: false
model: opus
effort: high
argument-hint: "[optional plan path]"
---

# Plan Refine

Improve an existing plan without implementing application code.

Target plan: `$ARGUMENTS`

If no path was provided, locate the most relevant active/recent `<!-- cwt-plan:v1 -->` plan in the configured plans directory or `.claude/plans/`. Do not choose a completed plan when an active one exists.

Read `${CLAUDE_SKILL_DIR}/PLAN-SCHEMA.md` and audit the target plan against it.

## Optimize for execution cost

Prioritize, in order:

1. missing or ambiguous requirements that would force an implementer to reinterpret the request;
2. speculative/unverified paths;
3. missing stable symbols or entrypoints that would force broad search;
4. increments that are too large, too coupled, or leave the project inconsistent;
5. hidden cross-repo or cross-increment dependencies;
6. missing validation/done criteria;
7. duplicated code/context that can be replaced by path+symbol references;
8. details that are cheap to rediscover and do not belong in the plan.

Reuse existing project context first. Verify only facts needed to repair the plan. Do not broadly restudy the repository when the existing plan/context already narrows the answer.

Preserve completed increment status and user-approved architecture decisions unless current source proves them impossible or stale. Record material corrections rather than silently changing intent.

Write the refined plan in place. If the target is not a CWT v1 plan, upgrade it to the schema when practical.

Finish with a compact report: plan path, changes that reduce execution discovery, and any remaining uncertainty.
