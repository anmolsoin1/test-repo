import logging
import os

import pytest

BASE_URL = "https://the-internet.herokuapp.com"
LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "playwright-run.log")


@pytest.fixture(scope="session", autouse=True)
def run_logger():
    """Session-wide file logger; the log is uploaded as a HE artefact."""
    logger = logging.getLogger("fw-playwright-python")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(LOG_FILE, mode="w")
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
    logger.info("run started")
    yield logger
    logger.info("run finished")
    handler.close()


@pytest.hookimpl(tryfirst=True, wrapper=True)
def pytest_runtest_makereport(item, call):
    report = yield
    if report.when == "call":
        logging.getLogger("fw-playwright-python").info(
            "%s %s", item.nodeid, report.outcome.upper()
        )
    return report
