# fw-nightwatch — Nightwatch on HyperExecute (local headless Chrome)

Nightwatch 3.x running on the HyperExecute runner with a **fully local,
version-matched Chrome + chromedriver** — no Selenium grid, no system browser
dependency. Config conventions follow the official
[LambdaTest/Hyperexecute-Nightwatch-Sample](https://github.com/LambdaTest/Hyperexecute-Nightwatch-Sample)
repo, but its `remote` (grid) environment is replaced with a `local`
environment that launches headless Chrome on the runner itself.

## What it proves

- Nightwatch test discovery + autosplit on HyperExecute (`ls tests/*.js`,
  one scenario per test file, concurrency 2).
- Browser bootstrapping on a bare linux runner: `scripts/setup-chrome.sh`
  downloads a **pinned Chrome-for-Testing build (152.0.7977.82)** and its
  exact-matching chromedriver via `@puppeteer/browsers` into `./browsers/`
  (gitignored; downloaded fresh on each runner, kept out of the upload
  payload via `.hypertestignore`).
- `nightwatch.conf.js` finds those binaries recursively, so the same config
  works on the linux runner (`chrome-linux64/chrome`) and locally on mac
  (`chrome-mac-arm64/...app/...`).
- Real UI flows against https://the-internet.herokuapp.com:
  - `tests/login.js` — form login (valid creds), logout, flash-message and
    URL assertions.
  - `tests/dynamicLoading.js` — explicit waits: `waitForElementVisible` for
    the hidden→visible swap, `waitForElementNotVisible` for the loader, and
    `waitUntil` + `perform`-based polling for the final text.
- Nightwatch's built-in JUnit XML (`reports/CHROME_*.xml`) uploaded as a
  partial report + artefact.

## Layout

```
nightwatch.conf.js      # local env: chromedriver start_process + headless chrome
scripts/setup-chrome.sh # pins CHROME_VERSION, installs chrome + chromedriver
tests/login.js          # login + logout flows
tests/dynamicLoading.js # dynamic loading with explicit waits
hyperexecute.yaml       # autosplit, scenarioCommandStatusOnly: true
.hypertestignore        # keeps node_modules/, browsers/, reports/ out of the payload
```

## How to run

On HyperExecute (from this directory):

```bash
/Users/anmolsoin/knowledge-base-LT/he-ledger-check/hyperexecute \
  --user anmolsoin --key <stage-key> \
  --config hyperexecute.yaml --env stage --no-track
```

Locally (mac/linux):

```bash
npm ci
npm run setup:chrome
npx nightwatch --env local            # all tests
npx nightwatch --env local tests/login.js --testcase "logout returns to the login page"
```

## Notes / gotchas

- All 4 test cases (16 assertions) genuinely pass — no deliberate failure in
  this framework.
- On stage, `partialReports` (junit) does **not** associate individual test
  IDs — the UI shows scenario-level pass/fail only. That is a known stage
  limitation, not a config error.
- Test cases in one file share a browser session; `tests/login.js` calls
  `.end()` between cases to force a fresh session (reusing the session made
  `setValue` intermittently land nothing).
- After a click that navigates, wait on a new-page marker (e.g. `#username`)
  before reading `#flash` — `#flash` exists on both pages and resolves stale.
