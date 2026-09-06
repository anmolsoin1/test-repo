#!/bin/bash
# fw-jmeter scenario runner.
# Usage: bash run_jmeter.sh <path-to-plan.jmx>
# Runs the plan non-GUI, writes JTL + HTML dashboard under reports/,
# tees the console log, and exits non-zero if any sample failed
# (HE scenarioCommandStatusOnly maps the exit code to the scenario status).
set -uo pipefail

JMX="$1"
NAME="$(basename "$JMX" .jmx)"
mkdir -p reports
LOG="jmeter-run.log"
DASH="reports/dashboard-${NAME}"
JTL="reports/${NAME}.jtl"

JMETER_HOME_DIR="$(ls -d apache-jmeter-* 2>/dev/null | head -1)"
if [ -z "${JMETER_HOME_DIR}" ] || [ ! -x "${JMETER_HOME_DIR}/bin/jmeter" ]; then
  echo "FATAL: apache-jmeter install not found (pre step should have extracted it)" | tee -a "$LOG"
  exit 2
fi

echo "==== $(date -u +%FT%TZ) scenario=${NAME} plan=${JMX} ====" | tee -a "$LOG"
"${JMETER_HOME_DIR}/bin/jmeter" -n -t "$JMX" -l "$JTL" -e -o "$DASH" 2>&1 | tee -a "$LOG"
JMETER_RC=${PIPESTATUS[0]}
echo "jmeter exit code: ${JMETER_RC}" | tee -a "$LOG"

if [ ! -f "$JTL" ]; then
  echo "FATAL: no JTL produced for ${NAME}" | tee -a "$LOG"
  exit 3
fi

TOTAL=$(($(wc -l < "$JTL") - 1))
FAILED=$(awk -F',' 'NR>1 && $8=="false" {c++} END {print c+0}' "$JTL")
echo "samples=${TOTAL} failed=${FAILED}" | tee -a "$LOG"

# tarball the dashboard so it uploads as one artefact
tar -czf "reports/dashboard-${NAME}.tar.gz" -C reports "dashboard-${NAME}" 2>/dev/null || true

if [ "$JMETER_RC" -ne 0 ] || [ "$FAILED" -gt 0 ]; then
  echo "SCENARIO RESULT: FAIL (${NAME})" | tee -a "$LOG"
  exit 1
fi
echo "SCENARIO RESULT: PASS (${NAME})" | tee -a "$LOG"
exit 0
