import sys
from tkinter import messagebox
import pymysql
from pymysql import ProgrammingError
from common import Values, Config as properties


class DBConnection:
    def __init__(self):
        self._host_name = properties.get_setting(key=Values.HOSTNAME)
        self._port = int(properties.get_setting(key=Values.PORT))
        self._user = properties.get_setting(key=Values.USERNAME)
        self._password = properties.get_setting(key=Values.PASSWORD)
        self._db_name = properties.get_setting(key=Values.DATABASE_NAME)

        self._connection_object = pymysql.connect(host=self._host_name,
                                                  port=self._port,
                                                  user=self._user,
                                                  passwd=self._password)
        self._cursor = self._connection_object.cursor()

    def get_connection_object(self):
        return self._connection_object

    """ Check whether the database exists. If not read the .sql file and create the database"""
    def run_sql_file(self,filename):
        '''
        The function takes a filename and a connection as input
        and will run the SQL query on the given connection
        '''
        file = open(filename, 'r')
        sql = file.read().replace('\n', '').split(';')[:-1]

        for sql_command in sql:
            try:
                self._cursor.execute(sql_command)
            except ProgrammingError as exec:
                error = str(exec)
                if "database exists" in error:
                    self.use_database()
                    print("Database Already Exists")
                    break;
                else:
                    messagebox.showerror("Error",error)
                    sys.exit(0)
            else:
                print("Executing : \n {}".format(sql_command,))

        self._connection_object.commit()

    def insert_login_into_db(self, user):
        sql = '''INSERT INTO login(username,salt,hash,email_id,is_admin,currently_loggedin,created_time) 
        VALUES(%s,%s,%s,%s,%s,%s,%s)'''
        data = (user.get_username(),
                user.get_salt(),
                user.get_hash(),
                user.get_email_id(),
                user.is_admin(),
                user.get_currently_loggedin(),
                user.get_created_time())
        self._cursor.execute(sql,data)
        self._connection_object.commit()

    def close_database(self):
        self._connection_object.commit()
        self._connection_object.close()

    def use_database(self):
        sql = 'USE '+self._db_name
        self._connection_object.cursor().execute(sql)
