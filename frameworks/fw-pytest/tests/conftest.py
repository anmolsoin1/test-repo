import logging
import os

import pytest
import requests

BASE_URL = "https://jsonplaceholder.typicode.com"

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "pytest-run.log")


@pytest.fixture(scope="session", autouse=True)
def configure_logging():
    """Session-wide file logging; the log file is uploaded as a HE artifact."""
    logger = logging.getLogger("he-pytest")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(os.path.abspath(LOG_PATH), mode="w")
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )
    if not logger.handlers:
        logger.addHandler(handler)
    logger.info("Logging configured, base URL = %s", BASE_URL)
    yield
    logger.info("Test session finished")


@pytest.fixture(scope="session")
def api():
    session = requests.Session()
    session.headers.update({"Accept": "application/json"})
    return session
