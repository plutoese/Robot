# coding=UTF-8

import time
from selenium import webdriver

profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", "60.191.164.22")
profile.set_preference("network.proxy.http_port", 3128)
profile.update_preferences()

browser=webdriver.Firefox(firefox_profile=profile)
browser.get("http://www.baidu.com")
browser.maximize_window()
time.sleep(20)
browser.quit()