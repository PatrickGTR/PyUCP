
# connect_sql.py
# handles all the database connection.

import pymysql

from modules import config

class MySQL():
    def __enter__(self):
        try:
            self.conn = pymysql.connect(host=config.getMySQLHost(),
                                    user=config.getMySQLUsername(),
                                    passwd=config.getMySQLPassword(),
                                    db=config.getMySQLDatabase(),
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