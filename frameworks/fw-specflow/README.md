# fw-specflow — HyperExecute v0.1 SpecFlow (.NET BDD) on stage

SpecFlow 3.9.74 + SpecFlow.NUnit on net8.0, run via HyperExecute yaml
`version: "0.1"` with **raw discovery at feature level** and
`dotnet test --filter` as the runner command. No browser — scenarios are
API-driven against https://jsonplaceholder.typicode.com via `HttpClient`
from the step definitions. Conventions follow the LT sample repo
`LambdaTest/specflow-selenium-hyperexecute-sample`
(`yaml/specflow_hyperexecute_hybrid_sample.yaml`).

## What it contains

- `FwSpecflow.csproj` — pinned deps: SpecFlow/SpecFlow.NUnit/
  SpecFlow.Tools.MsBuild.Generation 3.9.74, NUnit 4.2.2,
  NUnit3TestAdapter 4.6.0, Microsoft.NET.Test.Sdk 17.11.1,
  NUnitXml.TestLogger 3.1.20. Lockfile note: `RestorePackagesWithLockMode`
  is set in the csproj and `dotnet restore --force-evaluate` was run
  locally, but SDK 8.0.424 did not emit `packages.lock.json` in this
  setup — deps are pinned inline instead.
- `Features/PostsApi.feature` (@posts), `Features/UsersApi.feature` (@users)
  — 3 scenarios each; tags `@smoke`/`@regression`/`@list`/`@single` plus
  `@deliberate-failure`. Feature-level tags double as the discovery unit.
- `Steps/ApiSteps.cs` — `[Binding]` step definitions; appends every request
  and assertion to `logs/execution.log` (uploaded as artefact).
- Exactly one deliberate failure: scenario
  `DELIBERATE FAILURE - existing post wrongly expected to be missing`
  (expects 404 for post 5, which returns 200).
- `hyperexecute.yaml` — full run (discovery = all feature-level tags).
- `hyperexecute-smoke.yaml` — tag-filtered variant (only `@smoke`).
- `.hypertestignore` — excludes `bin/ obj/ logs/ TestResults/` from payload.

## How discovery works (the non-obvious part)

SpecFlow.NUnit generates NUnit test names from the **scenario titles**
(`GETPostsReturns100Posts`, …) — the feature name does NOT appear in the
FullyQualifiedName, so `Name~<feature>` filtering does not work. Tags,
however, become NUnit **Categories** (feature-level tags are inherited by
every scenario in the file). So:

- discovery: `grep -rhi '^@' Features --include=\*.feature | sort -u | sed 's/@//'`
  emits `posts`, `users` (one feature-level tag per feature file);
- runner: `dotnet test -c Release --no-build --filter "(Category=$test)"`
  runs exactly that feature's scenarios.

The build happens in `pre:` (v0.1 builds on the VM — unlike the v0.2
dotnet/nunit framework mode in `../fw-dotnet`, which never builds and
needs the DLL shipped in the payload).

## How to run

```bash
# from this directory (concurrent CLI processes in one dir clobber
# .updatedhyperexecute.yaml)
../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute.yaml --env stage --no-track --validate   # first
../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute.yaml --env stage --no-track
# tag-filtered variant:
../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute-smoke.yaml --env stage --no-track
```

Local check (uses the SDK installed by ../fw-dotnet):

```bash
export DOTNET_ROOT=$PWD/../fw-dotnet/.dotnet
$DOTNET_ROOT/dotnet test -c Release
# expected: Failed: 1, Passed: 5, Total: 6
```

## What it proves (stage, jobs #100 / #102 first pass, #115 / #116 final)

- v0.1 raw discovery over Gherkin feature files with SpecFlow on dotnet 8:
  scenarios = features, autosplit across linux tasks, runner filters per
  feature via SpecFlow tag → NUnit Category mapping.
- `scenarioCommandStatusOnly: true` is required on stage or all scenarios
  show as "skipped" (no test-id association exists on stage).
- Package restore: **SpecFlow 3.9.74 restores cleanly on stage** (NuGet
  reachable from the HE VMs) — no Reqnroll fallback was needed.
- Per-scenario pass/fail DOES surface here (unlike fw-dotnet v0.2): the
  `users` scenario with the deliberate failure is **failed /
  test_step_failed**, the job is **failed / "Job failed as encountered a
  Test level failure"**; `posts` and `smoke` scenarios are completed.
- `Frameworks` stays **[]** — expected: no grid sessions are created
  (pure API tests) and this is not a native cypress/dotnet framework mode.
- `stage-tests/<scenarioStageId>` returns empty on stage (no test rows).
- Artefacts: `NUnit_Xml` (TestResults/results.xml) and `Execution_Logs`
  upload fine. Gotcha: the dotnet test host's cwd is the assembly output
  dir, so step-definition logs land in `bin/Release/net8.0/logs/` — the
  uploadArtefacts path must point there (`logs/execution.log` at project
  root matches nothing → artefact record "failed / no file uploaded",
  seen in jobs #100/#102 before the path fix).
- partialReports (xml, frameworkName specflow, location TestResults) is
  accepted; report enabled on all jobs.
