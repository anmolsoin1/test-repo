require "rspec"
require "capybara/rspec"
require "capybara/dsl"
require "selenium-webdriver"

BASE_URL = ENV.fetch("BASE_URL", "https://the-internet.herokuapp.com")
GRID_URL = "https://#{ENV.fetch("LT_USERNAME")}:#{ENV.fetch("LT_ACCESS_KEY")}" \
           "@stage-hub.lambdatestinternal.com/wd/hub"

Capybara.register_driver :lt_grid do |app|
  capabilities = Selenium::WebDriver::Remote::Capabilities.chrome(
    "browserVersion" => "latest",
    "LT:Options" => {
      "platformName" => "Windows 11",
      "build"        => "he-playground fw-ruby",
      "name"         => "the-internet rspec+capybara",
      "selenium_version" => "4.8.6"
    }
  )
  Capybara::Selenium::Driver.new(app, browser: :remote, url: GRID_URL, capabilities: capabilities)
end

Capybara.default_driver = :lt_grid
Capybara.default_max_wait_time = 30
Capybara.app_host = BASE_URL

RSpec.configure do |config|
  config.include Capybara::DSL
  config.after(:each) do
    Capybara.reset_sessions!
  end
end

# Explicit-wait helper on the raw selenium driver (Selenium::WebDriver::Wait).
def selenium_wait(timeout: 30, &block)
  Selenium::WebDriver::Wait.new(timeout: timeout, interval: 0.5).until do
    block.call(page.driver.browser)
  end
end

# Plain polling loop — intentionally NOT a Capybara waiter.
def poll_until(timeout: 30, interval: 1)
  deadline = Time.now + timeout
  loop do
    return true if yield
    raise "poll_until timed out after #{timeout}s" if Time.now > deadline
    sleep interval
  end
end
