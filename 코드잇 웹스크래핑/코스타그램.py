from selenium import webdriver
from bs4 import BeautifulSoup
# selenium docs개정으로 생긴 구문 find_element(BY.CSS.SELECTOR,"")
from selenium.webdriver.common.by import By
import time
import requests ; from openpyxl import Workbook

wb = Workbook(write_only=True)
ws= wb.create_sheet()
ws.append(['이미지 주소','내용','해시 태그','좋아요 수 ','댓글 수 '])

driver = webdriver.Chrome()
driver.implicitly_wait(2)
driver.get("https://workey.codeit.kr/costagram/index")

# requests.get -> driver.page_source 를 쓰면 된다.
# response = requests.get("https://workey.codeit.kr/costagram/index")

time.sleep(1)
#로그인 하기

#로그인 버튼 누르기
driver.find_element(By.CSS_SELECTOR,'a.top-nav__login-link').click()
time.sleep(1)

# 아이디 , 비번 -> send_keys로 보내고 로그인 버튼 클릭
driver.find_element(By.CSS_SELECTOR,'input.login-container__login-input').send_keys('codeit')
driver.find_element(By.CSS_SELECTOR,'input.login-container__password-input').send_keys('datascience')
driver.find_element(By.CSS_SELECTOR,'input.login-container__login-button').click()
time.sleep(1)

#스크롤 내리기 ( 맨 마지막으로 스크롤 내려도 밑에서 업데이트 되어 새로운 것이 생길 수 잇으니, time.sleep()과 new_height, last_height를 비교하기)
# 스크롤 맨 마지막 값 반환
last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     # 맨 마지막으로 스크롤 수행하기
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(0.5)
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

time.sleep(1)

#포스트들을 한번에 받아오기 (find_elements를 통해)
elements = driver.find_elements(By.CSS_SELECTOR,'div.post-list__post')


# time.sleep() 을 넉넉하게 시간을 줘서 적절하게 웹스크래핑이 되는지 조사하자 - 안그러면 중복으로 수집되는 경우 발생
for ele in elements:
    ele.click()
    time.sleep(1)
    # 여기서부터 beautifulsoup을 selenium과 같이 활용 , 클릭, 스크롤 같은 처리는 selenium / html분석은 bs4가 유리한 듯
    # driver.page_source로 현재 페이지의 html코드를 반환한다.
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # 현재 페이지의 div 태그의 style 속성을 가진 것들을 선택
    div_with_style = soup.select('div[style]')

    if div_with_style:
        '''
        인덱스를 사용해야한다.
        style_attribute = div_with_style['style']
        TypeError: list indices must be integers or slices, not str
        '''
        style_attribute = div_with_style[0]['style']
        # print(style_attribute)
        # url(" ~~~  ") 로 둘러싸인 안쪽 부분을 추출한다.
        url_text = style_attribute.split('url("')[1].split('")')[0]
        image_url = "https://workey.codeit.kr" + url_text
        img_urls.append(image_url)

        content = driver.find_element(By.CSS_SELECTOR,'.content__text').text.strip()
        hashtags = driver.find_element(By.CSS_SELECTOR,'.content__tag-cover').text.strip()
        like_count = driver.find_element(By.CSS_SELECTOR,'.content__like-count').text.strip()
        comment_count= driver.find_element(By.CSS_SELECTOR,'.content__comment-count').text.strip()
        ws.append([content, hashtags, like_count, comment_count])

        # print(content, hashtags, like_count, comment_count)

    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR,'.close-btn').click()
    time.sleep(1)

driver.quit()
wb.save('코스타그램.xlsx')
wb.close()
#이미지 다운로드 url을 입력해서 image를 다운로드 받는다

for i in range(len(img_urls)):
    time.sleep(1)
    image_url = img_urls[i]
    response = requests.get(image_url)
    filename = f'image{i}.jpg'
    with open(filename, 'wb+') as f:
        f.write(response.content)


