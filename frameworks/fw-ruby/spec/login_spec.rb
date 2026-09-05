require "spec_helper"

RSpec.describe "the-internet login", type: :feature do
  it "navigates from home via link_text and logs in with valid credentials" do
    visit "/"
    click_link "Form Authentication" # link_text locator
    fill_in "username", with: "tomsmith"        # css #username
    fill_in "password", with: "SuperSecretPassword!"
    find(:xpath, "//button[@type='submit']").click # xpath locator
    selenium_wait { |d| d.find_elements(css: "#flash.success").any? }
    expect(page).to have_css("#flash.success", text: "You logged into a secure area!")
    expect(page).to have_xpath("//div[@id='content']//h2", text: "Secure Area")
  end

  it "rejects invalid credentials with an error flash" do
    visit "/login"
    fill_in "username", with: "not-a-user"
    fill_in "password", with: "wrong"
    click_button "Login"
    expect(page).to have_css("#flash.error", text: "Your username is invalid!")
  end

  it "logs out from the secure area" do
    visit "/login"
    fill_in "username", with: "tomsmith"
    fill_in "password", with: "SuperSecretPassword!"
    click_button "Login"
    expect(page).to have_css("a.button.secondary.radius", text: "Logout")
    click_link "Logout"
    expect(page).to have_css("#flash.success", text: "You logged out of the secure area!")
  end

  it "deliberate-failure: expects a marketing banner that does not exist" do
    visit "/login"
    # INTENTIONAL FAILURE — proves failure reporting works end to end.
    expect(page).to have_css("#marketing-banner", text: "Try KaneAI today!")
  end
end
