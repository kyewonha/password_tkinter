import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver

options = Options()
#쿠팡에서 자동화 방지를 만들어놓았는데 뚫는 꼼수(웹스크래핑 방지를 위해)
options.add_argument('--disable-blink-features=AutomationControlled')
driver = webdriver.Chrome('chromedriver 경로',options=options)
driver.implicitly_wait(3)

# 쿠팡 '커피' 검색 결과 페이지 접속
driver.get('https://www.coupang.com/np/search?component=&q=%EC%BB%A4%ED%94%BC&channel=user')
time.sleep(1)
products = driver.find_elements(By.CSS_SELECTOR,'li.search-product')

time.sleep(1)


# 검색 결과 페이지로 계속 돌아올 것이기 때문에 저장해 놓기
# current_window_handle 속성은 브라우저에서 현재 포커스된 창 또는 탭의 고유 식별자(창 핸들)를 검색하는 데 사용됩니다.
# 브라우저의 각 창이나 탭에는 일반적으로 긴 문자열인 고유 식별자가 할당됩니다.

search_result_window = driver.current_window_handle
print(search_result_window)

for product in products:
    # 아이템 클릭
    product.click()
    time.sleep(1)

    # 아이템 상세 페이지로 포커스 이동
    # 원 페이지는 window_handles[0] 새로 띄운 페이지는 window_handles[1]
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(1)
    # 아이템 상세 페이지에서 필요한 정보 가져오기

    # 아이템 상세 페이지 닫기
    driver.close()

    # 검색 결과 페이지로 포커스 이동 - 그래야 아이템 (product)를 클릭할 수 있음
    driver.switch_to.window(search_result_window)

driver.quit()