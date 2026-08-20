---
name: execution-plan
description: Build an execution-grade implementation plan that minimizes rediscovery for downstream agents.
disable-model-invocation: true
context: fork
agent: general-purpose
background: false
model: opus
effort: high
argument-hint: "[task description]"
---

# Execution Plan

Create a high-confidence implementation plan for:

$ARGUMENTS

Do not implement application code. Do not commit or push.

Your consumer is a fresh implementation agent that should spend as few tokens as practical rediscovering architecture, paths, and requirements.

## Planning protocol

1. Read `${CLAUDE_SKILL_DIR}/PLAN-SCHEMA.md` before finalizing the plan.
2. Reuse existing project context before broad exploration: applicable `CLAUDE.md`, rules, relevant skills/memory, project docs, and `.claude/context-system/` when present. Do not assume the Context Toolkit exists.
3. Treat persisted context as routing/decision evidence, not unquestionable truth. Verify task-critical facts against current source.
4. Spend discovery progressively: exact known paths/symbols first, then targeted search, then bounded module exploration. Broad scans are a last resort.
5. For large independent unknowns, use isolated Explore/Plan subagents when available and require terse findings with exact paths/symbols. Avoid redundant agents exploring the same area.
6. Convert the request into explicit requirements, derived requirements, non-goals, constraints, compatibility expectations, and decisions.
7. Build a verified change map. Existing paths must exist; new paths must be explicitly `CREATE`; deletions must be verified. Prefer symbols over line numbers.
8. Split into the minimum number of independently valid increments. A small change should remain one increment.
9. Each increment must be executable by a fresh agent using mostly the listed files/symbols. Include behavior, decisions/constraints, validation, and done criteria. Reference existing patterns by path+symbol rather than copying code.
10. Optimize total planning + execution tokens, not plan length in isolation.

## Saving the plan

Prefer the project's configured `plansDirectory` if discoverable. When project-local plans are configured as `.claude/plans`, save there. Otherwise save to `.claude/plans/` only when doing so is consistent with the project; if not, return the plan and report where Claude Code currently stores plans.

Use a short kebab-case filename. Add `<!-- cwt-plan:v1 -->` near the top.

Finish by reporting only the plan path, number of increments, and any unresolved discovery that would materially affect execution.

## Reference

The complete schema is bundled at `${CLAUDE_SKILL_DIR}/PLAN-SCHEMA.md`.
