# fw-cypress — HyperExecute native Cypress mode (stage)

Playground for HyperExecute's **native Cypress mode** (`cypress: true` +
`cypressOps` in the yaml). Runs three Cypress spec files against
https://the-internet.herokuapp.com on stage.

## Structure

- `package.json` / `package-lock.json` — `cypress` pinned to `13.15.2`,
  `cypress-xpath` pinned to `2.0.1`
- `cypress.config.js` — baseUrl `https://the-internet.herokuapp.com`,
  support file `cypress/support/e2e.js` (registers `cypress-xpath`),
  video off (keeps the job < 3 min)
- `cypress/support/e2e.js` — one line: `require("cypress-xpath")`
- `cypress/e2e/login.cy.js` — **locator variety**: css id selectors
  (`#username`), attribute selectors (`[name="username"]` — same mechanism
  as `[data-cy="..."]`; the site has no `data-cy` attributes),
  `cy.contains("button", "Login")` by visible text, and `cy.xpath(...)`
  via cypress-xpath (3 `it`s, all pass)
- `cypress/e2e/checkboxes.cy.js` — three passing checkbox tests (incl. a
  `should($els)` callback-polling test) plus one **deliberately failing**
  test (`DELIBERATE_FAILURE ...`) to show a failed row in the UI
- `cypress/e2e/dynamic-loading.cy.js` — **waits**: `cy.intercept` +
  `cy.wait("@dynamicPage")` API wait, explicit per-command `{ timeout: ... }`
  overrides, and `should()` callback polling (Cypress's built-in
  retry-ability — no hard sleeps) against the 5-second dynamic-loading page
- `hyperexecute.yaml` — autosplit over `ls cypress/e2e`, `cypress: true`
  with `cypressOps` (Build / Tags / BuildTags / Network / FullHar /
  ProjectName), `scenarioCommandStatusOnly: true` so scenario status
  follows the `npx cypress run` exit code

## Run

```bash
cd he-playground/fw-cypress
../../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute.yaml --env stage --no-track --validate   # validate first
../../../he-ledger-check/hyperexecute --user anmolsoin --key <STAGE_KEY> \
  --config hyperexecute.yaml --env stage --no-track
```

Stage key: `entries/0003-qa-test-accounts-ltqa.md` → row
`anmolsoin@testmuai.com (stage)`. Always run the CLI with this directory as
cwd (concurrent CLI processes in one dir clobber `.updatedhyperexecute.yaml`).

## What it proves

- Native cypress mode works on stage (`runson: linux`,
  `runtime: node 20`, cypress 13.15.2 installed via `npm ci` in `pre`).
- Autosplit creates one scenario per spec file; with 3 specs and
  `concurrency: 2`, the runner packed two specs onto one task (task 1 =
  checkboxes; task 2 = login + dynamic-loading). The UI shows per-spec
  rows (`Checkboxes.cy.js`, `Login.cy.js`, `Dynamic-loading.cy.js`).
- `cypressOps` Build/Tags/ProjectName surface in the HyperExecute UI;
  job is tagged framework `cypress` (`Frameworks: ["cypress"]`).
- A native **Custom Cypress Report** button + HyperExecute
  `report.html` (~477 KB) are generated per job; the mochawesome JSON
  (auto-injected by native mode at `cypress/results/mochawesome.json`)
  is uploaded as the `cypress-results` artefact.
- `cy.intercept`/`cy.wait('@alias')`, explicit `{timeout}` overrides,
  `should()` callback polling, and `cy.xpath` (cypress-xpath 2.0.1 via
  the support file) all work unchanged in native mode on stage.
- Deliberate failure shows as a failed scenario; the other specs pass.

## Verified runs (jobs #58, #73, #85)

- Latest job (#85, 2026-09-04):
  https://stage-hyperexecute.lambdatestinternal.com/hyperexecute/task?jobId=ca37afe8-3853-40d0-b52f-efad871382e1
  API status `failed`, remark `Job failed as encountered a Test level
  failure` — exactly the deliberate failure in `checkboxes.cy.js`;
  tasks: 1 failed / 1 completed; `total_tests: 3`.
  `stage-tests/<scenarioStageId>` IS populated — **one row per scenario
  (spec file), not per `it`**: 3 rows total, statuses `failed` (checkboxes),
  `passed` (login), `passed` (dynamic-loading); `name` and `session_id`
  are empty strings in every row. Per-`it` detail exists only inside the
  mochawesome JSON artefact / Custom Cypress Report, not in the API.
- #73 (first v2 attempt) unexpectedly failed `login.cy.js`: the button
  text is `" Login"` (leading space, icon font) — `have.text "Login"`
  is too strict; fixed with `contain.text`. Everything else passed.
- Screenshot of the #85 UI: `fw-cypress-job85-ui.png` (job #58:
  `fw-cypress-job58-ui.png`).

## Gotchas seen on stage

- `uploadArtefacts` globs that match nothing on a task report
  `failed / no file uploaded` — point them at files native mode always
  writes (`cypress/results/**/*`).
- One run hit a runner glibc flake: `Inconsistency detected by ld.so:
  ../elf/dl-tls.c: 481 ...` which crashed Chrome before any test ran
  (task marked `test_step_failed`). Retry fixes it.
- `post:` steps are skipped (`postrun cancelled`) when the scenario
  fails.
- `Tasks[].session_ids` / `test_ids` stay null in the job API — use
  `stage-tests/<scenarioStageId>` for per-scenario rows.
