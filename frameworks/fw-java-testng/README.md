# fw-java-testng — production-grade TestNG API suite for HyperExecute (stage)

## What it is

Maven + TestNG 7.9.0 (pinned, surefire 3.2.5) suite hitting the public
JSONPlaceholder API, run on HyperExecute **stage** with
`framework: maven/testng`, `discoveryType: method`, `discoveryMode: remote`.
Each test *method* becomes its own scenario row (DataProvider invocations
collapse into one row — see "Verified findings").

## Structure

- `PostsApiTest` — smoke/regression API checks (GET list, GET one, POST).
- `PostsDataProviderTest` — `@DataProvider(name="postIds")` × 5 IDs → 5
  invocations in one scenario row (surefire: "Tests run: 5").
- `UsersApiTest` — smoke check + the **one deliberate failure**
  (`deliberateFailure_user999`, group `regression`: JSONPlaceholder returns
  404 for user 999).
- `FlakyRetryTest` + `RetryAnalyzer` — `IRetryAnalyzer` (max 2 retries)
  wired via `@Test(retryAnalyzer=...)`; the test is flaky by design and
  **passes on retry** within the same run. The failed first attempt shows
  in scenario history as a skipped/retried entry next to the passed one.

## How to run

```bash
HE=/Users/anmolsoin/knowledge-base-LT/he-ledger-check/hyperexecute
KEY=<stage-access-key>   # entries/0003
cd he-playground/fw-java-testng
$HE --user anmolsoin --key $KEY --config hyperexecute.yaml --env stage --no-track        # full suite (1 deliberate failure)
$HE --user anmolsoin --key $KEY --config hyperexecute-smoke.yaml --env stage --no-track  # smoke group only (all green)
```

## What it proves

- Method-level discovery: one scenario row per test method.
- Group filtering via `framework.flags: ['-Dgroups=smoke']`
  (hyperexecute-smoke.yaml): discovery finds only the 4 smoke methods and
  the deliberate failure never runs. **`framework.runnerFlags` does NOT
  filter** — verified on stage: with `runnerFlags: ['-Dgroups=smoke']`
  (job #81) the regression-only deliberate failure still ran and failed.
- Surefire XML reports uploaded as artefacts (`target/surefire-reports/**`).

## Verified findings (stage, jobs #71 / #81 / #87 / #91, 2026-09-04)

- **Retry analyzer:** `flakyPassesOnRetry` fails attempt 1, RetryAnalyzer
  triggers attempt 2 which passes. Surefire counts "Tests run: 2,
  Failures: 0, Skipped: 1" (the retried attempt is reported SKIPPED). The
  HE reporter POSTs two result entries for the same `testID` (skipped +
  passed). It does **not** create extra scenario rows — one scenario, and
  the retry detail is only visible inside the scenario log.
- **DataProvider:** 5 invocations run inside one scenario row
  (`postByIdHasMatchingId`); a single `testID` is reported for all 5.
- **Stage test-ID association trap:** passing scenarios show
  `skipped / no test id associated` and `stage-tests/<stageId>` returns
  empty, even though tests genuinely pass (BUILD SUCCESS in logs). Only
  *failures* associate (`failed / test_step_failed`). Because of this, the
  full run's executor task with only-passing tests reports task status
  `skipped`, and a groups-filtered job without
  `scenarioCommandStatusOnly: true` ends `skipped` overall despite being
  green (job #87). hyperexecute-smoke.yaml therefore sets
  `scenarioCommandStatusOnly: true` → job #91 `completed`, scenarios
  `completed` (remark still "no test id associated").
