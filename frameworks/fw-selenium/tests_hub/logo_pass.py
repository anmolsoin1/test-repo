import sys; sys.path.insert(0, 'tests_hub')
from common import *
d = make_driver("logo-exp pass")
try:
    d.get("https://the-internet.herokuapp.com/login")
    WebDriverWait(d, 15).until(EC.presence_of_element_located((By.ID, "username"))).send_keys("tomsmith")
    d.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
    d.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    WebDriverWait(d, 15).until(EC.text_to_be_present_in_element((By.ID, "flash"), "You logged into a secure area!"))
    mark(d, "passed", "logo experiment pass"); print("LOGO-EXP PASS")
except Exception as e:
    mark(d, "failed", str(e)[:200]); print("LOGO-EXP FAIL:", e); d.quit(); sys.exit(1)
d.quit()
