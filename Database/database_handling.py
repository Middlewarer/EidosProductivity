import sqlite3
from datetime import datetime
import os

#env-before-after

DB_NAME = 'tracker_database.db'

print('Создаем БД')

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()


#User Table Creation
cursor.execute('''CREATE TABLE IF NOT EXISTS user

                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                status INTEGER NOT NULL ,
                name TEXT NOT NULL UNIQUE,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL)
                ''')

print('Инициализация user успешна')
#Session Table Creation
cursor.execute('''CREATE TABLE IF NOT EXISTS session (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                time_in_mins INTEGER NOT NULL,
                created_at TIMESTAMP NOT NULL )
''')

print('Инициализация session успешна')


def create_user(status, name, username, password):
    global cursor
    cursor.execute(f'''INSERT INTO user (status, name, username, password) VALUES (?, ?, ?, ?)''', (status, name, username, password))
    cursor.connection.commit()

def create_session(title: str, time_in_mins: int) -> None:
    global cursor
    created_at = datetime.now()
    cursor.execute('''INSERT INTO session (title, time_in_mins, created_at) VALUES (?, ?, ?)''', (title, time_in_mins, created_at))
    cursor.connection.commit()



