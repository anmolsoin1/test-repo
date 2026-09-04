# fw-dotnet — HyperExecute v0.2 framework mode (dotnet/nunit)

Minimal NUnit (net8.0) test project for proving HyperExecute yaml `version: "0.2"`
framework mode with `dotnet/nunit` + remote method discovery on **stage**.

## What it contains

- `FwDotnet.csproj` — net8.0 test project, pinned deps (Microsoft.NET.Test.Sdk
  17.11.1, NUnit 4.2.2, NUnit3TestAdapter 4.6.0, NUnitXml.TestLogger 3.1.20).
- `PostsApiTests.cs` / `UsersApiTests.cs` — 4 tests against
  https://jsonplaceholder.typicode.com via `HttpClient` (list + single-entity
  asserts), `[Category]` attributes as tags (`Smoke`, `List`, `Single`,
  `DeliberateFailure`). `GetUserById_DELIBERATE_FAILURE_Expects404ForExistingUser`
  is the one deliberate failure.
- `hyperexecute.yaml` — v0.2 framework config (see below).
- `bin/Release/net8.0/` — **pre-built test assembly, required in the payload**.
- `dotnet-install.sh` — local SDK bootstrap (excluded from upload via `.gitignore`,
  together with `.dotnet/` and `obj/`).

## The one non-obvious requirement: ship the built DLL

The dotnet v0.2 runner **never builds**. Discovery fails in ~2s with:

```
ERROR: no built 'FwDotnet.dll' found under '/home/ltuser/foreman/fw-dotnet/bin' —
either it is not built, or its output is elsewhere (UseArtifactsOutput, custom
OutputPath). The runner never builds: build it first, or pass --assembly with the
built test .dll
```

So before dispatching:

```bash
curl -sSL https://dot.net/v1/dotnet-install.sh -o dotnet-install.sh
./dotnet-install.sh --channel 8.0 --install-dir "$PWD/.dotnet"
export DOTNET_ROOT="$PWD/.dotnet" PATH="$PWD/.dotnet:$PATH"
dotnet build -c Release        # produces bin/Release/net8.0/FwDotnet.dll
```

The `runtime: {language: dotnet, version: "8"}` block is accepted by validation
and adds a `setup-runtime` stage (~10-13s) on each VM; jobs also ran without it,
but keep it — without it the discovery VM may lack the SDK.

## hyperexecute.yaml (final, verbatim)

```yaml
---
version: "0.2"
globalTimeout: 20
runson: linux
autosplit: true
concurrency: 2
retryOnFailure: false
maxRetries: 0
# Without this, every scenario is marked skipped ("no test id associated")
# on stage even though the test executed. With it, scenario status follows
# the runner command exit code (scenarios show "completed").
scenarioCommandStatusOnly: true

runtime:
  language: dotnet
  version: "8"

framework:
  name: dotnet/nunit
  version: "8"
  discoveryType: method
  discoveryMode: remote
  defaultReports: true

jobLabel: ['he-playground', 'fw-dotnet']
```

Run it (from this directory — concurrent CLI processes in one dir clobber
`.updatedhyperexecute.yaml`):

```bash
../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute.yaml --env stage --no-track
```

## What it proves (stage, jobs #56 / #57 / #60)

- Remote discovery works: discovery VM resolves the shipped DLL
  (`resolved assembly: .../bin/Release/net8.0/FwDotnet.dll`, NUnit Adapter 4.6.0,
  "Total items discovered: 4").
- **Method-level scenarios: YES.** 4 scenarios named
  `FwDotnet.Tests.PostsApiTests.GetPosts_ReturnsListOf100` etc., autosplit 2+2
  across 2 linux tasks, each scenario runs exactly its one method
  (`Total tests executed: 1` per scenario log).
- **Test-ID association on stage: NO.** Every scenario remark is
  `no test id associated`; `stage-tests/<scenarioStageId>` returns empty;
  `session_ids` null. Without `scenarioCommandStatusOnly: true` scenarios show
  as **skipped** even though the test ran and passed — with it they show
  **completed**. Pass/fail is NOT surfaced per scenario either way (the
  deliberate failure's scenario is "completed" too); the failure is visible only
  in the scenario log ("Failed! - Failed: 1") and in Log Highlights (Error 1,
  Failure 1).
- `defaultReports: true` produces a downloadable report.html (~475 KB,
  "Open Report" / "Download Report" buttons work).
- `uploadArtefacts` with a glob that matches nothing (e.g. `TestResults/**` —
  the runner does not emit TRX) shows "Artefact upload failed" in every scenario
  log and artefact status `failed / no file uploaded`. Dropped from final yaml.
