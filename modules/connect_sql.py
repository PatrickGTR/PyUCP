
# connect_sql.py
# handles all the database connection.

import pymysql

from modules.config import Config

class MySQL():
    def __enter__(self):
        try:
            conf = Config()
            self.conn = pymysql.connect(host=conf.MYSQL_HOST,
                                    user=conf.MYSQL_USERNAME,
                                    passwd=conf.MYSQL_PASSWORD,
                                    db=conf.MYSQL_DATABASE,
                                    autocommit=True,
                                    cursorclass=pymysql.cursors.DictCursor)
        except pymysql.ProgrammingError as err:
            print(f"ERROR: Caught an Error: {err}")
        finally:
            self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc, value, tb):
        self.cursor.close()
        self.conn.close()