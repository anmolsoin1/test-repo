# fw-selenium — HyperExecute + Selenium Grid on stage

Real Selenium `Remote` sessions against the **stage selenium hub**
(`stage-hub.lambdatestinternal.com/wd/hub`) launched from a HyperExecute
job on stage. Tests hit https://the-internet.herokuapp.com/login.

## What it proves

- Selenium grid sessions can be opened from HE runners against the stage hub.
- Pass/fail is marked with the `lambda-hook` execute_script action
  (`setTestStatus`) — **not** `lambdatest_action` (that is the Playwright hook).
- Whether grid-backed scenarios get test IDs / per-test rows in the HE
  sentinel API on stage (checked via `session_ids` on tasks and the
  `stage-tests` endpoint — see the KB codemap / live-session notes).

## Layout

- `tests/common.py` — remote driver factory (Windows 10 / Chrome latest,
  `LT:Options` build `HE-Selenium-Playground`, video+network+console true),
  `lambda-hook` status marker, exit-code wrapper.
- `tests/login_pass.py` — valid login, must pass.
- `tests/login_fail_deliberate.py` — **deliberate failure** (asserts a banner
  the site never shows).
- `requirements.txt` — pinned selenium.
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
