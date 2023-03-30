import requests #api작업을 위한 requests 모듈
from datetime import datetime
import smtplib #이메일 자동화를 위한 smtplib
import time #time.sleep(60) while문 안에서 60초마다 한번씩 실행되게
my_id = "gunha491@gmail.com"
my_password = "g!wjswnryeo12"

MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5<=iss_latitude<=MY_LAT+5 and MY_LONG-5<= iss_longitude<= MY_LONG+5:
        return True

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status() #응답오류 확인
    data = response.json() #json파일을 python 으로 변환
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0]) #데이터의 sunrise 데이터중 시간만 받는다.
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    print(datetime.now())
    time_now = datetime.now().hour
    if time_now>= sunset or time_now<= sunrise:
        return True

while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        connection= smtplib.SMTP("smtp.gmail.com")
        connection.starttls()
        connection.login(my_id, my_password)
        connection.sendmail(
            from_addr=my_id,
            to_addrs=my_id,
            msg="subject: look up \n \n the iss is above you in the sky."

        )




#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



