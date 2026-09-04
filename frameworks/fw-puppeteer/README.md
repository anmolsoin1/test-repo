# fw-puppeteer — HyperExecute playground (Puppeteer, plain node)

Puppeteer on HyperExecute without any test framework: two plain node spec
files driven by a tiny hand-written runner (`runner.js`), with hand-rolled
JUnit XML output (`lib/junit.js`) — no mocha/jest/junit packages.

## What it proves

- Puppeteer can launch its own bundled headless Chromium on a HyperExecute
  linux runner (download happens during `npm ci` in `pre`).
- A framework-less setup works: discovery is `ls tests/*.spec.js`, each spec
  is a scenario, `scenarioCommandStatusOnly: true` makes scenario status
  follow the runner's exit code.
- Hand-written JUnit XML in `reports/` is picked up by `partialReports` and
  uploaded as an artefact.
- Tag convention via filename prefix: `smoke_*.spec.js` (passing login test)
  vs `regression_*.spec.js` (one **deliberate** failure —
  `regression_login_invalid_password.spec.js` asserts a success banner after
  a wrong-password login; the job is expected to end `failed` with 1 passed /
  1 failed scenario).

## Layout

- `package.json` / `package-lock.json` — pinned `puppeteer@23.11.1`
- `runner.js` — launches Chromium (`--no-sandbox`), runs each spec in a fresh
  page, times it, writes `reports/puppeteer-results.xml`, exits non-zero on
  any failure
- `lib/junit.js` — dependency-free JUnit `<testsuite>` XML builder
- `tests/smoke_login.spec.js` — real login on the-internet.herokuapp.com (pass)
- `tests/regression_login_invalid_password.spec.js` — deliberate failure
- `hyperexecute.yaml` — the job definition

## Run locally

```bash
npm ci
node runner.js tests/smoke_login.spec.js          # passes
node runner.js tests/regression_login_invalid_password.spec.js  # fails (deliberate)
```

## Run on HyperExecute (stage)

```bash
cd he-playground/fw-puppeteer
../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute.yaml --env stage --no-track
```

Validate first with `--validate` instead of `--no-track`. Then verify via the
sentinel API (see `he-playground/` sibling READMEs) — never trust CLI output.
