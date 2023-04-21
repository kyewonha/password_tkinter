from tkinter import *
#위에는 클래스 아래는 모듈
from tkinter import messagebox
import random
import pyperclip
import json


# pyper

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():

    input3.delete(0,END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    letters_list= [random.choice(letters) for _ in range(nr_letters)]
    symbols_list= [random.choice(symbols) for _ in range(nr_symbols)]
    numbers_list= [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = letters_list + symbols_list + numbers_list

    random.shuffle(password_list)
    # print(password_list)

    x="".join(password_list)
    pyperclip.copy(x)
    input3.insert(0, x)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def find_password():
     #json파일을 열어서 기존 입력값을 확인한다.

    website = input1.get()
    try:
        with open('data.json') as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title='Error', message ='no data file found')

    else:
        if website in data:
            email = data[website]['email']
            password= data[website]['password']
            messagebox.showinfo(title='website', message=f'Email: {email}\n Password: {password}')
        else:
            messagebox.showinfo(title='Error', message=f'no details for {website} exists')




def save():
    website_input = input1.get()
    email_input = input2.get()
    password_input = input3.get()
    new_data = {
        website_input: {
            "email": email_input,
            "password": password_input,
        }}

    if len(website_input)==0 or len(password_input)==0:
        messagebox.showinfo(title='Oops', message="you have left fields empty")
    else:
        try:
            with open('data.json', 'r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)

        else:
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            input1.delete(0, END)
            input3.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window =Tk()
window.title("password manager")
window.config(padx=40, pady= 40)
canvas = Canvas(width=200, height=200)
lock = PhotoImage(file= 'logo.png')
canvas.create_image(100,100, image=lock)
canvas.grid(column=1, row=0)

website= Label(text="Website:")
website.grid(column=0, row=1)

input1= Entry(width=21)
input1.grid(column=1, row=1)
input1.focus() # 마우스 시작커서 잡아주기

search_Button = Button(text="search")
search_Button.grid(column=2, row=1)

email = Label(text="Email/Username:")
email.grid(row=2, column=0)

# email.insert(END, "you22th@naver.com")

input2 = Entry(width=35)
input2.grid(column=1, row=2, columnspan=2)
input2.insert(0, "you22th@naver.com")

password= Label(text="Password:")
password.grid(row=3, column=0)

input3= Entry()
input3.grid(row=3, column=1)

password_button = Button(text="Generate password" , command=generate_password)
password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(row=4, column=1, columnspan=2)




window.mainloop()