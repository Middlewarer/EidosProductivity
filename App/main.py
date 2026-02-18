from tkinter import *
from tkinter.font import BOLD
import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Database.database_handling import create_session



window = Tk()

conn = sqlite3.connect('../Database/tracker_database.db')
cursor = conn.cursor()

def view_all_sessions():
    cursor.execute('''
                SELECT *
                FROM session
            ''')

    sessions = cursor.fetchall()
    print(sessions)

label_style = {
    'bg': '#D4A373',
    'fg': 'brown',
    'font': ('Arial', 11),
    'padx': 10,
    'pady': 5
}

def start_session():
    minutes = radio_var.get()

    if not minutes:
        status_label.config(text="❌ Выбери время!")
        return

    seconds = minutes * 60
    status_label.config(text=f"✅ Сессия началась на {minutes} мин.")
    start_btn.config(state='disabled')  # блокируем кнопку
    countdown(seconds)


def countdown(remaining: int) -> None:

    beg_remaining = remaining
    if remaining <= 0:
        status_label.config(text="⏰ Сессия завершена!")
        start_btn.config(state='normal')  # разблокируем кнопку
        timer_label.config(text="00:00")

        create_session('Sessione : _)', beg_remaining)
        print('Session created successfully')
        return

    mins = remaining // 60
    secs = remaining % 60
    timer_label.config(text=f"{mins:02d}:{secs:02d}")
    window.after(1000, countdown, remaining - 1)


window.title('EidosProductivity')
window.iconbitmap('logo.ico')
window.resizable(width=False, height=False)
window.geometry('800x550')
window['bg'] = '#FEFAE0'



#variables
radio_var = IntVar()


center_hello = Label(window, text='EidosProductivity', bg='#FEFAE0', font=('Arial', 20, BOLD),)
center_hello.pack()

main_frame = Frame(window)
main_frame.config(bg='#D4A373')

rb0 = Radiobutton(window, text='Нулевой вариант | 1 минута', variable=radio_var, value=1, **label_style)
rb1 = Radiobutton(window, text='Первый вариант | 5 минут', variable=radio_var, value=5, **label_style)
rb2 = Radiobutton(window, text='Второй вариант | 15 минут', variable=radio_var, value=15, **label_style)
rb3 = Radiobutton(window, text='Третий вариант | 30 минут', variable=radio_var, value=30, **label_style)
buttons = [rb0, rb1, rb2, rb3]
for i in buttons:
    i.pack()

start_btn = Button(window, text="▶ Начать сессию",
                      command=start_session,
                      bg='#4CAF50', fg='white',
                      font=('Arial', 11))
start_btn.pack()

timer_label = Label(window, text="00:00"
                    , **label_style)
timer_label.pack()



check_logs = Button(window, command=view_all_sessions)
check_logs.pack()

status_label = Label(window, text='')
status_label.pack()

view_all_sessions()

window.mainloop()
