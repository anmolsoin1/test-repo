import os, logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# KEY DIFFERENCE: hub.lambdatest.com (the canonical host HE VMs resolve
# internally) instead of stage-hub.lambdatestinternal.com — testing whether
# platform-observable grid traffic is what sets the job's Frameworks field.
HUB = "https://%s:%s@hub.lambdatest.com/wd/hub" % (os.environ["LT_USERNAME"], os.environ["LT_ACCESS_KEY"])

def make_driver(name):
    options = webdriver.ChromeOptions()
    options.platform_name = "Windows 10"
    options.set_capability("build", "HE-Logo-Experiment")
    options.set_capability("name", name)
    options.set_capability("video", True)
    options.set_capability("network", True)
    options.set_capability("console", True)
    return webdriver.Remote(command_executor=HUB, options=options)

def mark(driver, status, remark):
    driver.execute_script('lambda-hook: {"action": "setTestStatus", "arguments": {"status":"%s", "remark":"%s"}}' % (status, remark))
