"""Dropdown + checkboxes on the-internet — form controls."""
import pytest
from playwright.sync_api import expect

from conftest import BASE_URL


@pytest.mark.smoke
def test_dropdown_select_by_value(page):
    page.goto(f"{BASE_URL}/dropdown")
    dropdown = page.locator("#dropdown")
    dropdown.select_option("1")
    expect(dropdown).to_have_value("1")
    dropdown.select_option(label="Option 2")
    expect(dropdown).to_have_value("2")


@pytest.mark.regression
def test_checkboxes_toggle_independently(page):
    page.goto(f"{BASE_URL}/checkboxes")
    boxes = page.locator("#checkboxes input[type='checkbox']")
    expect(boxes).to_have_count(2)
    first, second = boxes.nth(0), boxes.nth(1)
    # initial state: first unchecked, second checked
    expect(first).not_to_be_checked()
    expect(second).to_be_checked()
    first.check()
    expect(first).to_be_checked()
    expect(second).to_be_checked()
    second.uncheck()
    expect(first).to_be_checked()
    expect(second).not_to_be_checked()


@pytest.mark.regression
def test_deliberate_failure_checkbox_default_state(page):
    """DELIBERATE FAILURE: asserts checkbox 1 is checked by default (it is not)."""
    page.goto(f"{BASE_URL}/checkboxes")
    first = page.locator("#checkboxes input[type='checkbox']").nth(0)
    # wrong on purpose — the first checkbox starts UNCHECKED
    expect(first).to_be_checked()
