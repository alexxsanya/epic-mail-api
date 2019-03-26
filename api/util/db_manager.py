import psycopg2
from config import app_config
from psycopg2.extras import RealDictCursor

class DB_Manager:

    def __init__(self,app_env):
        self.conn = None
        self.app_env = app_env

    def run_query(self,query,query_option="default"):
        try:
            self.conn = psycopg2.connect(app_config[self.app_env].DATABASE_URL)
            
            self.conn.autocommit = True
            cur = self.conn.cursor(cursor_factory=RealDictCursor)
            cur.execute(query)
            
            option = {
                'default':cur,
                'fetch_all': cur.fetchall(),
                'fetch_one': cur.fetchone(),
            }

            return option.get(query_option, "Invalid Option")

        except psycopg2.DatabaseError as error:
            return error

    def create_tables(self):

        sql_file = open('api/util/tables.sql','r') 
        
        self.run_query(query=sql_file.read())

        self.conn.close()

    def drop_tables(self):
        query = """
                DROP TABLES users, messages,
                            messages_sent, messages_received,
                            groups, group_users;
                """ 
        self.run_query(query)

        self.conn.close()

