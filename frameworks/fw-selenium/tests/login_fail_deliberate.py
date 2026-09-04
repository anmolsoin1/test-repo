import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from selenium.webdriver.common.by import By
from common import login, run


def body(driver):
    """DELIBERATE FAILURE: asserts a message that the-internet never shows."""
    login(driver, "tomsmith", "SuperSecretPassword!")
    flash = driver.find_element(By.ID, "flash").text
    assert "Welcome to the Secure Area, hero!" in flash, "expected banner missing; got: " + flash
    return "unreachable"


if __name__ == "__main__":
    sys.exit(run("HE Selenium - DELIBERATE FAIL wrong banner", body))
