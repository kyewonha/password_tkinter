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
SKYBLUE = "#91c5f5"
FONT_NAME = "Courier"
WORK_MIN = 25 * 60
SHORT_BREAK_MIN = 5 * 60
LONG_BREAK_MIN = 20 * 60
reps=0 #함수 호출 시 마다 +1 해줄라고
timer= None # 전역변수로 사용하려면 None으로 초기 설정을 해야 함.
remaining_time = None
timer_paused =None
#    ---------------------------- TIMER RESET ------------------------------- #

def reset_timer():
    global reps
    start_button.config(state=NORMAL)
    window.after_cancel(timer) #타이머의 동작을 멈춘다.
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_marks.config(text="")
    reps = 0
#---------------------------------------------
def pause_timer():
    global timer_paused
    global timer , remaining_time # remaining_time 일시정지 후 재생해도 기존 시간을 기억하게
    # start_button이 활성화된다.
    start_button.config(state=NORMAL)
    #일시정지 되었을 때 또 일시정지 할 수 없게
    if timer_paused:
        return
    #timer_paused 전역변수 설정으로 일시정지 중복 실행을 방지한다.
    timer_paused = True
    if timer is not None:
        #count_down에서 생성한 timer를 삭제한다.
        window.after_cancel(timer)
    remaining_time_str = canvas.itemcget(timer_text, 'text')
    # remaining_time을 초로 반환해야 count_down 인자로 집어넣을 수 있다.
    if remaining_time_str:
        remaining_time = int(remaining_time_str.split(':')[0]) * 60 + int(remaining_time_str.split(':')[1])
        #remaining_time은 전역 변수기 때문에 return 하지 않아도 다음 함수에서 remaining_time에 대한 값을 기억해서 사용할 수 있다.

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, timer_paused, remaining_time
    # 여러번의 timer가 생성되는 것을 방지하고자 문제 해결 방안을 생각
    # 1) 전역변수 활용 방법을 고안했으나 -> if timer_running: return으로 지정했으나 -> 다른 함수랑 겹쳐 사용할 때 자꾸 오류발생
    # 2) 버튼을 비활성(start_buton.config(state=DISABLED)으로 하는 걸로 수정
    timer_paused= False # 일시정지 모드 해제
    if remaining_time is None: # pause_timer()를 하지 않았을 때
        reps += 1 # reps는 한 바퀴 돌 때 마다 +1 해준다.
        work_sec = WORK_MIN #내가 수정하기 쉽게 위에서 조작해놨다.
        short_break_sec = SHORT_BREAK_MIN
        long_break_sec = LONG_BREAK_MIN
        if reps % 8 == 0: # 8번 반복하면 길게 휴식하기
            count_down(long_break_sec)
            title_label.config(text="Break", fg=PINK)
            canvas.configure(bg=YELLOW)
            window.config(bg=YELLOW)
            check_marks.config(bg=YELLOW, fg= RED)
            title_label.config(bg=YELLOW)
        elif reps % 2 == 0: #8의 배수가 아닌 2의 배수에서 이렇게 작동하자.
            count_down(short_break_sec)
            title_label.config(text="Break", fg=PINK)
            canvas.configure(bg=YELLOW)
            window.config(bg=YELLOW)
            check_marks.config(bg=YELLOW, fg= RED)
            title_label.config(bg=YELLOW)
        else: #나머지는 ~~~~
            count_down(work_sec)
            title_label.config(text="Work")
            canvas.configure(bg=SKYBLUE)
            window.config(bg=SKYBLUE)
            check_marks.config(bg=SKYBLUE, fg= RED)
            title_label.config(bg=SKYBLUE, fg= "#ffffff")
    #pause_timer를 실행후 start버튼을 누를때
    else:
        count_down(remaining_time)
        # remaining_time을 none으로 해줘야 일시정지 후 start해도 시간이 끝나면
        # None을 해야 위에 reps+=1 이하 구문들을 실행하고 마커가 채워지고 암튼 계속 실행된다.
        remaining_time= None
    #start버튼을 누른 후 타이머가 동작하면 그동안 start버튼 비활성화
    start_button.config(state= DISABLED)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    #처음에는 스타트 버튼이 안눌리게
    start_button.config(state=DISABLED)
    global timer
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f'0{count_sec}'
    canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')
    if count > 0:
        #1000ms =1s 1초 후의 동일한 함수에 1만큼 인자를 전달한 후 실행
        #timer 는 1초마다 재생성이 아닌 업데이트
        timer = window.after(1000, count_down, count - 1)
    #시간이 다 되면
    else:
        #start_timer에 reps 를 1만큼 증가시키는 코드가 있다.
        start_timer()
        marks = ""
        work_session = math.floor(reps / 2)
        for _ in range(work_session):
            marks += "✓"
        check_marks.config(text=marks)

    # 일시정지 상태일 때는 타이머가 실행되지 않도록 수정
    if timer_paused:
        timer = None
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

