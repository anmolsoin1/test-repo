"""Reusable API-testing helpers: explicit wait, polling, retry-on-flake.

These are deliberately dependency-free so they run in the bare HyperExecute
python runtime with only pytest + requests installed.
"""
import functools
import logging
import time

log = logging.getLogger("he-pytest.helpers")


class WaitTimeoutError(AssertionError):
    """Raised when wait_until/poll_until exceed their deadline."""


def wait_until(predicate, timeout=10.0, interval=0.5, desc="condition"):
    """Explicit wait: call predicate() every `interval` seconds until it
    returns truthy or `timeout` seconds elapse. Returns the truthy value.
    Raises WaitTimeoutError on expiry."""
    deadline = time.monotonic() + timeout
    attempts = 0
    while True:
        attempts += 1
        value = predicate()
        if value:
            log.info("wait_until(%s) satisfied after %d attempt(s)", desc, attempts)
            return value
        if time.monotonic() >= deadline:
            raise WaitTimeoutError(
                f"wait_until({desc}) not satisfied within {timeout}s "
                f"({attempts} attempts, interval={interval}s)"
            )
        time.sleep(interval)


def poll_until(fn, predicate, timeout=10.0, interval=1.0, desc="poll"):
    """Polling helper: call fn() every `interval` seconds until
    predicate(result) is true, with an overall `timeout` deadline.
    Returns the first satisfying result. Raises WaitTimeoutError on expiry."""
    deadline = time.monotonic() + timeout
    attempts = 0
    last = None
    while True:
        attempts += 1
        last = fn()
        if predicate(last):
            log.info("poll_until(%s) satisfied after %d attempt(s)", desc, attempts)
            return last
        if time.monotonic() >= deadline:
            raise WaitTimeoutError(
                f"poll_until({desc}) predicate never matched within {timeout}s "
                f"(last result: {last!r})"
            )
        time.sleep(interval)


def assert_schema(obj, schema, path="root"):
    """Response-schema assertion: every key in `schema` must exist in `obj`
    and be an instance of the given type (or tuple of types). Nested dicts
    are recursed into. Raises AssertionError with a dotted path on mismatch."""
    assert isinstance(obj, dict), f"{path}: expected dict, got {type(obj).__name__}"
    for key, expected in schema.items():
        loc = f"{path}.{key}"
        assert key in obj, f"{loc}: missing key (have: {sorted(obj)})"
        value = obj[key]
        if isinstance(expected, dict):
            assert_schema(value, expected, path=loc)
        else:
            assert isinstance(value, expected), (
                f"{loc}: expected {expected}, got {type(value).__name__} "
                f"(value: {value!r})"
            )


def retry_on_flake(retries=2, delay=0.5, exceptions=(AssertionError,)):
    """Decorator: rerun the test body up to `retries` extra times if it raises
    one of `exceptions`. Use sparingly, only on tests hitting known-flaky
    endpoints; each retry is logged so flakes stay visible."""
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, retries + 2):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    log.warning(
                        "retry_on_flake: %s attempt %d/%d failed: %s",
                        fn.__name__, attempt, retries + 1, exc,
                    )
                    if attempt > retries:
                        break
                    time.sleep(delay)
            raise last_exc
        return wrapper
    return decorator
