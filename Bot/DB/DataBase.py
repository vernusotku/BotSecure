import mysql.connector
from mysql.connector import Error
class Database:
    def __init__(self):
        self.cursor = None
        self.connection = None

        self.host_name = None
        self.db = None
        self.host_user = None
        self.host_password = None
    def create_connection(self,host_name,db,host_user,host_password):
        self.host_user = host_user
        self.host_name = host_name
        self.db = db
        self.host_password = host_password

        try:
            self.connection = mysql.connector.connect(
                host = host_name,
                user = host_user,
                passwd = host_password,
                database = db
            )
            self.cursor = self.connection.cursor(buffered=True)
            print('MySQL connect')
            return True
        except Error as e:
          print(f'Error: {e}')

    def create_database(self, query):
        if not self.connection.is_connected():
            self.create_connection(self.host_name,self.db,self.host_user,self.host_password)
            self.close_cursor()
        try:
            self.cursor.execute(query)
        except Error as e:
            print(f'Error: {e}')

        return True


    def close_cursor(self):
        self.cursor.close()
        self.connection.commit()
    def close_connection(self):
        self.connection.close()

    def connection_exist(self):
        if self.connection:
            return True
        return False