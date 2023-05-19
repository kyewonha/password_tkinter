import requests
from datetime import datetime

# 내 현재 pixela 사이트  ='https://pixe.la/v1/users/kyewonha/graphs/graph1.html'
pixela_endpoint= "https://pixe.la/v1/users"

USERNAME= "kyewonha"
TOKEN= "sdkfjkdjfwoa12"

# https://docs.pixe.la/entry/post-user 참고해서 매개변수 만들기
pixela_params={
'token': TOKEN ,
'username' : USERNAME ,
'agreeTermsOfService': 'yes',
'notMinor': 'yes',
}

#계정 생성
# response = requests.post(url = pixela_endpoint, json=pixela_params)
# print(response.text)

# 그래프 생성
graph_endpoint = f'{pixela_endpoint}/{USERNAME}/graphs'
graph_id = 'graph1'
graph_config = {
    'id': graph_id,
    'name' : 'Cycling graph',
    'unit' : 'Km', #딱히 이름 정하는데 원칙이 있는 건 아님
    'type' : 'float',
    'color' : 'ajisai'
}
graph_header = {'X-USER-TOKEN' : TOKEN}

'''
requests모듈 안의 매개변수 쓰임의 차이 짚고 넘어가기
params -> url 중간에  ? 마크 뒤의 여러가지 쿼리스트링 작성에 도움 ?apikey= 2342342 등등  (보내는 형식은 파이썬 딕셔너리) 
json ->  url 본문의 내용 전달하는데 쓰임 (보내는 형식은 json스타일)
'''

# 기능1 )))) requests.post를 통해 기록을 업로드하자
postpixel_endpoint= f'{graph_endpoint}/{graph_id}'
headers = {'X-USER-TOKEN': TOKEN}
today = datetime.now()
# 방식 2: today = datetime(year=2023, month=4, day=24)
formatted_today= today.strftime('%Y%m%d')

# 여러 번 실행한다고 덧셈 되는 거 아니다.
postpixel_params = {
    'date' : formatted_today,
    'quantity' : input("얼마나 달리셨습니까?:  "),
}

# 업로드를 원할 시 주석 제거 후 사용
# response = requests.post(url= postpixel_endpoint, headers= headers, json=postpixel_params)
# print(response.text)


# 기능2 )))) requests.put을 통해 기존의 업로드를 수정해서 업데이트하자.
put_endpoint= f'{pixela_endpoint}/{USERNAME}/graphs/{graph_id}/{formatted_today}'
put_json = {
    'quantity': '5.67'
}

# 수정을 원할 시 주석을 제거 후 사용
# response= requests.put(url= put_endpoint,headers= headers, json= put_json)
# print(response.text)


# 기능3 )))) requests.delete을 통해 기존의 업로드를 삭제하자.
delete_endpoint= f'{pixela_endpoint}/{USERNAME}/graphs/{graph_id}/{formatted_today}'

# 기록 삭제를 원할 시 주석을 제거 후 사용
# response= requests.delete(url= put_endpoint,headers= headers, json= put_json)
# print(response.text)