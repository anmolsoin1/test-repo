# fw-jmeter — Apache JMeter performance plans on HyperExecute (stage)

## What this is

Runs real JMeter `.jmx` test plans in non-GUI mode on a HyperExecute linux
runner against the public `https://jsonplaceholder.typicode.com` API, and
uploads the JTL results files, the JMeter HTML dashboards (tarballed), and the
console log as job artefacts.

Reference patterns: `repos/LTQAAutomation/Benchmarking/` (`run_rbac_benchmark.sh`
runner shape, `*.jmx` hand-written plans) — shrunk to playground size.

## Layout

- `plans/posts-read-plan.jmx` — TG 5 users × 3 loops; GET `/posts`,
  GET `/posts/1`, GET `/posts/1/comments`; response-code, body-substring,
  JSONPath, and duration (<5s) assertions; Summary Report listener.
- `plans/posts-write-plan.jmx` — TG 5 users × 3 loops; POST `/posts` (201
  assert), PUT `/posts/1`, DELETE `/posts/1`; JSON bodies via raw POST body,
  `Content-Type` header manager.
- `plans/deliberate-fail-plan.jmx` — the ONE deliberate failure: GET
  `/no-such-endpoint-he-playground` asserted as 200 (server returns 404).
  Proves JMeter assertion failures propagate to a failed HE scenario.
- `run_jmeter.sh` — per-scenario runner: `jmeter -n -t <plan> -l reports/<n>.jtl
  -e -o reports/dashboard-<n>`, counts failed samples in the JTL, tarballs the
  dashboard, exits 1 if any sample failed (with
  `scenarioCommandStatusOnly: true` the exit code IS the scenario status).
- `hyperexecute.yaml` — raw dynamic discovery (`ls plans/*.jmx` → 3 scenarios),
  java 17 runtime, `pre:` downloads + extracts apache-jmeter-5.6.3 from
  archive.apache.org.

## How to run

```bash
cd he-playground/fw-jmeter
../../he-ledger-check/hyperexecute --user anmolsoin --key <stage-key> \
  --config hyperexecute.yaml --env stage --no-track
```

Then poll `GET https://api-stage-hyperexecute.lambdatestinternal.com/sentinel/v1.0/job/<jobId>?show_test_summary=true`
(basic auth `anmolsoin:<key>`).

## What it proves

- JMeter can be installed fresh on the HE linux runner in `pre:` (tgz from
  archive.apache.org) and driven non-GUI with the raw test-discovery mode.
- One `.jmx` file = one HE scenario (autosplit across scenarios,
  concurrency 2).
- JMeter assertion failures → non-zero runner exit → failed scenario, while
  the other two plans pass (deliberate-fail is isolated).
- JTL CSVs + HTML dashboards + console log survive as downloadable artefacts.

## Expected result

2 scenarios pass, 1 scenario fails (deliberate-fail-plan). `Frameworks` on the
job stays empty (no grid sessions, non-native framework) — JMeter jobs show no
framework logo on stage.

## Verified run (stage, 2026-09-05)

Job #99 `6c6a432b-0c24-4fe8-b8bb-76faeff5bb52` — status `failed` ("Job failed
as encountered a Test level failure", by design): posts-read 45/45 pass,
posts-write 45/45 pass, deliberate-fail 4/28 samples failed → scenario failed.
All three artefact groups (JTL 2.7 KB, dashboards 3.0 MB, run log) uploaded
`completed`. JMeter install via archive.apache.org tgz in `pre:` works on the
linux runner with `runtime: java 17`. Note: JMeter's own exit code is 0 even
with assertion failures — the runner must count `"false"` rows in the JTL and
exit non-zero itself for the scenario to fail.
