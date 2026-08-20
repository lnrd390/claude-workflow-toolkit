#!/usr/bin/env python3
"""Deterministic quality gate for ExitPlanMode plans.

It intentionally validates structure, not architectural correctness. A denied ExitPlanMode
feeds concise missing-section feedback back to Claude so the plan can be repaired in Plan mode.
"""
from __future__ import annotations

import json
import os
import re
import sys
from typing import Iterable


def has(pattern: str, text: str) -> bool:
    return re.search(pattern, text, re.IGNORECASE | re.MULTILINE) is not None


def missing_patterns(text: str, patterns: Iterable[tuple[str, str]]) -> list[str]:
    return [label for label, pattern in patterns if not has(pattern, text)]


def deny(reason: str) -> int:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }
    json.dump(output, sys.stdout)
    sys.stdout.write("\n")
    return 0


def main() -> int:
    if os.environ.get("CWT_DISABLE_PLAN_GATE") == "1":
        return 0

    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("tool_name") != "ExitPlanMode":
        return 0

    tool_input = payload.get("tool_input") or {}
    plan = str(tool_input.get("plan") or "")
    if not plan.strip():
        # Fail open if Claude Code did not inject plan content for some version/platform reason.
        return 0

    if "<!-- cwt:no-gate -->" in plan:
        return 0

    # Relaxed mode is for genuine research/non-code plans; still require a usable skeleton.
    if "<!-- cwt:relaxed -->" in plan:
        missing = missing_patterns(
            plan,
            [
                ("Goal", r"^#{1,4}\s+.*goal\b|^##\s+request contract\b"),
                ("Steps", r"^#{1,4}\s+.*(?:steps|approach|execution)\b"),
                ("Validation", r"^#{1,4}\s+.*(?:validation|verify|verification)\b"),
            ],
        )
        if missing:
            return deny("CWT relaxed plan gate: add " + ", ".join(missing) + " before leaving Plan mode.")
        return 0

    required = [
        ("CWT schema marker <!-- cwt-plan:v1 -->", r"<!--\s*cwt-plan:v1\s*-->"),
        ("Request contract", r"^##\s+Request contract\b"),
        ("Existing context reused", r"^##\s+Existing context reused\b"),
        ("Change map", r"^##\s+Change map\b"),
        ("Execution increments", r"^##\s+Execution increments\b"),
        ("at least one Increment", r"^###\s+Increment\s+\d+\b"),
        ("Final verification", r"^##\s+Final verification\b"),
    ]
    missing = missing_patterns(plan, required)

    increments = list(re.finditer(r"^###\s+Increment\s+\d+\b.*$", plan, re.IGNORECASE | re.MULTILINE))
    packet_errors: list[str] = []
    for idx, match in enumerate(increments):
        start = match.start()
        end = increments[idx + 1].start() if idx + 1 < len(increments) else len(plan)
        section = plan[start:end]
        label_match = re.match(r"^###\s+(Increment\s+\d+[^\n]*)", section, re.IGNORECASE)
        label = label_match.group(1) if label_match else f"Increment {idx + 1}"
        checks = [
            ("Status", r"^Status:\s*(pending|in_progress|blocked|completed)\b"),
            ("Files", r"^#{4,6}\s+Files\b|^Files:\s*$"),
            ("file action", r"\b(?:MODIFY|CREATE|DELETE)\b\s+`?[^\s`]+"),
            ("Required behavior", r"^#{4,6}\s+Required behavior\b|^Required behavior\s*:"),
            ("Constraints / decisions", r"^#{4,6}\s+Constraints\s*/\s*decisions\b|^Constraints\s*/\s*decisions\s*:"),
            ("Validation", r"^#{4,6}\s+Validation\b|^Validation\s*:"),
            ("Done when", r"^#{4,6}\s+Done when\b|^Done when\s*:"),
        ]
        miss = missing_patterns(section, checks)
        if miss:
            packet_errors.append(f"{label}: missing {', '.join(miss)}")

    if missing or packet_errors:
        parts = []
        if missing:
            parts.append("missing plan sections: " + ", ".join(missing))
        if packet_errors:
            parts.append("; ".join(packet_errors[:4]))
        return deny(
            "CWT execution-plan quality gate rejected this plan. "
            + " | ".join(parts)
            + ". Repair the plan using the execution-grade planning policy, then call ExitPlanMode again. "
              "Use <!-- cwt:relaxed --> only for genuinely non-code/research plans, or <!-- cwt:no-gate --> for an intentional one-off bypass."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
