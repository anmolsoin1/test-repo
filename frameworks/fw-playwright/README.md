# fw-playwright — HyperExecute Playwright (raw mode) matrix entry

Production-grade Playwright suite running on HyperExecute **stage** in
raw-discovery mode against https://the-internet.herokuapp.com.

## What it proves

- **Locator variety** across specs: `getByLabel`, `getByRole` (button /
  link / heading / checkbox), `getByText`, `getByTestId` (via
  `testIdAttribute: 'id'` workaround — the site has no `data-testid`),
  css selectors, and xpath.
- **Wait strategies**: explicit waits (`locator.waitFor` with
  visible/hidden/attached/detached), polling waits (`expect.poll`), and
  API-based waits (`page.waitForResponse`) — exercised against
  `/dynamic_loading/1`, `/dynamic_loading/2`, and `/dynamic_controls`,
  which are built for exactly this.
- **Multiple tests per spec** (3–4 `test()` per file) so each HyperExecute
  scenario (= spec file in raw mode) carries several test results.
- **One deliberate failure** (`artifact-demo.spec.js`, test name starts
  with `DELIBERATE-FAILURE`) to exercise failure screenshots, junit
  failure reporting, and artefact upload. All other tests genuinely pass.

## Layout

- `tests/login.spec.js` — 4 tests, getByLabel/getByRole/getByText/css/xpath
- `tests/dynamic-loading.spec.js` — 4 tests, waitFor + waitForResponse + expect.poll
- `tests/dynamic-controls.spec.js` — 3 tests, remove/add + enable/disable + getByTestId
- `tests/checkboxes.spec.js` — 3 tests, css/getByRole/xpath
- `tests/artifact-demo.spec.js` — 1 test, the deliberate failure
- `playwright.config.js` — chromium only, 1 worker, list+junit+html reporters
- `hyperexecute.yaml` — raw discovery (`ls tests/*.spec.js`), autosplit,
  `scenarioCommandStatusOnly: true`

## How to run

Local:

```bash
npm ci && npx playwright install chromium
npx playwright test --project=chromium   # 14 pass, 1 deliberate fail
```

HyperExecute (stage), from this directory:

```bash
/Users/anmolsoin/knowledge-base-LT/he-ledger-check/hyperexecute \
  --user anmolsoin --key <stage-key> \
  --config hyperexecute.yaml --env stage --no-track
```

Verify via API (basic auth `anmolsoin:<key>`):

```bash
curl -s -u anmolsoin:<key> \
  "https://api-stage-hyperexecute.lambdatestinternal.com/sentinel/v1.0/job/<jobId>?show_test_summary=true"
```

## Known stage behaviour (verified)

- Raw-mode Playwright runs produce **no `stage-tests` rows** on stage —
  per-test association only happens in native cypress mode (see fw-cypress).
  junit/partialReports do not associate test IDs either. The junit XML and
  HTML report still upload as artefacts.
- `post:` steps are skipped for failed scenarios, so reporters/artefacts
  must be produced by the runner command itself.
