# coding=UTF-8

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

browser = webdriver.Firefox()
browser.get("http://epub.cnki.net/kns/brief/result.aspx?dbprefix=CJFQ")
browser.maximize_window()
print(browser.window_handles)
time.sleep(5)
browser.find_element_by_id("1_4").click()
time.sleep(1)
browser.find_element_by_id("expertvalue").send_keys("TI='生态' and KY='生态文明'")
time.sleep(3)

select = Select(browser.find_element_by_id("year_from"))
select.select_by_visible_text("2014")

browser.find_element_by_xpath("//input[@value='清除']").click()
browser.find_element_by_xpath("//input[@name='经济与管理科学']").click()
time.sleep(10)
browser.find_element_by_id("btnSearch").click()
time.sleep(5)
browser.switch_to.frame('iframeResult')
browser.find_element_by_css_selector('#selectCheckbox').click()
time.sleep(1)
browser.find_element_by_link_text('导出 / 参考文献').click()
time.sleep(5)
print(browser.window_handles)
browser.switch_to.window(browser.window_handles[1])
browser.find_element_by_css_selector('.GTContentTitle > td:nth-child(1) > input:nth-child(1)').click()
time.sleep(5)
#print(browser.page_source)
'''
time.sleep(10)
browser.switch_to.frame('iframeResult')
browser.find_element_by_link_text("被引").click()

time.sleep(10)
table_data = browser.find_element_by_css_selector("#ctl00").text
print(table_data)

browser.find_element_by_link_text("下一页").click()
time.sleep(10)
table_data = browser.find_element_by_css_selector("#ctl00").text
print('***************************************')
print(table_data)
'''
browser.quit()




