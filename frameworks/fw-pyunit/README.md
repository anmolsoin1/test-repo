# fw-pyunit — Python stdlib unittest × Selenium on HyperExecute (stage)

Fills the Selenium × Python-PyUnit cell of the HE framework matrix.

## What it does

Runs `unittest` test-case classes against the-internet.herokuapp.com on the
LambdaTest grid from inside an HE VM, using the **canonical hub host**
`https://<user>:<key>@hub.lambdatest.com/wd/hub` (HE resolves it internally)
so the job's `Frameworks` field populates (framework logo in the UI).

- `tests/test_login.py` — `LoginTests`: valid login/logout flow,
  invalid-credential rejection via `subTest` data variety, and one
  clearly-named **deliberate failure**
  (`test_regression_DELIBERATE_FAILURE_wrong_page_title`) to prove failure
  propagation.
- `tests/test_dynamic_loading.py` — `DynamicLoadingTests`: hidden element,
  element rendered after the fact, a hand-rolled polling loop, index links.
- Locator variety: id, name, css, xpath, tag, link_text, partial link_text.
- Waits: `WebDriverWait` explicit waits + `poll_until_text` polling loop.
- unittest structure: `setUp`/`tearDown` per test (fresh grid session each,
  status reported back via `lambda-hook: setTestStatus`), `subTest` cases.
- Logging to `pyunit-run.log` (uploaded as an artefact).
- `run_one.py` — stdlib-only per-file runner: runs the module, writes a
  JUnit XML report to `reports/` (uploaded via partialReports), exit code
  follows the result. `TAG` env var filters tests by name (tag variant).

## How to run

```bash
HE=/Users/anmolsoin/knowledge-base-LT/he-ledger-check/hyperexecute
cd /Users/anmolsoin/knowledge-base-LT/he-playground/fw-pyunit
$HE --user anmolsoin --key <stage-key> --config hyperexecute.yaml --env stage --no-track
# smoke (tag-filtered) variant:
$HE --user anmolsoin --key <stage-key> --config hyperexecute-smoke.yaml --env stage --no-track
```

Validate first with `--validate`. Deps: `selenium==4.25.0`
(`requirements.txt`, pinned — stdlib unittest needs no test framework dep).

## What it proves

- HE runs raw-mode Python unittest suites (v0.1, no pytest needed).
- Grid sessions via the canonical host set the job's `Frameworks` field.
- `scenarioCommandStatusOnly: true` maps runner exit codes to scenario
  statuses (stage has no test rows for raw mode — stage-tests stays empty).
- partialReports picks up stdlib-generated JUnit XML.
