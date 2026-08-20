---
name: plan-next-step
description: Execute the next ready increment from a CWT execution plan with minimal rediscovery, then update its status.
disable-model-invocation: true
context: fork
agent: general-purpose
background: false
model: sonnet
effort: medium
argument-hint: "[optional plan path]"
---

# Plan Next Step

Execute exactly one ready increment from an execution plan.

Target plan: `$ARGUMENTS`

If no plan path is supplied, find the most relevant active/recent `<!-- cwt-plan:v1 -->` plan in the configured plans directory or `.claude/plans/`.

## Selection

- Select the first `pending` increment whose dependencies are `completed`.
- If none is ready, report why and stop.
- Change its status to `in_progress` before implementation.

## Execution contract

Treat the selected increment as the primary execution packet.

1. Read the plan's Request contract, Change map, selected increment, and only dependency facts needed for it. Do not re-plan the full feature.
2. Read the listed files/symbols first.
3. Search outside the listed files only when the plan is stale, a referenced symbol moved, compilation/tests expose another required change, or correctness cannot otherwise be established.
4. Preserve stated DECISION/CONSTRAINT items unless current source makes them impossible. If so, stop and explain rather than silently redesigning the feature.
5. Do not implement later increments opportunistically.
6. Run the increment's validation. Add a narrowly necessary validation step only when the listed checks are insufficient to establish correctness.
7. If successful, set status to `completed` and add a terse `Execution note:` only for information future increments actually need.
8. If blocked, set status to `blocked` and add a concise blocker. Do not mark complete.

Do not commit or push unless the plan explicitly requires it or the user separately instructed it.

Finish with: increment executed, files actually changed, validation result, and next ready increment if one exists.
