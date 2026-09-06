"""Dynamic loading on the-internet — explicit waits + polling."""
import pytest
from playwright.sync_api import expect

from conftest import BASE_URL


@pytest.mark.smoke
def test_example1_hidden_element_becomes_visible(page):
    page.goto(f"{BASE_URL}/dynamic_loading/1")
    page.locator("#start button").click()
    # expect() wait on hidden-then-visible element
    finish = page.locator("#finish h4")
    expect(finish).to_be_visible(timeout=15000)
    expect(finish).to_have_text("Hello World!")


@pytest.mark.regression
def test_example2_element_rendered_after_fact(page):
    page.goto(f"{BASE_URL}/dynamic_loading/2")
    # element does not exist in DOM yet
    assert page.locator("#finish").count() == 0
    page.locator("#start button").click()
    # explicit wait_for_selector polling-ish (attached, then visible)
    page.wait_for_selector("#finish", state="attached", timeout=15000)
    page.wait_for_selector("#finish h4", state="visible", timeout=15000)
    expect(page.locator("#finish h4")).to_have_text("Hello World!")


@pytest.mark.regression
def test_example2_loading_bar_disappears(page):
    page.goto(f"{BASE_URL}/dynamic_loading/2")
    page.locator("#start button").click()
    # poll until the spinner is hidden (example 2 keeps it in the DOM, display:none)
    page.wait_for_selector("#loading", state="hidden", timeout=15000)
    expect(page.locator("#finish h4")).to_be_visible()
