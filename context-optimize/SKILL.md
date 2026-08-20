---
name: context-optimize
description: Audit and improve an existing Claude Code context architecture using accumulated evidence, static context measurements, and real telemetry when available.
disable-model-invocation: true
context: fork
agent: general-purpose
model: opus
effort: high
argument-hint: "[optional: conservative|normal|aggressive]"
---

# Context Optimize

Improve the current project's Claude Code context system based on evidence. The goal is not to make `.claude` prettier; the goal is to reduce unnecessary context and repeated discovery while preserving or improving task quality.

Do not modify application code, dependencies, product behavior, or business data. Do not commit or push changes.

## Optimization objective

Minimize expected context/token cost and rediscovery effort subject to these constraints:

1. Project-specific correctness must not regress.
2. Critical instructions must remain available at the time they are needed.
3. Maintenance complexity and staleness risk must not increase without evidence of a compensating benefit.
4. Changes should be measurable and reversible.

A lower token number is not automatically an improvement if Claude then has to reread the repository or makes more mistakes.

## 1. Load the existing control plane

Inspect:

- the applicable `CLAUDE.md` hierarchy
- `.claude/rules/**`
- `.claude/skills/**`
- `.claude/agents/**`
- `.claude/settings*.json`
- `.claude/hooks/**`
- `.claude/context-system/**`
- relevant nested Claude configuration in child repositories/subprojects
- Git history/diff for Claude configuration since the last optimization, when available

If `.claude/context-system/` does not exist, reconstruct a minimal state/snapshot layer before optimizing. Do not require rerunning the bootstrap skill.

Read previous `optimization-log.jsonl` experiments first. Evaluate pending experiments before introducing new ones.

## 2. Gather evidence

### Static evidence

Measure the current configuration at minimum:

- always-loaded CLAUDE.md characters/lines under this scope
- unconditional rule characters/lines
- path-scoped rule count and coverage intent
- model-visible skill catalog size when determinable
- skill bodies and supporting references that duplicate other sources
- agent count and preloaded skill footprint
- stale or broken file references
- contradictory instructions
- duplicated instruction clusters
- imported files that inflate startup context
- rules whose scope is broader than their actual applicability
- procedures embedded in always-loaded context
- canonical facts duplicated from code/docs

Compare against prior snapshots.

### Real usage evidence

If the control plane declares an accessible telemetry source, aggregate data since the last optimization. Prefer medians/rates and normalize by session/prompt count where possible.

Useful Claude Code telemetry includes:

- input tokens
- output tokens
- cache read tokens
- cache creation tokens
- estimated cost
- model
- `query_source` (main/subagent/auxiliary)
- skill attribution
- agent attribution
- active time

If tool-detail telemetry is explicitly available, also inspect repeated Read/Grep/Glob patterns and large tool-result costs, but do not enable sensitive verbose logging merely for this audit.

Do not compare raw total tokens across periods with very different task volume. Prefer measures such as input tokens per prompt/session, main-vs-subagent share, cache ratios, and repeated discovery patterns.

If fewer than roughly five representative sessions are available after a change, treat telemetry conclusions as low-confidence unless the signal is extreme.

If no real telemetry is available, say so in the experiment record and rely on static evidence only. Never invent usage data.

## 3. Evaluate previous experiments

For every experiment with `decision: pending`:

- identify the change and intended mechanism
- compare the relevant before/after static metrics
- compare real usage metrics when available and reasonably comparable
- inspect whether the change caused new rediscovery, confusion, missed rules, or maintenance churn
- choose one: `keep`, `revert`, `refine`, or `insufficient-data`
- record the evidence and confidence

Revert an experiment only when the configuration change is isolated and the intended prior state can be recovered safely from Git/history or the log. Never overwrite unrelated later edits.

## 4. Find the highest-value optimization opportunities

Prioritize candidates in this order:

1. Delete stale, contradictory, duplicated, or cheaply derivable always-loaded text.
2. Convert unconditional rules to path-scoped rules.
3. Move multi-step procedures out of CLAUDE.md into on-demand skills.
4. Move detailed skill content into supporting files loaded only when needed.
5. Shorten vague or redundant skill descriptions.
6. Remove low-value auto-invocable skills that increase the skill catalog without improving behavior.
7. Move repo-specific context from a multi-repo parent into nested repo configuration.
8. Split noisy exploration/review work into specialized isolated agents only when evidence shows repeated main-context pollution.
9. Reduce agent preloaded skills when they are rarely useful.
10. Repair maintenance triggers/watch patterns that miss genuine architecture changes or fire too often.

Do not create new infrastructure unless it fixes an observed problem.

## 5. Use an experiment discipline

Do not make a large bundle of speculative changes.

Default to one to three independent, high-confidence improvements per optimization run. Use `$ARGUMENTS` to adjust:

- `conservative`: one very high-confidence change
- `normal` or empty: up to three reasonably independent changes
- `aggressive`: more changes are allowed, but each still needs evidence and must remain reversible

Before each change, append an experiment record with:

- unique id/date
- Git correlation point if available
- evidence window
- problem observed
- metrics_before
- proposed change
- mechanism/hypothesis
- expected measurable effect
- risk
- confidence
- `decision: pending`

After applying the change:

- validate configuration
- take a new static snapshot
- add `metrics_after_static`
- leave the experiment `pending` for real usage evaluation on a later run unless the change merely fixes an objectively stale/broken instruction

For objectively stale/broken fixes, the decision may be `keep` immediately with the reason recorded.

## 6. Maintain the routing architecture

Keep the same hierarchy of intent:

- ALWAYS: minimal CLAUDE.md facts/invariants
- CONDITIONAL: path-scoped rules
- ON_DEMAND: skills/supporting files
- ISOLATED: subagents
- LEARNED: auto-memory
- CONTROL PLANE: `.claude/context-system/`, never imported into normal context

Targets remain:

- root repo CLAUDE.md preferably <= 100 lines
- multi-repo workspace CLAUDE.md preferably <= 60 lines
- no CLAUDE.md over 200 lines without a documented reason
- no unconditional rule that is obviously domain/path-specific
- no giant codebase summaries
- no broad automatic LLM maintenance hooks

## 7. Check multi-repository behavior explicitly

If the managed scope contains child repositories:

- verify parent context is only cross-repo context
- verify child-specific knowledge stays in child CLAUDE/rules/skills
- verify existing nested config is not duplicated at the parent
- verify unrelated child CLAUDE files are not being loaded unnecessarily for common sessions; use `claudeMdExcludes` only when there is clear evidence of unwanted ancestor/sibling context
- keep workspace coordination instructions tiny

## 8. Validate self-maintenance

Inspect the maintenance contract and deterministic hooks.

The desired behavior is:

- ordinary source edits: no context-maintenance LLM work
- high-signal architecture/config/source-of-truth edits: one bounded reminder before task completion
- no recursive Claude invocation
- no agent/prompt hook running on every turn
- no permanent dirty marker churn
- no repeated edits to `.claude` when nothing became stale

If the hook creates more overhead than it saves, narrow or remove it and rely on the concise maintenance contract.

## 9. Finish with a compact optimization report

Report only:

- evidence window and telemetry availability
- experiments from the previous run and their decisions
- changes made now and why
- static before/after measurements
- real usage deltas when statistically meaningful
- new pending experiment ids and what should improve if they work
- any unresolved limitation

If evidence does not justify a change, make no change and say that the current configuration remains the best supported design.
