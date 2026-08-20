# Claude Workflow Toolkit

> Unofficial community toolkit for Claude Code. Not affiliated with or endorsed by Anthropic.

A modular toolkit for making Claude Code workflows more context-efficient, repeatable, and execution-oriented.

The repository currently contains two complementary modules:

- **Context Toolkit** — bootstraps and periodically optimizes a token-efficient `.claude` architecture.
- **Planning Toolkit** — turns planning into an execution contract with verified change maps, incremental steps, and optional quality gates.

The overall goal is simple:

> Give each Claude session or agent as much relevant context as necessary, and as little irrelevant context as possible.

## How the pieces fit together

```text
User request
    |
    v
Context Toolkit
reuse existing project knowledge first
    |
    v
Planning Toolkit
targeted discovery + execution-grade plan
    |
    v
Incremental execution
one ready increment at a time
    |
    v
Validation
```

The toolkits are independent. You can install either one by itself, but they are designed to work well together.

---

## Repository structure

```text
claude-workflow-toolkit/
├── README.md
├── LICENSE
│
├── context-toolkit/
│   ├── README.md
│   ├── standalone-bootstrap-prompt.md
│   ├── context-bootstrap/
│   │   └── SKILL.md
│   └── context-optimize/
│       └── SKILL.md
│
└── planning-toolkit/
    ├── README.md
    ├── install.py
    ├── uninstall.py
    ├── settings.example.json
    ├── standalone-planning-prompt.md
    │
    ├── policy/
    │   ├── plan-mode-policy.md
    │   └── PLAN-SCHEMA.md
    │
    ├── hooks/
    │   ├── inject_plan_policy.py
    │   ├── validate_exit_plan.py
    │   ├── reset_plan_policy_state.py
    │   └── plan-mode-policy.md
    │
    ├── skills/
    │   ├── execution-plan/
    │   │   ├── SKILL.md
    │   │   └── PLAN-SCHEMA.md
    │   ├── plan-refine/
    │   │   ├── SKILL.md
    │   │   └── PLAN-SCHEMA.md
    │   └── plan-next-step/
    │       └── SKILL.md
    │
    ├── examples/
    │   └── example-plan.md
    │
    └── tests/
        └── test_hooks.py
```

`context-toolkit/README.md` and `planning-toolkit/README.md` contain the detailed documentation for each module.

---

# 1. Context Toolkit

The Context Toolkit provides two global, manual-only Claude Code skills:

- `/context-bootstrap`
- `/context-optimize`

### `/context-bootstrap`

Run it once from a repository or project/workspace folder.

It analyzes the project and builds or repairs a `.claude` architecture designed around:

- minimal always-loaded instructions;
- path-scoped rules;
- on-demand skills;
- isolated agents where useful;
- project auto-memory;
- conservative maintenance;
- single-repo and multi-repo layouts.

It is intentionally generic: it adapts to the directory from which Claude Code is started.

### `/context-optimize`

Run it periodically after representative usage.

It audits the context architecture, removes stale or duplicated information, evaluates previous optimization experiments, and improves the setup using available static measurements and real Claude Code telemetry when configured.

## Install Context Toolkit

From the root of this repository:

```bash
mkdir -p ~/.claude/skills

cp -R context-toolkit/context-bootstrap \
  ~/.claude/skills/context-bootstrap

cp -R context-toolkit/context-optimize \
  ~/.claude/skills/context-optimize
```

Then enter a project:

```bash
cd /path/to/project
claude
```

and run:

```text
/context-bootstrap
```

Optional audit-only mode:

```text
/context-bootstrap audit-only
```

After several representative sessions:

```text
/context-optimize
```

For full details, see [`context-toolkit/README.md`](context-toolkit/README.md).

---

# 2. Planning Toolkit

The Planning Toolkit makes plans useful as handoff artifacts for later sessions or implementation agents.

Its planning policy aims to:

- reuse existing context before broad repository exploration;
- perform targeted discovery only for missing information;
- identify exact repositories, paths, and symbols;
- distinguish verified facts, decisions, constraints, and instructions;
- preserve the original request as an explicit contract;
- split large work into coherent, independently executable increments;
- include validation commands and completion criteria;
- minimize implementation-time rediscovery.

A plan should help a capable implementation agent execute rather than redesign the task from scratch.

## Components

### `/execution-plan`

Manual high-value planner using a forked context.

Example:

```text
/execution-plan Add refresh-token rotation without changing the public API contract
```

### `/plan-refine`

Audits an existing plan and improves it for execution efficiency.

Example:

```text
/plan-refine .claude/plans/refresh-token-rotation.md
```

### `/plan-next-step`

Optional executor that takes one ready increment from a CWT plan, executes it, validates it, and updates the plan status.

If you already use another `next-step` skill, you can keep it and make it follow `planning-toolkit/policy/PLAN-SCHEMA.md`.

### Optional Plan mode integration

The full installer can also configure deterministic Claude Code hooks that:

1. inject the planning policy only while Claude is actually in Plan mode;
2. validate the structure of a plan before `ExitPlanMode`;
3. keep project plans under `.claude/plans`.

The structural validator uses Python and does not call an additional LLM.

## Install Planning Toolkit

From the root of this repository:

```bash
python3 planning-toolkit/install.py
```

If you are developing this repository and want your installed global skills to follow the checkout directly:

```bash
python3 planning-toolkit/install.py --symlink
```

Skills only, without hooks or settings changes:

```bash
python3 planning-toolkit/install.py --skills-only
```

For full details, escape hatches, tests, and uninstall instructions, see [`planning-toolkit/README.md`](planning-toolkit/README.md).

---

# Recommended setup

For the complete workflow:

```bash
git clone <your-repository-url>
cd claude-workflow-toolkit

mkdir -p ~/.claude/skills

cp -R context-toolkit/context-bootstrap \
  ~/.claude/skills/context-bootstrap

cp -R context-toolkit/context-optimize \
  ~/.claude/skills/context-optimize

python3 planning-toolkit/install.py
```

Restart Claude Code after installing the Planning Toolkit.

Then, in a project:

```bash
cd /path/to/project
claude
```

Bootstrap its context architecture once:

```text
/context-bootstrap
```

For normal work, simply state the task or use Plan mode.

For an explicit high-value planning pass:

```text
/execution-plan <task>
```

For incremental execution:

```text
/plan-next-step
```

Periodically optimize the project context architecture:

```text
/context-optimize
```

---

# Single repositories and multi-repo workspaces

Both toolkits are designed to work when Claude Code is started from either:

```text
single-repo/
├── .git/
└── ...
```

or:

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

For multi-repo projects, the intended architecture is a very small coordination layer at the workspace root with repository-specific context kept close to the relevant subtree.

For tasks concerning only one child repository, starting Claude Code directly inside that repository can provide an even smaller working scope.

---

# Design principles

The toolkit follows a few general rules:

```text
existing context > rediscovery
path-scoped context > global context
on-demand knowledge > always-loaded knowledge
path + symbol > copied source code
verified decision > repeated reasoning
acceptance criteria > implementation essays
targeted search > broad exploration
isolated investigation > polluting the main context
one coherent increment > arbitrary micro-steps
measurement > intuition when optimizing
```

The toolkit does **not** try to eliminate all code reading. Claude should still inspect task-relevant implementation before modifying it.

The target is repeated broad rediscovery and unnecessary context consumption.

---

# Development and tests

Planning Toolkit hook tests require no third-party Python packages:

```bash
python3 -m unittest planning-toolkit/tests/test_hooks.py
```

Because Claude Code evolves quickly, toolkit behavior should be periodically checked against current Claude Code releases and documentation.

---

# License

This project is intended to be distributed under the MIT License.

See [`LICENSE`](LICENSE).

---

## Disclaimer

This is an unofficial community project for Claude Code.

It is not affiliated with, maintained by, sponsored by, or endorsed by Anthropic.
