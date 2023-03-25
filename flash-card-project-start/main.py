BACKGROUND_COLOR = "#B1DDC6"
Font_setting= ("Ariel", 40, 'italic')
Answer_font_Setting = ("Ariel", 60, 'bold')

import pandas as pd
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import random

#take data and make flash card
data= pd.read_csv('./data/french_words.csv')
to_learn = data.to_dict(orient= 'records')

def next_card():
    current_card = random.choice(to_learn)
    canvas.itemconfig(word_label1, text='French')
    canvas.itemconfig(word_label2, text= current_card['French'])




#--ui---------
window =Tk()
window.title("flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=800, height= 540, highlightthickness=0, bg= BACKGROUND_COLOR)
canvas.pack()

background_ch = Image.open('./images/card_back.png')
background_ch_photo = ImageTk.PhotoImage(background_ch)
background = Image.open('./images/card_front.png')
background_photo = ImageTk.PhotoImage(background)
front_img= canvas.create_image(400,270,image= background_photo)
canvas.grid(column=0, row=0 ,columnspan=2)
word_label1=canvas.create_text(400, 150,text="" , font= Font_setting,anchor='center' )
word_label2=canvas.create_text(400, 263,text="" , font= Answer_font_Setting, anchor='center')

x_pic = Image.open('./images/wrong.png')
x_photo = ImageTk.PhotoImage(x_pic)
x_mark= Button(window, image= x_photo, highlightthickness=0, borderwidth=0, command=next_card)
x_mark.grid(row=1, column=0)

v_pic = Image.open('./images/right.png')
v_photo = ImageTk.PhotoImage(v_pic)
v_mark= Button(window, image= v_photo, highlightthickness=0, borderwidth=0, command=next_card)
v_mark.grid(row=1, column=1)


window.mainloop()