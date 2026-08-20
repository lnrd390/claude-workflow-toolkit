#!/usr/bin/env python3
"""Reset/clean the once-per-session planning-policy marker."""
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

    session_id = _safe_id(str(payload.get("session_id", "unknown")))
    marker = _state_dir() / f"{session_id}.injected"
    try:
        marker.unlink(missing_ok=True)
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
