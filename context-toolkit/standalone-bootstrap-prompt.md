# Standalone Claude Code context-bootstrap prompt

Use this when you do not have the global skill installed yet. Paste it into Claude Code from the repository or multi-repository workspace you want to configure.

---

Analyze the current working scope and bootstrap a token-efficient, self-maintaining Claude Code context architecture.

Do not modify application code, dependencies, product behavior, generated artifacts, business data, or Git history. Do not commit or push.

Your objective, in order, is:
1. preserve correctness and project-specific knowledge;
2. minimize always-loaded context;
3. minimize repeated codebase discovery across sessions;
4. load domain/task context only when relevant;
5. isolate broad/noisy exploration in subagents;
6. keep the context system maintainable, measurable, and resistant to staleness.

Infer the scope automatically:
- if the current directory is inside a Git repository, manage the Git top-level repository;
- if it is not inside a repository but contains multiple genuine Git repositories, treat it as a multi-repository workspace;
- otherwise treat it as a standalone project directory.

For a multi-repository workspace, keep the parent as a tiny coordination layer and keep repo-specific context inside each child repository. Preserve and audit existing child `.claude` and `CLAUDE.md` configuration rather than flattening it.

Before writing anything, inspect existing Claude/agent configuration and high-signal project sources. Use bounded exploration and Explore subagents for large independent areas. Do not generate a giant repository summary.

Classify persistent information into:
- ALWAYS: minimal CLAUDE.md facts needed in nearly every session;
- CONDITIONAL: path-scoped `.claude/rules/`;
- ON_DEMAND: `.claude/skills/` plus supporting files;
- ISOLATED: `.claude/agents/` for work that benefits from separate context;
- LEARNED: native auto-memory;
- DO_NOT_PERSIST: cheap-to-rediscover, obvious, volatile, or duplicated facts.

Apply these rules:
- persist only stable, high-value, expensive-to-rediscover knowledge;
- prefer canonical path references over copied code/docs;
- prefer deletion over duplication;
- prefer path-scoped rule over global rule;
- prefer skill over multi-step procedure in CLAUDE.md;
- do not use CLAUDE.md imports as a token-saving mechanism;
- keep root CLAUDE.md preferably <=100 lines (<=60 for a multi-repo workspace root) and never >200 without a strong reason;
- avoid unconditional rules unless genuinely universal;
- keep skill descriptions short because model-visible skill catalogs consume context;
- create agents only when context isolation has a concrete benefit;
- never overwrite existing configuration blindly.

Add a very short always-loaded maintenance contract: when a task makes an existing Claude instruction, canonical path, build/test command, rule, skill, agent definition, or architecture assumption false or materially incomplete, update the relevant Claude configuration in the same task. Do not add speculative facts. Prefer delete > replace > add. Do not run broad context audits automatically.

When safe, add conservative deterministic command hooks that cost essentially no tokens during normal work:
- observe successful Edit/Write operations;
- mark context dirty only when high-signal architecture/config/source-of-truth files change;
- on Stop, block once with a short request for a bounded reconciliation of only affected Claude configuration;
- never launch another Claude process;
- never use an LLM hook on every turn;
- fail open if the hook cannot run safely.
If a portable safe hook is not possible, rely on the maintenance contract only.

Create a non-loaded `.claude/context-system/` control plane with compact state, watch patterns, static snapshots, and an optimization experiment log. Never import this directory into normal session context.

Take before/after static measurements including root CLAUDE/rule lines and characters, path-scoped rule count, project skill count, model-visible skill description size when determinable, agent count, stale references, duplicate instructions, and approximate always-loaded characters. Do not call these exact token counts.

Detect existing Claude Code OpenTelemetry configuration. If a real telemetry sink already exists, record how a future optimizer can query aggregate token/cache/cost/model/skill/agent/query-source metrics. If none exists, do not install or enable a noisy collector/exporter; mark real telemetry unavailable and continue with static evidence. Never invent usage data.

Validate JSON, YAML/frontmatter, hook executability/paths, settings merges, nested context behavior, and that no application files were changed.

Finish by reporting:
- detected scope;
- files created/changed;
- what loads always, conditionally, on demand, and in isolated agents;
- maintenance mode;
- telemetry status;
- before/after static context measurements;
- unresolved limitations only if material.

Implement the configuration now. Do not stop after proposing it.
