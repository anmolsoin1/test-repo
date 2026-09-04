#!/bin/bash
# Outcome is injected per run via --vars OUTCOME=pass|fail|timeout
# Same scenario name across runs => Scenario History shows the rotation.
echo "rotate.sh running with OUTCOME=${OUTCOME:-pass}"
case "${OUTCOME:-pass}" in
  pass)    echo "passing this run";  exit 0 ;;
  fail)    echo "failing this run";  exit 1 ;;
  timeout) echo "sleeping past testSuiteStep"; sleep 180; exit 0 ;;
  *)       exit 0 ;;
esac
