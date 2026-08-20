# Context Toolkit

> Part of [Claude Workflow Toolkit](../README.md).  
> Unofficial community toolkit for Claude Code. Not affiliated with or endorsed by Anthropic.

Context Toolkit provides two global, manual-only Claude Code skills:

- `context-bootstrap` — one-shot setup or repair of a token-efficient `.claude` architecture.
- `context-optimize` — periodic, evidence-driven optimization of that architecture.

The goal is to reduce repeated codebase rediscovery and unnecessary always-loaded context while still giving Claude enough information to work correctly.

The toolkit is designed for both single repositories and project folders containing multiple repositories.

---

## How it works

The Context Toolkit organizes project knowledge by loading cost and relevance:

```text
ALWAYS
    ↓
CLAUDE.md
small, universal project facts only

CONDITIONAL
    ↓
.claude/rules/
path-scoped instructions

ON DEMAND
    ↓
.claude/skills/
procedures and detailed reference knowledge

ISOLATED
    ↓
.claude/agents/
specialized work in separate contexts

LEARNED
    ↓
Claude Code auto-memory
empirical, non-canonical knowledge

DO NOT PERSIST
    ↓
cheaply rediscoverable information
```

The core principle is:

> Persist only information whose future rediscovery costs more than keeping it available.

The toolkit does **not** try to eliminate all code reading. Claude should still inspect task-relevant implementation before changing it.

---

# Skills

## `/context-bootstrap`

`context-bootstrap` analyzes the directory from which Claude Code is started and builds or repairs a `.claude` architecture optimized for context efficiency.

It is intentionally generic.

It can be run from:

```text
single-repo/
├── .git/
└── ...
```

or from a workspace containing multiple repositories:

```text
product-workspace/
├── backend/
│   └── .git/
├── frontend/
│   └── .git/
├── mobile/
│   └── .git/
└── infrastructure/
    └── .git/
```

The bootstrap determines the topology itself and adapts the context architecture to it.

Typical responsibilities include:

- keeping root `CLAUDE.md` minimal;
- creating path-scoped rules where appropriate;
- moving procedural knowledge into on-demand skills;
- creating specialized agents only where useful;
- avoiding duplicated source-code documentation;
- keeping repository-specific knowledge close to its repository;
- creating a lightweight context maintenance/control layer where useful;
- excluding irrelevant generated files or sensitive paths where appropriate;
- preserving existing useful Claude Code configuration instead of blindly replacing it.

The bootstrap is designed to prefer:

```text
file reference > copied source code
path-scoped rule > global rule
skill > procedural CLAUDE.md content
agent-local knowledge > global knowledge
deletion > duplication
targeted discovery > broad repository scanning
```

It should not persist information merely because it *might* be useful.

Information that can be rediscovered cheaply with one or two targeted reads/searches should normally stay out of persistent context.

---

## `/context-optimize`

`context-optimize` audits an existing context architecture after it has seen real use.

Its purpose is not simply to rewrite `.claude`, but to improve it according to measurable criteria.

It can:

- detect stale paths and architectural assumptions;
- remove duplicated instructions;
- shrink always-loaded context;
- move overly specific global knowledge into scoped rules or skills;
- review skill and agent boundaries;
- compare current configuration against previous snapshots;
- evaluate prior optimization experiments;
- use real Claude Code telemetry when available;
- record whether a change should be kept, refined, reverted, or left pending for more data.

The optimizer should prefer small, reversible changes over large speculative rewrites.

---

# Installation

From the root of the `claude-workflow-toolkit` repository:

```bash
mkdir -p ~/.claude/skills

cp -R context-toolkit/context-bootstrap \
  ~/.claude/skills/context-bootstrap

cp -R context-toolkit/context-optimize \
  ~/.claude/skills/context-optimize
```

If those directories already exist, review or replace their `SKILL.md` files rather than accidentally nesting another copy inside them.

You can check your installed Claude Code version with:

```bash
claude --version
```

Both skills are configured as manual-only skills, so they are invoked explicitly rather than automatically by Claude.

---

# Usage

## Single repository

Start Claude Code from the repository root:

```bash
cd /path/to/repository
claude
```

Then run:

```text
/context-bootstrap
```

For an audit without writing changes:

```text
/context-bootstrap audit-only
```

After bootstrap, start a fresh Claude Code session so you can observe the final context-loading behavior from a clean session.

Useful diagnostics include:

```text
/context
/skills
/hooks
/doctor
```

You do not need to run these on every session. They are mainly useful after initial setup or when debugging the configuration.

---

## Multi-repository project folder

Suppose your project looks like this:

```text
my-product/
├── backend/
│   └── .git/
├── frontend/
│   └── .git/
├── mobile/
│   └── .git/
└── infra/
    └── .git/
```

Start Claude Code from the project/workspace root:

```bash
cd /path/to/my-product
claude
```

Then run:

```text
/context-bootstrap
```

The intended result is a very small workspace-level coordination layer, with repository-specific knowledge kept near each child repository.

Conceptually:

```text
my-product/
├── CLAUDE.md
├── .claude/
│
├── backend/
│   ├── CLAUDE.md
│   └── .claude/
│
├── frontend/
│   ├── CLAUDE.md
│   └── .claude/
│
└── infra/
    ├── CLAUDE.md
    └── .claude/
```

The exact structure is chosen by the bootstrap based on the actual project. It should not create files or directories merely to match a template.

For a task concerning only one repository, starting Claude Code directly inside that child repository will often provide the smallest working scope.

---

# Normal usage after bootstrap

After the initial bootstrap, ordinary development should look normal.

Start Claude Code and state the task:

```text
Implement ...
```

or enter Plan mode and ask for a plan.

The intended behavior is:

- universal context is already available;
- path-specific rules become relevant only where needed;
- detailed procedures remain on-demand;
- repository-wide discovery is avoided unless necessary;
- investigations that would create large amounts of temporary context can be isolated in subagents;
- Claude still reads the actual code involved in the task before editing it.

You should **not** rerun `/context-bootstrap` for every session.

The context architecture should maintain itself conservatively as the project evolves, with periodic deeper optimization handled by `/context-optimize`.

---

# Periodic optimization

After several representative sessions, or after meaningful architectural changes, run:

```text
/context-optimize
```

Optional variants:

```text
/context-optimize conservative
/context-optimize aggressive
```

A useful optimization loop is:

```text
baseline
   ↓
small context change
   ↓
real project usage
   ↓
measure
   ↓
/context-optimize
   ↓
KEEP / REFINE / REVERT / INSUFFICIENT DATA
```

This avoids repeatedly changing `.claude` based only on intuition.

---

# Context system data

When useful, the bootstrap may create a control-plane directory such as:

```text
.claude/
└── context-system/
    ├── state.json
    ├── watch-patterns.txt
    ├── optimization-log.jsonl
    ├── snapshots/
    └── TELEMETRY.md
```

This data is for maintenance and optimization.

It should **not** be imported into normal Claude context merely because it exists.

Possible data includes:

- approximate always-loaded context size;
- unconditional rule footprint;
- number of path-scoped rules;
- skill metadata footprint;
- stale references;
- duplicate instructions;
- Git revision;
- previous optimization experiments;
- telemetry availability.

Static character counts or approximations should never be presented as exact token measurements.

---

# Real token telemetry

Claude Code can expose OpenTelemetry data including metrics or events related to:

- input tokens;
- output tokens;
- cache reads;
- cache creation;
- cost;
- model;
- skill;
- agent;
- query source;
- session activity.

Context Toolkit deliberately does **not** install or enable an observability stack automatically.

If an accessible telemetry sink is already configured, the optimizer can use it.

Otherwise the toolkit falls back to static configuration measurements and explicitly records that real token telemetry is unavailable.

This avoids adding a large monitoring system merely to reduce token usage.

---

# Relationship with Planning Toolkit

Context Toolkit and [Planning Toolkit](../planning-toolkit/README.md) are independent, but complementary.

Context Toolkit answers:

> What should Claude already know, and when should that knowledge load?

Planning Toolkit answers:

> Given a task, what exact work should an implementation agent perform?

Together:

```text
existing project context
        ↓
minimal targeted discovery
        ↓
execution-grade plan
        ↓
focused implementation
```

Planning Toolkit should reuse context produced by Context Toolkit when available, but must continue to work when Context Toolkit has never been installed on a project.

---

# Skill behavior

The two global skills are intentionally manual-only.

They use a forked context for the expensive audit/optimization work so that broad repository analysis does not unnecessarily pollute the main working conversation.

The toolkit intentionally relies on documented Claude Code primitives rather than assuming a particular project structure.

Claude Code evolves quickly, so toolkit behavior should occasionally be checked against current Claude Code documentation and releases.

---

# Standalone bootstrap prompt

If you do not want to install the global skill, you can use:

[`standalone-bootstrap-prompt.md`](standalone-bootstrap-prompt.md)

Copy its contents into Claude Code from the project directory you want to bootstrap.

The installed skill is preferable for repeated use because it is easier to invoke consistently.

---

# Design principles

The Context Toolkit follows these general rules:

```text
minimal always-loaded context
        >
large global documentation

existing knowledge
        >
repeated broad discovery

path + symbol
        >
copied implementation

canonical project fact
        >
temporary observation

on-demand knowledge
        >
always-loaded procedural detail

measurement
        >
guesswork

small reversible optimization
        >
large speculative rewrite
```

The best context architecture is not the one containing the most documentation.

It is the one that minimizes the combined cost of:

```text
persistent context
+
rediscovery
+
incorrect assumptions
+
maintenance
```

while preserving reliable execution.

---

# License

This module is distributed under the license of the parent repository.

See [`../LICENSE`](../LICENSE).

---

## Disclaimer

This is an unofficial community project for Claude Code.

It is not affiliated with, maintained by, sponsored by, or endorsed by Anthropic.
