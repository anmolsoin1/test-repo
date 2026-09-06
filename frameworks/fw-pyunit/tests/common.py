"""Shared helpers for the fw-pyunit suite.

Driver goes to the CANONICAL host hub.lambdatest.com (HE VMs resolve it
internally) — this is what populates the job's Frameworks field (logo).
LT_USERNAME / LT_ACCESS_KEY are auto-injected into the HE VM env.
"""
import logging
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

HUB = "https://%s:%s@hub.lambdatest.com/wd/hub" % (
    os.environ["LT_USERNAME"],
    os.environ["LT_ACCESS_KEY"],
)
BASE_URL = "https://the-internet.herokuapp.com"
LOG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pyunit-run.log"))


def get_logger(name):
    logger = logging.getLogger("he-pyunit." + name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(LOG_PATH, mode="a")
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )
        logger.addHandler(handler)
    return logger


def make_driver(test_name):
    options = webdriver.ChromeOptions()
    options.platform_name = "Windows 10"
    options.set_capability("build", "HE-PyUnit-Playground")
    options.set_capability("name", test_name)
    options.set_capability("video", True)
    options.set_capability("network", True)
    options.set_capability("console", True)
    return webdriver.Remote(command_executor=HUB, options=options)


def mark(driver, status, remark):
    driver.execute_script(
        'lambda-hook: {"action": "setTestStatus", "arguments": '
        '{"status":"%s", "remark":"%s"}}' % (status, remark)
    )


def wait_for(driver, locator, timeout=15):
    """Explicit wait until a (By.X, value) locator is visible."""
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))


def poll_until_text(driver, locator, needle, timeout=15, interval=0.5):
    """Hand-rolled polling loop: re-read element text until it contains
    `needle` or the timeout expires. Returns the final text."""
    deadline = time.time() + timeout
    text = ""
    while time.time() < deadline:
        try:
            text = driver.find_element(*locator).text
            if needle in text:
                return text
        except Exception:
            pass
        time.sleep(interval)
    return text
