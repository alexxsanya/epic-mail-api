import pytest
import psycopg2
import json
from api.util import DB_Manager

class BaseClass():
    
    create_user_query = """
                INSERT INTO users (firstname, lastname, email, 
                                        recoveryemail,password)
                VALUES ('denis', 'steven', 'steven@epicmail.com', 
                    'Alexxx@1','sana@epicmail.com'
                );
            """ 
    query_users = """
                    SELECT * FROM users
                """
    drop_user = """
                    Drop users;
                """

class TestDBConnection(BaseClass):
    
    def test_query_executes(self,db):
        result = db.run_query(self.create_user_query)
        assert "no results to fetch" == str(result)

    @pytest.mark.xfail(raises=psycopg2.IntegrityError)
    def test_query_duplicate_fails(self,db):
        result = db.run_query(self.create_user_query)
        assert isinstance(result,psycopg2.IntegrityError)

    def test_query_user(self,db):
        result = db.run_query(self.query_users,query_option='fetch_all')

        assert 'denis' == result[0]['firstname']
