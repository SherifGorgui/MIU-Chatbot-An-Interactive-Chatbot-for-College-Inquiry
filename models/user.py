from websockets import Data
from models.db_connection import DatabaseConnection
from datetime import datetime
class User:
    __db = DatabaseConnection()
    __conn = __db.get_conn()
    __cursor = __db.get_cursor()

    __id = None
    __name = None
    __email = None

    
    def __set_name(self):
        self.__name = self.__email.split('@')[0]
        print('name: ', self.__name)

    def __set_id(self):
        sql = """SELECT `id` FROM `accounts` WHERE email = %s"""
        self.__cursor.execute(sql, (self.__email,))
        result = self.__cursor.fetchone()
        self.__id = result[0]
        self.__conn.commit()
        print('set_id')

    def set_email(self, email):
        self.__email = email
        self.__set_name()

        now = datetime.now()
        # dd/mm/YY H:M:S
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")

        sql = "INSERT INTO `accounts`(`name`, `email`, `createdat`) VALUES  (%s, %s, %s)"
        val = (self.__name, self.__email, date_time)
        self.__cursor.execute(sql, val)
        self.__conn.commit()
        print('set_email')
        self.__set_id()

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email