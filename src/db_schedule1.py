import sqlite3


class DBSchedule:
    def __init__(self, db_name):
        try:
            sqlite_connection = sqlite3.connect(db_name)
            cursor = sqlite_connection.cursor()

            sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS sqlitedb_tg_schedule (
                                        id INTEGER PRIMARY KEY,
                                        username TEXT NOT NULL,
                                        city TEXT NOT NULL,
                                        schedule_time TEXT NOT NULL,
                                        chat_id INTEGER NOT NULL);'''

            cursor.execute(sqlite_create_table_query)
            sqlite_connection.commit()
            self.db_name = db_name
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def add_schedule(self, username, city, schedule_time, chat_id):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            add_schedule_query = f'''INSERT INTO sqlitedb_tg_schedule
                        (username, city, schedule_time, chat_id) VALUES
                        ('{username}', '{city}', '{schedule_time}', {chat_id})'''
            cursor.execute(add_schedule_query)

            sqlite_connection.commit()
            cursor.close()
            return True
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def get_all_schedules(self):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            select_all_query = '''SELECT * FROM sqlitedb_tg_schedule'''
            cursor.execute(select_all_query)

            return cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def get_schedules_by_username(self, username):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            select_query = f'''SELECT * FROM sqlitedb_tg_schedule
            WHERE username="{username}"'''
            cursor.execute(select_query)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def get_schedules_by_schedule_time(self, schedule_time):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            select_query = f'''SELECT * FROM sqlitedb_tg_schedule
            WHERE schedule_time="{schedule_time}"'''
            cursor.execute(select_query)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def get_schedule(self, username, city, schedule_time, chat_id):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            select_query = f'''SELECT * FROM sqlitedb_tg_schedule
            WHERE username="{username}" AND
            city="{city}" AND
            schedule_time="{schedule_time}" AND
            chat_id="{chat_id}"'''
            cursor.execute(select_query)

            return cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def del_all_schedules(self):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            del_all_query = '''DELETE FROM sqlitedb_tg_schedule'''
            cursor.execute(del_all_query)
            sqlite_connection.commit()
            cursor.close()
            return True
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def del_schedule_by_username_and_city(self, username, city):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            select_query = f'''SELECT * FROM sqlitedb_tg_schedule
            WHERE username="{username}" AND city="{city}"'''
            cursor.execute(select_query)
            result = cursor.fetchall()

            del_all_query = f'''DELETE FROM sqlitedb_tg_schedule
            WHERE username="{username}" AND city="{city}"'''
            cursor.execute(del_all_query)

            sqlite_connection.commit()
            cursor.close()
            return result
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()

    def del_schedule_by_username_city_time(self, username, city, time):
        try:
            sqlite_connection = sqlite3.connect(self.db_name)
            cursor = sqlite_connection.cursor()

            select_query = f'''SELECT * FROM sqlitedb_tg_schedule
            WHERE username="{username}" AND city="{city}" AND schedule_time="{time}"'''
            cursor.execute(select_query)
            result = cursor.fetchall()

            del_all_query = f'''DELETE FROM sqlitedb_tg_schedule
            WHERE username="{username}" AND city="{city}" AND schedule_time="{time}"'''
            cursor.execute(del_all_query)

            sqlite_connection.commit()
            cursor.close()
            return result
        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite", error)
        finally:
            if (sqlite_connection):
                sqlite_connection.close()
