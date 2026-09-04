# fw-cypress — HyperExecute native Cypress mode (stage)

Playground for HyperExecute's **native Cypress mode** (`cypress: true` +
`cypressOps` in the yaml). Runs two Cypress spec files against
https://the-internet.herokuapp.com on stage.

## Structure

- `package.json` / `package-lock.json` — `cypress` pinned to `13.15.2`
- `cypress.config.js` — baseUrl `https://the-internet.herokuapp.com`, no
  support file, video off (keeps the job < 3 min)
- `cypress/e2e/login.cy.js` — login happy path + invalid-credentials error
  (both pass)
- `cypress/e2e/checkboxes.cy.js` — two passing checkbox tests plus one
  **deliberately failing** test (`DELIBERATE_FAILURE ...`) to show a failed
  row in the UI
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
- Autosplit creates one scenario per spec file (2 specs → 2 tasks);
  the UI shows per-spec rows labelled `Login.cy.js` / `Checkboxes.cy.js`.
- `cypressOps` Build/Tags/ProjectName surface in the HyperExecute UI;
  job is tagged framework `cypress` (`Frameworks: ["cypress"]`).
- A native **Custom Cypress Report** button + HyperExecute
  `report.html` (~476 KB) are generated per job; the mochawesome JSON
  (auto-injected by native mode at `cypress/results/mochawesome.json`)
  is uploaded as the `cypress-results` artefact.
- Deliberate failure shows as a failed scenario; the other spec passes.

## Verified run (job #58)

- Job: https://stage-hyperexecute.lambdatestinternal.com/hyperexecute/task?jobId=26759254-4a46-4d0b-b44a-c87d308ba7d9
- API status `failed`, remark `Job failed as encountered a Test level
  failure` — exactly the deliberate failure; taskCount 1 completed /
  1 failed; `stage-tests` populated (one row per scenario: passed /
  failed, `name` empty — native mode reports per-spec, not per-`it`).
- Screenshot of the UI: `fw-cypress-job58-ui.png`.

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
