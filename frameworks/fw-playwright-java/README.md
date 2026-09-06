# fw-playwright-java — Playwright for Java on HyperExecute (stage)

## What it is

Production-grade Playwright-Java (Maven + TestNG) sample for the HE framework
matrix. Two test classes:

- `JsonPlaceholderApiTest` — 5 API tests using Playwright's `APIRequestContext`
  against `https://jsonplaceholder.typicode.com`. No browser download needed —
  fast and cheap.
- `ExampleUiTest` — 2 UI tests against `https://example.com` using a **local
  headless chromium** installed in the HE `pre` step via the Playwright CLI
  (`mvn exec:java ... CLI "install chromium"`). No LambdaTest grid session is
  created on purpose — this proves local-browser execution inside the HE VM.

`api_DELIBERATE_FAILURE_wrongUserIdAssertion` is the ONE deliberate failure
(asserts userId 999 where it is 1) to prove red-status propagation.

## Layout

- `pom.xml` — pinned deps: playwright-java 1.49.0, testng 7.10.2, surefire 3.5.2
- `src/test/java/com/ltqa/fw/` — tests + `RunLogger` (writes `target/test-run.log`)
- `xml/testng.xml` — full suite (7 tests); `xml/testng-smoke.xml` — smoke subset (3 tests)
- `hyperexecute.yaml` — full run; `hyperexecute-smoke.yaml` — smoke variant

## How to run

```bash
cd he-playground/fw-playwright-java
KEY=$(grep 'anmolsoin@testmuai.com` (stage)' ../../../entries/0003-qa-test-accounts-ltqa.md | grep -o 'LT_[A-Za-z0-9]*')
../../he-ledger-check/hyperexecute --user anmolsoin --key $KEY \
  --config hyperexecute.yaml --env stage --no-track
```

## What it proves

- raw discovery (`grep 'include name' xml/testng*.xml`) + `mvn test -Dtest=$test`
  runner with `scenarioCommandStatusOnly: true` (statuses follow exit codes,
  since stage has no test-row reporting for this path)
- TestNG groups (`api`/`ui`/`smoke`) + a group-filtered smoke variant yaml
- browser install in `pre`, maven dependency caching (`.m2`), browser caching
  (`.playwright-browsers` via `PLAYWRIGHT_BROWSERS_PATH`)
- artefact upload of run log + surefire reports; one deliberate failure

## Expected caveats

- `Frameworks` stays `[]` — no grid session is created (local chromium only)
  and this is not HE's native playwright mode. That is expected per the shared
  logo-mechanism findings.
- stage-tests rows are not populated on this path (expected on stage).

## Gotchas discovered on stage (v0.1 bring-up)

- **surefire `suiteXmlFiles` + `-Dtest` = zero tests, exit 0.** With a suite
  file configured, `mvn test -Dtest=$test` silently runs NOTHING and still
  exits 0, so every scenario showed "completed" in 2s with empty
  surefire-reports. Fix: no `suiteXmlFiles` in pom; runner uses
  `-Dtest=*#$test` (class-wildcard + method).
- **`WaitForSelectorOptions` is not public in playwright-java** — locator
  waits use `new Locator.WaitForOptions()`.
- **example.com changed its copy in the 2025 redesign.** "illustrative
  examples" → "documentation examples"; link "More information..." →
  "Learn more". Two failed runs were caused by asserting the old text.

## Verified runs (stage, 2026-09-05)

- Full: job #125 (`213130a5-37cf-416c-b6b8-f6e003ec9411`) — 6/7 scenarios
  completed, exactly the one deliberate failure red; artefacts uploaded
  (TestRunLog 1101 B, SurefireReports 8949 B); Frameworks `[]`.
- Smoke: job #126 (`fef5c8ab-de19-4f4b-9c9f-cd65918d7cd1`) — 3/3 completed.
