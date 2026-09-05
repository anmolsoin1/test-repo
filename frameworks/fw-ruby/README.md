# fw-ruby — RSpec + Capybara + Selenium (remote grid) on HyperExecute

## What it proves
- HE `runtime: ruby` image runs a pinned-bundle RSpec suite (`Gemfile.lock`, bundler deployment mode, vendor/bundle cache).
- Capybara drives the **stage selenium grid** (`stage-hub.lambdatestinternal.com/wd/hub`) via `selenium-webdriver` remote Chrome.
- Locator variety: css, xpath, link_text (`spec/login_spec.rb`, `spec/checkboxes_spec.rb`).
- Explicit waits: `Selenium::WebDriver::Wait` (`selenium_wait` helper) AND a raw polling loop (`poll_until`) in `spec/spec_helper.rb`.
- `scenarioCommandStatusOnly: true` raw-mode run; per-scenario html reports uploaded as artefacts.
- Exactly ONE deliberate failure: `login_spec.rb` → "deliberate-failure: expects a marketing banner that does not exist". All other specs genuinely pass.

## Layout
- `Gemfile` / `Gemfile.lock` — rspec 3.12.0, capybara 3.39.2, selenium-webdriver 4.9.1 (pinned).
- `spec/spec_helper.rb` — `:lt_grid` Capybara driver, wait helpers, session reset.
- `spec/login_spec.rb` — 4 examples (3 pass, 1 deliberate fail).
- `spec/checkboxes_spec.rb` — 3 examples, all pass.
- `hyperexecute.yaml` — autosplit, 2 spec files, concurrency 2.

## Run (stage)
```bash
cd he-playground/fw-ruby
BIN=/Users/anmolsoin/knowledge-base-LT/he-ledger-check/hyperexecute
$BIN --user anmolsoin --key <stage-key> --config hyperexecute.yaml --env stage --validate
$BIN --user anmolsoin --key <stage-key> --config hyperexecute.yaml --env stage --no-track
# poll: GET https://api-stage-hyperexecute.lambdatestinternal.com/sentinel/v1.0/job/<jobId>?show_test_summary=true
```
No `node_modules`; deps installed by HE `pre:` via bundler.

## Runtime note (stage trap)
`runtime: {language: ruby, version: ...}` passes `--validate` but is broken on the
stage linux image: HE's bundled `setup-ruby` only knows versions up to 3.1.2 and
downloads `*-ubuntu-20.04.tar.gz` assets that ruby-builder deleted upstream (404).
Forcing `env: ImageOS: ubuntu22` downloads `ruby-3.1.2-ubuntu-22.04.tar.gz` OK but
the binary exits 1 on the image (ABI mismatch — image is really ubuntu-20.04).
So this project runs on the image's **system ruby 2.7.0** with gems pinned for it:
selenium-webdriver **4.8.6** (4.9+ requires ruby >= 3.0), capybara 3.39.2, rspec 3.12.0.
Note: `Chrome::Options#set_capability` does not exist in 4.8.6 — use
`Remote::Capabilities.chrome(...)` + `capabilities:` on the Capybara driver.

## Verified (job #90, 2026-09-05)
- Job `fde8bef6-9079-4c45-bc92-252137931d47`, job_number 90, status `failed`
  (expected — the single deliberate failure).
- Task `...4968SLT` (checkboxes_spec.rb): scenario completed, "3 examples, 0 failures".
- Task `...51263AKM` (login_spec.rb): scenario failed, "4 examples, 1 failure" —
  the only failure is `login_spec.rb:33 deliberate-failure`. Other 3 pass via the
  stage selenium grid (remote Chrome sessions against stage-hub wd/hub).
- Artefact `rspec-report` uploaded (report.html per scenario).
- `stage-tests/<scenarioStageId>` returns `[]` and tasks have no session_ids —
  expected: raw-mode + `scenarioCommandStatusOnly` on stage does not associate
  per-test rows (same trap as the other raw fw-* dirs).

