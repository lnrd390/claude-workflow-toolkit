#!/usr/bin/env python3
"""Remove CWT planning hooks and optionally installed skills from ~/.claude."""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

MARKER = "claude-workflow-toolkit/planning"
SKILLS = ("execution-plan", "plan-refine", "plan-next-step")


def contains_toolkit(group: dict) -> bool:
    return any(MARKER in str(h.get("command", "")).replace("\\", "/") for h in group.get("hooks", []))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--remove-skills", action="store_true")
    parser.add_argument("--remove-project-plans-setting", action="store_true")
    args = parser.parse_args()

    claude = Path.home() / ".claude"
    settings_path = claude / "settings.json"
    if settings_path.exists():
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        hooks = data.get("hooks", {})
        for event in list(hooks):
            groups = hooks.get(event, [])
            if isinstance(groups, list):
                hooks[event] = [g for g in groups if not (isinstance(g, dict) and contains_toolkit(g))]
                if not hooks[event]:
                    hooks.pop(event, None)
        if not hooks:
            data.pop("hooks", None)
        if args.remove_project_plans_setting and data.get("plansDirectory") == ".claude/plans":
            data.pop("plansDirectory", None)
        settings_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    shutil.rmtree(claude / "hooks" / "claude-workflow-toolkit" / "planning", ignore_errors=True)
    shutil.rmtree(claude / "state" / "claude-workflow-toolkit" / "planning", ignore_errors=True)

    if args.remove_skills:
        for name in SKILLS:
            path = claude / "skills" / name
            if path.is_symlink():
                path.unlink(missing_ok=True)
            elif path.exists():
                shutil.rmtree(path)

    print("CWT planning integration removed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
