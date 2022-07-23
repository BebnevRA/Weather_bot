import psycopg2


class DBSchedule:
    def __init__(self, user, port, password, host):
        try:
            self.user = user
            self.port = port
            self.password = password
            self.host = host
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            create_table_query = '''CREATE TABLE IF NOT EXISTS tg_schedule (
                                        id SERIAL PRIMARY KEY,
                                        username TEXT NOT NULL,
                                        city TEXT NOT NULL,
                                        schedule_time TEXT NOT NULL,
                                        chat_id INTEGER NOT NULL);'''

            cursor.execute(create_table_query)
            connection.commit()
        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def add_schedule(self, username, city, schedule_time, chat_id):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            add_schedule_query = f'''INSERT INTO tg_schedule
                        (username, city, schedule_time, chat_id) VALUES
                        ('{username}', '{city}', '{schedule_time}', {chat_id})'''
            cursor.execute(add_schedule_query)

            connection.commit()
            cursor.close()
            return True

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def get_all_schedules(self):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            select_all_query = '''SELECT * FROM tg_schedule'''
            cursor.execute(select_all_query)
            return cursor.fetchall()

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def get_schedules_by_username(self, username):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            select_query = f'''SELECT * FROM tg_schedule
            WHERE username=  '{username}' '''
            cursor.execute(select_query)
            print(1)
            return cursor.fetchall()

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def get_schedules_by_schedule_time(self, schedule_time):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            select_query = f'''SELECT * FROM tg_schedule
            WHERE schedule_time = '{schedule_time}' '''
            cursor.execute(select_query)
            return cursor.fetchall()

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def get_schedule(self, username, city, schedule_time, chat_id):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            select_query = f'''SELECT * FROM tg_schedule
            WHERE username = '{username}' AND
            city = '{city}' AND
            schedule_time= '{schedule_time}' AND
            chat_id = '{chat_id}' '''
            cursor.execute(select_query)

            return cursor.fetchall()

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def del_all_schedules(self):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            del_all_query = '''DELETE FROM tg_schedule'''
            cursor.execute(del_all_query)
            connection.commit()
            cursor.close()
            return True

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def del_schedule_by_username_and_city(self, username, city):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            select_query = f'''SELECT * FROM tg_schedule
            WHERE username = '{username}' AND city = '{city}' '''
            cursor.execute(select_query)
            result = cursor.fetchall()

            del_all_query = f'''DELETE FROM tg_schedule
            WHERE username = '{username}' AND city = '{city}' '''
            cursor.execute(del_all_query)

            connection.commit()
            cursor.close()
            return result

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()

    def del_schedule_by_username_city_time(self, username, city, time):
        try:
            connection = psycopg2.connect(user=self.user, port=self.port,
                                          password=self.password, host=self.host)
            cursor = connection.cursor()

            select_query = f'''SELECT * FROM tg_schedule
            WHERE username = '{username}' AND 
            city = '{city}' AND schedule_time = '{time}' '''
            cursor.execute(select_query)
            result = cursor.fetchall()

            del_all_query = f'''DELETE FROM tg_schedule
            WHERE username = '{username}' AND 
            city = '{city}' AND 
            schedule_time = '{time}' '''
            cursor.execute(del_all_query)

            connection.commit()
            cursor.close()
            return result

        except psycopg2.OperationalError as error:
            print("Ошибка при подключении к db: \n", error)
        except psycopg2.Error as error:
            print("Произошла следующая ошибка: \n", error)
        finally:
            if (connection):
                connection.close()
