"""Spec 3: API-state wait (requests polling) + ONE deliberate failure.

Wait strategy: poll a REST endpoint (jsonplaceholder) with `requests` until a
condition holds (post id=1 exists and has a non-empty title), with timeout.
Then combine API state with the browser, and finally the single deliberate
failure of the suite, clearly named in the session name and remark.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(__file__))

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import run

BASE = "https://the-internet.herokuapp.com"
API = "https://jsonplaceholder.typicode.com/posts/1"


def wait_for_api_state(log, timeout=30, interval=2):
    """Poll jsonplaceholder until post 1 exists with a non-empty title."""
    deadline = time.time() + timeout
    attempts = 0
    while time.time() < deadline:
        attempts += 1
        resp = requests.get(API, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("id") == 1 and data.get("title"):
                log.info("api-state wait satisfied after %d attempt(s): %r", attempts, data["title"])
                return data
        log.info("api-state wait attempt %d: status=%s, retrying", attempts, resp.status_code)
        time.sleep(interval)
    raise TimeoutError("API state never satisfied within {}s".format(timeout))


def body(driver, log):
    checks = []

    # --- check 1: API-state wait via requests polling ---
    post = wait_for_api_state(log)
    assert post["userId"] == 1, post
    checks.append("api-state wait ok")
    log.info("check 1 ok: post title = %r", post["title"])

    # --- check 2: combine API state with browser — verify the-internet
    #     home page lists the links used by the other specs (By.XPATH) ---
    driver.get(BASE)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[text()='Welcome to the-internet']")))
    links = {a.text for a in driver.find_elements(By.XPATH, "//div[@id='content']//a")}
    for expected in ("Form Authentication", "Dropdown", "Checkboxes", "Dynamic Loading"):
        assert expected in links, (expected, sorted(links))
    checks.append("home links ok")
    log.info("check 2 ok: %d links found on home page", len(links))

    # --- check 3: DELIBERATE FAILURE — asserts a banner text the login
    #     page never shows. Clearly named; everything above must pass. ---
    driver.get(BASE + "/login")
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    assert "Welcome to the Secure Area, hero!" in flash, (
        "DELIBERATE FAILURE: expected banner missing; got: " + flash
    )
    return "unreachable"


if __name__ == "__main__":
    sys.exit(run("HE Selenium - api-state spec + DELIBERATE FAIL wrong banner", body))
