from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Chrome()#executable_path=r'/Users/kevindick/Downloads/chromedriver.exe')
driver.get("https://www.gasbuddy.com/Station/1")
html_source = driver.page_source
if 'Oops...' in html_source: print('Fail')
else: print('Exists!')
driver.quit()
