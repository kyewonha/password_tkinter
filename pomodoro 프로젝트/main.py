from tkinter import *
#이미지 편집을 도와주기 위한 pil 패키지
from PIL import Image, ImageTk
import math

# 프로젝트 하면서 느낀점 기능을 여러 개 구현 시킬 수록 앞의 기능이 막힐 수 있다. 이럴 때 전역변수를 자주 만들어서 기능적으로 충돌이 없게 만드는게 중요한거같다.

# ---------------------------- CONSTANTS ------------------------------- #
#칼라헥스코드 지정
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25 * 60
SHORT_BREAK_MIN = 5 * 60
LONG_BREAK_MIN = 20 * 60
reps=0 #함수 호출 시 마다 +1 해줄라고
timer= None #이따 전역변수로 지정을 해주기 위해
remaining_time = None
timer_paused =None
timer_running =None
#    ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    window.after_cancel(timer) #타이머의 동작을 멈춘다.
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    global reps
    reps = 0
#---------------------------------------------
def pause_timer():
    global timer_paused
    global timer , remaining_time, timer_running
    timer_running =False
    if timer_paused:
        return
    timer_paused = True
    if timer is not None:
        window.after_cancel(timer)
    remaining_time_str = canvas.itemcget(timer_text, 'text')
    if remaining_time_str:
        remaining_time = int(remaining_time_str[:2]) * 60 + int(remaining_time_str[3:])

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, timer, timer_paused, remaining_time, timer_running
    # timer_running: 여러번의 timer가 생성되는 것을 방지한다.
    if timer_running:
        return
    timer_paused= False
    timer_running= True
    if remaining_time is None:
        reps += 1
        work_sec = WORK_MIN #* 60
        short_break_sec = SHORT_BREAK_MIN #* 60
        long_break_sec = LONG_BREAK_MIN #* 60
        if reps % 8 == 0:
            count_down(long_break_sec)
            title_label.config(text="Break", fg=RED)
        elif reps % 2 == 0:
            count_down(short_break_sec)
            title_label.config(text="Break", fg=PINK)
        else:
            count_down(work_sec)
            title_label.config(text="Work", fg=GREEN)
    else:
        count_down(remaining_time)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    start_button.config(state=DISABLED)
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f'0{count_sec}'
    canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        marks = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            marks += "✓"
        check_marks.config(text=marks)

    # 일시정지 상태일 때는 타이머가 실행되지 않도록 수정
    if timer_paused:
        timer = None
    start_button.config(state=NORMAL)
# ---------------------------- UI SETUP ------------------------------- #

window =Tk()
window.title('Pomodoro')
window.config(padx= 30, pady=30, bg=YELLOW)

title_label= Label(text="Timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME,15,"bold"))
title_label.grid(column=1, row=0)

#작은 토마토를 원해서 canvas 사이즈부터 줄였다. highlightthickness는 테두리 없애기 위해서 . 시각적인 효과
canvas = Canvas(width=100, height= 112, bg=YELLOW, highlightthickness=0)
#이미지 형식으로 집어 넣어야 코드가 동작한다. 
img= Image.open('./tomato.png')
#zoom을 0.5로 잡아서 전체적인 이미지 사이즈를 줄인다.
zoom =0.5
#tuple과 listcomprehension을 이용해 각각의 픽셀사이즈를 줄여준다.
pixel_x, pixel_y = tuple([int(zoom * x) for x in img.size])
img = ImageTk.PhotoImage(img.resize((pixel_x, pixel_y)))
canvas.create_image(50,56, image= img)
timer_text= canvas.create_text(50,55, text="00:00" ,fill = 'white', font=(FONT_NAME, 15, 'bold'))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2, ipadx=20, ipady=20)

reset_button= Button(text="Reset", highlightthickness=0, command=reset_timer, padx=7)
reset_button.grid(column=1, row=2, ipadx=20, ipady=20)

pause_button= Button(text="pause", highlightthickness=0, command=pause_timer, padx =7)
pause_button.grid(column=2, row=2, ipadx=20, ipady=20)

check_marks= Label(fg=GREEN, bg=YELLOW)
check_marks.grid(column=1, row=3)


window.mainloop()

