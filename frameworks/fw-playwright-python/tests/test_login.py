"""Login flows on the-internet /login — locator variety + API wait."""
import pytest
from playwright.sync_api import expect

from conftest import BASE_URL


@pytest.mark.smoke
def test_valid_login_redirects_to_secure_area(page):
    page.goto(f"{BASE_URL}/login")
    # locator variety: css attribute selector + css id
    page.locator("input[name='username']").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    # API-state wait: capture the POST /authenticate response on submit
    with page.expect_response("**/authenticate") as resp_info:
        page.locator("button[type='submit']").click()
    assert resp_info.value.status in (302, 303)  # the-internet redirects after POST
    expect(page).to_have_url(f"{BASE_URL}/secure")
    # expect() auto-wait on a text locator
    expect(page.locator("text=You logged into a secure area!")).to_be_visible()


@pytest.mark.smoke
def test_invalid_login_shows_error_flash(page):
    page.goto(f"{BASE_URL}/login")
    # xpath locator variety
    page.locator("//input[@id='username']").fill("notauser")
    page.locator("//input[@id='password']").fill("wrongpass")
    page.locator("button.radius").click()
    flash = page.locator("#flash")
    expect(flash).to_contain_text("Your username is invalid!")


@pytest.mark.regression
def test_logout_returns_to_login_page(page):
    page.goto(f"{BASE_URL}/login")
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    page.locator("button[type='submit']").click()
    expect(page).to_have_url(f"{BASE_URL}/secure")
    # link_text-style locator via role/text
    page.get_by_role("link", name="Logout").click()
    expect(page).to_have_url(f"{BASE_URL}/login")
    expect(page.locator("#flash")).to_contain_text("You logged out of the secure area!")
