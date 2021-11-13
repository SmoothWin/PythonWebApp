
from psycopg2 import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()

class DBData:
    def __init__(self):
        try:
            self.con = connect(host=os.environ.get("DB_HOST"),
                                        dbname=os.environ.get("DB_DATABASE"),
                                        user=os.environ.get("DB_USER"),
                                        port=os.environ.get("DB_PORT"),
                                        password=os.environ.get("DB_PASSWORD"))
        except Error as e:
            print(e)
            self.close()


    def select_query(self, table_name, params=None):
        cursor = self.con.cursor(dictionary=True)
        try:
            print(table_name)
            cursor.execute('SELECT * FROM ' + table_name)
            return cursor.fetchall()
        except Error as e:
            print(e)
            self.close()

    def bulk_insert_query(self, table_name, params=None):
        cursor = self.con.cursor(dictionary=True)
        try:
            data = params
            query_params = ", ".join(params.keys())
            records_list_template = ','.join(['%s'] * len(data))
            insert_query = 'insert into {} ({}) values {}'.format(table_name,query_params,records_list_template)
            print(insert_query)
            # cursor.execute(insert_query, data)
        except Error as e:
            print(e)
            self.close()


    def close(self):
        self.con.close()

