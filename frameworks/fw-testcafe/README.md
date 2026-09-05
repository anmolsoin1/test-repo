# fw-testcafe — HyperExecute playground (TestCafe, raw mode)

TestCafe 3.7.2 on HyperExecute **stage**, raw mode (`scenarioCommandStatusOnly:
true`). Two fixture files against the-internet.herokuapp.com: one passing
login, one **deliberate failure**.

## What it proves

- TestCafe can run on a HyperExecute linux runner using a Chrome binary it
  bootstraps itself: `pre` installs `chrome@stable` via
  `npx -y @puppeteer/browsers install chrome@stable` and `runner.js` finds the
  binary under `chrome/linux-*/chrome-linux64/chrome`.
- **Browser bootstrap gotcha:** `testcafe path:<bin>:headless` fails with
  `Error: The specified browser name is not valid!` — the `:headless` suffix
  is not parsed for the `path:` provider (and paths containing spaces break
  its argument splitting). Working form:
  `testcafe "path:<bin> --headless=new --no-sandbox --disable-dev-shm-usage"`.
- Selector variety: by id (`#username`), css class (`button.radius`), visible
  text (`Selector('h2').withText(...)`).
- Wait strategies: fixed `t.wait(1000)`, explicit
  `Selector.with({ timeout: 10000 })`, and a hand-rolled polling assertion
  loop (`pollUntil` in `tests/smoke-login.js`).
- Reporters: `spec` to stdout + TestCafe's built-in `xunit` reporter writes
  `reports/<fixture>.xml`, picked up by `partialReports` (known stage trap:
  junit partialReports never associate test IDs — scenario status comes from
  the runner exit code via `scenarioCommandStatusOnly: true`).
- The `hyperexecute` browser provider plugin
  (`testcafe-browser-provider-hyperexecute`, targets the LT selenium grid) is
  documented in this dir's history but NOT used: it points at the prod hub
  and this playground runs raw-mode local browser instead.

## Layout

- `package.json` / `package-lock.json` — pinned `testcafe@3.7.2`
- `runner.js` — finds Chrome (CHROME_BIN env / argv override / `chrome/` dir /
  PATH), runs one fixture headless, writes xunit report, exit code = result
- `tests/smoke-login.js` — passing login flow (selectors + waits + polling)
- `tests/regression-login-invalid-password.js` — **deliberate failure**:
  wrong password, asserts a success banner; job is expected `failed` with
  1 passed / 1 failed scenario
- `hyperexecute.yaml` — the job definition

## Run locally

```bash
npm ci
CHROME_BIN="/path/to/chrome" node runner.js tests/smoke-login.js                       # passes
CHROME_BIN="/path/to/chrome" node runner.js tests/regression-login-invalid-password.js # fails (deliberate)
# or let runner.js find one: npx -y @puppeteer/browsers install chrome@stable
```

## Run on HyperExecute (stage)

```bash
cd he-playground/fw-testcafe
../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute.yaml --env stage --no-track
```

Validate first with `--validate`. Verify via the sentinel API (see
`he-playground/fw-puppeteer/README.md`) — never trust CLI output.
