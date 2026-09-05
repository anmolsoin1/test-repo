"""Spec 1: login + dropdown + checkboxes on the-internet.

Locator variety: By.ID, By.CSS_SELECTOR, By.XPATH.
Wait strategy: WebDriverWait + expected_conditions (visibility/clickable).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

from common import run

BASE = "https://the-internet.herokuapp.com"


def body(driver, log):
    wait = WebDriverWait(driver, 15)
    checks = []

    # --- login page: By.ID inputs, By.CSS_SELECTOR submit ---
    driver.get(BASE + "/login")
    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("tomsmith")
    driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    flash = wait.until(EC.visibility_of_element_located((By.ID, "flash"))).text
    assert "You logged into a secure area!" in flash, flash
    checks.append("login ok")
    log.info("check 1 ok: login flash = %s", flash.strip())

    # --- dropdown page: By.ID select + Select API, By.XPATH option ---
    driver.get(BASE + "/dropdown")
    select_el = wait.until(EC.visibility_of_element_located((By.ID, "dropdown")))
    Select(select_el).select_by_visible_text("Option 2")
    selected = driver.find_element(By.XPATH, "//select[@id='dropdown']/option[@selected]").text
    assert selected == "Option 2", selected
    checks.append("dropdown ok")
    log.info("check 2 ok: dropdown selected = %s", selected)

    # --- checkboxes page: By.XPATH inputs, toggle and verify ---
    driver.get(BASE + "/checkboxes")
    boxes = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//form[@id='checkboxes']/input")))
    assert len(boxes) == 2, len(boxes)
    before = boxes[0].is_selected()
    boxes[0].click()
    after = driver.find_elements(By.XPATH, "//form[@id='checkboxes']/input")[0].is_selected()
    assert before != after, "checkbox state did not toggle"
    checks.append("checkboxes ok")
    log.info("check 3 ok: checkbox toggled %s -> %s", before, after)

    return "; ".join(checks)


if __name__ == "__main__":
    sys.exit(run("HE Selenium - forms spec (login/dropdown/checkboxes)", body))
