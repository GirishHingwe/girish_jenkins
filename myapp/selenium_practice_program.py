from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Remote(
    command_executor= 'http://localhost:4444/wd/hub',
    options=options
)

driver.get("https://google.com")
print(driver.title)
driver.quit()