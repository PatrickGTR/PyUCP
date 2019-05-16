import pymysql

from modules import config

class MySQL():
    def __enter__(self):
        self.conn = pymysql.connect(host=config.Config.MYSQL_HOST,
                                user=config.Config.MYSQL_USERNAME,
                                passwd=config.Config.MYSQL_PASSWORD,
                                db=config.Config.MYSQL_DATABASE,
                                autocommit=True,
                                cursorclass=pymysql.cursors.DictCursor)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc, value, tb):
        self.cursor.close()
        self.conn.close()
