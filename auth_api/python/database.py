import mysql.connector
import os


# Database class to establish the database connection
class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            host = os.environ['DB_HOST']
            user = os.environ['DB_USER']
            password = os.environ['DB_PASSWORD']
            database = os.environ['DB_NAME']
            port = os.environ['DB_PORT']

            self.conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            return self.conn
        except mysql.connector.Error as error:
            print("Failed to connect to database: {}".format(error))
            return None

    def get_cursor(self):
        return self.conn.cursor()

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
