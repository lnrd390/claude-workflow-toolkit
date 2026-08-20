#!/usr/bin/env python3
"""Inject the CWT planning policy once per Claude Code session while in Plan mode."""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path


def _state_dir() -> Path:
    override = os.environ.get("CWT_STATE_DIR")
    if override:
        return Path(override)
    return Path.home() / ".claude" / "state" / "claude-workflow-toolkit" / "planning"


def _safe_id(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_.-]+", "_", value or "unknown")
    return value[:180] or "unknown"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if os.environ.get("CWT_DISABLE_PLAN_POLICY") == "1":
        return 0
    if payload.get("permission_mode") != "plan":
        return 0

    session_id = _safe_id(str(payload.get("session_id", "unknown")))
    marker = _state_dir() / f"{session_id}.injected"
    if marker.exists():
        return 0

    policy_path = Path(__file__).with_name("plan-mode-policy.md")
    try:
        policy = policy_path.read_text(encoding="utf-8").strip()
    except OSError:
        return 0

    try:
        marker.parent.mkdir(parents=True, exist_ok=True)
        marker.write_text("1\n", encoding="utf-8")
    except OSError:
        # Injection is more important than state persistence; a later prompt may inject again.
        pass

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": policy,
        }
    }
    json.dump(output, sys.stdout)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
