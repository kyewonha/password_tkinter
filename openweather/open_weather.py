import requests
#api를 다룰때 requests 모듈을 사용한다.

lat= 35.8269
lon= 127.1039
#appid는 apikey를 홈페이지에서 생성한다.
appid= '5d01925345e48a9eac9dc51d389369c3'

'''
강의 시점과 현재 사이 요금제 정책이 변경되어 기존 사이트가 이용 불가해서 계속 401에러가 났었음
faq 401 error를 들어가서 문제 확인 후 요금제 정책에 맞는 api를 사용하기로 함. 
디버깅하는데 시간 소요 많았다.
'''

own_endpoint = 'https://api.openweathermap.org/data/2.5/forecast'

weather_params = {
    'lat': lat,
    'lon': lon,
    'appid': appid,
}

# ? 이전까지를 endpoint로 잡는다.

response = requests.get(own_endpoint, params=weather_params)
# print(response.raise_for_status())

#12시간 슬라이싱
weather_data= response.json()
weather_slice = weather_data['list'][:12]

#will_rain이 true이면 프린트하기
will_rain= False

#weather_id 저장하기
for hour_data in weather_slice:
    condition_code= hour_data['weather'][0]['id']
    if int(condition_code) <700:
        will_rain = True

if will_rain:
    print("Bring an umbrella.")