##################### Hard Starting Project ######################
from datetime import datetime
# 이거 안쓰면 datetime.datetime.now() 이렇게 접근해야 한다.
import pandas as pd
import random
import smtplib

df= pd.read_csv("./birthdays.csv",encoding='utf-8')

myEmail = 'gunha491@gmail.com'
#구글 앱 비밀번호
myPassword = 'fjmczveudppwzitf'

today= datetime.now()
today_tuple= (today.month, today.day)

birthdays_dict = {(df_row['month'], df_row['day']): df_row for (index, df_row) in df.iterrows()}

if today_tuple in birthdays_dict:
    file_path = f'letter_templates/letter_{random.randint(1,3)}.txt'
    birthday_person = birthdays_dict[today_tuple]
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents= contents.replace("[NAME]", birthday_person['name'])

# 구글 앱 비밀번호 (windows 컴퓨터를 생성하고 위에 mypassword에 기존 비밀번호 대신 집어넣음.)
    with smtplib.SMTP("smtp.gmail.com", port= 587) as connection:
        connection.starttls()
        connection.login(myEmail, myPassword)
        connection.sendmail(from_addr=myEmail,
                            to_addrs= birthday_person['email'],
                            msg=f"Subject:Happy Birthday {birthday_person['name']}!\n\n{contents}")

#HINT 3: Then you could compare and see if today's month/day matches one of the keys in birthday_dict like this:
# if (today_month, today_day) in birthdays_dict:

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv
# HINT: https://www.w3schools.com/python/ref_string_replace.asp

# 4. Send the letter generated in step 3 to that person's email address.
# HINT: Gmail(smtp.gmail.com), Yahoo(smtp.mail.yahoo.com), Hotmail(smtp.live.com), Outlook(smtp-mail.outlook.com)



