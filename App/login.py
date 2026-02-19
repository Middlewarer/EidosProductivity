from tkinter import *
import os
import sys

db_path = os.path.join(os.path.dirname(__file__), '..', 'Database')
if db_path not in sys.path:
    sys.path.append(db_path)

window = Tk()


try:
    from database_handling import init_database, create_session, get_all_sessions, identify_user
    print("✅ Модуль database_handling успешно импортирован")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print(f"Путь поиска: {sys.path}")
    sys.exit(1)



def login():
    try:
        user_username = login_entry.get()
        user_password = password_entry.get()
        print('==============')
        print(user_username, user_password)
        global USER_ID

        USER_ID = identify_user(user_username, user_password)
        if USER_ID is None:
            print('Login Failed!')
            return 0
        else:
            print('User Logged In!')
            window.destroy()
            return USER_ID
    except Exception as e:
        print(e)
        label_error_text = Label(window, text=e, font=("Arial", 10), padx=10, pady=20)
        label_error_text.pack()

USER_ID = None #id default user
style_labels = {
    'bg': '#FEFAE0'
}

window.title('EidosProductivity')
window.geometry('800x550')
window['bg'] = '#FEFAE0'
window.resizable(width=False, height=False)

    # Заголовок
title_label = Label(window, text="Вход в аккаунт", font=("Arial", 20, "bold"), **style_labels)
title_label.place(relx=0.5, y=100, anchor="center")  # relx=0.5 - центр по горизонтали

    # Поле логина
login_label = Label(window, text="Логин:", font=("Arial", 10), **style_labels)
login_label.place(relx=0.5, y=180, anchor="center")

login_entry = Entry(window, font=("Arial", 10), **style_labels)
login_entry.place(relx=0.5, y=210, width=250, height=30, anchor="center")

    # Поле пароля
password_label = Label(window, text="Пароль:", font=("Arial", 10), **style_labels)
password_label.place(relx=0.5, y=260, anchor="center")

password_entry = Entry(window, font=("Arial", 10), show="*", **style_labels)
password_entry.place(relx=0.5, y=290, width=250, height=30, anchor="center")

    # Кнопка
register_btn = Button(window, text="Залогиниться", font=("Arial", 10), command=login)
register_btn.place(relx=0.5, y=350, width=200, height=35, anchor="center")

window.mainloop()




