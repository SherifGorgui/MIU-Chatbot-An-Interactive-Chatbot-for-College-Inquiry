from models.db_connection import DatabaseConnection
class QuestionAnswer: 

    __db = DatabaseConnection()
    __conn = __db.get_conn()
    __cursor = __db.get_cursor()

    def insert_data(self, userId, question, answer, dateTime):
        sql =  "INSERT INTO `chat`(`userId`, `question`, `answer`, `dateTime`) VALUES (%s, %s, %s, %s)"
        # val = (userId, question, answer, dateTime)
        self.__cursor.execute(sql, (userId, question, answer, dateTime,))
        self.__conn.commit()
        print("insert_data")