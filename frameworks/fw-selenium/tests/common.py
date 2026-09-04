import logging
import os
import sys

from selenium import webdriver
from selenium.webdriver.common.by import By

HUB = "https://{}:{}@stage-hub.lambdatestinternal.com/wd/hub"
BUILD = "HE-Selenium-Playground"


def make_driver(test_name):
    user = os.environ["LT_USERNAME"]
    key = os.environ["LT_ACCESS_KEY"]
    options = webdriver.ChromeOptions()
    options.set_capability("platformName", "Windows 10")
    options.set_capability("browserVersion", "latest")
    options.set_capability("LT:Options", {
        "build": BUILD,
        "name": test_name,
        "video": True,
        "network": True,
        "console": True,
    })
    return webdriver.Remote(
        command_executor=HUB.format(user, key),
        options=options,
    )


def mark(driver, status, remark):
    driver.execute_script(
        'lambda-hook: {{"action": "setTestStatus","arguments":{{"status":"{}","remark":"{}"}}}}'.format(
            status, remark
        )
    )


def run(test_name, body):
    """body(driver) -> remark string; raise to fail."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    os.makedirs("logs", exist_ok=True)
    handler = logging.FileHandler("logs/{}.log".format(test_name.replace(" ", "_")))
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    log = logging.getLogger(test_name)
    log.addHandler(handler)
    driver = None
    try:
        driver = make_driver(test_name)
        log.info("grid session started: %s", driver.session_id)
        remark = body(driver)
        mark(driver, "passed", remark)
        log.info("PASSED: %s", remark)
        return 0
    except Exception as exc:  # noqa: BLE001
        log.exception("FAILED: %s", exc)
        if driver is not None:
            mark(driver, "failed", str(exc)[:200])
        return 1
    finally:
        if driver is not None:
            driver.quit()


def login(driver, username, password):
    driver.get("https://the-internet.herokuapp.com/login")
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()


if __name__ == "__main__":
    sys.exit(0)
