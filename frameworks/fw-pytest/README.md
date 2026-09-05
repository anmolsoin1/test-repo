# fw-pytest — production-grade pytest API-testing framework for HyperExecute (stage)

API test suite against `https://jsonplaceholder.typicode.com`, run on
HyperExecute **stage** in raw mode (`scenarioCommandStatusOnly: true`) with
autosplit, dynamic discovery, and junit partial reports.

## What it proves

- **Explicit wait helper** — `wait_until(predicate, timeout, interval)`
  (`tests/helpers.py`): polls a predicate until truthy or the deadline
  expires, raising `WaitTimeoutError`.
- **Polling helper** — `poll_until(fn, predicate, timeout, interval)`:
  repeatedly calls `fn()` until `predicate(result)` matches, with a deadline.
- **Retry-on-flake helper** — `@retry_on_flake(retries, delay)` decorator:
  reruns the test body on failure, logging each retry.
- **Parametrized tests** — `@pytest.mark.parametrize` over post/user/comment
  ids, so the 3 files carry 45 tests.
- **Response-schema assertions** — `assert_schema(obj, schema)` validates
  keys + types recursively (incl. nested `address.geo`), not just status
  codes.
- **Markers** — `smoke` vs `regression` (`tests/pytest.ini`); the smoke yaml
  runs `-m smoke`, the full yaml runs everything.
- **One deliberate failure** — `test_posts.py::test_post_not_found` (GET
  /posts/999 expects an id back). Everything else genuinely passes.

## Layout

- `tests/helpers.py` — wait_until / poll_until / retry_on_flake / assert_schema
- `tests/conftest.py` — session-wide `api` requests.Session fixture + file
  logging to `pytest-run.log` (uploaded as HE artefact)
- `tests/test_posts.py`, `tests/test_users.py`, `tests/test_comments.py`
- `requirements.txt` — pinned deps (`pytest==8.3.2`, `requests==2.32.3`)
- `hyperexecute.yaml` — full run (all markers)
- `hyperexecute-smoke.yaml` — smoke-marker run only

## How to run

```bash
cd he-playground/fw-pytest
KEY=LT_GsJOkDD7fZFOAaA0AMBVK2muSGFuiz6BysimcQeReBnfK8m  # anmolsoin stage
../../he-ledger-check/hyperexecute --user anmolsoin --key $KEY \
  --config hyperexecute.yaml --env stage --no-track --validate   # validate
../../he-ledger-check/hyperexecute --user anmolsoin --key $KEY \
  --config hyperexecute.yaml --env stage --no-track              # dispatch
```

The CLI returns at dispatch; poll
`GET https://api-stage-hyperexecute.lambdatestinternal.com/sentinel/v1.0/job/<jobId>?show_test_summary=true`
(basic auth `anmolsoin:$KEY`) for status.

## Expected result

45 tests: 44 passed, 1 failed (`test_post_not_found`, deliberate). Job status
`Failed`, one scenario task per test file (3 tasks with concurrency 2).
`stage-tests` stays empty — junit partialReports do not associate test IDs on
stage (only native cypress mode does; see fw-cypress).
