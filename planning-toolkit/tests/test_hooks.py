#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOOKS = ROOT / "hooks"
EXAMPLE = ROOT / "examples" / "example-plan.md"


def run(script: str, payload: dict, env: dict | None = None) -> tuple[int, str, str]:
    e = os.environ.copy()
    if env:
        e.update(env)
    p = subprocess.run(
        [sys.executable, str(HOOKS / script)],
        input=json.dumps(payload),
        text=True,
        capture_output=True,
        env=e,
    )
    return p.returncode, p.stdout.strip(), p.stderr.strip()


class HookTests(unittest.TestCase):
    def test_policy_only_in_plan_mode_and_once(self):
        with tempfile.TemporaryDirectory() as td:
            env = {"CWT_STATE_DIR": td}
            base = {"session_id": "s1", "hook_event_name": "UserPromptSubmit", "prompt": "x"}
            rc, out, _ = run("inject_plan_policy.py", {**base, "permission_mode": "default"}, env)
            self.assertEqual(rc, 0)
            self.assertEqual(out, "")
            rc, out, _ = run("inject_plan_policy.py", {**base, "permission_mode": "plan"}, env)
            self.assertEqual(rc, 0)
            self.assertIn("additionalContext", out)
            rc, out2, _ = run("inject_plan_policy.py", {**base, "permission_mode": "plan"}, env)
            self.assertEqual(out2, "")
            run("reset_plan_policy_state.py", {"session_id": "s1"}, env)
            _, out3, _ = run("inject_plan_policy.py", {**base, "permission_mode": "plan"}, env)
            self.assertIn("additionalContext", out3)

    def test_example_plan_passes(self):
        plan = EXAMPLE.read_text(encoding="utf-8")
        rc, out, err = run("validate_exit_plan.py", {"tool_name": "ExitPlanMode", "tool_input": {"plan": plan}})
        self.assertEqual(rc, 0)
        self.assertEqual(out, "", (out, err))

    def test_incomplete_plan_is_denied(self):
        rc, out, _ = run("validate_exit_plan.py", {"tool_name": "ExitPlanMode", "tool_input": {"plan": "# Do thing\n- edit file"}})
        self.assertEqual(rc, 0)
        data = json.loads(out)
        self.assertEqual(data["hookSpecificOutput"]["permissionDecision"], "deny")

    def test_relaxed_plan_passes(self):
        plan = """<!-- cwt:relaxed -->\n# Research\n## Goal\nUnderstand X\n## Steps\n1. Inspect\n## Validation\nSummarize evidence\n"""
        rc, out, _ = run("validate_exit_plan.py", {"tool_name": "ExitPlanMode", "tool_input": {"plan": plan}})
        self.assertEqual(rc, 0)
        self.assertEqual(out, "")


if __name__ == "__main__":
    unittest.main()
