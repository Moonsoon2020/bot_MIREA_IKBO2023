import sqlite3
class DB:  # Класс для работы с Базой Данных
    def __init__(self):  # инициализация класса
        self.con = sqlite3.connect('db_For_TGbot.sqlite', check_same_thread=False)  # подключение БД
        create_table1 = """CREATE TABLE IF NOT EXISTS Users (
    id         INTEGER PRIMARY KEY
                       UNIQUE
                       NOT NULL,
    name    text    NOT NULL,
    post       BOOLEAN NOT NULL,
    id_tg TEXT
);"""
        self.con.cursor().execute(create_table1)  # создание отсутствующих и необходимых таблиц
        self.con.commit()

    def add_user(self, name, post, id_tg):
        """ добавление пользователя """
        self.con.cursor().execute(f'''INSERT INTO Users(name, post, id_tg)
         VALUES ('{name}', {post}, '{id_tg}')''')
        self.con.commit()

    def get_ids(self):
        """ получение всех айди пользователей """
        return [[x[0], x[1]] for x in self.con.cursor().execute(f'''SELECT id_tg, name FROM Users''').fetchall()]

    def get_name(self):
        """ получение всех айди пользователей """
        return self.con.cursor().execute(f'''SELECT name FROM Users''').fetchone()
    def is_check(self, id_tg):
        """ проверка"""
        if self.con.cursor().execute(f'''SELECT name FROM Users WHERE 
                                     id_tg = "{id_tg}"''').fetchall():
            return True
        else:
            return False

