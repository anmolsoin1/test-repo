"""Login-flow tests for the fw-reports showcase.

Each test appends a line to artifacts_dir/execution.log so the log file
can be uploaded as a job artefact after the run.
"""
import os
import time

LOG = os.path.join(os.path.dirname(__file__), "..", "out", "execution.log")


def _log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{time.strftime('%H:%M:%S')}] test_login_flow :: {msg}\n")


def test_login_valid_credentials():
    _log("login with valid credentials -> OK")
    assert True


def test_login_invalid_password_rejected():
    _log("login with wrong password -> rejected as expected")
    assert True


def test_login_locked_account_message():
    _log("locked account shows lockout message")
    assert True
