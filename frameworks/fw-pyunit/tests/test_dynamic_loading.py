"""Dynamic-loading tests for the-internet.herokuapp.com (unittest style).

Covers: hidden element (example 1), element rendered after the fact
(example 2), explicit WebDriverWait plus a hand-rolled polling loop, and a
partial link_text locator.
"""
import unittest

from selenium.webdriver.common.by import By

from common import (
    BASE_URL,
    get_logger,
    make_driver,
    mark,
    poll_until_text,
    wait_for,
)


class DynamicLoadingTests(unittest.TestCase):
    log = get_logger("dynamic")

    def setUp(self):
        self.log.info("setUp: starting grid session for %s", self.id())
        self.driver = make_driver("pyunit-" + self._testMethodName)

    def tearDown(self):
        failed = True
        try:
            result = self._outcome.result
            failed = any(
                test is self for test, _exc in (result.failures + result.errors)
            )
        except Exception:
            pass
        mark(
            self.driver,
            "failed" if failed else "passed",
            self._testMethodName + (" FAILED" if failed else " OK"),
        )
        self.log.info("tearDown: %s -> %s", self.id(), "failed" if failed else "passed")
        self.driver.quit()

    # ---- tests ----

    def test_smoke_hidden_element_appears_after_start(self):
        self.driver.get(BASE_URL + "/dynamic_loading/1")
        # finish text exists in DOM but is hidden before Start
        finish = self.driver.find_element(By.CSS_SELECTOR, "#finish h4")
        self.assertFalse(finish.is_displayed())
        self.driver.find_element(By.XPATH, "//div[@id='start']/button").click()
        shown = wait_for(self.driver, (By.CSS_SELECTOR, "#finish h4"))
        self.assertEqual(shown.text, "Hello World!")

    def test_regression_element_rendered_after_fact(self):
        self.driver.get(BASE_URL + "/dynamic_loading/2")
        self.driver.find_element(By.CSS_SELECTOR, "#start button").click()
        # element does not exist until loading finishes
        self.assertEqual(len(self.driver.find_elements(By.ID, "finish")), 0)
        shown = wait_for(self.driver, (By.ID, "finish"))
        self.assertIn("Hello World!", shown.text)

    def test_regression_polling_loop_waits_for_hello_world(self):
        """Hand-rolled polling loop (no WebDriverWait) over example 2."""
        self.driver.get(BASE_URL + "/dynamic_loading/2")
        self.driver.find_element(By.XPATH, "//button[text()='Start']").click()
        text = poll_until_text(self.driver, (By.ID, "finish"), "Hello World!", timeout=20)
        self.assertIn("Hello World!", text)

    def test_smoke_dynamic_loading_index_links(self):
        self.driver.get(BASE_URL + "/dynamic_loading")
        # partial link_text locator variety
        self.driver.find_element(By.PARTIAL_LINK_TEXT, "on page that is hidden").click()
        self.assertIn("/dynamic_loading/1", self.driver.current_url)
        self.driver.back()
        self.driver.find_element(
            By.PARTIAL_LINK_TEXT, "rendered after the fact"
        ).click()
        self.assertIn("/dynamic_loading/2", self.driver.current_url)


if __name__ == "__main__":
    unittest.main()
