# fw-taiko-codecept — Taiko + CodeceptJS on HyperExecute (stage)

Two independent HyperExecute jobs from one directory, both on **stage**,
`scenarioCommandStatusOnly: true` (status follows the command exit code).

## What it is

- **Taiko** (`hyperexecute-taiko.yaml`) — `taiko/the-internet-login.js` is a
  REPL-style taiko script (taiko globals injected by the runner, run via
  `npx taiko <file>`). It logs into https://the-internet.herokuapp.com/login
  (`tomsmith` / `SuperSecretPassword!`), asserts the secure-area flash text,
  logs out, asserts the logout flash. Chromium flags
  `--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage` are required
  on the linux runners — without them the scenario fails with
  `test_step_failed` at browser launch.
- **CodeceptJS** (`hyperexecute-codeceptjs.yaml`) — REST helper (no browser)
  against https://jsonplaceholder.typicode.com. Two test files, four
  scenarios, tagged `@smoke` / `@regression`. The runner command uses
  `--grep @smoke` to demonstrate tag filtering (3 of 4 scenarios run) and
  `mocha-junit-reporter` writes per-file junit XML into `reports/`
  (`MOCHA_FILE=reports/junit-<file>.xml`), uploaded as an artefact and wired
  into `partialReports`.

## Layout

```
hyperexecute-taiko.yaml       # job 1
hyperexecute-codeceptjs.yaml  # job 2
taiko/the-internet-login.js   # REPL-style taiko script
codecept/posts_test.js        # @smoke scenarios
codecept/users_test.js        # @smoke @regression / @regression scenarios
codecept.conf.js              # REST + JSONResponse helpers
package.json / package-lock.json
```

## Run locally

```bash
npm ci
npm run test:taiko            # needs a chromium; taiko postinstall fetches one
npm run test:codecept         # all 4 scenarios
npm run test:codecept:smoke   # --grep @smoke → 3 scenarios
npm run test:codecept:junit   # junit xml into reports/
```

## Run on HyperExecute (stage)

```bash
BIN=../../he-ledger-check/hyperexecute
$BIN --user anmolsoin --key <STAGE_KEY> --config hyperexecute-taiko.yaml --env stage --no-track --validate
$BIN --user anmolsoin --key <STAGE_KEY> --config hyperexecute-taiko.yaml --env stage --no-track
$BIN --user anmolsoin --key <STAGE_KEY> --config hyperexecute-codeceptjs.yaml --env stage --no-track
```

## What it proves / gotchas

- **Delete `node_modules` before dispatching.** The CLI zips the whole
  directory; a 203 MB `node_modules` (taiko) produced jobs that died with
  `lambda_error` / "not able to get your test scripts". With
  `node_modules` removed the same yamls ran fine — the runner does `npm ci`.
- The locally downloaded taiko chromium
  (`node_modules/taiko/.local-chromium/.../*.app`) also breaks the zip
  (`ERR::ZIP::ARC ... is a directory`) — remove it before dispatch.
- `npx taiko <file>` needs an explicit `openBrowser()`; on linux runners pass
  the `--no-sandbox` args above.
- CodeceptJS 4 `seeResponseContainsJson` does not match arrays (`[{...}]`
  assertions fail); assert on single objects instead.
- A `--grep` that matches zero scenarios exits 0 ("0 passed") — keep at
  least one tagged scenario per discovered file or accept the no-op.
- `stage-tests` API rows are empty on stage ("no test id associated") —
  statuses are driven by `scenarioCommandStatusOnly`.
