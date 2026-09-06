"""Login tests for the-internet.herokuapp.com/login (unittest style).

Covers: valid login, invalid-password rejection via subTest data variety,
and one clearly-named DELIBERATE failure for pipeline signal.
Tag convention: `smoke` or `regression` appears in the test name; run_one.py
filters on the TAG env var.
"""
import unittest

from selenium.webdriver.common.by import By

from common import BASE_URL, get_logger, make_driver, mark, wait_for


class LoginTests(unittest.TestCase):
    log = get_logger("login")

    def setUp(self):
        self.log.info("setUp: starting grid session for %s", self.id())
        self.driver = make_driver("pyunit-" + self._testMethodName)
        self.driver.get(BASE_URL + "/login")
        wait_for(self.driver, (By.ID, "username"))

    def tearDown(self):
        # unittest outcome detection (works on 3.10)
        failed = True
        try:
            result = self._outcome.result
            failed = any(
                test is self for test, _exc in (result.failures + result.errors)
            )
        except Exception:
            pass
        status = "failed" if failed else "passed"
        mark(self.driver, status, self._testMethodName + (" FAILED" if failed else " OK"))
        self.log.info("tearDown: %s -> %s", self.id(), status)
        self.driver.quit()

    # ---- tests ----

    def test_smoke_valid_login_lands_on_secure_area(self):
        # id locators
        self.driver.find_element(By.ID, "username").send_keys("tomsmith")
        self.driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        # css locator on the submit button
        self.driver.find_element(By.CSS_SELECTOR, "button.radius[type='submit']").click()
        header = wait_for(self.driver, (By.XPATH, "//h2[contains(text(),'Secure Area')]"))
        self.assertIn("Secure Area", header.text)
        flash = wait_for(self.driver, (By.ID, "flash"))
        self.assertIn("You logged into a secure area!", flash.text)
        # link_text locator for logout
        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        flash = wait_for(self.driver, (By.ID, "flash"))
        self.assertIn("You logged out of the secure area!", flash.text)

    def test_regression_invalid_credentials_are_rejected(self):
        cases = [
            ("baduser", "SuperSecretPassword!", "Your username is invalid!"),
            ("tomsmith", "wrongpassword", "Your password is invalid!"),
            ("", "", "Your username is invalid!"),
        ]
        for username, password, expected in cases:
            with self.subTest(username=username, password=password):
                self.driver.get(BASE_URL + "/login")
                wait_for(self.driver, (By.ID, "username")).send_keys(username)
                self.driver.find_element(By.NAME, "password").send_keys(password)
                self.driver.find_element(By.TAG_NAME, "button").click()
                flash = wait_for(self.driver, (By.CSS_SELECTOR, "#flash.error"))
                self.assertIn(expected, flash.text)

    def test_regression_DELIBERATE_FAILURE_wrong_page_title(self):
        """DELIBERATE FAILURE — asserts a wrong title to prove failure
        propagation (exit code, red status, artefact remark)."""
        self.assertEqual(
            self.driver.title,
            "This Title Does Not Exist — deliberate pyunit failure",
            "intentional mismatch",
        )


if __name__ == "__main__":
    unittest.main()
