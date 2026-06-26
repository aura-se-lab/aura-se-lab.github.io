---
name: fly-deploy-check
description: Use after deploying to Fly.io, or when the user asks whether a Fly deploy actually succeeded / "did the deploy work" / "check fly". Verifies the deploy is genuinely healthy (newest release complete + every machine started + all health checks passing + optional HTTPS 2xx probe), prints the log tail + exit + a one-line read, and on FAILURE automatically forms a fix plan and dispatches a fixer to diagnose → fix → redeploy → re-verify until green. Pairs with the bundled fly-deploy-guard PostToolUse hook that fires this check automatically after any `fly deploy`.
---

# Fly Deploy Check

One command to answer "did Fly actually deploy this?" — and, when it didn't, to drive the fix to green automatically instead of stopping at a red exit.

**Core principle:** a deploy command exiting 0 only proves the CLI *ran*. A deploy is "done" only when the **newest release is complete, every machine is started, every health check passes**, and (if given) a real HTTPS probe returns 2xx. Verify the effect, never the call.

## Steps

1. **Resolve the app.** Use the user's argument if given; else read `app =` from a `fly.toml` in the working tree. If neither exists, ask which app (do not guess).

2. **Run the verifier** (it prints structured fields + the log tail and sets the exit code):
   ```
   bash "$CLAUDE_PROJECT_DIR/.claude/skills/fly-deploy-check/check_deploy.sh" <app> [https-health-url]
   ```
   (If `$CLAUDE_PROJECT_DIR` is unset, run the script by its path under `.claude/skills/fly-deploy-check/` in the repo root.)
   - Pass the health URL when you know it (e.g. a `/health` endpoint) — the HTTP 2xx probe is the strongest signal.
   - The script prints `RELEASE_VERSION/STATUS`, `MACHINES`, optional `HEALTH_HTTP`, a `----- last log lines -----` tail, and a final `DEPLOY_OK=1|0` + `READ:` line. Exit 0 = healthy, exit 1 = not verified.

3. **If `DEPLOY_OK=1`:** report success in chat with the evidence anchor — the **log tail**, the **resolved status** (`RELEASE_STATUS`, machine summary, `HEALTH_HTTP`), and the one-line `READ:`. Done. Do not claim green without that tail + status in the same message.

4. **If `DEPLOY_OK=0` (auto plan + fix):** do NOT stop at red. In the same turn:
   1. **Gather evidence** — the script already tailed logs; if the cause isn't obvious, pull more: `flyctl logs -a <app>`, `flyctl releases -a <app>`, `flyctl status -a <app>`, and the failed machine's detail (`flyctl machine status <id> -a <app>`). Build failure → builder log; crash loop → app stderr; failing health checks → the check command + startup logs.
   2. **Form a fix plan** — state the likely root cause and the exact next action; enter plan mode for anything non-trivial. Root cause before fix.
   3. **Dispatch a fixer** — launch a debugger / general-purpose agent with the failure evidence + plan to implement a minimal, targeted fix.
   4. **Redeploy and re-verify** — redeploy (`flyctl deploy -a <app>` from the app dir) and run `check_deploy.sh` again. Loop diagnose → fix → redeploy → verify until `DEPLOY_OK=1` or 3 attempts.
   5. **Escalate on 3 failures** — stop, summarize what each attempt revealed, and ask the operator rather than a 4th blind fix.

5. **Always report** the final state with the tail + exit + read, and (if it failed) what you changed and whether it's now green — never a bare "deployed".

## Notes
- The script is **fail-closed here** (missing app / unreachable flyctl → exit 1 = "not verified"); the hook path is fail-open so it never breaks an unrelated session.
- `--quick` skips the log-tail snapshot (faster; used by the hook). The skill flow always shows the tail.
- Long deploys: if `flyctl deploy` ran in the background, wait for it to finish before trusting the check (a release mid-roll reads as not-yet-complete).

## Bundled automation (hook)
`.claude/hooks/fly-deploy-guard.py` is a `PostToolUse`/`Bash` hook registered in `.claude/settings.json`: after any `fly deploy` / `flyctl deploy` command it runs `check_deploy.sh --quick` and, if the deploy didn't verify, returns exit 2 so Claude is told to invoke this skill and drive the fix. It resolves the verifier relative to its own location, is fail-open, and only acts on deploy commands — inert for everything else. To disable, remove the entry from `.claude/settings.json`.
