import pymysql

class mysql():
    def __enter__(self):
        self.conn = pymysql.connect(host="localhost",
                                user="root",
                                passwd="",
                                db="cnr",
                                autocommit=True,
                                cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc, value, tb):
        self.cursor.close()
        self.conn.close()
