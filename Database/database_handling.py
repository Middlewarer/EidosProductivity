import sqlite3
from datetime import datetime
import os

# Путь к файлу базы данных внутри папки Database
DB_PATH = os.path.join(os.path.dirname(__file__), 'tracker_database.db')


def get_connection():
    """Возвращает подключение к БД"""
    return sqlite3.connect(DB_PATH)


def init_database():
    """Создаёт таблицы, если их нет"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS user
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status INTEGER NOT NULL,
                    name TEXT NOT NULL UNIQUE,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL)
                    ''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS session (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    time_in_mins INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL)
                    ''')

    conn.commit()
    conn.close()
    print('Инициализация БД успешна')


def create_user(status, name, username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO user (status, name, username, password) VALUES (?, ?, ?, ?)''',
                   (status, name, username, password))
    conn.commit()
    conn.close()


def identify_user(username: str, password: str):
    """
    Идентифицирует пользователя по логину и паролю
    Возвращает ID пользователя или None если не найден
    """
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Выполняем запрос
        cursor.execute('''SELECT id FROM user WHERE username = ? AND password = ?''',
                       (username, password))

        # Получаем результат
        result = cursor.fetchone()

        # Если пользователь найден, возвращаем ID
        if result:
            return result[0]  # возвращаем ID
        else:
            return None  # пользователь не найден

    except Exception as e:
        print(f"Ошибка при идентификации пользователя: {e}")
        return None
    finally:
        # Важно закрывать соединение
        if conn:
            conn.close()

def create_session(title: str, time_in_mins: int) -> str:
    conn = get_connection()
    cursor = conn.cursor()
    created_at = datetime.now()
    cursor.execute('''INSERT INTO session (title, time_in_mins, created_at) VALUES (?, ?, ?)''',
                   (title, time_in_mins, created_at))
    conn.commit()
    conn.close()
    print(f"✅ Сессия создана: {title}, {time_in_mins} мин")
    return f'{title} | {time_in_mins} мин'



def get_all_sessions():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM session')
    sessions = cursor.fetchall()
    conn.close()
    return sessions