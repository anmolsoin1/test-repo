# fw-selenium — HyperExecute + Selenium Grid on stage

Real Selenium `Remote` sessions against the **stage selenium hub**
(`stage-hub.lambdatestinternal.com/wd/hub`) launched from a HyperExecute
job on stage. Tests hit https://the-internet.herokuapp.com and
https://jsonplaceholder.typicode.com.

## What it proves

- Selenium grid sessions can be opened from HE runners against the stage hub.
- Locator variety works on the stage grid: `By.ID`, `By.CSS_SELECTOR`,
  `By.XPATH`, `By.LINK_TEXT`, `By.PARTIAL_LINK_TEXT`, `By.TAG_NAME`.
- Wait strategies: `WebDriverWait` + `expected_conditions`
  (visibility / element_to_be_clickable / presence_of_all), **FluentWait**
  (`WebDriverWait` with `poll_frequency` + `ignored_exceptions` — Selenium's
  fluent-wait API), and an **API-state wait** (poll a REST endpoint with
  `requests` until a condition holds, then continue in the browser).
- Pass/fail is marked with the `lambda-hook` execute_script action
  (`setTestStatus`) — **not** `lambdatest_action` (that is the Playwright hook).
- Whether grid-backed scenarios get test IDs / per-test rows in the HE
  sentinel API on stage (checked via `session_ids` on tasks and the
  `stage-tests` endpoint — expected empty on stage).

## Layout

- `tests/common.py` — remote driver factory (Windows 10 / Chrome latest,
  `LT:Options` build `HE-Selenium-Playground`, video+network+console true),
  `lambda-hook` status marker, per-spec file logging into `logs/`,
  exit-code wrapper.
- `tests/spec_1_forms.py` — login (`By.ID` + `By.CSS_SELECTOR`),
  dropdown (`By.ID` + `Select` + `By.XPATH` option), checkboxes (`By.XPATH`
  toggle). All checks must pass.
- `tests/spec_2_waits.py` — home → dynamic_loading/2 via
  `By.LINK_TEXT` / `By.PARTIAL_LINK_TEXT`, `By.TAG_NAME` heading sanity,
  explicit `WebDriverWait` on `#finish`, then FluentWait
  (0.5s poll, ignores `StaleElementReferenceException`) on the same element.
  All checks must pass.
- `tests/spec_3_api_state.py` — API-state wait polling jsonplaceholder
  post 1 with `requests` until the title is present; verifies the home-page
  link list via `By.XPATH`; then the suite's **ONE deliberate failure**
  (asserts a banner the login page never shows — clearly named in the
  session name).
- `requirements.txt` — pinned `selenium==4.25.0`, `requests==2.32.3`.
- `hyperexecute.yaml` — autosplit, `scenarioCommandStatusOnly: true` so
  scenario status follows the command exit code.

## Run

```bash
cd he-playground/fw-selenium
export LT_ACCESS_KEY=<stage-access-key>   # entries/0003, anmolsoin@testmuai.com (stage)
../../he-ledger-check/hyperexecute --user anmolsoin --key $LT_ACCESS_KEY \
  --config hyperexecute.yaml --env stage --no-track
```

Validate first with `--validate`. Poll for completion via the sentinel API
(basic auth `anmolsoin:<key>`):

```bash
curl -su anmolsoin:$LT_ACCESS_KEY \
  "https://api-stage-hyperexecute.lambdatestinternal.com/sentinel/v1.0/job/<jobId>?show_test_summary=true"
```
