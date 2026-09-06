# fw-karate — HyperExecute + Karate (API BDD) on stage

Minimal but production-grade Karate matrix cell for the HyperExecute framework
playground. Raw discovery mode, maven on Java 17.

## What it does

- Tests the public https://jsonplaceholder.typicode.com API with two feature files:
  - `src/test/java/jsonplaceholder/posts.feature` — 5 scenarios (GET list, GET one,
    POST create, nested comments, `match each` schema checks)
  - `src/test/java/jsonplaceholder/users.feature` — 3 scenarios (list, nested
    address/company match, `match each` on todos)
- Tags: `@smoke` (4 scenarios) / `@regression` (5 scenarios, overlaps).
- Exactly one deliberate failure: `DELIBERATE FAILURE - wrong status expected for
  missing post` in `posts.feature` (GET /posts/99999 returns 404, scenario asserts 200).
- `runners/JsonPlaceholderRunner.java` drives via `Runner.path($FeaturePath)`,
  `outputCucumberJson(true)` + `outputJunitXml(true)` into `target/karate-reports`.

## How to run

```bash
# from this directory (he-playground/fw-karate)
KEY=LT_GsJOkDD7fZFOAaA0AMBVK2muSGFuiz6BysimcQeReBnfK8m
BIN=../../he-ledger-check/hyperexecute
$BIN --user anmolsoin --key $KEY --config hyperexecute.yaml --env stage --no-track --validate
$BIN --user anmolsoin --key $KEY --config hyperexecute.yaml --env stage --no-track
# tag-filtered variant (@smoke only, should be fully green):
$BIN --user anmolsoin --key $KEY --config hyperexecute-smoke.yaml --env stage --no-track
```

## What it proves

- HE `runtime: java 17` + maven provisioning on stage VMs (deps resolve online into
  `m2/`, cached across runs via `cacheDirectories`).
- `testDiscovery: raw, mode: dynamic` with autosplit per `.feature` file.
- `$test` interpolation into the surefire runner command; `scenarioCommandStatusOnly: true`
  so scenario status follows the exit code (API tests create no grid sessions, so
  stage-tests rows stay empty and `Frameworks` will NOT populate — expected).
- Karate partialReports (`frameworkName: karate`, html) plus junit xml / cucumber json
  uploaded as artefacts.
- Karate tag filtering through `-DKarateTags` (`hyperexecute-smoke.yaml`).

## Layout

```
pom.xml                      karate-junit5 1.4.1, surefire 3.1.2, Java 17
hyperexecute.yaml            full run (autosplit, concurrency 2)
hyperexecute-smoke.yaml      @smoke-only variant (green)
src/test/java/karate-config.js
src/test/java/runners/JsonPlaceholderRunner.java
src/test/java/jsonplaceholder/posts.feature   (incl. deliberate failure)
src/test/java/jsonplaceholder/users.feature
```
