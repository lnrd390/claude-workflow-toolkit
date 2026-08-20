---
name: context-bootstrap
description: Bootstrap or repair a token-efficient, self-maintaining Claude Code context architecture for the current repository or multi-repository workspace.
disable-model-invocation: true
context: fork
agent: general-purpose
model: opus
effort: high
argument-hint: "[auto|repo|workspace|audit-only]"
---

# Context Bootstrap

Build a Claude Code context system for the current working scope so future sessions can start with the minimum useful persistent context, load domain knowledge only when relevant, and avoid repeatedly rediscovering stable project facts.

This is a configuration task. Do not modify application code, dependencies, generated artifacts, product behavior, or business data. Do not commit or push changes.

## Primary objective

Optimize for this objective, in order:

1. Correctness and preservation of project-specific knowledge.
2. Minimal always-loaded context.
3. Minimal repeated codebase discovery across sessions.
4. Minimal irrelevant context for any individual task or subagent.
5. Low maintenance cost and low risk of stale documentation.
6. Measurable, reversible improvements over time.

Do not optimize token count by removing information that prevents expensive rediscovery or repeated mistakes.

## Non-negotiable context rules

Use these rules when deciding what to persist:

- Persist only information that is stable across sessions, materially affects future decisions, and is expensive or error-prone to rediscover.
- Prefer a canonical file/path reference over copying source code or documentation.
- Prefer deletion over duplication.
- Prefer path-scoped rules over unconditional rules.
- Prefer skills over multi-step procedures in CLAUDE.md.
- Prefer supporting files inside a skill over a huge SKILL.md.
- Prefer isolated subagent context for broad exploration or noisy investigation.
- Prefer native auto-memory for learned, non-canonical observations.
- Never persist facts that can be discovered cheaply in roughly one or two targeted reads/searches unless they are critical invariants.
- Never generate a giant CODEBASE.md, repository dump, directory listing, dependency inventory, or architecture encyclopedia merely to save future exploration.
- Do not use CLAUDE.md imports as a token-saving mechanism: imports still load at startup.
- Avoid unconditional `.claude/rules/*.md` unless the rule is genuinely universal.
- Keep every always-loaded instruction concise, specific, non-duplicated, and actionable.
- Treat existing project instructions as valuable evidence. Merge, relocate, or trim them carefully; never overwrite blindly.

## 1. Determine the managed scope automatically

Honor `$ARGUMENTS` when it explicitly contains `repo`, `workspace`, or `audit-only`. Otherwise infer the scope.

Use the current working directory and Git metadata:

- If the current directory is inside a Git repository, manage that repository from its Git top-level directory.
- If the current directory is not inside a Git repository and contains multiple genuine Git repositories below it, treat the current directory as a multi-repository workspace.
- Otherwise treat the current directory as a standalone project directory.

When detecting nested repositories, exclude dependency, cache, generated, vendored, build, and hidden tool directories such as `.git`, `node_modules`, `vendor`, `dist`, `build`, `.next`, `.cache`, `.venv`, `venv`, `target`, coverage output, and similar directories discovered in the project.

For a multi-repository workspace:

- The workspace root is only a coordination layer.
- Each child Git repository remains an independent context scope.
- Existing child `CLAUDE.md`, `.claude/`, rules, skills, agents, and settings must be audited rather than flattened into the parent.
- Parent instructions should contain only cross-repository facts that are useful when a task spans repositories.
- Repo-specific information belongs in that repo, so it loads only when Claude enters that subtree.

If this is `audit-only`, perform every analysis and produce the proposed changes, but do not write files.

## 2. Inventory existing Claude and agent configuration first

Before proposing anything, inspect existing relevant configuration, including when present:

- `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`
- `.claude/rules/**`
- `.claude/skills/**`
- `.claude/agents/**`
- `.claude/settings.json` and `.claude/settings.local.json`
- `.claude/hooks/**`
- `AGENTS.md`
- Cursor, Copilot, Windsurf, Cline, Devin, or other agent instruction files
- project documentation that is already canonical for architecture, build, test, deployment, or domain conventions

Detect contradictions, stale paths, repeated instructions, oversized always-loaded files, unconditional rules that should be scoped, procedures that should be skills, and skills that duplicate source-of-truth documentation.

Do not duplicate another agent instruction file merely because it exists. Reuse or reference a canonical source only when doing so does not increase startup context unnecessarily.

## 3. Explore the project with a bounded discovery pass

Learn enough to design the context routing system, not enough to rewrite the documentation.

Inspect high-signal sources first:

- repository/workspace manifests and lockfiles
- build, test, lint, typecheck, formatting, and task-runner configuration
- CI/CD definitions
- package/module boundaries
- entry points and routing/registration files
- schemas, migrations, API specifications, generated-code boundaries
- test layout and representative tests
- existing architecture/decision documents
- top-level README only when it is maintained and authoritative

Because this skill normally runs in an isolated fork, keep broad discovery bounded inside this forked context. If you are running these instructions outside a fork and Explore subagents are available, use them for large independent areas and require terse summaries with concrete file references. Do not depend on nested subagent spawning from inside the fork.

Classify every candidate fact into one of these buckets:

- ALWAYS: needed in nearly every session.
- CONDITIONAL: needed only for specific paths/domains.
- ON_DEMAND: workflow/reference material needed for certain tasks.
- ISOLATED: work better delegated to a specialized subagent with separate context.
- LEARNED: useful empirical knowledge suited to auto-memory, not canonical instructions.
- DO_NOT_PERSIST: cheap to rediscover, obvious from code, volatile, or redundant.

## 4. Build the native Claude Code architecture

Use native mechanisms. Adapt the exact file set to the project; do not create empty scaffolding just to match a template.

### Always-loaded layer

Create or refine the project/workspace `CLAUDE.md` (or `.claude/CLAUDE.md` if that is already the project's convention).

It should contain only genuinely universal information such as:

- the minimum project/workspace identity and boundaries needed to orient Claude
- essential canonical commands when they are non-obvious or easy to get wrong
- critical cross-cutting invariants
- high-cost pitfalls Claude must know before touching the code
- a very short context-maintenance contract defined below

Targets:

- Prefer <= 100 lines for a repository root.
- Prefer <= 60 lines for a multi-repository workspace root.
- Never exceed 200 lines without a documented reason.

Do not include long directory maps, dependency lists, generated API summaries, tutorials, or copied source snippets.

### Conditional layer

Create/refine `.claude/rules/**/*.md` for domain- or path-specific instructions.

- Add `paths:` frontmatter whenever the rule is not universal.
- Scope rules as narrowly as practical without creating dozens of tiny files.
- Group related paths when the same rule really applies to all of them.
- Remove or merge contradictory and duplicate rules.
- Do not create a rule whose content is merely obvious from the matching source files.

### On-demand layer

Create/refine `.claude/skills/<name>/SKILL.md` only for recurring procedures or substantial reference knowledge that should not always be loaded.

- Keep descriptions short and discriminative.
- Keep SKILL.md focused; put large references/examples in supporting files.
- Do not create a skill for a one-off task.
- Default project workflow skills to model-invocable only when automatic invocation is genuinely useful.
- Use `disable-model-invocation: true` for project workflows whose timing should remain user-controlled.
- Avoid a large catalog of vaguely described auto-invocable skills because skill descriptions themselves consume context.

### Isolated agent layer

Create/refine `.claude/agents/*.md` only when context isolation has a clear benefit, for example:

- a large backend/frontend split
- database/schema work with specialized reference material
- review/security tasks that read many files and return a compact result
- cross-repository coordination that should not pollute the main session

Give each agent the smallest useful toolset and preload only the skills it actually needs. Do not create agents just to mirror team job titles.

### Learned knowledge

Use native auto-memory for empirical learnings, debugging observations, user corrections, and non-canonical patterns. Do not copy those into CLAUDE.md unless they become stable project rules.

## 5. Install a tiny self-maintenance contract

Add a concise section to the appropriate always-loaded CLAUDE.md. Preserve its meaning, but phrase it compactly for the project:

> When a task makes an existing Claude instruction, rule, skill, agent definition, canonical path, build/test command, or architecture assumption false or materially incomplete, update the relevant `.claude` configuration in the same task. Do not add facts merely because they might be useful. Prefer delete > replace > add; path-scoped rule > global rule; skill > procedure in CLAUDE.md. Do not run broad context audits automatically. Treat `.claude/context-system/` as maintainer state, not normal task context.

This contract must stay short. It is the fallback guarantee even if hooks are unavailable.

## 6. Add conservative deterministic maintenance triggers when safe

Prefer command hooks, not prompt hooks or experimental agent hooks, for automatic maintenance triggering.

If the environment supports a reliable local scripting runtime, create a small project-local maintenance trigger under `.claude/hooks/` and merge it into `.claude/settings.json` without destroying existing settings.

The trigger should:

1. Observe successful `Edit|Write` operations at negligible token cost.
2. Ignore changes inside `.claude/context-system/`, generated directories, dependency directories, and other irrelevant paths.
3. Mark context as dirty only for high-signal files/patterns that can invalidate persistent context, such as:
   - workspace/package/project manifests
   - build/test/lint/typecheck configuration
   - CI/CD configuration
   - schema/migration/API-spec sources of truth
   - route/plugin/module registries when architecturally important
   - container/orchestration configuration
   - files that existing CLAUDE/rules/skills explicitly cite as canonical sources
4. Record only the relevant changed paths in a runtime dirty file.
5. On `Stop`, if the dirty marker exists and `stop_hook_active` is false, block stopping once with a short instruction to perform a bounded reconciliation of only the affected Claude configuration.
6. On the continuation stop (`stop_hook_active` true), allow stopping and clean up stale runtime markers.
7. Never trigger a full repository audit automatically.
8. Never invoke another Claude process from a hook.
9. Never make an LLM call from the hook.
10. Fail open if the hook cannot run safely.

Generate the implementation in the most portable runtime already present on the machine/project. Do not install a runtime or dependency solely for this feature.

If a robust hook cannot be implemented safely, skip it and record `policy_only` maintenance mode in the context-system state.

## 7. Create a non-loaded context control plane

Create `.claude/context-system/` as maintainer-only state. Nothing in this directory should be imported by CLAUDE.md or unconditional rules.

Create only useful files, typically:

- `state.json` — schema version, managed scope, mode, last bootstrap/optimization time, Claude Code version if discoverable, maintenance mode, telemetry status.
- `watch-patterns.txt` — high-signal paths/patterns used by the maintenance trigger.
- `optimization-log.jsonl` — one JSON object per deliberate optimization experiment/change.
- `snapshots/` — compact static measurements taken by bootstrap/optimizer.
- `TELEMETRY.md` — how real usage telemetry can be connected when available.
- a local `.gitignore` for runtime dirty files and raw/local telemetry.

Do not put ordinary project documentation here.

## 8. Record static baseline metrics

Create a compact baseline snapshot before and after the bootstrap. Do not pretend these are exact token counts.

At minimum record:

- lines and characters in root always-loaded CLAUDE.md files
- lines and characters in unconditional project rules
- count of path-scoped rules
- count of project skills
- total characters in model-visible skill names/descriptions when determinable
- count of project agents
- number of nested CLAUDE.md files touched by this managed scope
- stale/broken path references found
- duplicate instruction groups removed or consolidated
- approximate always-loaded character total for files under this project's control

If practical, include the current Git commit SHA as a correlation point.

## 9. Integrate real telemetry only when a sink already exists

Claude Code can expose real token, cache, cost, model, skill, agent, and query-source telemetry through OpenTelemetry.

Detect whether telemetry is already enabled and whether there is an accessible configured sink/backend or an existing project convention for querying it.

If yes:

- record how the optimizer can query or import aggregated project/session data
- prefer aggregate data over raw prompt contents
- do not copy secrets into project files
- do not enable verbose tool-input logging unless it is already explicitly used and appropriate

If no usable telemetry sink exists:

- do not install a collector
- do not enable noisy console exporters
- set telemetry status to `unavailable`
- write the exact metrics that would be useful later into `TELEMETRY.md`
- continue using static measurements and repository evidence

Never invent token/cost measurements.

## 10. Verification

Before finishing:

- validate all JSON and YAML/frontmatter you created or edited
- ensure hook scripts are executable where required
- ensure hook paths are relative/portable for the current platform
- verify settings were merged rather than overwritten
- verify existing project behavior/configuration outside Claude context files is unchanged
- verify there are no unconditional rules that should obviously be path-scoped
- verify no large source/docs were imported into CLAUDE.md
- verify root and nested context do not contradict each other
- verify multi-repository parent context contains only cross-repository knowledge
- verify runtime telemetry/dirty artifacts are ignored locally
- take the post-bootstrap static snapshot

Finish with a concise report containing:

- detected scope: repo, standalone project, or multi-repo workspace
- files created/changed
- what loads always vs conditionally vs on demand vs in isolated agents
- maintenance mode: hook-assisted or policy-only
- telemetry status: connected or unavailable
- before/after static context measurements
- any important limitation that could not be resolved automatically

Do not end with generic suggestions. The configured project should be usable immediately in a fresh Claude Code session.
