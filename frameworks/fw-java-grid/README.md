# fw-java-grid — Java Selenium Grid + TestNG on HyperExecute (STAGE)

## What this proves

A HyperExecute **v0.1 raw** `maven/testng` job whose tests open **real
LambdaTest grid sessions from inside the HE VM** via the canonical host
`https://<LT_USERNAME>:<LT_ACCESS_KEY>@hub.lambdatest.com/wd/hub`. That inner
session is what populates the job's **`Frameworks: ["selenium"]`** field — the
Se logo in the HyperExecute UI. Hitting `stage-hub.lambdatestinternal.com`
directly bypasses detection and leaves `Frameworks` empty.

Also demonstrated: failure propagation — with `scenarioCommandStatusOnly: true`
(stage has no test-case rows), scenario status follows the maven exit code, so
the single deliberate failure flips exactly one scenario to failed.

## Layout

- `src/test/java/com/ltplayground/grid/GridBase.java` — RemoteWebDriver
  session per test method (canonical hub, Chrome latest on Windows 11),
  credentials from `LT_USERNAME`/`LT_ACCESS_KEY` env (HE injects them; yaml
  also sets literals; constants are the last fallback), run log appended to
  `target/grid-run.log` (uploaded artefact).
- `LoginTest.java` (groups `smoke, regression`) — the-internet login:
  valid login, invalid login, logout. Locators: `By.id`, `By.cssSelector`,
  `By.xpath`, `By.linkText`. `WebDriverWait` explicit waits.
- `CheckboxesTest.java` (groups `smoke, regression`) — checkbox toggling +
  dynamic loading via `FluentWait` (500 ms polling).
- `DeliberateFailureTest.java` (group `regression` only) — one passing test +
  `testDeliberateFailure_wrongHeading`, the single intentional failure.
- `hyperexecute.yaml` — full run (3 classes, expect 1 failed scenario).
- `hyperexecute-smoke.yaml` — tag/group-filtered variant (smoke classes only,
  all green).

## How to run

```bash
BIN=/Users/anmolsoin/knowledge-base-LT/he-ledger-check/hyperexecute
cd /Users/anmolsoin/knowledge-base-LT/he-playground/fw-java-grid
$BIN --user anmolsoin --key <STAGE_KEY> --config hyperexecute.yaml --env stage --no-track
$BIN --user anmolsoin --key <STAGE_KEY> --config hyperexecute-smoke.yaml --env stage --no-track
```

`<STAGE_KEY>` = `entries/0003-qa-test-accounts-ltqa.md`, row
`anmolsoin@testmuai.com (stage)`. Always run from this directory — concurrent
CLI runs in one directory clobber `.updatedhyperexecute.yaml`.

Verify after dispatch (queue can be 1–19 min):

```bash
KEY=<STAGE_KEY>
curl -su anmolsoin:$KEY \
  "https://api-stage-hyperexecute.lambdatestinternal.com/sentinel/v1.0/job/<jobId>?show_test_summary=true" | jq .
```

Check `.data.Frameworks` — must be `["selenium"]`. `stage-tests` stays empty
on stage even with grid sessions (expected).

## Reports / artefacts

- Surefire XML/TXT per scenario VM, uploaded as `surefire-reports` artefact +
  `partialReports` (type xml, frameworkName junit).
- `grid-run.log` — session ids and per-step log, uploaded as `grid-run-log`.

## Deps

Pinned in `pom.xml`: selenium-java 4.25.0, testng 7.9.0, surefire 3.2.5,
Java 11 target. Maven has no lockfile; versions are exact literals (no ranges).
No `node_modules`/`vendor` in the payload; `target/` is regenerated on the VM.
