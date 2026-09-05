require "spec_helper"

RSpec.describe "the-internet checkboxes", type: :feature do
  it "toggles checkbox 1 via css and checkbox 2 via xpath" do
    visit "/checkboxes"
    box1 = find(:css, "#checkboxes input:nth-of-type(1)")
    box2 = find(:xpath, "//form[@id='checkboxes']/input[2]")
    expect(box1).not_to be_checked
    expect(box2).to be_checked
    box1.click
    box2.click
    expect(find(:css, "#checkboxes input:nth-of-type(1)")).to be_checked
    expect(find(:xpath, "//form[@id='checkboxes']/input[2]")).not_to be_checked
  end

  it "polls until checkbox state settles after a toggle (polling loop)" do
    visit "/checkboxes"
    find(:css, "#checkboxes input:nth-of-type(1)").click
    poll_until(timeout: 20, interval: 1) do
      page.driver.browser
          .find_element(css: "#checkboxes input:nth-of-type(1)")
          .selected?
    end
    selenium_wait(timeout: 10) do |d|
      d.find_element(css: "#checkboxes input:nth-of-type(1)").selected?
    end
  end

  it "waits explicitly for the page heading via Selenium::WebDriver::Wait" do
    visit "/checkboxes"
    heading = selenium_wait(timeout: 20) do |d|
      el = d.find_element(xpath: "//div[@id='content']//h3")
      el if el.text == "Checkboxes"
    end
    expect(heading.text).to eq("Checkboxes")
  end
end
