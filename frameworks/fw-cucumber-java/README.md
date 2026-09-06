# fw-cucumber-java — Cucumber-JVM 7 + Selenium Grid on HyperExecute (STAGE)

## What this is

A production-grade Cucumber-JVM (Maven) sample for the HyperExecute
framework matrix. Tests run against `the-internet.herokuapp.com` using
Selenium 4 `RemoteWebDriver` pointed at the **canonical** hub host
`https://<LT_USERNAME>:<LT_ACCESS_KEY>@hub.lambdatest.com/wd/hub`
(auto-injected env vars inside the HE VM; the VM resolves the host
internally). Driving grid sessions through the canonical host is what
populates the job's `Frameworks` field → the cucumber/framework logo in
the HyperExecute UI.

## Layout

- `pom.xml` — pinned deps: cucumber-java / cucumber-testng `7.18.1`,
  selenium-java `4.25.0`, testng `7.10.2`, surefire `3.2.5`.
- `src/test/java/runner/TestRunner.java` — TestNG Cucumber runner;
  emits `target/cucumber-reports/CucumberTestReport.json` +
  `cucumber-pretty.html`.
- `src/test/java/stepdefs/` — glue:
  - `DriverFactory.java` — lazily creates one RemoteWebDriver per scenario
    on the canonical hub host.
  - `Hooks.java` — `@Before`/`@After`: scenario logging, failure screenshot
    attachment, driver quit.
  - `LoginSteps.java` — locator variety: `By.id`, `By.cssSelector`,
    `By.xpath`, `By.linkText`; `WebDriverWait` explicit waits throughout.
  - `CheckboxSteps.java` — indexed xpath + attribute selectors, polling
    via `visibilityOfAllElementsLocatedBy`.
  - `RunLog.java` — timestamped log mirrored to
    `target/cucumber-reports/execution.log` (uploaded as an artefact).
- `src/test/resources/features/login.feature` — `@login`; a
  `@regression` **Scenario Outline with a 3-row Examples table**
  (valid login / bad username / bad password = data-driven rows) plus a
  `@smoke` logout scenario.
- `src/test/resources/features/checkbox.feature` — `@checkbox`; a
  `@smoke` scenario, a `@regression` scenario, and exactly one
  **`@deliberate-failure`** scenario (`DELIBERATE FAILURE - nonexistent
  promo banner is expected`).

## HyperExecute configs

- `hyperexecute.yaml` — full run. v0.1 **raw** static discovery
  (`ls src/test/resources/features/*.feature`), autosplit with
  `concurrency: 2`, runner per feature file:
  `mvn test -Dtest=TestRunner -Dcucumber.features="$test"`.
  `scenarioCommandStatusOnly: true` (stage has no test rows; scenario
  status follows the mvn exit code, so the deliberate failure marks the
  checkbox scenario failed). Cucumber JSON uploaded via `partialReports`
  (type json) and `uploadArtefacts`.
- `hyperexecute-smoke.yaml` — tag-filtered variant adding
  `-Dcucumber.filter.tags=@smoke`; runs only the 2 `@smoke` scenarios,
  all green (deliberate failure excluded).

## How to run

```bash
KEY=<stage-access-key>   # entries/0003, anmolsoin@testmuai.com (stage) row
cd he-playground/fw-cucumber-java   # ALWAYS run the CLI from this dir
../../he-ledger-check/hyperexecute --user anmolsoin --key $KEY \
  --config hyperexecute.yaml --env stage --no-track --validate   # validate first
../../he-ledger-check/hyperexecute --user anmolsoin --key $KEY \
  --config hyperexecute.yaml --env stage --no-track              # dispatch
# smoke variant: same with --config hyperexecute-smoke.yaml
```

## What it proves

- Cucumber-JVM 7 runs on HE with raw v0.1 discovery + autosplit, one
  scenario (VM) per feature file.
- Data-driven Scenario Outline rows, tag filtering, explicit waits, and
  locator variety all work end-to-end.
- Grid sessions via the canonical hub host populate the job `Frameworks`
  field (framework logo) — direct stage-hub host does NOT.
- Cucumber JSON partial reports + artefacts upload; a deliberate failure
  surfaces correctly as a failed scenario (full run) and is excluded by
  the `@smoke` filter (smoke run).
