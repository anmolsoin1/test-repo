# fw-playwright-python — Playwright (pytest-playwright) on HyperExecute stage

UI test suite against `https://the-internet.herokuapp.com`, run on
HyperExecute **stage** in raw mode (`scenarioCommandStatusOnly: true`) with
autosplit, dynamic discovery, and junit partial reports. Browser is **local
chromium on the runner** — `python -m playwright install chromium` in `pre`
(proven to work on the linux image; no `--with-deps` needed).

## What it proves

- **pytest-playwright sync API** — `page` fixture, `expect()` auto-waiting
  assertions (`to_be_visible`, `to_have_url`, `to_have_value`,
  `to_be_checked`, `to_contain_text`).
- **Locator variety** — css (`#password`, `button.radius`), attribute
  (`input[name='username']`), xpath (`//input[@id='username']`), text
  (`text=You logged into...`), role+name (`get_by_role("link",
  name="Logout")`).
- **Explicit waits** — `page.wait_for_selector(..., state="attached" |
  "visible" | "hidden")` on the dynamic-loading examples (polling-ish;
  example 2 keeps `#loading` in the DOM with `display:none`, so wait for
  `hidden`, not `detached`).
- **API-state wait** — `page.expect_response("**/authenticate")` around the
  login form submit, asserting the redirect status (302/303).
- **Markers** — `smoke` vs `regression` (`tests/pytest.ini`); the smoke yaml
  runs `-m smoke` (5 tests), the full yaml runs all 9.
- **One deliberate failure** —
  `test_dropdown_checkboxes.py::test_deliberate_failure_checkbox_default_state`
  asserts checkbox 1 is checked by default (it is not). Everything else
  genuinely passes.
- **Logging to artefact** — session logger + per-test outcome hook in
  `tests/conftest.py` write `playwright-run.log`, uploaded as HE artefact.

## Layout

- `tests/test_login.py` — valid/invalid login, logout (3 tests)
- `tests/test_dynamic_loading.py` — example 1 + example 2 waits (3 tests)
- `tests/test_dropdown_checkboxes.py` — dropdown, checkboxes, deliberate
  failure (3 tests)
- `tests/conftest.py` — file logger + `pytest_runtest_makereport` hook
  (pytest 8 style: `wrapper=True`, `report = yield`, `return report`)
- `requirements.txt` — pinned deps (`pytest==8.3.2`,
  `pytest-playwright==0.5.2`, `playwright==1.46.0`)
- `hyperexecute.yaml` — full run (all markers)
- `hyperexecute-smoke.yaml` — smoke-marker run only

## How to run

```bash
cd he-playground/fw-playwright-python
KEY=<stage-access-key>  # see entries/0003, anmolsoin@testmuai.com (stage)
../../he-ledger-check/hyperexecute --user anmolsoin --key $KEY \
  --config hyperexecute.yaml --env stage --no-track --validate   # validate
../../he-ledger-check/hyperexecute --user anmolsoin --key $KEY \
  --config hyperexecute.yaml --env stage --no-track              # dispatch
```

The CLI returns at dispatch; poll
`GET https://api-stage-hyperexecute.lambdatestinternal.com/sentinel/v1.0/job/<jobId>?show_test_summary=true`
(basic auth `anmolsoin:$KEY`) for status.

## Expected result

Full run: 9 tests — 8 passed, 1 failed (deliberate). Job status `Failed`,
one scenario task per test file (3 tasks, concurrency 2). Smoke run: 5
tests, all pass, job status `Passed`. `Frameworks` stays `[]` and
`stage-tests` stays empty — local chromium creates no grid sessions and
junit partialReports do not associate test IDs on stage.

## Gotchas

- pytest 8 removed `hookwrapper=True` — use `wrapper=True` and
  `return report` in the makereport hook, else INTERNALERROR.
- Dynamic loading example 2: `#loading` is hidden, never detached —
  `state="detached"` times out; use `state="hidden"`.
