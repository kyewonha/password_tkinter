import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

# response = requests.get("https://workey.codeit.kr/orangebottle/index")

driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get("https://workey.codeit.kr/orangebottle/index")
time.sleep(2)
branches_info=[]
branches = driver.find_elements(By.CSS_SELECTOR, 'div.branch')
for element in branches:
    name = element.find_element(By.CSS_SELECTOR, 'p.city').text
    address = element.find_element(By.CSS_SELECTOR, 'p.address').text
    phonenum = element.find_element(By.CSS_SELECTOR, 'span.phoneNum').text
    branches_info.append([name, address, phonenum])



print(branches_info)
driver.quit()
