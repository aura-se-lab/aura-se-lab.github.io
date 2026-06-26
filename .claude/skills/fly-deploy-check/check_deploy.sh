#!/usr/bin/env bash
# fly-deploy-check — verify a Fly.io deploy ACTUALLY succeeded and print the
# evidence the global CLAUDE.md CI/CD rule requires: the log tail, the exit /
# conclusion, and a one-line read. "Succeeded" = newest release complete AND every
# machine started AND every health check passing (AND an optional HTTPS probe 2xx).
#
# Usage:  check_deploy.sh [app] [health_url] [--quick]
#   app         Fly app name. Omitted -> read `app =` from ./fly.toml.
#   health_url  Optional HTTPS URL expected to return 2xx.
#   --quick     Skip the (slow) log-tail snapshot; status checks only. Used by the hook.
#
# Exit 0 = deploy verified healthy.  Exit 1 = NOT verified (caller should plan+fix).
# Fail-open on tooling errors is intentional ONLY for the hook path; here a missing
# app or unreachable flyctl yields exit 1 (treated as "not verified").
set -uo pipefail

APP=""; HEALTH_URL=""; QUICK=0
for a in "$@"; do
  case "$a" in
    --quick) QUICK=1 ;;
    http*://*) HEALTH_URL="$a" ;;
    *) [ -z "$APP" ] && APP="$a" ;;
  esac
done

if [ -z "$APP" ] && [ -f fly.toml ]; then
  APP="$(grep -E '^app[[:space:]]*=' fly.toml | head -1 | sed -E 's/.*=[[:space:]]*"?([^"]+)"?.*/\1/')"
fi
if [ -z "$APP" ]; then
  echo "DEPLOY_OK=0"; echo "ERROR: no app given and no ./fly.toml found"; exit 1
fi
echo "FLY_APP=$APP"

# --- Newest release status -------------------------------------------------
REL_JSON="$(flyctl releases --json -a "$APP" 2>/dev/null || true)"
REL_LINE="$(python3 - "$REL_JSON" <<'PY'
import sys, json
try: rels = json.loads(sys.argv[1] or "[]")
except Exception: rels = []
if not rels:
    print("?|none"); raise SystemExit
def ver(x): return x.get("version", x.get("Version", 0))
r = max(rels, key=ver)
print(f'{ver(r)}|{(r.get("status") or r.get("Status") or "?").lower()}')
PY
)"
REL_VER="${REL_LINE%%|*}"; REL_STATUS="${REL_LINE#*|}"
echo "RELEASE_VERSION=$REL_VER"
echo "RELEASE_STATUS=$REL_STATUS"

# --- Machine state + health checks -----------------------------------------
MACH_JSON="$(flyctl machines list --json -a "$APP" 2>/dev/null || true)"
MACH_LINE="$(python3 - "$MACH_JSON" <<'PY'
import sys, json
try: ms = json.loads(sys.argv[1] or "[]")
except Exception: ms = []
total=len(ms); started=0; cok=0; ctot=0; bad=[]
for m in ms:
    st=(m.get("state") or "").lower()
    started += st=="started"
    for c in (m.get("checks") or []):
        ctot+=1; cok += (c.get("status") or "").lower()=="passing"
    if st!="started": bad.append(f'{m.get("id","?")}:{st or "?"}')
ok = total>0 and started==total and (ctot==0 or cok==ctot)
print(f'{int(ok)}|{started}/{total} started, {cok}/{ctot} checks passing|{",".join(bad) or "-"}')
PY
)"
M_OK="${MACH_LINE%%|*}"; M_REST="${MACH_LINE#*|}"
echo "MACHINES=${M_REST%%|*}"
echo "MACHINES_BAD=${M_REST##*|}"

# --- Optional HTTP health probe --------------------------------------------
HTTP_OK=1
if [ -n "$HEALTH_URL" ]; then
  CODE="$(curl -s -o /dev/null -w '%{http_code}' --max-time 12 "$HEALTH_URL" 2>/dev/null || echo 000)"
  echo "HEALTH_HTTP=$CODE ($HEALTH_URL)"
  case "$CODE" in 2*) HTTP_OK=1 ;; *) HTTP_OK=0 ;; esac
fi

# --- Log tail (recent buffered lines) --------------------------------------
if [ "$QUICK" = 0 ]; then
  echo "----- last log lines ($APP) -----"
  timeout 8 flyctl logs -a "$APP" 2>/dev/null | tail -10
  echo "---------------------------------"
fi

# --- Verdict ---------------------------------------------------------------
REL_OK=0
case "$REL_STATUS" in complete|succeeded|success) REL_OK=1 ;; esac
if [ "$REL_OK" = 1 ] && [ "$M_OK" = 1 ] && [ "$HTTP_OK" = 1 ]; then
  echo "DEPLOY_OK=1"
  echo "READ: release v$REL_VER $REL_STATUS; machines healthy${HEALTH_URL:+; health probe 2xx}."
  exit 0
fi
echo "DEPLOY_OK=0"
echo "READ: deploy NOT verified (release=$REL_STATUS machines_ok=$M_OK http_ok=$HTTP_OK) -> trigger plan+fix."
exit 1
