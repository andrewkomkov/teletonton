import os
import sqlite3
try:
      os.mkdir(r'../db')
except:
      pass

conn = sqlite3.connect(r'../db/messages.db')


def create_table_with_dialogs():
    ''' Создадим таблицу со списком диалогов'''
    c = conn.cursor()
    c.execute(f'''
          CREATE TABLE IF NOT EXISTS dialogs
          ([dialog_id] INTEGER PRIMARY KEY, [name] TEXT)
          ''')
    conn.commit()


def store_dialog(dialog_id, dialog_name):
    ''' Функция для сохранения диалога в таблицу со списком диалогов'''
    c = conn.cursor()
    c.execute(f'''
          INSERT INTO dialogs (dialog_id,name)
                VALUES
                ({dialog_id},'{str(dialog_name).replace("'",'')}')
          ''')
    conn.commit()


def create_table(name):
    ''' Функция для создания таблицы под конкретный диалог'''
    c = conn.cursor()
    c.execute(f'''
          CREATE TABLE IF NOT EXISTS "{name}"
          ([message_id] INTEGER PRIMARY KEY, [author] TEXT, [text] TEXT, [date] TEXT)
          ''')
    conn.commit()


def store_message(table_name, message_id, author, text, date):
    ''' Функция для сохранения одного сообщения в таблицу с конкретным диалогом'''
    c = conn.cursor()
    c.execute(f'''
          INSERT INTO "{table_name}" (message_id,author,text, date)
                VALUES
                ({message_id},'{str(author).replace("'",'')}','{str(text).replace("'",'')}','{str(date)}')
          ''')
    conn.commit()


def create_table_with_users():
    ''' Создадим таблицу пользователей'''
    c = conn.cursor()
    c.execute(f'''
          CREATE TABLE IF NOT EXISTS users
          ([user_id] INTEGER PRIMARY KEY, [user_name] TEXT, [phone] TEXT, [first_name] TEXT, [last_name] TEXT)
          ''')
    conn.commit()


def store_user(id, username, phone, first_name, last_name):
    ''' Функция для сохранения одного пользователя в таблицу с пользователями'''
    c = conn.cursor()
    c.execute(f'''
          INSERT INTO users (user_id,user_name,phone,first_name,last_name)
                VALUES
                ({id}
                ,'{str(username).replace("'",'')}'
                ,'{str(phone).replace("'",'')}'
                ,'{str(first_name).replace("'",'')}'
                ,'{str(last_name).replace("'",'')}')
          ''')
    conn.commit()

def create_view():
    ''' Функция для создания представления для удобства сопоставления загруженных диалогов'''
    c = conn.cursor()
    c.execute(f'''
         CREATE VIEW IF NOT EXISTS table_names AS 
         SELECT d.dialog_id,d.name FROM sqlite_schema a
         INNER JOIN  dialogs d ON a.name = d.dialog_id
          ''')
    conn.commit()

create_table_with_dialogs()
create_view()
create_table_with_users()