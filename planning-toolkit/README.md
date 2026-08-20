# Claude Planning Toolkit

> Part of `claude-workflow-toolkit`. Unofficial community tooling for Claude Code; not affiliated with or endorsed by Anthropic.

This module turns Claude Code plans into **execution contracts**: plans that reuse existing project context, spend discovery progressively, identify exact files/symbols, preserve requirements/decisions, and split large work into independently executable increments.

The goal is not maximal plan detail. The goal is lower **planning + implementation rediscovery cost** while preserving correctness.

## Components

- `/execution-plan` — manual-only Opus/high-effort planner in a forked context.
- `/plan-refine` — manual-only plan audit/refinement using the same execution schema.
- `/plan-next-step` — optional manual-only Sonnet executor for exactly one ready increment. If you already have your own `next-step` skill, keep it and use `policy/PLAN-SCHEMA.md` as the compatibility contract.
- Plan-mode policy hook — injects a compact execution-planning policy only when Claude Code is actually in Plan mode, once per session (and again after compaction).
- ExitPlanMode quality gate — deterministic Python validation of plan structure; it does not call an LLM.
- Project-local plans — optional global `plansDirectory: .claude/plans` setting so plans can be consumed by later sessions/agents.

## Why it is independent of the Context Toolkit

If the Context Toolkit has already bootstrapped a project, the planner consumes its `CLAUDE.md`, scoped rules, and context routing information before doing new discovery. If it is absent, planning still works: the discovery budget simply starts from the project configuration and task-relevant source.

Likewise, `plan-next-step` is optional. The plan format is plain Markdown and can be executed manually or by another skill.

## Install: full integration

From the root of your `claude-workflow-toolkit` checkout:

```bash
python3 planning-toolkit/install.py
```

This:

1. installs `execution-plan`, `plan-refine`, and `plan-next-step` under `~/.claude/skills/`;
2. copies hook scripts under `~/.claude/hooks/claude-workflow-toolkit/planning/`;
3. backs up and merges `~/.claude/settings.json` without replacing unrelated settings;
4. injects the plan policy on `UserPromptSubmit` only while `permission_mode == "plan"`;
5. validates plans on `PreToolUse: ExitPlanMode`;
6. resets the once-per-session policy marker after context compaction and session end;
7. sets `plansDirectory` to `.claude/plans` so plans live with the project.

Restart Claude Code after installation.

If you develop the toolkit and want edits in this Git checkout to update installed skills immediately:

```bash
python3 planning-toolkit/install.py --symlink
```

Install only the manual skills, with no hooks/settings changes:

```bash
python3 planning-toolkit/install.py --skills-only
```

Keep Claude Code's default plan storage instead of `.claude/plans`:

```bash
python3 planning-toolkit/install.py --keep-default-plans
```

## Normal Plan mode

After full installation, use Claude Code normally and enter Plan mode. On the first prompt submitted while `permission_mode` is `plan`, the hook injects `policy/plan-mode-policy.md` as additional context. It does not inject the policy during normal coding turns.

Before Claude can leave Plan mode, the deterministic gate checks for the CWT v1 execution-plan structure. If major execution fields are missing, `ExitPlanMode` is denied with concise feedback and Claude can repair the plan.

The validator intentionally checks **structure**, not whether an architecture decision is smart. Opus/reasoning does the planning; the hook only prevents obviously incomplete handoffs.

### Escape hatches

For a genuine non-code/research plan, include:

```text
<!-- cwt:relaxed -->
```

For a one-off plan that must bypass the structural gate:

```text
<!-- cwt:no-gate -->
```

To disable locally from the shell:

```bash
export CWT_DISABLE_PLAN_POLICY=1
export CWT_DISABLE_PLAN_GATE=1
```

## Manual planning skill

For an explicit high-value planning pass:

```text
/execution-plan Add refresh-token rotation without changing the API contract
```

The skill runs in a forked general-purpose context with Opus/high effort and should save a CWT v1 plan to the configured plans directory.

Refine an existing plan later:

```text
/plan-refine .claude/plans/add-refresh-token-rotation.md
```

or simply:

```text
/plan-refine
```

## Execute incrementally

If you do not already have a `next-step` workflow:

```text
/plan-next-step .claude/plans/add-refresh-token-rotation.md
```

With no argument it attempts to locate the active/recent CWT v1 plan. It executes one ready `pending` increment using Sonnet, validates it, and updates the status.

If you already have your own `next-step` skill, adapt it to this tiny contract:

1. locate a `<!-- cwt-plan:v1 -->` plan;
2. choose the first `pending` increment whose dependencies are completed;
3. read the Request contract + Change map + selected increment, not every unrelated section;
4. read listed files/symbols first and broaden discovery only if the plan is stale/incomplete;
5. preserve stated decisions/constraints;
6. validate, then set the increment `completed` or `blocked`.

See `policy/PLAN-SCHEMA.md`.

## Multi-repo workspaces

The schema has an explicit Repository column in the Change map. A plan can span a workspace root and several child Git repositories while keeping each increment scoped to the minimum necessary repos. Prefer increments that avoid bouncing one implementation agent across unrelated repositories when a dependency boundary allows staging them.

## Token/context philosophy

The planner follows this discovery ladder:

```text
existing context
    -> exact path/symbol reads
    -> targeted search
    -> bounded module exploration
    -> broad repository exploration only if required
```

And this information hierarchy:

```text
path + symbol > copied code
verified decision > repeated reasoning
acceptance criterion > implementation essay
one coherent increment > artificial micro-steps
```

A correct plan still reads the task-relevant code. The optimization target is repeated **broad** rediscovery, not zero reads.

## Verify hooks locally

No third-party Python packages are needed:

```bash
python3 -m unittest planning-toolkit/tests/test_hooks.py
```

You can also inspect Claude Code's active hooks with `/hooks` and plan context with `/context`.

## Uninstall

Remove hooks but leave the skills:

```bash
python3 planning-toolkit/uninstall.py
```

Remove hooks and installed skills:

```bash
python3 planning-toolkit/uninstall.py --remove-skills
```

Also remove the `.claude/plans` user setting if it still has exactly that value:

```bash
python3 planning-toolkit/uninstall.py --remove-skills --remove-project-plans-setting
```

## Files

```text
planning-toolkit/
├── README.md
├── install.py
├── uninstall.py
├── settings.example.json
├── standalone-planning-prompt.md
├── policy/
│   ├── plan-mode-policy.md
│   └── PLAN-SCHEMA.md
├── hooks/
│   ├── inject_plan_policy.py
│   ├── validate_exit_plan.py
│   ├── reset_plan_policy_state.py
│   └── plan-mode-policy.md
├── skills/
│   ├── execution-plan/
│   ├── plan-refine/
│   └── plan-next-step/
├── examples/
│   └── example-plan.md
└── tests/
    └── test_hooks.py
```

## Current Claude Code primitives used

This module relies on documented Claude Code features including manual-only skills (`disable-model-invocation`), forked skill execution, `UserPromptSubmit` with `permission_mode`, `PreToolUse` matching `ExitPlanMode`, injected `plan` / `planFilePath` fields for plan hooks, and the `plansDirectory` setting. Because Claude Code evolves quickly, keep the toolkit tested against current documentation/releases.
