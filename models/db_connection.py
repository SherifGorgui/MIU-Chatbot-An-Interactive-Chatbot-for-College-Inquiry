import mysql.connector
from aifc import Error

class DatabaseConnection:
    __host = "localhost"
    __user = "root"
    __password = ""
    __database = "chatbot"

    def __init__(self):
        try:
            self.__conn = mysql.connector.connect(host=self.__host, user=self.__user, password=self.__password, database=self.__database)
            self.__cursor = self.__conn.cursor(buffered=True)
        except Error as e:
            print(e)

    def get_conn(self):
        return self.__conn
    
    def get_cursor(self):
        return self.__cursor
