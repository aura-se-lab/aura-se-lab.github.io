#!/usr/bin/env python3
"""fly-deploy-guard — PostToolUse/Bash hook (portable, repo-local).

After any `fly deploy` / `flyctl deploy` command, verify the deploy ACTUALLY
landed (newest release complete + machines started + checks passing) via the
fly-deploy-check skill's `check_deploy.sh --quick`. If it did NOT verify, exit 2
so Claude is told (stderr) to invoke the fly-deploy-check skill and drive the fix
— instead of trusting the deploy CLI's exit 0.

Portable: the verifier is resolved RELATIVE TO THIS FILE, so it works wherever the
repo is cloned (no machine-specific paths). Fail-open by design: any parse/tooling
error, or a non-deploy command, returns 0 so this hook never breaks an unrelated
session. Only ACTUAL deploy commands are acted on.

Registered in .claude/settings.json under PostToolUse with matcher "Bash":
  { "matcher": "Bash", "hooks": [ { "type": "command",
      "command": "python3 \"$CLAUDE_PROJECT_DIR/.claude/hooks/fly-deploy-guard.py\"",
      "timeout": 30 } ] }
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

# Resolve the verifier relative to this hook's location: <repo>/.claude/hooks/ ->
# <repo>/.claude/skills/fly-deploy-check/check_deploy.sh
_HERE = os.path.dirname(os.path.abspath(__file__))
CHECK = os.path.normpath(
    os.path.join(_HERE, "..", "skills", "fly-deploy-check", "check_deploy.sh")
)
APP_RE = re.compile(r"(?:-a|--app)[=\s]+([A-Za-z0-9][A-Za-z0-9-]*)")

# Only fire when a COMMAND SEGMENT actually invokes a deploy — not when the string
# "fly deploy" merely appears inside an echo/grep/commit-message argument. Split on
# shell separators and require a segment to START with (optional env=) fly|flyctl deploy.
_SEGMENTS = re.compile(r"(?:&&|\|\||[;\n|()])")
_DEPLOY_START = re.compile(r"^(?:\w+=\S*\s+)*(?:fly|flyctl)\s+deploy\b")


def _is_deploy_command(command: str) -> bool:
    return any(_DEPLOY_START.match(seg.strip()) for seg in _SEGMENTS.split(command))


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    if event.get("hook_event_name") != "PostToolUse" or event.get("tool_name") != "Bash":
        return 0
    command = (event.get("tool_input") or {}).get("command", "") or ""
    if not _is_deploy_command(command):
        return 0  # not a fly deploy — inert

    if not os.path.exists(CHECK):
        return 0  # checker missing — fail open

    cwd = event.get("cwd") or os.getcwd()
    app_match = APP_RE.search(command)
    args = ["bash", CHECK]
    if app_match:
        args.append(app_match.group(1))
    args.append("--quick")

    try:
        proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=25)
    except Exception:
        return 0  # any failure to run the check → fail open

    if proc.returncode == 0:
        return 0  # deploy verified healthy

    tail = (proc.stdout or "").strip().splitlines()
    summary = "\n".join(tail[-12:]) if tail else "(no check output)"
    print(
        "Fly deploy did NOT verify as healthy. Do not treat the deploy as done.\n"
        "Invoke the fly-deploy-check skill now to plan + fix → redeploy → re-verify.\n"
        f"--- check_deploy.sh output ---\n{summary}",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
