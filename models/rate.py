from models.db_connection import DatabaseConnection

class Rate:
    __db = DatabaseConnection()
    __conn = __db.get_conn()
    __cursor = __db.get_cursor()

    __user_id = None
    __rate = "Good"

    def __init__(self, user_id, rate, createdat):
        self.__user_id = user_id
        self.__rate = rate

        sql = "INSERT INTO `rating`(`user_id`, `rate`, `createdat`) VALUES  (%s, %s, %s)"
        val = (self.__user_id, self.__rate, createdat)
        self.__cursor.execute(sql, val)
        self.__conn.commit()
        print('set_rate')