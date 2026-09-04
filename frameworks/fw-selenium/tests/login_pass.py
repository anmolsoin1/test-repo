import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from selenium.webdriver.common.by import By
from common import login, run


def body(driver):
    login(driver, "tomsmith", "SuperSecretPassword!")
    flash = driver.find_element(By.ID, "flash").text
    assert "You logged into a secure area!" in flash, flash
    return "login succeeded: " + flash.strip()


if __name__ == "__main__":
    sys.exit(run("HE Selenium - the-internet login PASS", body))
