#!/usr/bin/env python3
"""Install the planning toolkit into the current user's Claude Code configuration.

Standard-library only. It backs up ~/.claude/settings.json, installs/symlinks skills,
copies hook assets, and merges hook groups idempotently.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path

TOOLKIT_MARKER = "claude-workflow-toolkit/planning"
SKILLS = ("execution-plan", "plan-refine", "plan-next-step")


def load_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SystemExit(f"Cannot parse {path}: {exc}")
    if not isinstance(data, dict):
        raise SystemExit(f"Expected JSON object in {path}")
    return data


def backup(path: Path) -> Path | None:
    if not path.exists():
        return None
    stamp = time.strftime("%Y%m%d-%H%M%S")
    out = path.with_name(path.name + f".cwt-backup-{stamp}")
    shutil.copy2(path, out)
    return out


def install_dir(src: Path, dst: Path, symlink: bool) -> None:
    if dst.is_symlink() or dst.exists():
        if dst.is_symlink() and dst.resolve() == src.resolve() and symlink:
            return
        stamp = time.strftime("%Y%m%d-%H%M%S")
        moved = dst.with_name(dst.name + f".cwt-backup-{stamp}")
        shutil.move(str(dst), str(moved))
        print(f"Backed up existing {dst} -> {moved}")
    dst.parent.mkdir(parents=True, exist_ok=True)
    if symlink:
        dst.symlink_to(src.resolve(), target_is_directory=True)
    else:
        shutil.copytree(src, dst)


def command_for(script: Path) -> str:
    py = shutil.which("python3") or shutil.which("python") or sys.executable
    # JSON stores a shell command. Quote both executable and script for spaces.
    return f'"{py}" "{script}"'


def handler_group(command: str, matcher: str | None = None) -> dict:
    group = {"hooks": [{"type": "command", "command": command}]}
    if matcher is not None:
        group["matcher"] = matcher
    return group


def contains_toolkit(group: dict) -> bool:
    for hook in group.get("hooks", []):
        if TOOLKIT_MARKER in str(hook.get("command", "")).replace("\\", "/"):
            return True
    return False


def add_group(settings: dict, event: str, group: dict) -> None:
    hooks = settings.setdefault("hooks", {})
    groups = hooks.setdefault(event, [])
    groups[:] = [g for g in groups if not (isinstance(g, dict) and contains_toolkit(g))]
    groups.append(group)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--symlink", action="store_true", help="symlink skills from this Git checkout instead of copying them")
    parser.add_argument("--skills-only", action="store_true", help="install skills but do not install global hooks or change plansDirectory")
    parser.add_argument("--keep-default-plans", action="store_true", help="do not set plansDirectory=.claude/plans")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    claude = Path.home() / ".claude"
    skill_home = claude / "skills"

    for name in SKILLS:
        install_dir(root / "skills" / name, skill_home / name, args.symlink)
        print(f"Installed skill /{name}")

    if args.skills_only:
        print("Skills-only installation complete.")
        return 0

    hook_dst = claude / "hooks" / "claude-workflow-toolkit" / "planning"
    hook_dst.mkdir(parents=True, exist_ok=True)
    for filename in ("inject_plan_policy.py", "validate_exit_plan.py", "reset_plan_policy_state.py", "plan-mode-policy.md"):
        shutil.copy2(root / "hooks" / filename, hook_dst / filename)
    for path in hook_dst.glob("*.py"):
        try:
            path.chmod(path.stat().st_mode | 0o111)
        except OSError:
            pass

    settings_path = claude / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings = load_json(settings_path)
    bkp = backup(settings_path)

    add_group(settings, "UserPromptSubmit", handler_group(command_for(hook_dst / "inject_plan_policy.py")))
    add_group(settings, "PreToolUse", handler_group(command_for(hook_dst / "validate_exit_plan.py"), "ExitPlanMode"))
    add_group(settings, "PostCompact", handler_group(command_for(hook_dst / "reset_plan_policy_state.py")))
    add_group(settings, "SessionEnd", handler_group(command_for(hook_dst / "reset_plan_policy_state.py")))

    if not args.keep_default_plans:
        settings["plansDirectory"] = ".claude/plans"

    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Updated {settings_path}")
    if bkp:
        print(f"Backup: {bkp}")
    if not args.keep_default_plans:
        print("Plan files will be stored under <project>/.claude/plans")
    print("Full planning integration installed. Restart Claude Code before testing it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
