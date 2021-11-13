import psycopg2
from dotenv import load_dotenv, dotenv_values

load_dotenv()

class DBData:
    def __init__(self):
        try:
            self.con = psycopg2.connect(host = dotenv_values("../.env.DB_HOST"),
                                        dbname = dotenv_values("../.env.DB_DATABASE"),
                                        user = dotenv_values("../.env.DB_USER"),
                                        port = dotenv_values("../.env.DB_PORT"),
                                        password = dotenv_values("../.env.DB_PASSWORD"))

        except psycopg2.Error as e:
            print(e)
            self.con.close()
    def select_query(self, table_name, params=None):