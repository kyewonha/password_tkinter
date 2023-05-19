
#  nutritionix api 와 sheety api 를 통합

import requests
import os

# header를 작성하기 위한 nutritionix 사이트에서 api key, id 발급 -> 한번만 하면 계속 가능
api_id = os.environ.get('API_ID_NUT')
api_key = os.environ.get('API_KEY_NUT')


# authorize를 받기 위한 header 작성
'''
Obtaining API Keys & Authenticating

Signup for a Nutritionix API developer account at developer.nutritionix.com
When logged into the Nutritionix developer console, get your APP ID and APP Key at this page: https://developer.nutritionix.com/admin/access_details
Required HEADERS when accessing Nutritionix V2 API endpoints:
x-app-id: Your app ID issued from developer.nutritionix.com)
x-app-key: Your app key issued from developer.nutritionix.com)
'''

header_item = {
    "x-app-id": api_id,
    "x-app-key": api_key,
}

#body를 집어넣는다.

# 입력예시 ) input_= 'running 3 hour, walking 20 min',tennis 2 hour, walk 30 min
# 위 api는 자동으로 자연어 처리를 해서 어떤 운동을 얼마나 했는지. natural하게 작성해도 받아들인다.

input_1 = input("어떤 운동을 하셨나요?: ")
# input_1 = 'run 30 min, bicycle 30 min'
body= { "query":input_1,
        "gender":"female",
        "weight_kg":76,
        "height_cm":181,
        "age":26
        }
a= requests.post(url = 'https://trackapi.nutritionix.com/v2/natural/exercise', headers= header_item, json=body)
result= a.json()
# print(result)

# TODO json파일을 하나씩 쪼갠다.

#행 구분
from datetime import datetime

now_time = datetime.now()
now_month = now_time.strftime('%m'); now_day= now_time.strftime('%d')
now_year = now_time.strftime('%Y'); now_hour = now_time.strftime('%H')
now_min = now_time.strftime("%M")
# print(type(now_time))


for i in range(len(result['exercises'])):
    
    # 1열 ~ 5열 세팅 ( 날짜, 시간, 운동, 총 수행 시간, 총 칼로리 소모량)
    a_row = f'{now_month}/{now_day}/{now_year}'
    b_row = f'{now_hour}:{now_min}'
    c_row = result['exercises'][i]['user_input'].title()
    d_row= result['exercises'][i]['duration_min']
    # print(d_row)
    e_row= result['exercises'][i]['nf_calories']

    # TODO sheety api와 interact해서 스프레드시트에 옮긴다.
    sheety_url= 'https://api.sheety.co/6d79efedb697246c02e8e254bd9bdf57/workout기록/workouts'
    # sheety_headers= {'Authorization':'Basic bnVsbDpudWxs'} 비밀번호가 틀린지 authorization 인코딩이 잘못됨. -> 조회도 잘 안되서 짜증남
    sheety_body= {'workout':
    {
        'date': a_row,
        'time': b_row,
        'exercise': c_row,
        'duration': d_row,
        'calories': e_row
    }
    }
    response = requests.post(sheety_url, json = sheety_body, )
    print(response.status_code)

    