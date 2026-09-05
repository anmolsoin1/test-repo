"""Spec 2: navigation links + dynamic_loading/2.

Locator variety: By.LINK_TEXT, By.PARTIAL_LINK_TEXT, By.TAG_NAME, By.XPATH, By.CSS_SELECTOR.
Wait strategies:
  - WebDriverWait + expected_conditions (visibility of #finish after start).
  - FluentWait: WebDriverWait with poll_frequency + ignored_exceptions
    (Selenium's fluent wait API) for the same async element.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import run

BASE = "https://the-internet.herokuapp.com"


def body(driver, log):
    checks = []

    # --- home page navigation: By.LINK_TEXT + By.PARTIAL_LINK_TEXT ---
    driver.get(BASE)
    driver.find_element(By.LINK_TEXT, "Dynamic Loading").click()
    assert driver.current_url.endswith("/dynamic_loading"), driver.current_url
    driver.find_element(By.PARTIAL_LINK_TEXT, "rendered after the fact").click()
    assert driver.current_url.endswith("/dynamic_loading/2"), driver.current_url
    checks.append("link nav ok")
    log.info("check 1 ok: reached %s via LINK_TEXT/PARTIAL_LINK_TEXT", driver.current_url)

    # --- By.TAG_NAME: page structure sanity before starting ---
    headings = driver.find_elements(By.TAG_NAME, "h3")
    assert any("Dynamically Loaded" in h.text for h in headings), [h.text for h in headings]
    checks.append("tag_name ok")
    log.info("check 2 ok: h3 headings = %s", [h.text for h in headings])

    # --- explicit wait: click start, wait for #finish to be visible ---
    driver.find_element(By.CSS_SELECTOR, "#start button").click()
    finish = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )
    assert finish.text == "Hello World!", finish.text
    checks.append("explicit wait ok")
    log.info("check 3 ok: #finish text = %s", finish.text)

    # --- fluent wait: reload, start again, poll #finish with poll_frequency
    #     and ignored stale-element exceptions ---
    driver.get(BASE + "/dynamic_loading/2")
    driver.find_element(By.CSS_SELECTOR, "#start button").click()
    fluent = WebDriverWait(
        driver,
        15,
        poll_frequency=0.5,
        ignored_exceptions=[StaleElementReferenceException],
    )
    finish2 = fluent.until(lambda d: d.find_element(By.ID, "finish"))
    fluent.until(lambda d: finish2.text.strip() != "")
    assert "Hello World!" in finish2.text, finish2.text
    checks.append("fluent wait ok")
    log.info("check 4 ok: fluent wait got #finish = %s", finish2.text)

    return "; ".join(checks)


if __name__ == "__main__":
    sys.exit(run("HE Selenium - waits spec (links/dynamic loading)", body))
