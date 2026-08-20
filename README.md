# Claude Context Toolkit

> Unofficial community toolkit for Claude Code. Not affiliated with or endorsed by Anthropic.

Two global, manual-only Claude Code skills:

- `context-bootstrap`: one-shot setup/repair of a token-efficient `.claude` architecture.
- `context-optimize`: periodic evidence-driven optimization of that architecture.

Both skills are configured with `disable-model-invocation: true`, so Claude cannot auto-trigger them and their descriptions are not loaded into normal model context. They run in a forked `general-purpose` context using Opus/high effort, so the expensive audit does not pollute the main conversation.

The toolkit intentionally uses documented Claude Code skill primitives and avoids depending on a specific Claude Code version number. Claude Code evolves quickly, so check the current Skills documentation if a frontmatter field changes.

## Install

Copy the two skill directories into your personal Claude Code skills directory:

```bash
mkdir -p ~/.claude/skills
cp -R context-bootstrap ~/.claude/skills/context-bootstrap
cp -R context-optimize ~/.claude/skills/context-optimize
```

If those directories already exist, review/replace their `SKILL.md` files rather than nesting another copy inside them.

Use a recent Claude Code version. You can check your installed version with:

```bash
claude --version
```

## Single repository

```bash
cd /path/to/repo
claude
```

Then run:

```text
/context-bootstrap
```

For a preview without writing:

```text
/context-bootstrap audit-only
```

Start a fresh Claude Code session after bootstrap so the final load graph is clean. Optionally inspect `/context`, `/skills`, `/hooks`, and `/doctor` once.

## Multi-repository project folder

If a folder is a project/workspace containing multiple Git repositories:

```text
my-product/
  backend/.git/
  frontend/.git/
  infra/.git/
```

start Claude Code from `my-product/` and run `/context-bootstrap`. The skill should create/optimize a tiny workspace coordination layer and leave repo-specific knowledge in the child repos, where Claude Code can discover nested CLAUDE.md/skills when it enters those subtrees.

For a task that concerns only one repository, starting Claude Code directly inside that child repo usually gives the smallest working scope. A tiny ancestor workspace CLAUDE.md may still load; the bootstrap is designed to keep that cost negligible.

## Normal usage

After bootstrap, do not invoke the bootstrap skill for ordinary work. Start a session and state the task. The design aims to make universal context already available, path-specific rules appear when relevant files are opened, detailed workflows load as skills only when needed, and broad investigations use isolated subagents where useful.

This reduces broad rediscovery; it does not eliminate the need to read the task-relevant code. A correct plan should still inspect the implementation it is about to change.

## Periodic optimization

After several representative sessions, or when the project has evolved substantially, run:

```text
/context-optimize
```

Variants:

```text
/context-optimize conservative
/context-optimize aggressive
```

The optimizer evaluates prior experiments, compares static snapshots, and uses real Claude Code OpenTelemetry data when an accessible sink has been configured. It makes only evidence-backed, reversible context changes.

## Real token telemetry

Claude Code can export OpenTelemetry metrics/events for tokens, cache reads/creation, cost, model, skill, agent, query source, active time, and more. The bootstrap deliberately does not install or enable a telemetry backend automatically. If you already have an OTLP/Prometheus/log backend, the bootstrap records how it can be queried. Otherwise it uses static context measurements and marks real telemetry unavailable.

This avoids adding a monitoring stack merely to save tokens.
