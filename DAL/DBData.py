import psycopg2.extras
from psycopg2 import connect, Error
from dotenv import load_dotenv
import os

load_dotenv()


class DBData:
    def __init__(self):
        try:
            # self.con = connect(host=os.environ.get("DB_HOST"),
            #                             dbname=os.environ.get("DB_DATABASE"),
            #                             user=os.environ.get("DB_USER"),
            #                             port=os.environ.get("DB_PORT"),
            #                             password=os.environ.get("DB_PASSWORD"))
            self.con = connect(os.environ.get('DATABASE_URL'))
        except Error as e:
            print(e)
            self.close()


    def select_query_all(self):
        cursor = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            # print(table_name)
            sql = 'select t.date_time, t.temperature, h.date_time, h.humidity, s.date_time, s.online from temperature t cross join humidity h cross join status s';
            sql2 = 'SELECT * FROM temperature';
            cursor.execute(sql)
            self.con.commit()
            return cursor.fetchall()
        except Error as e:
            print(e)
            self.close()

    def select_query(self, table_name, params=None):
        cursor = self.con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            # print(table_name)
            cursor.execute('SELECT * FROM ' + table_name)
            return cursor.fetchall()
        except Error as e:
            print(e)
            self.close()

    def bulk_insert_query(self, table_name, params=None):
        cursor = self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            query_params = ", ".join(params[0].keys())
            records_list_template = ','.join(['%s'] * len(params))
            insert_query = 'insert into {} ({}) values {}'.format(table_name,query_params,records_list_template)
            list = []
            for i in params:
                current_tuple = []
                for key in params[0].keys():
                    current_tuple.append(i[key])
                list.append(tuple(current_tuple))
            cursor.execute(insert_query, list)
            self.con.commit()
            return "{} row of data inserted in {} table.".format(len(list), table_name);
        except Error as e:
            print(e)
            self.close()
            return e


    def close(self):
        self.con.close()

