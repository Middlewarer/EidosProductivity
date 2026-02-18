from tkinter import *
from tkinter.font import BOLD
import sys
import os

# Добавляем путь к папке Database в sys.path
# Используем абсолютный путь
db_path = os.path.join(os.path.dirname(__file__), '..', 'Database')
if db_path not in sys.path:
    sys.path.append(db_path)

# Пробуем импортировать модуль
try:
    from database_handling import init_database, create_session, get_all_sessions
    print("✅ Модуль database_handling успешно импортирован")
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print(f"Путь поиска: {sys.path}")
    sys.exit(1)

# Инициализируем базу данных
try:
    init_database()
    print("✅ База данных инициализирована")
except Exception as e:
    print(f"❌ Ошибка инициализации БД: {e}")

window = Tk()

def view_all_sessions():
    """Выводит все сессии из БД в консоль"""
    try:
        sessions = get_all_sessions()
        print("\n=== Все сессии ===")
        if not sessions:
            print("В базе нет сессий")
        for session in sessions:
            print(f"ID: {session[0]}, Название: {session[1]}, Время: {session[2]} мин, Создано: {session[3]}")
        print("==================\n")
    except Exception as e:
        print(f"❌ Ошибка при получении сессий: {e}")

# Настройки стиля для виджетов
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
    global beg_remaining
    beg_remaining = seconds // 60  # сохраняем минуты для создания сессии
    countdown(seconds)

def countdown(remaining: int) -> None:
    if remaining <= 0:
        status_label.config(text="⏰ Сессия завершена!")
        start_btn.config(state='normal')
        timer_label.config(text="00:00")
        text = session_name_label.get()
        # Сохраняем сессию в БД
        try:
            create_session(text, beg_remaining)
            print("✅ Сессия создана в БД")

            view_all_sessions()
        except Exception as e:
            print(f"❌ Ошибка при создании сессии: {e}")
        return

    mins = remaining // 60
    secs = remaining % 60
    timer_label.config(text=f"{mins:02d}:{secs:02d}")
    window.after(1000, countdown, remaining - 1)

window.resizable(width=False, height=False)
window.geometry('800x550')
window['bg'] = '#FEFAE0'

radio_var = IntVar()
beg_remaining = 0


center_hello = Label(window, text='EidosProductivity', bg='#FEFAE0', font=('Arial', 20, BOLD))
center_hello.pack(pady=20)

# Радиокнопки времени
rb0 = Radiobutton(window, text='Нулевой вариант | 1 минута', variable=radio_var, value=1, **label_style)
rb1 = Radiobutton(window, text='Первый вариант | 5 минут', variable=radio_var, value=5, **label_style)
rb2 = Radiobutton(window, text='Второй вариант | 15 минут', variable=radio_var, value=15, **label_style)
rb3 = Radiobutton(window, text='Третий вариант | 30 минут', variable=radio_var, value=30, **label_style)
buttons = [rb0, rb1, rb2, rb3]
for btn in buttons:
    btn.pack(pady=2)

#gpt нагенеренный
session_name_label = Entry(
    window,
    width=30,                    # Ширина в символах
    font=("Arial", 12),          # Шрифт
    fg="blue",                    # Цвет текста
    bg="lightyellow",             # Цвет фона
    borderwidth=2,                # Ширина рамки
    relief="solid",               # Тип рамки
    justify="center",             # Выравнивание (left, center, right)                     # Скрывать ввод (для паролей)
    state="normal",               # Состояние (normal, disabled, readonly)
    cursor="hand2"                 # Курсор при наведении
)
session_name_label.pack(pady=10)


# Старт бтн
start_btn = Button(window, text="▶ Начать сессию",
                   command=start_session,
                   bg='#4CAF50', fg='white',
                   font=('Arial', 11, 'bold'),
                   padx=20, pady=10)
start_btn.pack(pady=20)


timer_label = Label(window, text="00:00", **label_style)
timer_label.pack(pady=10)

# Логи
check_logs = Button(window, text="Показать все сессии",
                   command=view_all_sessions,
                   bg='#2196F3', fg='white',
                   font=('Arial', 10))
check_logs.pack(pady=10)

# Метка статуса
status_label = Label(window, text='', bg='#FEFAE0', font=('Arial', 10))
status_label.pack(pady=10)

window.mainloop()